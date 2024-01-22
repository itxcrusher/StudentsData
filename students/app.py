import json     # Serialize Data to JSON Format
import boto3    # Interact with AWS DynamoDB
from flask_lambda import FlaskLambda    # Integrate Flask with AWS Lambda
from flask import request   # Flask Framework Module
import os   # Access Environment Variables

app = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('students')
s3 = boto3.client('s3')
sns = boto3.client('sns')

@app.route('/students', methods=['GET', 'POST'])
def put_list_students():
    if request.method == 'GET':
        students = table.scan()['Items']
        return json_response(students)
    else:
        table.put_item(Item=request.form.to_dict())
        return json_response({"message": "student entry created"})

@app.route('/students/<id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_student(id):
    key = {'id': id}
    if request.method == 'GET':
        student = table.get_item(Key=key).get('Item')
        if student:
            return json_response(student)
        else:
            return json_response({"message": "student not found"}, 404)
    elif request.method == 'PATCH':
        attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
                             for key, value in request.form.items()}
        table.update_item(Key=key, AttributeUpdates=attribute_updates)
        return json_response({"message": "student entry updated"})
    else:
        table.delete_item(Key=key)
        return json_response({"message": "student entry deleted"})

def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}

def notification_handler(event, context):
    # Get the uploaded object details from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    size = event['Records'][0]['s3']['object']['size']
    # Construct the message to send
    subject = f"Object created in S3 bucket {bucket}"
    message = f"An object was uploaded to S3 bucket {bucket} with key {key} and size {size} bytes."
    # Publish the message to the SNS topic
    response = sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Message=message,
        Subject=subject
    )
    print(f"Notification sent to SNS topic: {response['MessageId']}")
    # Return the response
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }