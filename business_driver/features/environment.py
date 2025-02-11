import subprocess
import time

def before_all(context):
    context.server = subprocess.Popen(["python", "server.py"])
    time.sleep(2)

def after_all(context):
    context.server.terminate()
