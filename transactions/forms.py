from django import forms
from .models import Transaction
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True 
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
class DepositeForm(TransactionForm):
    def clean_amount(self):
        min_deposite_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposite_amount:
            raise forms.ValidationError( F" your need to at least {min_deposite_amount}$")
        return amount
    
class WithdrawalForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 50
        max_withdraw_amount = 50000
        balance = account.balance
        
        amount = self.cleaned_data.get('amount')
        if amount< min_withdraw_amount:
            raise forms.ValidationError(f"you can withdraw at least {min_withdraw_amount}$")
        if amount > max_withdraw_amount:
            raise forms.ValidationError(f"you can  withdraw at most {max_withdraw_amount}$")
        if amount > balance:
            raise forms.ValidationError(
                f""" you have {balance}$ in your account
                   you can not withdraw more than your account {max_withdraw_amount}
                """
            )
        return amount
class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount