import os

from PomReader import PomReader
from data.PomFile import PomFile
from operator import attrgetter

from data.TreeNode import TreeNode
from queue import SimpleQueue


class ProjectExplore:

    def __init__(self, path):
        self.path = path
        self.all_poms = set()
        self.basic_search()
        self.root_poms = self.get_root_poms()
        self.valid_trees = self.build_trees()

    def basic_search(self):
        for root, dirs, files in os.walk(self.path):
            level = root[len(self.path):].count(os.sep)
            for file in files:
                if file == "pom.xml":
                    full_path = os.path.join(root, file)
                    reader = PomReader(full_path)
                    pom_file = reader.read()
                    pom_file.set_level(level)
                    self.all_poms.add(pom_file)

    def build_trees(self):
        res = [self.build_tree_from_root_pom(x) for x in self.root_poms]
        return res

    """
    every time the iteration encounters an pom.xml file, it find its parent pom.xml by decomposing current root path
    remember that the stating root path does not have parent.
    """
    def build_tree_from_root_pom(self, root_pom):
        root_node = TreeNode(root_pom)
        for root, dirs, files in os.walk(root_pom.dir):
            ss = str(root).split("/")
            pre_root = "/".join(ss[0:len(ss)-1]) if root != root_pom.dir else None
            if pre_root:
                par_pom = next((x for x in self.all_poms if x.dir == pre_root), None)
                if par_pom:
                    par_node = root_node if par_pom is root_pom else TreeNode(par_pom)
                    for file in files:
                        if file == "pom.xml":
                            full_path = os.path.join(root, file)
                            child_pom = next(x for x in self.all_poms if x.path == full_path)
                            child_node = TreeNode(child_pom)
                            par_node.add_child(child_node)
        return root_node

    def get_root_poms(self):
        min_level = min(map(lambda x: x.level, self.all_poms))
        filtered = filter(lambda x: x.level == min_level, self.all_poms)
        return set(filtered)

    @staticmethod
    def is_valid(pom_file):
        return pom_file.packaging == "jar" or pom_file.packaging == ""

    def get_key_poms_from_valid_tree(self):
        res = []
        for tree in self.valid_trees:
            for node in tree:
                if ProjectExplore.is_valid(node.data):
                    res.append(node.data)
        return res


if __name__ == "__main__":
    path = "/Users/fy/Downloads/spring-security-oauth"
    explorer = ProjectExplore(path)
    trees = explorer.valid_trees
    trees[0].print_tree()
    keys = explorer.get_key_poms_from_valid_tree()
    print(keys)
