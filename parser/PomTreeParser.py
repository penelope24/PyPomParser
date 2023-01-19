import re
from typing import List

from data.TreeNode import TreeNode
from parser.Element import Element
from parser.ElementType import ElementType
from collections import deque


class PomTreeParser:

    def __init__(self, path):
        self.pom_file = path
        self.text = self.read()
        # self.delimiter = self.find_delimiter()
        self.delimiter = "  "
        self.text_lines = self.text.split("\n")
        self.element_tree = None

    def _init_patterns(self):
        pass

    def read(self) -> str:
        with open(self.pom_file, "r") as f:
            return f.read()

    def find_delimiter(self) -> str:
        pattern = re.compile(r"<project\s.*>\n(.*?)(?=<)")
        res = pattern.search(self.text)
        return res.group(1)

    def parse(self):
        stack: deque[TreeNode] = deque()
        r_left = re.compile(r"<([^/][\s\S]*?)[ >]".format(self.delimiter), flags=re.M)
        r_right = re.compile(r"</(.*?)>", flags=re.M)
        r_comment = re.compile(r"[  ]*<!--.*?>", flags=re.M)
        # labels_left = r_left.findall(self.text)
        # print(labels_left)
        # labels_right = r_right.findall(self.text)
        # print(labels_right)
        # diff = set(labels_left) - set(labels_right)
        # print(diff)
        end_pos: int = -1
        line = self.text_lines[0]
        label = r_left.search(line).group(1)
        root = TreeNode(label)
        stack.append(root)
        for i in range(1, len(self.text_lines)):
            line = self.text_lines[i]
            if line == "\n" or line == "" or r_comment.search(line):
                continue
            label = r_left.search(line).group(1) if r_left.search(line) else None
            par = stack[-1] if stack else None

            if label:
                node = TreeNode(label)
                stack.append(node)
                par.add_child(node)
            if r_right.search(line):
                stack.pop()
            level = len(stack)
            print(line)
            print(level)
            print("---")
            if not stack:
                end_pos = i
                break
        assert end_pos == len(self.text_lines) - 1
        assert not stack
        # root.print_tree()


if __name__ == "__main__":
    path = "/Users/fy/Downloads/spring-security-oauth/pom.xml"
    tree_parser = PomTreeParser(path)
    tree_parser.parse()
