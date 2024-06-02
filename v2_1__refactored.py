import json
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetsCustomerDatabase:
    def __init__(self, api_key_path, scope) -> None:
        creds = ServiceAccountCredentials.from_json_keyfile_name(api_key_path, scope)
        self.client = gspread.authorize(creds)
    
    def getCustomers(self, employee_email: str):
        sheet = self.client.open("customers").sheet1
        records = sheet.get_all_records()
        return [rec for rec in records if rec['customer_handled_by_email'] == employee_email]

class DatabricksCustomerDatabase:
    def __init__(self, api_key, db_host_url, warehouse_id) -> None:
        self.api_key = api_key
        self.db_host = db_host_url
        self.warehouse_id = warehouse_id

    def _executeQuery(self, query: str):
        query_resp = requests.post(
            self.db_host + '/api/2.0/sql/statements', 
            headers={'Authorization': 'Bearer ' + self.api_key},
            data=json.dumps({'statement': query, 'warehouse_id': self.warehouse_id}))
        if query_resp.status_code == 200:
            return query_resp.json()['result']['data_array'][0]
    
    def getCustomers(self, employee_email: str):
        query = f"select * from example.customers where customer_handled_by_email = {employee_email}"
        return self._executeQuery(query)

class CustomersPortal:
    def __init__(self, customer_database, employee_email: str) -> None:
        self.customer_database = customer_database
        self.employee_email = employee_email

    def eventShowCustomers(self, filter_active=False):
        '''This is the event that is triggered when an employee presses the `show customers` button'''
        customer_records = self.customer_database.getCustomers(self.employee_email)
        if filter_active:
            customer_records = [rec for rec in customer_records if rec['active_customer_flag'] == True]
        print(" | ".join(customer_records[0].keys()))
        for record in customer_records:
            print(" | ".join(record.items()))