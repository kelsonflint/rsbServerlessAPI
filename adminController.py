import boto3
from pprint import pprint
from uuid import uuid4
import time
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)



class AdminController:
    
    def __init__(self, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        self.table = dynamodb.Table('Admin')
        self.SECRET_KEY = 'resilient small business'

    def create(self, admin):
        #create UUID
        # epoch = time.time()
        uniqueID = "%s" % (uuid4())
        print("Admin created with ID:", uniqueID)
        passwordHash = generate_password_hash(admin['password'])

        
        try:
            response = self.table.put_item(
                Item={
                    'id': uniqueID,
                    'email': admin['email'],
                    'password': passwordHash,
                    'firstName': admin['firstName'],
                    'lastName': admin['lastName']
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            response['id'] = uniqueID
            response['email'] = admin['email']
            response['firstName'] = admin['firstName']
            response['lastName'] = admin['lastName']
            response['token'] = self.generateAuthToken(uniqueID).decode('ascii')
            return response


    def get(self, id):
        try:
            response = self.table.get_item(Key={'id': id})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    def update(self, id, admin):
        try:
            auth = self.verifyAuthToken(admin['token'])
            if auth and id == auth:
                response = self.table.update_item(
                    Key={
                        'id': id,
                    },
                    UpdateExpression="set email=:e, firstName=:fn, lastName=:ln",
                    ExpressionAttributeValues={
                        ':e': admin['email'],
                        #':p': admin['password'],
                        ':fn': admin['firstName'],
                        ':ln': admin['lastName']
                    },
                    ReturnValues="UPDATED_NEW"
                )
            else:
                return {"error": "unauthorized access"}
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("updated admin w/ id", id)
            return response

    def delete(self, id):
        try:
            response = self.table.delete_item(
                Key={
                    'id': id
                },
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("deleted admin w/ id", id)
            return response
    

    def findAdmin(self, credentials):
        try:
            response = self.table.query(
                IndexName='email',
                KeyConditionExpression=Key('email').eq(credentials['email']),
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            if response['Items']:
                return response['Items'][0]
            else:
                return None

    def verifyPassword(self, admin, credentials):
        if not admin or not check_password_hash(admin['password'], credentials['password']):
            return False
        else:
            return True

    def generateAuthToken(self, id, expiration = 1800):
        s = Serializer(self.SECRET_KEY, expires_in = expiration)
        return s.dumps({'adminId': id})

    def verifyAuthToken(self, token):
        s = Serializer(self.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        adminId = data['adminId']
        return adminId

    def authAdmin(self, credentials):

        admin = self.findAdmin(credentials)
        auth = self.verifyPassword(admin, credentials)
        if auth:
            del admin["password"]
            admin["token"] = self.generateAuthToken(admin["id"]).decode("ascii")
            return admin
        else:
            return {"error": "email or password was incorrect"}

if __name__ == '__main__':
    controller = AdminController()
    controller.create({
                    'id': "3",
                    'email': "meme@gmail.com",
                    'password': "pass",
                    'firstName': "first",
                    'lastName': "last"
                })
    admin1 = controller.get("3")
    if admin1:
        print('get admin succeded')
        pprint(admin1, sort_dicts=False)
    else:
        print('failed')
    admin1['email'] = "change@gmail.com"
    controller.update("3", admin1)
    changed1 = controller.get("3")
    print(changed1['email'])
    controller.delete("3")
