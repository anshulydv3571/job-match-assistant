# Job Match Assistant

A small Python tool that compares your resume against a folder of job descriptions and tells you which ones fit best, and which keywords you are missing for each.

I built it because I was reading job posts one by one and could not tell which ones were worth applying to first.

## What it does

- Scores each job description against your resume (0 to 100) using TF-IDF and cosine similarity from scikit-learn.
- Lists the important words in each job post that do not appear in your resume.
- Saves a dated CSV report, ranked from best match to worst.
- Remembers which job files it has already scored, so running it again only picks up new ones.

## How to run

    pip install -r requirements.txt
    python run.py --resume sample_data/resume.txt --jobs sample_data/jobs

Use `--all` to score every file again, and `--out folder_name` to change where the report is saved.

Example output:

      9.9%  data_analyst_intern.txt
      3.8%  backend_java_intern.txt
      1.1%  graphic_designer.txt

## Running it automatically

Save new job descriptions as `.txt` files in one folder, then schedule `run.py` so it runs every day.

On Windows, use Task Scheduler with the same command. On Linux or Mac, use cron, for example every day at 9 AM:

    0 9 * * * cd /path/to/job-match-assistant && python3 run.py --resume my_resume.txt --jobs my_jobs

## Tests

    python -m unittest discover -s tests

## Limitations

- The score is based on word overlap, not meaning. It is a quick filter and should not replace reading the job post.
- Resumes and job descriptions must be plain `.txt` files.
- Short job descriptions give noisy scores.

## Files

    matcher.py    scoring and keyword logic
    run.py        command line tool and report writer
    tests/        unit tests
    sample_data/  example resume and job posts
