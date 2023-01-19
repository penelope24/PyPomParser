import re


class Element:
    def __init__(self, full_text: str, delimiter: str, label: str):
        self.full_text = full_text
        self.delimiter = delimiter
        self.label = label
        self.terminal_str: str
        self.level: int
        self.is_terminal: bool
        self._init_regex()
        self._parse()

    def _init_regex(self):
        # self.ptr_for_label = re.compile(r"{}*</?(.*?)[ >]".format(self.delimiter), flags=re.M)
        # self.ptr_for_level = re.compile(r"^({}*)<".format(self.delimiter), flags=re.M)
        # self.ptr_for_terminal = re.compile(r"^{}*<[^/].*?>([^\n]*?)</.*?>".format(self.delimiter), flags=re.M)
        self.r_look_text_by_label = re.compile(r"({}*<{}>([\s\S]*?)</{}>)".format(self.delimiter, self.label, self.label))

    def _parse(self):
        text = self.r_look_text_by_label.search(self.full_text)
        print(self.r_look_text_by_label)
        print(text)
        print("---")
        print(text.group(0))
        print("---")
        print(text.group(1))


if __name__ == "__main__":
    path = "/Users/fy/Downloads/spring-security-oauth/pom.xml"
    text: str
    with open(path, "r") as f:
        text = f.read()
    ele = Element(text, " ", "modules")

