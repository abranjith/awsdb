# awsdb

## Description

	Wrapper around the excellent boto3 api. Works just fine with dynamodb
 
## Usage

**import into your source file:**

`	from awsdb import DB`
	
**Create db object:**

>\#created with defaults - resource="dynamodb", region_name='us-east-1', endpoint_url=None. This works fine if you are usign this in an aws lambda function

`		db = DB()`
	
>\#if you have a dynamodb running in your localhost

`		db = DB(endpoint_url = "http://localhost:8000")`
	
>\#get a specific table object

`		table = db.get_table(table_name = "TABLE_NAME")`
	
**Read**

>\#read something from db for a specific primary key. In my case I am using dynamodb and I get json response

`		key = {'pk': "PK1"}`

>\#response will contain 'Item' object from my dynamodb table

`		response = db.read(table_name = "TABLE_NAME", key = key)`
	
**Write**

>\#write something to db. In this case both key and data to be written is needed. In case key already exists, same record will be udated in db

`		key = {'pk': "PK1"}`

`		data = {'data': "My data"}`

`		response = dynamodb.write(table_name = "TABLE_NAME", key = key, data = data)`
