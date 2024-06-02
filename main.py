import os
import json
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials


class Database:
    def getCustomers(self, employee_email: str) -> list[dict[str, int | float | str]]:
        raise NotImplementedError()
    def getActiveCustomers(self, employee_email: str) -> list[dict[str, int | float | str]]:
        raise NotImplementedError()
    
class GoogleSheetsCustomerDatabase(Database):
    def __init__(self, env_folder_path) -> None:
        self.api_key_path = os.path.join(env_folder_path, 'google_api_key.json')
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.sheet_name = "customers"
        self.client = self._authenticate()
    
    def _authenticate(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.api_key_path, self.scope)
        client = gspread.authorize(creds)
        return client

    def getCustomers(self, employee_email: str):
        sheet = self.client.open(self.sheet_name).sheet1
        records = sheet.get_all_records()
        employee_customers = [rec for rec in records if rec['customer_handled_by_email'] == employee_email]
        return employee_customers

    def getActiveCustomers(self, employee_email: str):
        employee_customers = self.getCustomers(employee_email)
        active_customers = [rec for rec in employee_customers if rec['active_customer_flag'] == True]
        return active_customers

class DatabricksCustomerDatabase(Database):
    def __init__(self, env_folder_path) -> None:
        api_key_path = os.path.join(env_folder_path, 'databricks_api_key.env')
        with open(api_key_path, 'r') as file:
            self.api_key = file.readlines()[0]
        self.db_host = 'https://cab402-n10484027-example.databricks.com'
        self.warehouse_id = "prod"

    def _executeQuery(self, query: str):
        query_resp = requests.post(
            self.db_host + '/api/2.0/sql/statements', 
            headers={'Authorization': 'Bearer ' + self.api_key},
            data=json.dumps({'statement': query, 'warehouse_id': self.warehouse_id})
            )
        if query_resp.status_code == 200:
            return query_resp.json()['result']['data_array'][0]
    
    def getCustomers(self, employee_email: str):
        query = f"select * from example.customers where customer_handled_by_email = {employee_email}"
        return self._executeQuery(query)

    def getActiveCustomers(self, employee_email: str):
        query = f"select * from example.customers where customer_handled_by_email = {employee_email} and active_customer_flag"
        return self._executeQuery(query)

class CustomerDatabaseFactory:
    def getDatabase(email: str, env_folder_path: str) -> Database:
        domain_name = email.split('@')[1]
        if domain_name == 'example.com':
            return GoogleSheetsCustomerDatabase(env_folder_path)
        elif domain_name == 'otherexample.com':
            return DatabricksCustomerDatabase(env_folder_path)
        else:
            raise Exception(email + " is not in our domain") 


class CustomersPortal:
    def __init__(self, database: Database, employee_email: str) -> None:
        self.customer_database = database
        self.employee_email = employee_email

    def eventShowCustomers(self, filter_active = False):
        if filter_active:
            customer_records = self.customer_database.getCustomers(self.employee_email)
        else:
            customer_records = self.customer_database.getActiveCustomers(self.employee_email)

        self.printResults(customer_records)

    def printResults(self, records: list[dict[str, int | float | str]]):
        if len(records) > 0:
            print(" | ".join(records[0].keys()))
        for record in records:
            print(" | ".join(record.items()))

def main():
    employee_email = input("Please Enter your Employee Email: ")
    database = CustomerDatabaseFactory.getDatabase(employee_email)
    interface = CustomersPortal(database, employee_email)
    
    while True:
        print("select an option: \n 1: show all your customers \n 2: show your active customers \n e: exit the application")
        option = input("Option: ")
        if option == '1':
            interface.eventShowCustomers()
        if option == '2':
            interface.eventShowCustomers(filter_active=False)
        if option == 'e':
            break

if __name__ == '__main__':
    main()