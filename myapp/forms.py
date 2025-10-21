from django import forms
from django.contrib.auth.hashers import make_password
from .models import Student, Alumni, Faculty, Company, Administrator

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

        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        student.password = make_password(self.cleaned_data["password"])
        if commit:
            student.save()
        return student


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

        return cleaned_data

    def save(self, commit=True):
        alumni = super().save(commit=False)
        alumni.password = make_password(self.cleaned_data["password"])
        if commit:
            alumni.save()
        return alumni


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

        return cleaned_data

    def save(self, commit=True):
        faculty = super().save(commit=False)
        faculty.password = make_password(self.cleaned_data["password"])
        if commit:
            faculty.save()
        return faculty


class CompanyRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Company
        fields = ['company_name', 'email', 'password', 'company_type', 'phone_number']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        company_type = cleaned_data.get("company_type")

        # Check if required fields are present
        if not password:
            raise forms.ValidationError("Password is required.")
        if not confirm_password:
            raise forms.ValidationError("Please confirm your password.")
        if not company_type:
            raise forms.ValidationError("Company type is required.")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        company = super().save(commit=False)
        company.password = make_password(self.cleaned_data["password"])
        if commit:
            company.save()
        return company


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

        return cleaned_data

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.password = make_password(self.cleaned_data["password"])
        if commit:
            admin.save()
        return admin