import boto3

def create_user_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        GlobalSecondaryIndexes=[
            {
                'IndexName':'email',
                'KeySchema': [
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                }
            }
        ]
    )
    return table 

def delete_user_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    
    table = dynamodb.Table('Users')
    table.delete()

def create_admin_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='Admin',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        GlobalSecondaryIndexes=[
            {
                'IndexName':'email',
                'KeySchema': [
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                }
            }
        ]
    )
    return table 

def delete_admin_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    
    table = dynamodb.Table('Admin')
    table.delete()

def create_businesses_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='Businesses',
        KeySchema=[
            {
                'AttributeName': 'userId',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'id',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }        
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table 
    
def delete_businesses_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    
    table = dynamodb.Table('Businesses')
    table.delete()


def create_funding_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='Funding',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }   
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table 
    
def delete_funding_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    
    table = dynamodb.Table('Funding')
    table.delete()

def create_ta_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='technicalAssistance',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table 

def delete_ta_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    
    table = dynamodb.Table('technicalAssistance')
    table.delete()

def create_announcements_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='Announcements',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }   
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table 
    
def delete_announcements_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    
    table = dynamodb.Table('Announcement')
    table.delete()

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    # delete_user_table(dynamodb)
    # delete_businesses_table(dynamodb)
    # delete_funding_table(dynamodb)
    # delete_ta_table(dynamodb)
    
    # user_table = create_user_table(dynamodb)
    # print("User table status: ", user_table.table_status)
    # businesses_table = create_businesses_table(dynamodb)
    # print("Businesses table status: ", businesses_table.table_status)
    # funding_table = create_funding_table(dynamodb)
    # print("Funding table status: ", funding_table.table_status)
    # ta_table = create_ta_table(dynamodb)
    # print("TA table status: ", ta_table.table_status)
    # admin_table = create_admin_table(dynamodb)
    # print("Admin table status: ", admin_table.table_status)
    # announcements_table = create_announcements_table(dynamodb)
    # print("Announcements table status: ", announcements_table.table_status)

