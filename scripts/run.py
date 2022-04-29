"""
This scripts automatically runs a Macie discovery job in the environment,
against the bucket created by cf.yml
"""

import boto3

client = boto3.client('macie2')
response = client.list_custom_data_identifiers()
account_id = boto3.client('sts').get_caller_identity().get('Account')

print(response['items'][0]['id'])

bucket_name_parameter = 'MacieDevlabBucketName'
ssm_client = boto3.client('ssm')
bucket_name = ssm_client.get_parameter(
    Name=bucket_name_parameter
)['Parameter']['Value']

response = client.create_classification_job(
    customDataIdentifierIds=[
        response['items'][0]['id']
    ],
    description='test',
    initialRun=True,
    jobType='ONE_TIME',
    managedDataIdentifierSelector='ALL',
    name='test',
    s3JobDefinition={
        'bucketDefinitions': [
            {
                'accountId': account_id,
                'buckets': [bucket_name]
            },
        ],
    },
    samplingPercentage=100,
)