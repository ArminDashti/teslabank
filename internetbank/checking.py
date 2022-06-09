from .models import customer_accounts
from django.contrib.auth.models import User

class check_account:

    def check_customer_exist(self, get_account_number):
        get_customer_account_for_to_id = customer_accounts.objects.filter(account_number = get_account_number)
        if len(get_customer_account_for_to_id) == 0:
            return False
        else:
            return True

    def check_customer_password(self, customer_id, customer_password):
        user = User.objects.get(id=customer_id)
        if user.check_password(customer_password):
            return True
        else:
            return False
    
    def get_customer_information(self, auth_id):
        customer_auth = User.objects.get(id=auth_id)
        user_name = customer_auth.username
        first_name = customer_auth.first_name
        last_name = customer_auth.last_name
        customer_account = customer_accounts.objects.get(customer_id = auth_id)
        balance = customer_account.balance
        account_number = customer_account.account_number
        return {'auth_id':auth_id, 'user_name':user_name, 'first_name':first_name, 'last_name':last_name, 'balance':balance, 'account_number':account_number}
