import boto3
import botocore
import os

bucket_name_parameter = 'MacieDevlabBucketName'
sensitive_data_folder = 'sensitive-data'

ssm_client = boto3.client('ssm')
s3_client = boto3.client('s3')
macie_client = boto3.client('macie2')

bucket_name = ssm_client.get_parameter(
    Name='MacieDevlabBucketName'
)['Parameter']['Value']
bucket_location = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
if bucket_location is None:
    bucket_location = 'us-east-1'
print(f"Your Macie Bucket name is {bucket_name} in the {bucket_location} region")


list_files = os.listdir(sensitive_data_folder)
for file_name in list_files:
    response = s3_client.upload_file(f"./{sensitive_data_folder}/{file_name}", bucket_name, file_name)
print(f"Uploaded sensitive data to {bucket_name}")

try:
    macie_client.disable_macie()
    print("Disabled Macie to remove previous findings")
except macie_client.exceptions.from_code('AccessDeniedException') as e:
    print(e.response['Error']['Message'])

macie_client.enable_macie()
print("New configuration of Macie enabled")