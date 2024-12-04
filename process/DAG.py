import networkx as nx
from typing import List, Dict, Type, Callable, Any
from step import Step

class DAG:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.step_map = {}  # 将节点名称映射到具体的 Step 实例

    def add_step(self, step_class: Type[Step], name: str, dependencies: List[str] = None):
        """添加一个新的步骤到 DAG 中"""
        if dependencies is None:
            dependencies = []

        if name in self.step_map:
            raise ValueError(f"Step with name '{name}' already exists.")

        # 创建 Step 实例
        step_instance = step_class()
        self.step_map[name] = step_instance

        # 添加节点及其依赖关系
        self.graph.add_node(name)
        for dep in dependencies:
            if dep not in self.step_map:
                raise ValueError(f"Dependency '{dep}' does not exist.")
            self.graph.add_edge(dep, name)

        # 检查是否形成了循环
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Adding this step would create a cycle.")

    def run(self, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """按照拓扑排序顺序执行所有步骤"""
        context = initial_context if initial_context is not None else {}
        try:
            for node in nx.topological_sort(self.graph):
                step = self.step_map[node]
                print(f"Executing {node}")
                context = step.execute(context)
        except Exception as e:
            print(f"An error occurred during execution: {e}")
        return context