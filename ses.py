import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Extract bucket name and object key from the event
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
    except KeyError as e:
        print(f"KeyError: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid event format.')
        }

    # Initialize the SES client
    ses = boto3.client('ses', region_name='us-east-1')  # Change region as needed

    # Email parameters
    sender = 'your-email@example.com'  # Replace with your verified sender email
    recipient = 'recipient-email@example.com'  # Replace with the recipient email
    subject = 'New S3 Object Uploaded'
    body_text = f'A new object has been uploaded to your S3 bucket.\n\nBucket: {bucket}\nKey: {key}'

    # Create the email
    try:
        response = ses.send_email(
            Source=sender,
            Destination={
                'ToAddresses': [recipient]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body_text
                    }
                }
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error sending email.')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully!')
    }

