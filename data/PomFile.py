import os


class PomFile:

    def __init__(self, path, **kwargs):
        self.path = path
        ss = str(path).split("/")
        self.dir = "/".join(ss[0:len(ss)-1])
        self.level = -1
        self.qualified_name = kwargs["qualified"]
        self.packaging = kwargs["packaging"]

    def __eq__(self, other):
        if isinstance(other, PomFile):
            return self.path == other.path
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.path)

    def set_level(self, level):
        self.level = level


if __name__ == "__main__":
    pom = PomFile("qwe", level=1)
    print(pom.path)
    print(pom.level)
