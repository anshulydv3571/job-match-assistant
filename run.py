"""Command line tool: rank new job descriptions against your resume and save a CSV report.

Example:
    python run.py --resume sample_data/resume.txt --jobs sample_data/jobs
"""
import argparse
import csv
import json
from datetime import date
from pathlib import Path

from matcher import missing_keywords, rank_jobs

STATE_FILE = Path(".processed_jobs.json")


def load_state():
    """Names of job files we have already scored."""
    if STATE_FILE.exists():
        return set(json.loads(STATE_FILE.read_text()))
    return set()


def save_state(seen):
    STATE_FILE.write_text(json.dumps(sorted(seen)))


def read_jobs(folder, skip):
    """Read every .txt file in the folder, except the ones in skip."""
    jobs = {}
    for path in sorted(Path(folder).glob("*.txt")):
        if path.name not in skip:
            jobs[path.name] = path.read_text(encoding="utf-8", errors="ignore")
    return jobs


def main():
    parser = argparse.ArgumentParser(description="Rank job descriptions against a resume.")
    parser.add_argument("--resume", required=True, help="path to your resume as a .txt file")
    parser.add_argument("--jobs", required=True, help="folder of job descriptions (.txt)")
    parser.add_argument("--out", default="reports", help="folder for the CSV report")
    parser.add_argument("--all", action="store_true", help="also re-score jobs seen before")
    args = parser.parse_args()

    resume = Path(args.resume).read_text(encoding="utf-8", errors="ignore")
    seen = set() if args.all else load_state()
    jobs = read_jobs(args.jobs, seen)

    if not jobs:
        print("No new job descriptions found.")
        return

    ranked = rank_jobs(resume, jobs)
    Path(args.out).mkdir(exist_ok=True)
    report = Path(args.out) / f"report_{date.today()}.csv"

    with open(report, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["job_file", "match_percent", "missing_keywords"])
        for name, score in ranked:
            writer.writerow([name, score, ", ".join(missing_keywords(resume, jobs[name]))])
            print(f"{score:5.1f}%  {name}")

    save_state(seen | set(jobs))
    print(f"\nReport saved to {report}")


if __name__ == "__main__":
    main()
