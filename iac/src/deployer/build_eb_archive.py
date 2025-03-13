from helpers.beanstalk_helper import BeanstalkHelper


def build_archive():
    helper = BeanstalkHelper()

    zipfile, temp_dir = helper.build_flask_zip()
    # zipfile = 'trim-builder/iac/flask_temp_package_dir/TOMTEST.zip'


if __name__ == '__main__':
    build_archive()
