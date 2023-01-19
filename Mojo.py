import os

from PomEditor import PomEditor
from PomReader import PomReader
import subprocess
from subprocess import CalledProcessError


class Mojo:

    @staticmethod
    def copy_dependencies(cwd_path, output_path):
        base_pom_file = os.path.join(cwd_path, "pom.xml")
        editor = PomEditor(base_pom_file)
        editor.comment_trivial_modules()
        mvn_script = "mvn dependency:copy-dependencies -fae -DoutputDirectory=" + output_path
        try:
            subprocess.run(mvn_script, shell=True, check=True, capture_output=True, cwd=cwd_path)
        except CalledProcessError as e:
            print(e)
            print(e.stdout)

    @staticmethod
    def mvn_package(cwd_path):
        base_pom_file = os.path.join(cwd_path, "pom.xml")
        editor = PomEditor(base_pom_file)
        editor.comment_trivial_modules()
        mvn_script = "mvn clean install -DskipTests -Dmaven.javadoc.skip=true"
        print(mvn_script)
        try:
            subprocess.run(mvn_script, shell=True, check=True, capture_output=True, cwd=cwd_path)
        except CalledProcessError as e:
            print("err")
            print(e)

    @staticmethod
    def mvn_clean_install(root_pom_file, **kwargs):
        ss = root_pom_file.split("/")
        project_name = ss[len(ss)-2]
        cwd = "/".join(ss[0:len(ss)-1])
        print("project: ", project_name)
        print("cwd: ", cwd)
        profile = None
        if kwargs:
            profile = kwargs["profile"]
        mvn_script = "mvn clean install"
        if profile:
            mvn_script += " -P "
            mvn_script += profile
        mvn_script += " -DskipTests -Dmaven.javadoc.skip=true -fae"
        print(mvn_script)
        try:
            subprocess.run(mvn_script, shell=True, check=True, capture_output=True, cwd=cwd)
        except CalledProcessError as e:
            output_file = "/Users/fy/Documents/MyProjects/MyPomParser/log/" + project_name + "_log.txt"
            with open(output_file, "w") as f:
                f.write(e.stdout.decode("utf-8"))
                f.write("\n")

    @staticmethod
    def collect_build_jars(key_poms, tgt_dir):
        failed_poms = []
        for key_pom in key_poms:
            reader = PomReader(key_pom)
            jar_name = reader.get_qualified_name() + ".jar"
            try:
                subprocess.run(["cp", jar_name, tgt_dir], check=True)
            except CalledProcessError as e:
                failed_poms.append(key_pom)
        return failed_poms


if __name__ == "__main__":
    path = "/Users/fy/Downloads/spring-security-oauth"
    Mojo.mvn_clean_install(path, profile="bootstrap")