#!/usr/bin/env python3
"""Collect grades from student assignment repos.

Usage:
    # From repos listed in a students file:
    python collect_grades.py --students students.csv --assignment thermistor-assignment

    # From all forks of the template repo:
    python collect_grades.py --forks scott2b/thermistor-assignment

    # Output to specific file:
    python collect_grades.py --forks scott2b/thermistor-assignment -o grades.csv

Requires: gh CLI authenticated (gh auth login)
"""

import argparse
import csv
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def run_gh(args):
    """Run a gh CLI command and return parsed JSON output."""
    result = subprocess.run(
        ['gh'] + args,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def get_forks(repo):
    """Get all forks of a repository."""
    output = run_gh(['api', f'repos/{repo}/forks', '--paginate', '-q', '.[].full_name'])
    if not output:
        return []
    return [line for line in output.splitlines() if line.strip()]


def get_latest_grade(repo):
    """Download the grade artifact from the most recent workflow run."""
    runs_json = run_gh([
        'api', f'repos/{repo}/actions/runs',
        '-q', '.workflow_runs | map(select(.name == "Grade Assignment")) | sort_by(.created_at) | reverse | .[0]'
    ])

    if not runs_json:
        return None, 'no workflow runs found'

    try:
        run = json.loads(runs_json)
    except json.JSONDecodeError:
        return None, 'could not parse workflow run'

    run_id = run.get('id')
    conclusion = run.get('conclusion', 'unknown')

    if not run_id:
        return None, 'no run ID'

    artifacts_json = run_gh([
        'api', f'repos/{repo}/actions/runs/{run_id}/artifacts',
        '-q', '.artifacts[] | select(.name == "grade") | .id'
    ])

    if not artifacts_json:
        return None, f'no grade artifact (run {conclusion})'

    artifact_id = artifacts_json.strip().splitlines()[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = Path(tmpdir) / 'grade.zip'
        result = subprocess.run(
            ['gh', 'api', f'repos/{repo}/actions/artifacts/{artifact_id}/zip',
             '--output', str(zip_path)],
            capture_output=True
        )

        if result.returncode != 0:
            return None, 'could not download artifact'

        try:
            with zipfile.ZipFile(zip_path) as zf:
                with zf.open('grade.txt') as f:
                    score = float(f.read().decode().strip())
                    return score, 'ok'
        except (KeyError, ValueError) as e:
            return None, f'could not read grade: {e}'


def main():
    parser = argparse.ArgumentParser(description='Collect grades from student repos')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--forks', metavar='OWNER/REPO',
                        help='Collect from all forks of this repo')
    source.add_argument('--students', metavar='FILE',
                        help='CSV file with columns: student, repo')
    parser.add_argument('--assignment', default='assignment',
                        help='Assignment name for gradebook column')
    parser.add_argument('-o', '--output', default='grades.csv',
                        help='Output CSV file (default: grades.csv)')
    args = parser.parse_args()

    repos = []

    if args.forks:
        print(f"Finding forks of {args.forks}...")
        forks = get_forks(args.forks)
        repos = [(fork.split('/')[0], fork) for fork in forks]
        print(f"  Found {len(repos)} fork(s)")
        args.assignment = args.forks.split('/')[-1]

    elif args.students:
        with open(args.students) as f:
            reader = csv.DictReader(f)
            repos = [(row['student'], row['repo']) for row in reader]
        print(f"Loaded {len(repos)} student(s) from {args.students}")

    if not repos:
        print("No student repos found.")
        sys.exit(1)

    grades = []
    for student, repo in repos:
        print(f"  {student}: ", end='', flush=True)
        score, status = get_latest_grade(repo)
        if score is not None:
            print(f"{score}/100")
            grades.append({
                'student': student,
                'assignment': args.assignment,
                'score': score,
                'max': 100,
                'status': status
            })
        else:
            print(f"-- ({status})")
            grades.append({
                'student': student,
                'assignment': args.assignment,
                'score': '',
                'max': 100,
                'status': status
            })

    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['student', 'assignment', 'score', 'max', 'status'])
        writer.writeheader()
        writer.writerows(grades)

    print(f"\nGrades written to {args.output}")

    scored = [g for g in grades if g['score'] != '']
    if scored:
        scores = [g['score'] for g in scored]
        print(f"  Submitted: {len(scored)}/{len(grades)}")
        print(f"  Mean: {sum(scores)/len(scores):.1f}")
        print(f"  Min: {min(scores):.1f}, Max: {max(scores):.1f}")


if __name__ == '__main__':
    main()
