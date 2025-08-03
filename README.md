\# S3 Auto-Remediator



This Python script scans your AWS S3 buckets and automatically remediates public access by applying restrictive permissions. It logs all detected public buckets and remediation actions with timestamps.



\## Features

\- Detects publicly accessible S3 buckets

\- Automatically blocks public access using `put\_public\_access\_block`

\- Logs activity to `s3\_remediation\_log.txt` with clear timestamps

\- Modular and easy to extend



\## Usage



```bash

python s3\_remediator.py



\## Example Log Output


2025-08-03 17:10:29 - [*] Total buckets checked: 6
2025-08-03 17:10:30 - [!] Remediated bucket: my-public-bucket



\## Requirements

- boto3

- Python 3.8+



\## License

- MIT








