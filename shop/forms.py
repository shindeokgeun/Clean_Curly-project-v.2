# shop/forms.py
from django import forms
from .models import Product
class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label='수량')
    # quantity = forms.IntegerField(
    #     min_value=1,
    #     initial=1,
    #     widget=forms.NumberInput(attrs={'id': 'quantity-input'})
    # )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # Product 모델과 연결
        fields = ['name', 'price', 'discount_price', 'image', 'category', 
                  'shipping_info', 'seller', 'packaging_type', 
                  'sales_unit', 'weight_volume', 'expiration_date', 
                  'Notice_info', 'allergy_info', 'livestock_trace_info']