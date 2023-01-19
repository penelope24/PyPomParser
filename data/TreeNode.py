import os


class TreeNode:

    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []
        self.elements_index = []
        self.elements_index.append(self)

    def __len__(self):
        return len(self.elements_index)

    def __iter__(self):
        for node in self.elements_index:
            yield node

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return len(self.children) == 0

    def register(self, node):
        self.elements_index.append(node)
        if self.parent:
            self.parent.register(node)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        self.register(child)
        if child.children:
            for node in child.children:
                self.register(node)

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        prefix = (" " * 4 * self.get_level()) + ("|--" if self.parent else "")
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                assert isinstance(child, TreeNode)
                child.print_tree()


def build_tree():
    root = TreeNode("Food")

    italy = TreeNode("Italy")
    italy.add_child(TreeNode("Pizza"))
    italy.add_child(TreeNode("Lasgna"))
    italy.add_child(TreeNode("Pistacho Ice"))

    chinese = TreeNode("Chineese")
    chinese.add_child(TreeNode("Noodles"))
    chinese.add_child(TreeNode("Rice balls"))
    chinese.add_child(TreeNode("Fried Rice"))

    mexican = TreeNode("Mexican")
    mexican.add_child(TreeNode('Tacos'))
    mexican.add_child(TreeNode('Gyro'))
    mexican.add_child(TreeNode('Shawarma'))

    root.add_child(italy)
    root.add_child(chinese)
    root.add_child(mexican)

    return root


if __name__ == "__main__":
    root = build_tree()
    root.print_tree()
    print(len(root))