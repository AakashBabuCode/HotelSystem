from django import forms
from .models import Employee

# Registration Form (not using ModelForm, handling manually)
class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        employee = Employee(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=data['password']
        )
        employee.save()  # Save to MongoDB
        return employee

# Login Form (no changes needed here, it's fine as-is)
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)


# forms.py

from django import forms

class ProductForm(forms.Form):
    """Form to add new products."""
    name = forms.CharField(max_length=255, required=True, label='Product Name')
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label='Price')
    image = forms.FileField(required=False, label='Product Image')  # Use FileField for image uploads

