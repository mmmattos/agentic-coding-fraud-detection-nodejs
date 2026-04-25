
from planner import plan_system
from generator import generate_system
from executor import run_system
from validator import validate, fix

OUTPUT_DIR = "../generated"

def main():
    print("🧠 Agent starting...")

    goal = "Generate a distributed fraud detection system with gRPC"

    max_attempts = 5

    for attempt in range(1, max_attempts + 1):
        print(f"\n🔁 Attempt {attempt}")

        plan = plan_system(goal)
        generate_system(plan, OUTPUT_DIR)

        print("▶️ Running system...")
        stdout, stderr = run_system(OUTPUT_DIR)

        if validate(stdout):
            print("✅ System is valid!")
            print(stdout.splitlines()[:5])
            return
        else:
            print("❌ Validation failed")
            if stderr:
                print(stderr.strip())
            fix(stderr, OUTPUT_DIR)

    print("⚠️ Agent failed after all attempts")

if __name__ == "__main__":
    main()
