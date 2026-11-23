"""Command line tool: rank job descriptions against your resume.

Example:
    python run.py --resume sample_data/resume.txt --jobs sample_data/jobs
"""
import argparse
from pathlib import Path

from matcher import rank_jobs


def read_jobs(folder):
    """Read every .txt file in the folder into a {file_name: text} dict."""
    jobs = {}
    for path in sorted(Path(folder).glob("*.txt")):
        jobs[path.name] = path.read_text(encoding="utf-8", errors="ignore")
    return jobs


def main():
    parser = argparse.ArgumentParser(description="Rank job descriptions against a resume.")
    parser.add_argument("--resume", required=True, help="path to your resume as a .txt file")
    parser.add_argument("--jobs", required=True, help="folder of job descriptions (.txt)")
    args = parser.parse_args()

    resume = Path(args.resume).read_text(encoding="utf-8", errors="ignore")
    jobs = read_jobs(args.jobs)

    if not jobs:
        print("No job descriptions found.")
        return

    for name, score in rank_jobs(resume, jobs):
        print(f"{score:5.1f}%  {name}")


if __name__ == "__main__":
    main()
