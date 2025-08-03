import boto3
from datetime import datetime


def get_public_buckets(log_file):
    s3 = boto3.client('s3')
    public_buckets = []
    total_checked = 0

    buckets = s3.list_buckets()

    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        total_checked += 1

        acl = s3.get_bucket_acl(Bucket=bucket_name)

        for grant in acl['Grants']:
            grantee = grant.get('Grantee', {})
            permission = grant.get('Permission', '')

            if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                public_buckets.append(bucket_name)

                log_msg = f"[!] Public bucket found: {bucket_name} (Permission: {permission})"
                print(log_msg)
                log_file.write(f"{datetime.now()} - {log_msg}\n")

    log_file.write(f"{datetime.now()} - [*] Total buckets checked: {total_checked}\n")
    return public_buckets


def remediate_bucket(bucket_name, log_file):
    s3 = boto3.client('s3')

    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )

    print(f"[+] Remediated public access for: {bucket_name}")
    log_file.write(f"{datetime.now()} - [!] Remediated bucket: {bucket_name}\n")


if __name__ == "__main__":
    print("[*] Scanning for public buckets...")

    with open("s3_remediation_log.txt", "a") as log_file:
        public_buckets = get_public_buckets(log_file)

        for bucket in public_buckets:
            remediate_bucket(bucket, log_file)

        if not public_buckets:
            print("[✓] No public buckets found. All good.")

