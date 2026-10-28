from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class Roles(BaseModel):
    roles_name = models.CharField(max_length=50)

    def __str__(self):
        return self.roles_name

class Users(BaseModel):
    roles = models.ForeignKey(Roles, on_delete= models.CASCADE)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    is_active = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Audit_logs(BaseModel):
    users = models.ForeignKey(Users, on_delete= models.CASCADE)
    action = models.CharField(max_length=100)
    action_timestamp = models.DateTimeField(auto_now_add=True)
    entity_name = models.CharField(max_length=50)
        

    def __str__(self):
        return self.entity_name

class Client_profile(BaseModel):
    users = models.ForeignKey(Users, on_delete= models.CASCADE)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    birth_date = models.DateField()
    adress = models.CharField(max_length=60)
    monthly_income = models.DecimalField(12,2)
    phone_number = models.CharField(max_length=20)
    
    def __str__(self):
        return self.users

class Savings_account(BaseModel):
    client_profile = models.ForeignKey(Client_profile, on_delete= models.CASCADE)
    account_no = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    current_balance = models.DecimalField(12,2)
    annual_interest_rate = models.DecimalField(12,2)
    opened_at = models.DateTimeField(default=timezone.now)    
    
    def __str__(self):
        return self.account_no

class Savings_transaction(BaseModel):
    savings_account = models.ForeignKey(Savings_account, on_delete= models.CASCADE)
    transaction_type = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=50)
    amount = models.DecimalField(12,2)
    transaction_date = models.DateField()    
    
    def __str__(self):
        return self.savings_account

class Loan_application(BaseModel):
    client_profile = models.ForeignKey(Client_profile, on_delete= models.CASCADE)
    users = models.ForeignKey(Users, on_delete= models.CASCADE)
    requested_term_months = models.DecimalField(12,2)
    status = models.CharField(max_length=20)
    purpose = models.CharField(max_length=100)
    amount_requested = models.DecimalField(12,2)
    application_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.client_profile

class Loan_agreement(BaseModel):
    loan_application = models.ForeignKey(Loan_application, on_delete= models.CASCADE)
    signed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.loan_application

class Loans(BaseModel):
    loan_application = models.ForeignKey(Loan_application, on_delete= models.CASCADE)
    term_months = models.IntegerField()
    status = models.CharField(max_length=20)
    annual_interest_rate = models.DecimalField(12,2)
    principal_amount = models.DecimalField(12,2)
    outstanding_balance = models.DecimalField(12,2)
    disbursement_date = models.DateField()
    
    def __str__(self):
        return self.loan_application

class Amortization_schedule(BaseModel):
    loans = models.ForeignKey(Loans, on_delete= models.CASCADE)
    installment_no = models.IntegerField()
    due_date = models.DateField() 
    interest_due = models.DecimalField(12,2)
    principal_due = models.DecimalField(12,2)
    total_due = models.DecimalField(12,2)
    amount_paid = models.DecimalField(12,2)
    status = models.CharField(max_length=30)
        
    def __str__(self):
        return self.installment_no
    
class Loan_payments(BaseModel):
    loans = models.ForeignKey(Loans, on_delete= models.CASCADE)
    amortization_schedule = models.ForeignKey(Amortization_schedule, on_delete= models.CASCADE)
    payment_date = models.DateField() 
    amount = models.DecimalField(12,2)
    status = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=45)
    reference_number = models.CharField(max_length=30)

    def __str__(self):
        return self.loans

class Transaction_records(BaseModel):
    loans = models.ForeignKey(Loans, on_delete= models.CASCADE)
    savings_transaction = models.ForeignKey(Savings_transaction, on_delete= models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True) 
    debit_amount = models.DecimalField(12,2)
    credit_amount = models.DecimalField(12,2)
    entry_type = models.CharField(max_length=45)
    account_code = models.CharField(max_length=45)

    def __str__(self):
        return self.account_code

class Notifications(BaseModel):
    users = models.ForeignKey(Users, on_delete= models.CASCADE)
    channel = models.CharField(max_length=50)
    status = models.CharField(max_length=45)
    message = models.CharField(max_length=100)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.channel
    