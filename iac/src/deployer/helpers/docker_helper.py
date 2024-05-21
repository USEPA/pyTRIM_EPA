import base64, os, subprocess, shutil
import boto3
import docker
from datetime import datetime
from common import await_stack_completion, extract_output_val, die, figure_parent_dir, whoami_aws, loggy

IMAGE_TAG_NAME = "pytrim_iac"

class DockerHelper(object):
    def __init__(self):
        try:
            self.docker_client = docker.from_env()
            print(f"docker client: {self.docker_client}")
        except:
            die("Could not create Docker client; is Docker desktop/etc. running?")

    # this is the equivalent of manually running e.g.:
    #
    #       cd /Users/tfeiler/development/trim-builder/docker
    #       docker build -t pytrim_iac .
    #
    # note - I had to edit ~/.docker/config.json and change "credHelpers" to
    # "_credHelpers" (effectively commenting it out); before that I would get 
    # gcloud-sdk errors when attempting to call build on the image client.
    def build_image(self):
        parent_dir = figure_parent_dir()
        sep = os.path.sep

        loggy("setting up Docker temp directory (application code + entrypoint for image building)...")

        exit_status = subprocess.call(["python", f"{parent_dir}docker{sep}prepare_dockerized_pytrim.py", "-q"])
        if exit_status != 0:
            die("fatal error while preparing Docker image...")

        # sometimes this works and sometimes it doesn't (like it's painfully slow to do images.build via
        # docker_client, but cmdline tool takes just a few seconds). Not sure why.
        use_docker_sdk_to_build = False

        if use_docker_sdk_to_build:
            try:
                loggy(f"building Docker image from src '{parent_dir}docker{sep}' using SDK...")
                self.docker_client.images.build(
                    path = f"{parent_dir}docker{sep}",
                    tag = IMAGE_TAG_NAME,
                )

                loggy(f"build of '{IMAGE_TAG_NAME}' complete")
            except Exception as e:
                die("fatal exception '{e}' while building Docker image...")
        else:
            loggy("Alternate Docker build; SDK disabled...")
            exit_status = -1
            try:
                exit_status = subprocess.call(["docker", "build", "-t", IMAGE_TAG_NAME, f"{parent_dir}docker"])
            except Exception as e:
                die(f"fatal exception '{e}' while building Docker image...")

            if exit_status != 0:
                die(f"fatal issue while building Docker image...")

        temp_dir = f"{parent_dir}docker{sep}temp"
        loggy(f"Cleaning up temp directory '{temp_dir}'...")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    def get_login_data(self):
        ecr_client = boto3.client("ecr")
        loggy("fetching ECR authorization token...")
        # not specifying registryIds here, just using the default. Should we?
        ecr_auth = ecr_client.get_authorization_token().get("authorizationData")[0]

        ecr_registry_url = ecr_auth.get("proxyEndpoint").replace("https://", "")
        token = ecr_auth.get("authorizationToken")
        decoded = base64.b64decode(token)

        decoded_username, decoded_password = decoded.decode().split(":")

        """
        # this is the equivalent of manually running e.g.:
        #
        #       aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 426714360284.dkr.ecr.us-east-1.amazonaws.com
        # but, I kept getting expired credentials when then using this with docker push. Instead I now
        # explicitly pass in username/password which works.
        loggy("authenticating Docker client against ECR registry...")
        self.docker_client.login(
            username = decoded_username,
            password = decoded_password,
            registry = ecr_registry_url,
        )
        loggy("done!")
        """

        return ecr_registry_url, decoded_username, decoded_password

    # this is the equivalent of manually running e.g.:
    #
    #       docker tag pytrim_iac:latest 426714360284.dkr.ecr.us-east-1.amazonaws.com/pytrim-dev-iac/private_ecr_repo:pushtest
    def tag_image(self, repo_uri):
        loggy(f"Tagging image for {repo_uri}...")
        # ecr_registry_name = "pytrim-dev-iac/private_ecr_repo" # TODO -- get this from CF outputs?

        # low-level API; had trouble doing this with the images client directly
        image = self.docker_client.images.get(IMAGE_TAG_NAME)

        # tag = datetime.today().strftime('%Y%m%d%H%M')
        tag = 'latest'

        # image.tag("{registry}/{ecr_registry_name}", tag="pushtest") # TODO - what tag to really use?
        # image.tag(repo_uri, tag="pushtest2") # TODO - what tag to really use?
        image.tag(repo_uri, tag=tag)
        return tag


    # this is the equivalent of manually running e.g.:
    #
    #       docker push 426714360284.dkr.ecr.us-east-1.amazonaws.com/pytrim_proof_of_concept_repo:firstattempt
    def push_image_to_ecr(self, username, password, repo_uri, img_tag):
        # TODO - don't hardcode the push tag...
        # push_tag = "426714360284.dkr.ecr.us-east-1.amazonaws.com/pytrim-dev-iac/private_ecr_repo:pushtest2"
        push_tag = f"{repo_uri}:{img_tag}"
        loggy(f"pushing image '{push_tag}' to ECR...")
        # resp = self.docker_client.images.push(push_tag)
        auth = {
            "username": username,
            "password": password
        }
        loggy("*" * 100)
        resp = self.docker_client.images.push(push_tag, auth_config=auth)
        loggy(f"\t{resp}")

        loggy(f"push complete!")

    # see https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html
    # that gives manual CLI guidance; adapted here for Python SDK usage
    #
    # also helpful:
    # https://stackoverflow.com/questions/45839549/docker-python-api-tagging-containers
    def build_etc(self, stack_name):
        (stack_id, outputs) = await_stack_completion(stack_name)
        ecr_repo_uri = extract_output_val(outputs, "PyTrimPrivateECRRepoUri")
        """
        parent_dir = figure_parent_dir()
        loggy(f"IMAGES ({parent_dir}):")
        for img in self.docker_client.images.list():
            loggy(f"\t{img.id=}, {img.tags=}")
        """
        self.build_image()

        registry_url, ecr_username, ecr_password = self.get_login_data()
        img_tag = self.tag_image(ecr_repo_uri)
        self.push_image_to_ecr(ecr_username, ecr_password, ecr_repo_uri, img_tag)

