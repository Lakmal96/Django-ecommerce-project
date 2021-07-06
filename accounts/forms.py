from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from . models import Customer, Supplier, User


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_email(self):
        email = self.cleaned_data['email']
        if not '@gmail.com' in email:
            raise forms.ValidationError("E-mail has to be a gmail")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) != 10:
            raise forms.ValidationError(
                "Phone number should only contain 10 numbers")
        elif phone_number.isdecimal() == False:
            raise forms.ValidationError(
                "Phone number cannot include charcters")
        return phone_number

    # to make sure all operations are done in a single database transaction
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.phone_number = self.cleaned_data.get('phone_number')
        customer.address = self.cleaned_data.get('address')
        customer.save()
        return user


class SupplierSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)
    company_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_email(self):
        email = self.cleaned_data['email']
        if not '@gmail.com' in email:
            raise forms.ValidationError("E-mail has to be a gmail")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) != 10:
            raise forms.ValidationError(
                "Phone number should only contain 10 numbers")
        elif phone_number.isdecimal() == False:
            raise forms.ValidationError(
                "Phone number cannot include charcters")
        return phone_number

    # to make sure all operations are done in a single database transaction
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_supplier = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        supplier = Supplier.objects.create(user=user)
        supplier.phone_number = self.cleaned_data.get('phone_number')
        supplier.address = self.cleaned_data.get('address')
        supplier.company_name = self.cleaned_data.get('company_name')
        supplier.save()
        return user
