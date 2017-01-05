#!/usr/bin/env python
#
import boto3
import sys, getopt
from datetime import datetime, timedelta

costOptimization = {
        'Underutilized Amazon EBS Volumes':'DAvU99Dc4C',
        'Amazon EC2 Reserved Instance Lease Expiration':'1e93e4c0b5',
        'Idle Load Balancers':'hjLMh88uM8',
        'Low Utilization Amazon EC2 Instances':'Qch7DwouX1',
        'Unassociated Elastic IP Addresses':'Z4AUBRNSmz',
        'Underutilized Amazon Redshift Clusters':'G31sQ1E9U',
        'Amazon Route 53 Latency Resource Record Sets':'51fC20e7I2',
        'Amazon RDS Idle DB Instances':'Ti39halfu8'
        }

def usage():
    print("usage: ShowCostOptimize [-h] [-a AWS_ACCOUNT_ID]")

def checkIntValue(value):
    try:
        intTarget = int(value)
    except ValueError:
        print("This is not AWS account id!")
        sys.exit()

def checkIDLength(value):
    maxValue = 12
    if len(value) == int(maxValue):
        return value
    else:
        print("This is not AWS account id!")
        sys.exit()

def argvcheck():
    if len(sys.argv) < 2:
        usage()
        sys.exit()

def main():
    opts, args = getopt.getopt(sys.argv[1:],"ha:")
    argvcheck()
    aws_account_id = ""
    for op, value in opts:
        if op == "-a":
            checkIntValue(value)
            checkIDLength(value)
            aws_account_id = value
        elif op == "-h":
            usage()
            sys.exit()

    RoleObject= 'arn:aws:iam::' + aws_account_id + ':role/CollectTA'

    session = boto3.Session(profile_name='dcsrd',region_name='us-east-1')
    sts_client = session.client('sts')

    assumedRoleObject = sts_client.assume_role(
        RoleArn=RoleObject,
        RoleSessionName="AssumeRoleSession1"
    )

    credentials = assumedRoleObject['Credentials']

    support_client = session.client(
            'support',
            aws_access_key_id = credentials['AccessKeyId'],
            aws_secret_access_key = credentials['SecretAccessKey'],
            aws_session_token = credentials['SessionToken'],
            region_name = 'us-east-1',
            )

    cloudwatch_client = session.client(
            'cloudwatch',
            aws_access_key_id = credentials['AccessKeyId'],
            aws_secret_access_key = credentials['SecretAccessKey'],
            aws_session_token = credentials['SessionToken'],
            region_name = 'us-east-1',
            )

    cost = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/Billing',
        MetricName='EstimatedCharges',
        Dimensions=[
            {
                'Name': 'Currency',
                'Value': 'USD'
        },
        ],
        StartTime=datetime.today() - timedelta(hours = 12),
        EndTime=datetime.now(),
        Period=60,
        Statistics=[
            'Maximum',
        ],
        Unit='None'
    )
    
    for k, v in costOptimization.items():
        response = support_client.describe_trusted_advisor_check_result(
            checkId=v,
            language='en'
        )
        if response['result']['status'] == "warning":
            result = response['result']['categorySpecificSummary']['costOptimizing']['estimatedMonthlySavings']
        else:
            result = "Safe"
            print("Item: ",k)
            print(response['result']['status'], end='' )
            print(', Cost Possible Saving: ',result)
    
if __name__ == "__main__":
    main()
