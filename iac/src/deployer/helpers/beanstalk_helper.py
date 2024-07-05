import boto3, getopt, os, shutil, subprocess, sys, zipfile, time
from datetime import datetime
from common import await_beanstalk_app_deployment, await_stack_completion, figure_home_dir, whoami_aws, die, loggy

class BeanstalkHelper(object):
    def __init__(self):
        pass

    def capture_shell_command_output(self, cmd):
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        return result.stdout.decode("utf-8")[:-1]

    def build_flask_zip(self):
        home_dir = figure_home_dir()
        loggy("packaging Flask app...")

        temp_dir = f"{home_dir}flask_temp_package_dir"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        os.chdir(home_dir)
        shutil.copytree("../Scripts/", temp_dir)
        os.chdir(temp_dir)
        shutil.copyfile("../../requirements.txt", "./requirements.txt")
        # Berk said he does this; but I don't see any files matching this pattern?
        # cp ../../Pipfile* .

        # write a Git metadata file
        curr_branch = self.capture_shell_command_output(["git", "symbolic-ref", "--short", "HEAD"])
        curr_commit = self.capture_shell_command_output(["git", "rev-parse", "HEAD"])
        with open("trim_frontend/static/js/trim_deployment_info.js", "w") as git_file:
            build_time = self.make_key()
            pushing_user = os.getlogin()
            git_file.write("let SITE_DEPLOYMENT_INFO = { \"deployed_branch\": \"" + str(curr_branch) + "\", \"deployed_commit\": \"" + str(curr_commit) + "\", \"build_time\": \"" + str(build_time) + "\", \"deployed_by\": \"" + str(pushing_user) + "\" };")

        os.mkdir(".ebextensions")
        with open(".ebextensions/00-packages.config", "w") as f:
            f.write("packages:\n")
            f.write("  yum:\n")
            f.write("    git: []\n")
        
        zip_name = "TOMTEST.zip"
        with zipfile.ZipFile(zip_name, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            for root, dirs, files in os.walk("."):
                for file in files:
                    if not file.endswith(zip_name):
                        combined = os.path.join(root, file)
                        # print(f"ADDING '{combined}' to zip...")
                        archive.write(combined)

        return os.path.abspath(zip_name), temp_dir

    def find_deployment_bucket(self, s3):
        for b in s3.buckets.all():
            if b.name.startswith("elasticbeanstalk-"):
                return b

    def make_key(self):
        return datetime.today().strftime('%Y%m%d_%H%M')

    def format_bytes(self, num_bytes):
        file_size_suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if num_bytes == 0: return '0 B'
        i = 0
        while num_bytes >= 1024 and i < len(file_size_suffixes)-1:
            num_bytes /= 1024.
            i += 1
        f = ('%.2f' % num_bytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, file_size_suffixes[i])

    def upload_callback(self, size):
        if self.total_file_size == 0:
            return
        self.uploaded_amount += size
        # print("{} %".format(int(self.uploaded_amount / self.total_file_size * 100)))

        # only show every 5%...keep the above line in for now til we prove this works
        self.uploaded_percent = int(self.uploaded_amount / self.total_file_size * 100)
        if self.uploaded_percent % 5 == 0 and self.uploaded_percent > self.uploaded_percent_shown:
            print("\tUploaded {} %".format(self.uploaded_percent))
            self.uploaded_percent_shown = self.uploaded_percent

    def upload_to_s3(self, bucket, key, filename):
        print(f"upload [{filename}] under key [{key}] to bucket [{bucket.name}]")
        file_size = os.path.getsize(filename)
        print("file is [" + self.format_bytes(file_size) + "] big; starting")

        self.uploaded_amount = 0
        self.uploaded_percent_shown = -1
        self.uploaded_percent = 0
        self.total_file_size = os.stat(filename).st_size

        # self.bucket.upload_file(filename, key)
        bucket.upload_file(filename, key, Callback=self.upload_callback)
        print(f"done uploading to s3!")

    def prompt_for_description(self):
        description = input("Please enter a description for this version (leave empty to cancel): ")

        if description == "":
            print("No description entered; exiting")
            sys.exit(0)

        return description

    def create_app_version(self, eb_client, stack_name, version, description, bucket, key):
        response = eb_client.create_application_version(
            ApplicationName=stack_name,
            VersionLabel=version,
            Description=description,
            SourceBundle={
                'S3Bucket': bucket.name,
                'S3Key': key
            }
        )

        print(f"application version created: {response}")

    def push_to_eb(self, stack_name, zipped_file_path):
        s3 = boto3.resource("s3")
        eb_client = boto3.client("elasticbeanstalk")

        bucket = self.find_deployment_bucket(s3)

        # key = "20240508_1017"
        key = self.make_key()
        print(f"use '{bucket.name=}' / '{key=}' for deployment")
        self.upload_to_s3(bucket, key, zipped_file_path)

        description = self.prompt_for_description()

        self.create_app_version(eb_client, stack_name, key, description, bucket, key)

        # print(f"APP VERSION CREATE: '{key}' ({description}); oyu have to manually deploy it for now...")
        # return

        env_name = f"{stack_name}-web"
        print(f"env is '{env_name}'; updating environment...")

        response = eb_client.update_environment(
            ApplicationName=stack_name,
            EnvironmentName=env_name,
            VersionLabel=key
        )
        print(f"updated: {response}!")
        print(f"note - it will take some time for beanstalk to complete updating...")
        time.sleep(20)
        await_beanstalk_app_deployment(stack_name)

        """
        This is so weird - my changes (verified via printout monitoring) are not being picked up on first deploy. I
        need to do a restart before they really show up!?!?!
        """
        print(f"TAKE TWO, WHY OH WHY?!?!?")
        time.sleep(5)
        response = eb_client.restart_app_server(
            EnvironmentName=env_name
        )
        await_beanstalk_app_deployment(stack_name)


    def build_etc(self, stack_name):
        (stack_id, outputs) = await_stack_completion(stack_name)

        zipfile, temp_dir = self.build_flask_zip()
        # zipfile = '/Users/tfeiler/development/trim-builder/iac/flask_temp_package_dir/TOMTEST.zip'
        print(f"built zipfile '{zipfile}'")
        self.push_to_eb(stack_name, zipfile)

        shutil.rmtree(temp_dir)
