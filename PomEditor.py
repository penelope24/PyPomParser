import os
import html

from bs4 import BeautifulSoup
from queue import SimpleQueue


class PomEditor:

    def __init__(self, pom_file):
        self.bs_data = None
        self.pom_file = pom_file
        self.parse()

    def parse(self):
        with open(self.pom_file, "r") as f:
            data = f.read()
        self.bs_data = BeautifulSoup(data, "xml")

    def comment_trivial_modules(self):
        modules = self.bs_data.find("modules")
        if not modules:
            return None
        module_list = modules.find_all("module")
        trivial_modules = PomEditor.find_trivial_submodules(module_list)
        for filtered_module in trivial_modules:
            PomEditor.comment_tag(filtered_module)
        self.write_to_disk()

    @staticmethod
    def comment_tag(tag):
        l_str = html.unescape("&lt;!-- ")
        r_str = html.unescape(" --&gt;")
        tag.insert_before(l_str)
        tag.insert_after(r_str)

    # fixme format changed after write
    def write_to_disk(self):
        with open(self.pom_file, "w") as f:

            s = str(self.bs_data.project.prettify())
            # s = self.bs_data.prettify()
            f.write(html.unescape(s))
            # f.write(s)

    @staticmethod
    def find_trivial_submodules(module_list):
        stop_words = [
            "test", "sample", "doc"
        ]
        trivial_modules = []
        for module in module_list:
            s = module.string
            if any(x in s for x in stop_words):
                trivial_modules.append(module)
        return trivial_modules

    @staticmethod
    def new_pom_property(properties: dict):
        assert len(properties) == 1
        top_key = list(properties.keys())[0]
        soup = BeautifulSoup("<dummy></dummy>", "lxml")
        top_tag = soup.dummy
        top_tag.name = top_key
        top_value = properties.get(top_key)
        # recur
        level = 0
        if isinstance(top_value, str):
            top_tag.string = top_value
            return top_tag
        elif isinstance(top_value, dict):
            PomEditor.read_sub_dict(soup, level + 1, top_tag, top_value)
            return top_tag
        else:
            return None

    @staticmethod
    def read_sub_dict(soup, level, par_tag, sub_dict: dict):
        prefix = "\n" + "    " * level
        keys = list(sub_dict.keys())
        for key in keys:
            tag = soup.new_tag(key)
            value = sub_dict.get(key)
            if isinstance(value, str):
                tag.string = value
                par_tag.append(prefix)
                par_tag.append(tag)
                suffix = "\n" + "    " * (level - 1)
                par_tag.append(suffix)
            if isinstance(value, dict):
                par_tag.append(prefix)
                par_tag.append(tag)
                suffix = "\n" + "    " * (level - 1)
                par_tag.append(suffix)
                PomEditor.read_sub_dict(soup, level + 1, tag, value)

    @staticmethod
    def remove_empty_lines(text: str):
        lines = text.split("\n")
        filtered = filter(lambda x: x.strip(), lines)
        return "\n".join(filtered)


if __name__ == "__main__":
    prop = {
        "gourpId": "org",
        "artifactId": "artifact",
        "version": "1.0"
    }
    prop2 = {
        "plugin": {
            "groupId": "org.apache.maven.plugins",
            "artifactId": "maven-toolchains-plugin",
            "version": "1.1",
            "executions": {
                "execution": {
                    "goals": {
                        "goal": "toolchain"
                    }
                },
                "other": "123"
            },
            "configuration": {
                "toolchains": {
                    "jdk": {
                        "version": 1.8,
                        "vendor": "sun"
                    }
                }
            }
        }
    }
    path = "/Users/fy/Downloads/spring-security-oauth"
    editor = PomEditor(path + "/pom.xml")
    editor.write_to_disk()