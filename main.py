import os
import subprocess
import argparse
import sys

def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")

def main():
    parser = argparse.ArgumentParser(description="Run LocalBot pipeline")
    parser.add_argument(
        "--use-ai",
        type=str2bool,
        nargs="?",
        const=True,
        default=False,
        help="Enable AI tags (true/false)"
    )
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))  # /LocalBot
    go_script = os.path.join(base_dir, "go.sh")

    cmd = [go_script]
    if args.use_ai:
        cmd.append("--use-ai")

    try:
        subprocess.run(["bash", "-lc", f"cd {base_dir} && ./go.sh"], check=True)
        print("Pipeline completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Pipeline failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
