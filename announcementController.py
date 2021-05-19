import boto3
import time
from pprint import pprint
from uuid import uuid4
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class AnnouncementController:
    def __init__(self, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        self.table = dynamodb.Table('Announcements')
        self.SECRET_KEY = 'resilient small business'
    def create(self, a, token):
        if self.verifyAuthToken(token):
            uniqueId = "%s" % (uuid4())
            try:
                a['id'] = uniqueId
                response = self.table.put_item(Item=a)
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print('created new announcment', a['title'])
                return response
        else:
            return {
                "error": "invalid permissions"
            }
    
    def get(self, id):
        try:
            response = self.table.get_item(
                Key={
                    'id': id
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    def getAll(self):
        try:
            response = self.table.scan()['Items']
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response

    def update(self, id, a, token):
        if self.verifyAuthToken(token):
            try:
                response = self.table.update_item(
                    Key={
                        'id': id
                    },
                    UpdateExpression="set title=:t, description=:d, website=:w, endDate=:e, isActive=:a",
                    ExpressionAttributeValues={
                        ':t': a['title'],
                        ':d': a['description'],
                        ':w': a['website'],
                        ':e': a['endDate'],
                        ':a': a['isActive'],
                    }
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print("updated funding w/ id", id)
                return response
        else :
            return {
                "error": "invalid permissions"
            }

    def delete(self, id, token):
        if self.verifyAuthToken(token):
            try:
                response = self.table.delete_item(
                    Key={
                        'id': id
                    },
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print("deleted announcment w/ id", id)
                return response
        else :
            return {
                "error": "invalid permissions"
            }
    
    def verifyAuthToken(self, token):
        s = Serializer(self.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        if 'adminId' in data:
            return data['adminId']
        return None