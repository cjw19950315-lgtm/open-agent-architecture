"""Tool runtime with permissions, path isolation, tracing, and credential masking."""


class Tool:
    def __init__(self, name, description, permissions=()):
        self.name = name
        self.description = description
        self.permissions = tuple(permissions)

    def call(self, ctx, params):
        raise NotImplementedError


class FilesystemTool(Tool):
    def __init__(self):
        super().__init__("filesystem", "Read/write/list files inside the workspace.", permissions=("read", "write"))

    def call(self, ctx, params):
        op = params.get("op")
        policy = ctx["policy"]
        if op == "read":
            path = policy.resolve(params["path"])
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
            masked = ctx["masker"].mask(content)
            return {"path": params["path"], "bytes": len(content), "content": masked}
        if op == "write":
            path = policy.resolve(params["path"])
            decision = ctx["approval"].request({"action": "write", "path": params["path"]})
            if not decision.get("approved"):
                return {"approved": False, "reason": decision.get("reason", "denied"), "path": params["path"]}
            import os
            os.makedirs(os.path.dirname(path), exist_ok=True)
            content = params.get("content", "")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            return {"approved": True, "path": params["path"], "bytes": len(content)}
        if op == "list":
            import os
            root = policy.workspace
            names = []
            for name in sorted(os.listdir(root)):
                names.append(name)
            return {"files": names}
        raise ValueError("unsupported filesystem op: %s" % op)


class ToolRuntime:
    def __init__(self, tools=None, tracer=None, masker=None):
        self.tools = {t.name: t for t in (tools or [])}
        self.tracer = tracer
        self.masker = masker
        self.calls = []

    def register(self, tool):
        self.tools[tool.name] = tool
        return tool

    def call(self, name, params):
        if name not in self.tools:
            raise KeyError("unknown tool: %s" % name)
        span = self.tracer.span("tool:" + name) if self.tracer else None
        try:
            result = self.tools[name].call(self.context, params)
            record = {"tool": name, "params": params, "result": result}
            self.calls.append(record)
            return result
        finally:
            if span is not None:
                span.__exit__(None, None, None)

    def bind(self, context):
        self.context = context
        return self

    def snapshot(self):
        return list(self.calls)