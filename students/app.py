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

################## CRUD Method 1
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

################## CRUD Method 2
    # Get All Items
def get_all_items():
    items = table.scan()
    return items['Items']

def get_all(event, context):
    try:
        items = get_all_items()
        return {
            'statusCode': 200,
            'body': json.dumps(items),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    # Get Item by ID
def get_item_by_id(item_id):
    item = table.get_item(Key={'id': item_id})
    return item['Item'] if 'Item' in item else None

def get_id(event, context):
    try:
        item_id = event['pathParameters']['id']
        item = get_item_by_id(item_id)

        if item:
            return {
                'statusCode': 200,
                'body': json.dumps(item),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Item not found',
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    # Put Items
def put_item(item_id):   # , item_name
    response = table.put_item(Item={'id': item_id})     # , 'name': item_name
    return response

def put_items(event, context):
    try:
        data = json.loads(event['body'])
        item_id = data['id']

        response = put_item(item_id)    # , item_name

        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            }
        }
    
# Update Item by ID
def update_item(item_id, updated_id):
    delete_item(item_id)
    response = put_item(updated_id)
    # attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
    #                          for key, value in request.form.items()}
    # response = table.update_item(Key=item_id, AttributeUpdates=attribute_updates)
    # response = table.update_item(
    #     Key={'id': item_id},
    #     UpdateExpression='SET id = :updated_id',
    #     #ExpressionAttributeNames={'#id': 'id'},
    #     ExpressionAttributeValues={':updated_id': updated_id}
    # )
    return response

def update_items(event, context):
    try:
        data = json.loads(event['body'])
        updated_id = data['id']
        item_id = event['pathParameters']['id'] # data['id']

        response = update_item(item_id, updated_id)

        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            }
        }

# Delete Item by ID
def delete_item(item_id):
    response = table.delete_item(Key={'id': item_id})
    return response

def delete_items(event, context):
    try:
        item_id = event['pathParameters']['id']

        response = delete_item(item_id)

        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            }
        }
    
################# S3 Lambda Function to push notifications
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