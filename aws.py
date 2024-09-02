import boto3
import os

def connect_to_aws():
    """
    Connects to AWS environment using boto3.

    This function assumes that AWS credentials are set up in the environment
    variables or in the AWS credentials file.

    Returns:
    boto3.Session: A boto3 session object for interacting with AWS services.
    """
    try:
        # Create a boto3 session
        session = boto3.Session()

        # Verify the connection by getting the caller identity
        sts_client = session.client('sts')
        account_id = sts_client.get_caller_identity()["Account"]
        print(f"Successfully connected to AWS. Account ID: {account_id}")

        return session

    except Exception as e:
        print(f"An error occurred while connecting to AWS: {e}")
        return None


def list_vpcs(session):
    """
    Lists all VPCs in the AWS account.

    Args:
    session (boto3.Session): An established boto3 session.

    Returns:
    list: A list of dictionaries containing VPC information.
    """
    try:
        ec2_client = session.client('ec2')
        response = ec2_client.describe_vpcs()
        vpcs = response['Vpcs']
        
        vpc_list = []
        for vpc in vpcs:
            vpc_info = {
                'VpcId': vpc['VpcId'],
                'CidrBlock': vpc['CidrBlock'],
                'State': vpc['State'],
                'IsDefault': vpc['IsDefault']
            }
            if 'Tags' in vpc:
                vpc_info['Name'] = next((tag['Value'] for tag in vpc['Tags'] if tag['Key'] == 'Name'), 'Unnamed')
            else:
                vpc_info['Name'] = 'Unnamed'
            vpc_list.append(vpc_info)
        
        return vpc_list
    except Exception as e:
        print(f"An error occurred while listing VPCs: {e}")
        return None


# Example usage:
# aws_session = connect_to_aws()
# if aws_session:
#     # Use the session to interact with AWS services
#     ec2_client = aws_session.client('ec2')
#     vpcs = list_vpcs(ec2_client)
#     if vpcs:
#         for vpc in vpcs:
#             print(f"VPC ID: {vpc['VpcId']}, Name: {vpc['Name']}, CIDR: {vpc['CidrBlock']}")
#     s3 = aws_session.resource('s3')
#     # Perform operations with s3

