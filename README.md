# aws-trusted-advisor
AWS Trusted Advisor Command Line Tool

Preparation before running

Step 1: Create AWS IAM Policy to provide enough permission for access, see AssumeRole_Policy.json

Step 2: Create Collect_TA AWS IAM Role for cross account access, see Collect_TA_Policy.json

Step 3: Confirm the Trust Relationship have been configured in Collect_TA IAM Role, see Trust_Relationship.json

How to use it?

./ShowCostOptimize.py -a AWS_ACCOUNT_ID
