from django import forms
from . models import CustomizedOrder


class CustomizedOrderForm(forms.ModelForm):
    class Meta:
        model = CustomizedOrder
        fields = ('order_type', 'front_text', 'back_text', 'color', 'logo',
                  'design_image', 'description', 'quantity')