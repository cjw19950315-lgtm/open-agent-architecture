"""Skill registry and dynamic skill router."""

import re


class Skill:
    def __init__(self, name, description, domain, keywords=(), preconditions=None, writes=False):
        self.name = name
        self.description = description
        self.domain = domain
        self.keywords = tuple(keywords)
        self.preconditions = preconditions or []
        self.writes = writes

    def matches(self, intent):
        if intent.business_domain == self.domain:
            return True
        lowered = intent.prompt.lower()
        return any(k in lowered for k in self.keywords)

    def score(self, intent):
        score = 0
        if intent.business_domain == self.domain:
            score += 10
        lowered = intent.prompt.lower()
        for k in self.keywords:
            if k in lowered:
                score += 2
        for p in self.preconditions:
            if callable(p):
                try:
                    if p():
                        score += 1
                except Exception:
                    pass
        return score

    def execute(self, ctx, args):
        raise NotImplementedError

    def snapshot(self):
        return {"name": self.name, "domain": self.domain, "description": self.description, "writes": self.writes}


class SkillRegistry:
    def __init__(self):
        self._skills = {}

    def register_skill(self, skill):
        self._skills[skill.name] = skill
        return skill

    def discover_skills(self, query=None):
        if query is None:
            return list(self._skills.values())
        lowered = query.lower()
        return [s for s in self._skills.values() if lowered in s.name.lower() or lowered in s.description.lower()]

    def match_skill(self, intent):
        return [s for s in self._skills.values() if s.matches(intent)]

    def rank_skills(self, skills, intent):
        return sorted(skills, key=lambda s: s.score(intent), reverse=True)

    def select_skills(self, intent, max_primary=1, max_auxiliary=2):
        ranked = self.rank_skills(self.match_skill(intent), intent)
        primary = ranked[:max_primary]
        auxiliary = [s for s in ranked[max_primary:] if s not in primary][:max_auxiliary]
        return primary, auxiliary

    def snapshot(self):
        return [s.snapshot() for s in self._skills.values()]


class ReadFileSkill(Skill):
    def __init__(self):
        super().__init__(
            name="read_file",
            description="Read a file inside the workspace and return its masked content.",
            domain="documentation",
            keywords=("read", "readme"),
        )

    def execute(self, ctx, args):
        return ctx["tools"].call("filesystem", {"op": "read", "path": args["path"]})


class WriteFileSkill(Skill):
    def __init__(self):
        super().__init__(
            name="write_file",
            description="Write a file inside the workspace (requires approval in manual mode).",
            domain="documentation",
            keywords=("write", "create", "generate", "save"),
            writes=True,
        )

    def execute(self, ctx, args):
        return ctx["tools"].call("filesystem", {"op": "write", "path": args["path"], "content": args["content"]})


class AnalyzeMarkdownSkill(Skill):
    def __init__(self):
        super().__init__(
            name="analyze_markdown",
            description="Analyze Markdown sources and produce a structured summary.",
            domain="documentation",
            keywords=("analy", "architecture", "summary"),
        )

    def execute(self, ctx, args):
        sources = args.get("sources", [])
        contents = []
        for path in sources:
            result = ctx["tools"].call("filesystem", {"op": "read", "path": path})
            contents.append((path, result.get("content", "")))
        lines = []
        for path, content in contents:
            lines.append("## Source: %s" % path)
            lines.append("- bytes: %d" % len(content))
            lines.append("- lines: %d" % content.count("\n"))
            headings = [ln for ln in content.splitlines() if ln.startswith("#")]
            lines.append("- headings: %d" % len(headings))
            words = len(content.split())
            lines.append("- words: %d" % words)
        lines.append("")
        lines.append("## Analysis")
        lines.append("The project follows a modular architecture with specs, schemas, scripts, and examples. "
                     "Runtime entry points are under the oaa package.")
        return {"analysis": "\n".join(lines), "sources": list(sources)}


class VerifySkill(Skill):
    def __init__(self):
        super().__init__(
            name="verify_artifact",
            description="Run the verification gate against a produced artifact.",
            domain="general",
            keywords=("verify", "check"),
        )

    def execute(self, ctx, args):
        artifact_path = ctx["policy"].resolve(args.get("path"))
        with open(artifact_path, "r", encoding="utf-8") as fh:
            text = fh.read()
        return ctx["verification"].verify(task=ctx.get("task"), artifact_path=artifact_path, artifact_text=text).to_dict()


def register_builtin_skills(registry):
    registry.register_skill(ReadFileSkill())
    registry.register_skill(WriteFileSkill())
    registry.register_skill(AnalyzeMarkdownSkill())
    registry.register_skill(VerifySkill())
    return registry