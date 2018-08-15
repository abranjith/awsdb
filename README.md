# awsdb

## Description

Wrapper around the excellent [boto3](https://github.com/boto/boto3) api for DB operations in AWS. Works just fine with dynamodb
Tested with boto3==1.7.70 and python 3.6.*
 
## Usage

**import into your source file**

`	from awsdb import DB`
	
**Create db object**

	'''
	Creates with defaults - resource="dynamodb", region_name='us-east-1', endpoint_url=None. 
	This works fine if you are using this in an aws lambda function
	'''
	db = DB()
	
	'''
	If you have a dynamodb running in your localhost
	'''
	db = DB(endpoint_url = "http://localhost:8000")
	
	'''
	Get a specific table object. 
	This method creates the table and returns if not already present
	'''
	table = db.get_table(table_name = "TABLE_NAME", table_params = table_params)

	'''
	To just create table
	'''
	table = db.create_table(table_name = "TABLE_NAME", table_params = table_params)
	
**Read**

	'''
	Read something from db for a specific primary key. 
	In my case I am using dynamodb and I get json response back
	'''
	key = {'pk': "PK1"}

	'''
	Response will contain 'Item' object from my dynamodb table
	'''
	response = db.read(table_name = "TABLE_NAME", key = key)`
	
**Write**

	'''
	Write something to db
	In this case both key and data to be written is needed. If key already exists, existing record in table 
	will get updated with user data
	'''
	key = {'pk': "PK1"}
	data = {'data': "My data"}
	response = dynamodb.write(table_name = "TABLE_NAME", key = key, data = data)
