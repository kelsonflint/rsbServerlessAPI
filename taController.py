import boto3
import time
from pprint import pprint
from uuid import uuid4
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class TAController:

    def __init__(self, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        self.table = dynamodb.Table('technicalAssistance')
        self.SECRET_KEY = 'resilient small business'


    def create(self, ta, token):
        if self.verifyAuthToken(token):
            try:
                response = self.table.put_item(Item=ta)
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print('created new ta provider', ta['orgName'])
                return response
        else :
            return {
                "error": "invalid permissions"
            }
        
    def getAll(self):
        try:
            response = self.table.scan()['Items']
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response

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

    def update(self, id, t, token):
        if self.verifyAuthToken(token):
            try:
                response = self.table.update_item(
                    Key={
                        'id': id
                    },
                    UpdateExpression="set orgName=:on, description=:d, website=:w, phone=:p, email=:e, pocName=:poc, languages=:l, demographics=:demo, locations=:loc",
                    ExpressionAttributeValues={
                        ":on": t['orgName'],
                        ":d": t['description'],
                        ":w": t['website'],
                        ":p": t['phone'],
                        ":e": t['email'],
                        ":poc": t['pocName'],
                        ":l": t['languages'],
                        ":demo": t['demographics'],
                        ":loc": t['locations']
                    }
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print("updated ta provider w/ id", id)
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
                print("deleted ta provider w/ id", id)
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