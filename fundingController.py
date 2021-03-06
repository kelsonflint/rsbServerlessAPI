import boto3
import time
from pprint import pprint
from uuid import uuid4
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class FundingController:

    def __init__(self, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        self.table = dynamodb.Table('Funding')
        self.SECRET_KEY = 'resilient small business'

    def create(self, funding, token):
        if self.verifyAuthToken(token):
            try:
                response = self.table.put_item(Item=funding)
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print('created new funding', funding['fundingName'])
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

    def update(self, id, f, token):
        if self.verifyAuthToken(token):
            try:
                response = self.table.update_item(
                    Key={
                        'id': id
                    },
                    UpdateExpression="set fundingName=:fn, fundingType=:ft, provider=:p, website=:w, startDate=:sd, endDate=:ed, uses=:uses, description=:d, terms=:t, useCases=:uc, NAICS=:na, demographics=:demo, nonprofit=:non",
                    ExpressionAttributeValues={
                        ':fn': f['fundingName'],
                        ':ft': f['fundingType'],
                        ':p': f['provider'],
                        ':w': f['website'],
                        ':sd': f['startDate'],
                        ':ed': f['endDate'],
                        ':uses': f['uses'],
                        ':d': f['description'],
                        ':t': f['terms'],
                        ':uc': f['useCases'],
                        ':na': f['NAICS'],
                        ':demo': f['demographics'],
                        ':non': f['nonprofit']
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
                print("deleted funding w/ id", id)
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

if __name__ == '__main__':
    print('main')