
import subprocess

def validate(stdout):
    return "→" in stdout

def fix(stderr, output_dir):
    if "Cannot find module" in stderr:
        print("🛠 Installing dependencies...")
        subprocess.run(["npm", "install"], cwd=output_dir)
