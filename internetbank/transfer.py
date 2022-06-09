from .checking import check_account
from django.contrib.auth.models import User
from .models import customer_accounts, transaction

def run_transfer(from_id, to_id, amount):
    transaction_id = transaction.objects.create(from_id=from_id, to_id=to_id, amount=amount)
    c1 = customer_accounts.objects.get(account_number=from_id)
    c1.balance = int((c1.balance)) - int(amount)
    c1.save()
    c2 = customer_accounts.objects.get(account_number=to_id)
    c2.balance = int((c2.balance)) + int(amount)
    c2.save()
    return transaction_id.id
