import os
import subprocess
import sys
import time

os.environ['TEST_DB_SERVERLESS'] = ''  # Always false when running the webapp

EXPOSE = False

WEBAPP_PORT = 6060


def print_header(msg):
    print(f"\n######################## {msg} ########################")


def run_webapp():
    print_header("Starting WebApp")

    webapp_command = f"python webapp.py -p {WEBAPP_PORT}"
    if EXPOSE:
        webapp_command += " --expose"

    proc = subprocess.Popen(
        webapp_command, shell=True, env=os.environ,
        stdout=sys.stdout, stderr=sys.stderr
    )
    wait_for_output(proc, 10)
    return proc


def wait_for_output(subproc, timeout=2):
    while True:
        try:
            outs, errs = subproc.communicate(timeout=timeout)
            if not outs and not errs:
                break
            if outs:
                print(outs)
            if errs:
                print(errs)
        except subprocess.TimeoutExpired:
            break


def all_live(procs):
    for proc in procs:
        if proc is None:
            continue
        if proc.poll() is not None:
            return False
    return True


def check_proc(proc):
    return (proc is not None and proc.poll() is None)


def run_dev_processes(is_main):
    try:
        app_proc = run_webapp()

        while True:
            while all_live([app_proc]):
                time.sleep(1)

            if not check_proc(app_proc):
                app_proc = run_webapp()
    finally:
        print_header("Terminating Flask Applications ...")
        if app_proc is not None:
            app_proc.terminate()


if __name__ == '__main__':
    is_main = os.environ.get('WERKZEUG_RUN_MAIN') != 'true'

    if is_main:
        print_header("Running Dev Environment")
        try:
            from pipenv.vendor.dotenv import load_dotenv
            root = os.path.abspath(os.path.dirname(__file__))
            load_dotenv(os.path.join(root, '.env'))
        except Exception as e:
            print(e)

    try:
        run_dev_processes(is_main)
    except KeyboardInterrupt:
        pass
