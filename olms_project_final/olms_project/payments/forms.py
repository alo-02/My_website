from django import forms


class BkashPaymentForm(forms.Form):
    bkash_number = forms.CharField(
        label='bKash Number',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01XXXXXXXXX'})
    )
    transaction_id = forms.CharField(
        label='Transaction ID',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TrxID from bKash message'})
    )
