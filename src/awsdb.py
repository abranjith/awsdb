import boto3

class DB():
    TABLE_CACHE = {}
    def __init__(self, resource="dynamodb", region_name='us-east-1', endpoint_url=None):
        self.resource = resource
        self.region_name = region_name
        self.endpoint_url = endpoint_url
        self.dynamodb = boto3.resource(resource, region_name = region_name, endpoint_url = endpoint_url)
    
    def create_table(self, table_name=None, table_params = None):
        if not (table_name and table_params):
            raise Exception("Table name and params are needed")
        try:
            self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=table_params['KeySchema'],
                AttributeDefinitions=table_params['AttributeDefinitions'],
                ProvisionedThroughput=table_params['ProvisionedThroughput']
            )
            table = self.dynamodb.Table(table_name)
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            DB.TABLE_CACHE[table_name] = table
            return table
        except Exception as e:
            raise Exception("Table could not be created -\n", str(e))
    
    def get_table(self, table_name = None, table_params = None):
        if not table_name:
            raise Exception("Table name is needed")

        if(DB.TABLE_CACHE.get(table_name)):
            return DB.TABLE_CACHE.get(table_name)
        
        if self._is_table_present(table_name):
            table = self.dynamodb.Table(table_name)
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            DB.TABLE_CACHE[table_name] = table
            return table
        return self.create_table(table_name, table_params)

    def _is_table_present(self, table_name):
        db = boto3.client(self.resource,region_name=self.region_name, endpoint_url=self.endpoint_url)
        try:
            db.describe_table(TableName = table_name)
            return True
        except:
            pass
        return False

    def read(self, table_name=None, key=None):
        if not (table_name and key):
            raise Exception("Table name and key to read are needed")
        table = DB.TABLE_CACHE[table_name]
        if not table:
            raise Exception("Table not found")
        response = table.get_item(Key=key)
        return response.get('Item', None)
    
    def write(self, table_name=None, key=None, data=None):
        if not(table_name and key):
            raise Exception("Table name and key are mandatory for writing")
        table = DB.TABLE_CACHE[table_name]
        if self.read(table_name=table_name, key=key):
            update_exprsn, exprsn_attr_values = self._get_update_query(data) if data else (None,None)
            response = table.update_item(Key = key, UpdateExpression = update_exprsn, ExpressionAttributeValues = exprsn_attr_values, ReturnValues="UPDATED_NEW")
        else:
            if data:
                response = table.put_item(Item = {**key, **data})
            else:
                response = table.put_item(Item = key)

        try:
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True
        except:
            pass
        return False
    
    def _get_update_query(self, data):
        update_exprsn = "set "
        updates = []
        exprsn_attr_values = {}
        alpha = 'a'
        for k,v in data.items():
            updates.append("{} = :{}".format(k, alpha))
            exprsn_attr_values[":{}".format(alpha)] = v
            alpha = chr(ord(alpha) + 1)
        update_exprsn += ",".join(updates)
        return update_exprsn, exprsn_attr_values

if __name__ == "__main__":
    print("Can't call directly")
