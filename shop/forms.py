# shop/forms.py
from django import forms

class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label='수량')
    # quantity = forms.IntegerField(
    #     min_value=1,
    #     initial=1,
    #     widget=forms.NumberInput(attrs={'id': 'quantity-input'})
    # )