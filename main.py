# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from PomEditor import PomEditor
from ProjectExplore import ProjectExplore
from PomReader import PomReader
from Mojo import Mojo


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = "/Users/fy/Documents/MyProjects/cc2vec/test/spring-cloud-security"
    explorer = ProjectExplore(path)
    root_poms = explorer.get_root_poms()
    key_poms = explorer.get_key_poms()
    for root_pom in root_poms:
        editor = PomEditor(root_pom)
        editor.comment_trivial_modules()
        Mojo.mvn_package(root_pom)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
