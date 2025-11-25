from django import forms

class CouponForm(forms.Form):
    code = forms.CharField(
        label='Промокод',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите промокод'
        })
    )