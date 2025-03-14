#!/usr/bin/env python3

import argparse, os, shutil

SEP = os.path.sep

def get_project_base_dir():
    return SEP.join(os.path.abspath(__file__).split(SEP)[0:-3])

def get_docker_dir():
    return get_project_base_dir() + f"{SEP}docker/getflow"

def get_temp_dir():
    return get_docker_dir() + f"{SEP}temp"

def copy_application_code_to_temp_dir(src_dir, dest_dir):
    shutil.copytree(src_dir, dest_dir)
    os.makedirs(f"{dest_dir}{SEP}Scripts{SEP}trim_frontend{SEP}external_API{SEP}helpers{SEP}")
    shutil.copy(f"{src_dir}{SEP}trim_core{SEP}algorithms{SEP}GetFlow{SEP}getflow.py", dest_dir)
    # shutil.copy(f"{src_dir}{SEP}trim_core{SEP}algorithms{SEP}GetFlow{SEP}USGS_1_n36w083_20220512.tif", dest_dir)
    # shutil.copy(f"{src_dir}/../unsynced/dynamic_elevation_data.tif", dest_dir)
    shutil.copy(f"{src_dir}{SEP}trim_frontend{SEP}external_API{SEP}helpers{SEP}convert_to_geojson.py", f"{dest_dir}{SEP}Scripts{SEP}trim_frontend{SEP}external_API{SEP}helpers{SEP}")

    # TEMP ONLY
    # shutil.copy(f"/Users/38593/Downloads/Durham_Parcels.geojson", dest_dir)

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
    parser = argparse.ArgumentParser(
                        prog='prepare_dockerized.py',
                        description='copies necessary application code and Dockerized entrypoint to a temp directory for construction into Docker image')
    parser.add_argument("-q", "--quiet", help="suppress extraneous output", action="store_true")
    args = parser.parse_args()

    # figure out some directories
    print(f"\tPREPARE DOCKERIZED: Setup...")
    proj_base_dir = get_project_base_dir()
    docker_dir = get_docker_dir()
    temp_dir = get_temp_dir()

    # start from scratch
    remove_temp_dir(temp_dir)

    # copy the complete webapp codebase in
    print(f"\tPREPARE DOCKERIZED: Copying application code...")
    copy_application_code_to_temp_dir(f"{proj_base_dir}{SEP}Scripts", temp_dir)
    if not os.path.isfile(os.path.join(docker_dir, 'requirements.txt')):
        shutil.copy(os.path.join(docker_dir, '..', 'requirements.txt'), docker_dir)

	# copy GIS stuff in
    shutil.copy(f"{proj_base_dir}{SEP}docker{SEP}getflow{SEP}processing_saga_nextgen-1.0.0.zip", temp_dir)
    

    # copy the Dockerized entrypoint in
    print(f"\tPREPARE DOCKERIZED: Copying Dockerized entrypoint...")
    destination = f"{temp_dir}{SEP}getflow_entrypoint.py"
    shutil.copy(f"{docker_dir}{SEP}_entrypoint.py", destination)

    # add some comments to the entrypoint to alert people that it is a temp/generated file and any edits
    # will be lost...
    print(f"\tPREPARE DOCKERIZED: Adding anti-edit notice...")
    line_prepender(destination, [
        "# STOP!!!!!!",
        "# This version of the file is temporary and should NOT be edited; it is used in",
        "# building the getflow Docker image and when running within a Docker container.",
        "# If you edit this file, your changes will be lost the next time the Docker image is built/deployed.",
        "# If you need to make changes, edit <BASE_DIR>/docker/getflow/_entrypoint.py in the trim-builder repo",
        "# and rebuild/deploy the Docker getflow image.",
        "",
    ])

    if args.quiet is not True:
        print(f"\nAll done! Next steps:\n")
        print(f"\t* Run 'docker build -t <your_tag> .' to rebuild the Docker image.")

        print("")
        print(f"\tIF RUNNING LOCALLY:")
        print(f"\tdocker run --name local_getflow_dockerized -dit <your_tag>")

        print("")
    else:
        print(f"\tPREPARE DOCKERIZED: Done! docker build can proceed...")
