from bs4 import BeautifulSoup

from data.PomFile import PomFile


class PomReader:

    def __init__(self, pom_file):
        self.bs_data = None
        self.path = pom_file
        self.parse()

    def parse(self):
        with open(self.path, "r") as f:
            data = f.read()
        self.bs_data = BeautifulSoup(data, "xml")

    def read(self):
        return PomFile(self.path, packaging=self.get_packaging(), qualified=self.get_qualified_name())

    def get_profiles(self):
        res = []
        prop = self.bs_data.find("profiles")
        if not prop:
            return []
        profiles = prop.find_all("profile")
        if not profiles:
            return []
        for profile in profiles:
            id = profile.find("id")
            res.append(id.string)
        return res

    def get_modules(self):
        res = []
        prop = self.bs_data.find("modules")
        if not prop:
            return []
        modules = prop.find_all("module")
        if not modules:
            return []
        for module in modules:
            res.append(module.string)
        return res

    def get_packaging(self):
        packaging = self.bs_data.find("packaging")
        return packaging.getText() if packaging else ""

    def get_artifact_id(self):
        ll = self.bs_data.find_all("artifactId")
        tgt = [x for x in ll if x.parent.name == "project"]
        return tgt[0].getText() if tgt else ""

    def get_group_id(self):
        ll = self.bs_data.find_all("groupId")
        tgt = [x for x in ll if x.parent.name == "project"]
        if tgt:
            return tgt[0].getText() if tgt else ""
        else:
            parent_tgt = [x for x in ll if x.parent.name == "parent"]
            return parent_tgt[0].getText() if parent_tgt else ""

    def get_version(self):
        ll = self.bs_data.find_all("version")
        tgt = [x for x in ll if x.parent.name == "project"]
        if tgt:
            return tgt[0].getText() if tgt else ""
        else:
            parent_tgt = [x for x in ll if x.parent.name == "parent"]
            return parent_tgt[0].getText() if parent_tgt else ""

    def get_qualified_name(self):
        return self.get_group_id() + "." + self.get_artifact_id() + "." + self.get_version()

    def get_parent_group_id(self):
        parent = self.bs_data.find("parent")
        if not parent:
            return ""
        ll = self.bs_data.find_all("groupId")
        tgt = [x for x in ll if x.parent.name == "parent"]
        return tgt[0].getText() if tgt else ""

    def get_parent_artifact_id(self):
        parent = self.bs_data.find("parent")
        if not parent:
            return ""
        ll = self.bs_data.find_all("artifactId")
        tgt = [x for x in ll if x.parent.name == "parent"]
        return tgt[0].getText() if tgt else ""

    def get_parent_version(self):
        parent = self.bs_data.find("parent")
        if not parent:
            return ""
        ll = self.bs_data.find_all("version")
        tgt = [x for x in ll if x.parent.name == "parent"]
        return tgt[0].getText() if tgt else ""


if __name__ == "__main__":
    path = "/Users/fy/Downloads/spring-security-oauth"
    reader = PomReader(path + "/pom.xml")
    profiles = reader.get_modules()
    print(profiles)