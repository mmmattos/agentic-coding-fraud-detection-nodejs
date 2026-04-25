
import subprocess
import time

def run_system(output_dir):
    process = subprocess.Popen(
        ["node", "client.js"],
        cwd=output_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(3)
    process.kill()

    stdout, stderr = process.communicate()
    return stdout, stderr
