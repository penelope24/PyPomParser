import re

from parser.Element import Element
from parser.ElementType import ElementType


class PomParser:
    def __init__(self, path):
        self.pom_file = path
        self.text = self.read()
        self.main_text = self.read_main()
        self.delimiter = self.find_delimiter()
        self.elements: list[Element] = []
        self.find_all_elements()

    def _init_patterns(self):
        self.is_base_pattern = re.compile(r"\A<project.*?>")
        self.is_terminal_pattern = re.compile(r"<[^/].*?>.*?</.*?>\n")
        self.is_left_pattern = re.compile(r"({})?<[^/].*?>".format(self.delimiter))
        self.is_right_pattern = re.compile(r"({})?</.*?>".format(self.delimiter))
        self.is_valid_pattern = re.compile(r"({})?<[^/].*?>.*?</.*?>".format(self.delimiter))
        self.prefix_pattern = re.compile(r"(.*)<.*?>")

    def read(self) -> str:
        with open(self.pom_file, "r") as f:
            return f.read()

    def read_main(self) -> str:
        main_pattern = re.compile(r"^<project.*?>\n([\s\S]*)\n<\/project>", flags=re.M)
        main_text = main_pattern.search(self.text).group(1)
        return main_text

    def find_delimiter(self) -> str:
        pattern = re.compile(r"<project\s.*>\n(.*?)(?=<)")
        res = pattern.search(self.text)
        return res.group(1)

    def get_line_level(self, line) -> int:
        res = self.prefix_pattern.search(line).group(1)
        return len(res.split(self.delimiter)) - 1

    def find_all_elements(self):
        lines: list[str] = re.split("\n", self.text)
        for line in lines:
            level = self.get_line_level(line)
            element_type: ElementType = None
            if self.is_base_pattern.search(line):
                element_type = ElementType.BASE
                continue
            if self.is_terminal_pattern.search(line):
                element_type = ElementType.TERMINAL
                continue
            if self.is_left_pattern.search(line):
                element_type = ElementType.LEFT
                continue
            if self.is_right_pattern.search(line):
                element_type = ElementType.RIGHT
                continue
            element = Element(self.delimiter, level, line, element_type)
            self.elements.append(element)

    def find_elements(self, label, level):
        return list(filter(lambda x: x.label == label and x.level == level, self.elements))


if __name__ == "__main__":
    path = "/Users/fy/Downloads/spring-security-oauth/pom.xml"
    parser = PomParser(path)
    print(parser.main_text)
