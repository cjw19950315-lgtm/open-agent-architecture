"""LLM provider abstraction and the agent loop (prompt -> model -> tool -> result -> model)."""

import json
import os


class ModelResult:
    def __init__(self, content, tool_calls=None, finish_reason="stop", model=None):
        self.content = content
        self.tool_calls = tool_calls or []
        self.finish_reason = finish_reason
        self.model = model

    def to_dict(self):
        return {"content": self.content, "tool_calls": self.tool_calls, "finish_reason": self.finish_reason, "model": self.model}


class LLMProvider:
    name = "base"
    config = {}

    def generate(self, messages, tools=None):
        raise NotImplementedError


class DeterministicProvider(LLMProvider):
    """Offline deterministic provider so the runtime works without API keys."""

    name = "deterministic"
    config = {"mode": "offline", "version": "1.0"}

    def generate(self, messages, tools=None):
        system = ""
        user = ""
        for message in messages:
            if message.get("role") == "system":
                system = message.get("content", "")
            if message.get("role") == "user":
                user = message.get("content", "")
        tool_results = [m for m in messages if m.get("role") == "tool"]
        lowered = user.lower()

        if not tool_results:
            if "analy" in lowered:
                return ModelResult(
                    content=None,
                    tool_calls=[{"name": "analyze_markdown", "params": {"sources": ["README.md", "pyproject.toml"]}}],
                    finish_reason="tool_calls",
                    model=self.name,
                )
            if "read" in lowered:
                return ModelResult(
                    content=None,
                    tool_calls=[
                        {"name": "filesystem", "params": {"op": "read", "path": "README.md"}},
                        {"name": "filesystem", "params": {"op": "read", "path": "pyproject.toml"}},
                    ],
                    finish_reason="tool_calls",
                    model=self.name,
                )

        last_tool = tool_results[-1] if tool_results else None
        if last_tool is not None and last_tool.get("name") == "filesystem" and "analy" in lowered:
            return ModelResult(
                content=None,
                tool_calls=[{"name": "analyze_markdown", "params": {"sources": ["README.md", "pyproject.toml"]}}],
                finish_reason="tool_calls",
                model=self.name,
            )
        if last_tool is not None and last_tool.get("name") == "analyze_markdown":
            try:
                analysis = json.loads(last_tool["content"]).get("analysis", "")
            except Exception:
                analysis = str(last_tool.get("content", ""))
            if "WRITE_DISABLED" in system:
                return ModelResult(content=analysis, finish_reason="stop", model=self.name)
            if "write" in lowered:
                return ModelResult(
                    content=None,
                    tool_calls=[{"name": "write_file", "params": {"path": "analysis.md", "content": analysis}}],
                    finish_reason="tool_calls",
                    model=self.name,
                )
            return ModelResult(content=analysis, finish_reason="stop", model=self.name)

        if last_tool is not None and last_tool.get("name") == "write_file":
            return ModelResult(content="Task completed. Artifact produced and verified.", finish_reason="stop", model=self.name)

        return ModelResult(content="Task completed.", finish_reason="stop", model=self.name)


class OpenAIProvider(LLMProvider):
    """Optional OpenAI-compatible provider. Requires the openai package and an API key."""

    name = "openai"
    config = {}

    def __init__(self, model="gpt-5-codex", api_key=None, base_url=None):
        try:
            import openai
        except ImportError as exc:
            raise ImportError("openai package is required for OpenAIProvider") from exc
        self.model = model
        self.config = {"model": model, "base_url": base_url or "default"}
        self._client = openai.OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"), base_url=base_url)

    def generate(self, messages, tools=None):
        response = self._client.chat.completions.create(model=self.model, messages=messages, tools=tools)
        choice = response.choices[0].message
        tool_calls = []
        for call in (choice.tool_calls or []):
            tool_calls.append({"name": call.function.name, "params": json.loads(call.function.arguments or "{}")})
        return ModelResult(
            content=choice.content,
            tool_calls=tool_calls,
            finish_reason=response.choices[0].finish_reason,
            model=self.model,
        )


class AgentLoopError(Exception):
    pass


class AgentLoop:
    def __init__(self, provider, tool_runtime, tracer=None, max_steps=8):
        self.provider = provider
        self.tools = tool_runtime
        self.tracer = tracer
        self.max_steps = max_steps
        self.steps = []

    def run(self, system, user, tool_specs=None, seed_tool_results=None):
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        for seed in (seed_tool_results or []):
            messages.append(seed)
        for step_index in range(self.max_steps):
            span = self.tracer.span("agent_step:%d" % step_index) if self.tracer else None
            try:
                result = self.provider.generate(messages, tools=tool_specs)
                record = {"step": step_index, "model": result.model, "finish_reason": result.finish_reason}
                if result.content:
                    messages.append({"role": "assistant", "content": result.content})
                if not result.tool_calls:
                    record["final"] = result.content
                    self.steps.append(record)
                    return result
                for call in result.tool_calls:
                    params = call.get("params", {})
                    tool_result = self.tools.call(call["name"], params)
                    messages.append({
                        "role": "tool",
                        "name": call["name"],
                        "content": json.dumps(tool_result, ensure_ascii=False, default=str),
                    })
                    record.setdefault("calls", []).append({"name": call["name"], "params": params})
                self.steps.append(record)
            finally:
                if span is not None:
                    span.__exit__(None, None, None)
        raise AgentLoopError("agent loop exceeded max_steps=%d" % self.max_steps)

    def snapshot(self):
        return list(self.steps)