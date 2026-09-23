# AWS Serverless File Processor — Local Simulation

A free Python project that simulates an AWS serverless file-processing workflow locally.

## What it demonstrates
- S3-style incoming, processed, and rejected folders
- Lambda-style Python handler
- JSON validation
- Logging and error handling
- Automated tests with Python `unittest`

## Important
This project does **not** create or deploy any AWS resources, so it can be used without AWS free-tier credits.

## Architecture
```text
Incoming JSON
    ↓
data/incoming/
    ↓
Lambda-style handler
    ↓
Valid → data/processed/
Invalid → data/rejected/
```

## Run
```bash
python run_local.py
```

## Test
```bash
python -m unittest discover -s tests -v
```

## AWS mapping
| Local component | AWS equivalent |
|---|---|
| `data/incoming/` | Amazon S3 incoming prefix |
| `lambda_handler()` | AWS Lambda |
| `data/processed/` | Amazon S3 processed prefix |
| `data/rejected/` | Amazon S3 rejected prefix |
| Python logging | Amazon CloudWatch Logs |

## Skills
Python, JSON processing, validation, serverless design, AWS Lambda concepts, Amazon S3 concepts, logging, exception handling, testing.
