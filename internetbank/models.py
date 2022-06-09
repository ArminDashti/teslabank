from django.db import models

class transaction(models.Model):
    from_id = models.IntegerField()
    to_id = models.IntegerField()
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

class customer_accounts(models.Model):
    balance = models.IntegerField(default=100)
    latest_update = models.DateTimeField(auto_now_add=True)
    account_number = models.IntegerField()
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.account_number = int(str(self.customer) + '1020')
        super().save(*args, **kwargs)
    



