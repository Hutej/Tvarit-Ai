class NodeRegistry:
    def __init__(self):
        self.nodes = {}

    def register(self, name, node_func):
        self.nodes[name] = node_func
