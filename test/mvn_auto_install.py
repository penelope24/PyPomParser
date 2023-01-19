import os
from ProjectExplore import ProjectExplore
from PomEditor import PomEditor
from PomReader import PomReader
from Mojo import Mojo


if __name__ == "__main__":
    path = "/Users/fy/Downloads/spring-security-oauth"
    explore = ProjectExplore(path)
    trees = explore.build_tree()
    editor = PomEditor(path + "/pom.xml")
    editor.comment_trivial_modules()
    # for root in explore.get_root_poms():
    #     Mojo.mvn_clean_install(root.path)
    key_poms = explore.get_key_poms()
    print(key_poms)
