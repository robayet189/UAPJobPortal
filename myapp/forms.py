from django import forms
from django.contrib.auth.hashers import make_password
from .models import Student
from .models import Alumni
from .models import Faculty
from .models import Company
from .models import Administrator

class StudentRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'password', 'student_id', 'graduation_year']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Hash the password before saving
        if password:
            cleaned_data['password'] = make_password(password)

        return cleaned_data


class AlumniRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Alumni
        fields = ['first_name', 'last_name', 'email', 'password', 'student_id', 'graduation_year']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Hash the password before saving
        if password:
            cleaned_data['password'] = make_password(password)

        return cleaned_data



class FacultyRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Faculty
        fields = ['first_name', 'last_name', 'email', 'password', 'position']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Hash the password before saving
        if password:
            cleaned_data['password'] = make_password(password)

        return cleaned_data



class CompanyRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Company
        fields = ['company_name', 'email', 'password', 'company_type', 'phone_number']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Hash the password before saving
        if password:
            cleaned_data['password'] = make_password(password)

        return cleaned_data


class AdminRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Administrator
        fields = ['first_name','last_name','email', 'password', 'phone_number']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Hash the password before saving
        if password:
            cleaned_data['password'] = make_password(password)

        return cleaned_data

