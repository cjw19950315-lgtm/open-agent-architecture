"""Directed acyclic graph planner and parallel executor with fan-out/fan-in."""

import concurrent.futures
import threading
import uuid


class DAGNode:
    def __init__(self, node_id=None, func=None, deps=(), timeout=30, retries=0, writes=False, name=None):
        self.id = node_id or uuid.uuid4().hex[:8]
        self.func = func
        self.deps = tuple(deps)
        self.timeout = timeout
        self.retries = retries
        self.writes = writes
        self.name = name or self.id


class DAG:
    def __init__(self, name="task"):
        self.name = name
        self.nodes = {}
        self.edges = set()

    def add_node(self, node):
        self.nodes[node.id] = node
        return node

    def add_edge(self, source, target):
        self.edges.add((source, target))

    def topo_sort(self):
        indegree = {nid: 0 for nid in self.nodes}
        for source, target in self.edges:
            indegree[target] += 1
        queue = [nid for nid, deg in indegree.items() if deg == 0]
        order = []
        while queue:
            nid = queue.pop(0)
            order.append(nid)
            for source, target in self.edges:
                if source == nid:
                    indegree[target] -= 1
                    if indegree[target] == 0:
                        queue.append(target)
        if len(order) != len(self.nodes):
            raise ValueError("cycle detected in DAG %s" % self.name)
        return order

    def snapshot(self):
        return {
            "name": self.name,
            "nodes": [{"id": n.id, "name": n.name, "deps": list(n.deps), "writes": n.writes} for n in self.nodes.values()],
            "edges": [list(e) for e in sorted(self.edges)],
        }


class DAGExecutionError(Exception):
    def __init__(self, node_id, cause):
        super().__init__("node %s failed: %s" % (node_id, cause))
        self.node_id = node_id
        self.cause = cause


class DAGExecutor:
    def __init__(self, max_workers=4, tracer=None):
        self.max_workers = max_workers
        self.tracer = tracer

    def _run_node(self, node, context, results):
        def attempt():
            return node.func(context, results)

        last_error = None
        for attempt_index in range(node.retries + 1):
            try:
                return attempt()
            except Exception as exc:
                last_error = exc
                if attempt_index >= node.retries:
                    raise
        raise last_error

    def execute(self, dag, context, completed=None, initial_results=None, on_wave_complete=None):
        completed = set(completed or [])
        results = dict(initial_results or {})
        order = dag.topo_sort()
        done = set(completed)
        write_lock = threading.Lock()
        span = self.tracer.span("dag:" + dag.name) if self.tracer else None
        try:
            pending = [nid for nid in order if nid not in done]
            while pending:
                ready = []
                for nid in pending:
                    node = dag.nodes[nid]
                    if all(dep in done for dep in node.deps):
                        ready.append(node)
                if not ready:
                    raise DAGExecutionError("<graph>", "no ready nodes; unresolved dependencies")
                pending = [nid for nid in pending if nid not in {n.id for n in ready}]

                with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                    futures = {}
                    for node in ready:
                        def job(node=node):
                            if node.writes:
                                with write_lock:
                                    return self._run_node(node, context, results)
                            return self._run_node(node, context, results)
                        futures[pool.submit(job)] = node
                    for future in concurrent.futures.as_completed(futures):
                        node = futures[future]
                        try:
                            results[node.id] = future.result(timeout=node.timeout)
                        except Exception as exc:
                            raise DAGExecutionError(node.id, exc)
                        done.add(node.id)
                if on_wave_complete is not None:
                    on_wave_complete(done, dict(results))
        finally:
            if span is not None:
                span.__exit__(None, None, None)
        return results