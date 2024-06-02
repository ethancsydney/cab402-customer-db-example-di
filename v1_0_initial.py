import gspread
from oauth2client.service_account import ServiceAccountCredentials

class CustomerDatabase:
    def __init__(self, api_key_path, scope) -> None:
        creds = ServiceAccountCredentials.from_json_keyfile_name(api_key_path, scope)
        self.client = gspread.authorize(creds)
    
    def getCustomers(self, employee_email: str):
        sheet = self.client.open("customers").sheet1
        records = sheet.get_all_records()
        return [rec for rec in records if rec['customer_handled_by_email'] == employee_email]


class CustomersPortal:
    def __init__(self, scope, env_folder_path: str, employee_email: str) -> None:
        self.customer_database = CustomerDatabase(env_folder_path, scope)
        self.employee_email = employee_email

    def eventShowCustomers(self, filter_active = False):
        '''This is the event that is triggered when an employee presses the `show customers` button'''
        customer_records = self.customer_database.getCustomers(self.employee_email)
        if filter_active:
            customer_records = [rec for rec in customer_records if rec['active_customer_flag'] == True]
        print(" | ".join(customer_records[0].keys()))
        for record in customer_records:
            print(" | ".join(record.items()))



def manual_test():
    employee_email = input("Please Enter your Employee Email: ")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    interface = CustomersPortal(scope, employee_email)
    
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
    manual_test()