#!/usr/bin/env python3

import os, shutil

SEP = os.path.sep

def get_project_base_dir():
    return SEP.join(os.path.abspath(__file__).split(SEP)[0:-2])

def get_docker_dir():
    return get_project_base_dir() + f"{SEP}docker"

def get_temp_dir():
    return get_docker_dir() + f"{SEP}temp"

def copy_application_code_to_temp_dir(src_dir, dest_dir):
    shutil.copytree(src_dir, dest_dir)

def remove_temp_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

# thx https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
def line_prepender(filename, lines):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        for line in lines:
            # f.write(line.rstrip('\r\n') + '\n' + content)
            f.write(line.rstrip('\r\n') + '\n')
        f.write(content)

if __name__ == "__main__":
    # figure out some directories
    print(f"Setup...")
    proj_base_dir = get_project_base_dir()
    docker_dir = get_docker_dir()
    temp_dir = get_temp_dir()

    # start from scratch
    remove_temp_dir(temp_dir)

    # copy the complete webapp codebase in
    print(f"Copying application code...")
    copy_application_code_to_temp_dir(f"{proj_base_dir}{SEP}Scripts", temp_dir)
    
    # copy the Dockerized entrypoint in
    print(f"Copying Dockerized entrypoint...")
    destination = f"{temp_dir}{SEP}docker_entrypoint.py"
    shutil.copy(f"{docker_dir}{SEP}_entrypoint.py", destination)

    # add some comments to the entrypoint to alert people that it is a temp/generated file and any edits
    # will be lost...
    print(f"Adding anti-edit warning notice...")
    line_prepender(destination, [
        "# STOP!!!!!!",
        "# This version of the file is temporary and should NOT be edited; it is used in",
        "# building the Docker image and when running within a Docker container.",
        "# If you edit this file, your changes will be lost the next time the Docker image is built/deployed.",
        "# If you need to make changes, edit <BASE_DIR>/docker/_entrypoint.py in the trim-builder repo",
        "# and rebuild/deploy the Docker image.",
        "",
    ])

    print(f"\nAll done! Next steps:\n")
    print(f"\t* Run 'docker build -t <your_tag> .' to rebuild the Docker image.")

    print("")
    print(f"\tIF RUNNING LOCALLY:")
    print(f"\tdocker run --name local_pytrim_dockerized -dit <your_tag>")

    print("")
