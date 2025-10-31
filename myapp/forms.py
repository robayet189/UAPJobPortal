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


from django import forms
from django.contrib.auth.hashers import make_password
from .models import Faculty, FacultyEducation, FacultyExperience, FacultyProject, FacultyResearchInterest, \
    FacultyCourse, ProjectResearchArea


class FacultyRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Faculty
        fields = ['first_name', 'last_name', 'email', 'password', 'position', 'office', 'phone_number']
        widgets = {
            'password': forms.PasswordInput,
            'office': forms.TextInput(attrs={'placeholder': 'e.g., 7th floor, CSE dept. university campus'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g., +88-0167593251'}),
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


# Faculty Profile Forms
class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'position', 'office', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your bio...'}),
            'office': forms.TextInput(attrs={'placeholder': 'e.g., 7th Floor, CSE Department'}),
            'position': forms.TextInput(attrs={'placeholder': 'e.g., Professor, Assistant Professor'}),
        }


class FacultyEducationForm(forms.ModelForm):
    class Meta:
        model = FacultyEducation
        fields = ['degree', 'institution', 'period']
        widgets = {
            'degree': forms.TextInput(attrs={'placeholder': 'e.g., Ph.D. in Computer Science'}),
            'institution': forms.TextInput(attrs={'placeholder': 'e.g., University of Technology'}),
            'period': forms.TextInput(attrs={'placeholder': 'e.g., 2010 - 2014'}),
        }


class FacultyExperienceForm(forms.ModelForm):
    class Meta:
        model = FacultyExperience
        fields = ['job_title', 'company', 'period', 'description']
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Describe your responsibilities and achievements...'}),
            'job_title': forms.TextInput(attrs={'placeholder': 'e.g., Professor, Researcher'}),
            'company': forms.TextInput(attrs={'placeholder': 'e.g., University of Asia Pacific'}),
            'period': forms.TextInput(attrs={'placeholder': 'e.g., 2018 - Present'}),
        }


class FacultyProjectForm(forms.ModelForm):
    class Meta:
        model = FacultyProject
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your research project...'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g., AI-based Student Performance Prediction'}),
        }


class FacultyResearchInterestForm(forms.ModelForm):
    class Meta:
        model = FacultyResearchInterest
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Artificial Intelligence, Machine Learning'}),
        }


class FacultyCourseForm(forms.ModelForm):
    class Meta:
        model = FacultyCourse
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., CSE 101: Introduction to Programming'}),
        }


class ProjectResearchAreaForm(forms.ModelForm):
    class Meta:
        model = ProjectResearchArea
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Machine Learning, Data Analysis'}),
        }


# Formset for multiple entries
FacultyEducationFormSet = forms.modelformset_factory(
    FacultyEducation,
    form=FacultyEducationForm,
    extra=1,
    can_delete=True
)

FacultyExperienceFormSet = forms.modelformset_factory(
    FacultyExperience,
    form=FacultyExperienceForm,
    extra=1,
    can_delete=True
)

FacultyProjectFormSet = forms.modelformset_factory(
    FacultyProject,
    form=FacultyProjectForm,
    extra=1,
    can_delete=True
)

FacultyResearchInterestFormSet = forms.modelformset_factory(
    FacultyResearchInterest,
    form=FacultyResearchInterestForm,
    extra=1,
    can_delete=True
)

FacultyCourseFormSet = forms.modelformset_factory(
    FacultyCourse,
    form=FacultyCourseForm,
    extra=1,
    can_delete=True
)

ProjectResearchAreaFormSet = forms.modelformset_factory(
    ProjectResearchArea,
    form=ProjectResearchAreaForm,
    extra=1,
    can_delete=True
)


# Profile picture upload form
class FacultyProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['profile_picture']

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # Validate file size (5MB max)
            if profile_picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")

            # Validate file extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            extension = profile_picture.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("Unsupported file extension. Supported: JPG, JPEG, PNG, GIF")

        return profile_picture

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

from django import forms
from .models import Student, StudentEducation, StudentExperience, StudentProject, StudentSkill, ProjectTechnology

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'student_id', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class StudentEducationForm(forms.ModelForm):
    class Meta:
        model = StudentEducation
        fields = ['degree', 'institution', 'period']

class StudentExperienceForm(forms.ModelForm):
    class Meta:
        model = StudentExperience
        fields = ['job_title', 'company', 'period', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class StudentProjectForm(forms.ModelForm):
    class Meta:
        model = StudentProject
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class StudentSkillForm(forms.ModelForm):
    class Meta:
        model = StudentSkill
        fields = ['name']

# Alumni Profile Forms

from .models import Alumni, AlumniEducation, AlumniExperience, AlumniProject, AlumniSkill, AlumniProjectTechnology
class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'student_id', 'bio', 'current_position', 'company', 'linkedin_url']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class AlumniEducationForm(forms.ModelForm):
    class Meta:
        model = AlumniEducation
        fields = ['degree', 'institution', 'period']

class AlumniExperienceForm(forms.ModelForm):
    class Meta:
        model = AlumniExperience
        fields = ['job_title', 'company', 'period', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AlumniProjectForm(forms.ModelForm):
    class Meta:
        model = AlumniProject
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AlumniSkillForm(forms.ModelForm):
    class Meta:
        model = AlumniSkill
        fields = ['name']


# Add to forms.py
from .models import Company,CompanyProfile


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            'description', 'industry', 'company_size', 'founded_year',
            'website', 'address', 'city', 'country', 'mission_statement',
            'company_values', 'benefits', 'linkedin_url', 'twitter_url',
            'facebook_url'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your company, what you do, and your culture...'
            }),
            'mission_statement': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Your company\'s mission and vision...'
            }),
            'company_values': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'List your company values (one per line)...'
            }),
            'benefits': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'List company benefits and perks (one per line)...'
            }),
            'address': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Full company address...'
            }),
            'founded_year': forms.NumberInput(attrs={
                'min': 1900,
                'max': 2025
            })
        }

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        return website

    def clean_benefits(self):
        benefits = self.cleaned_data.get('benefits', '')
        # Validate that benefits are properly formatted
        if benefits:
            benefits_list = [benefit.strip() for benefit in benefits.split('\n') if benefit.strip()]
            if len(benefits_list) > 20:
                raise forms.ValidationError("Please limit benefits to 20 items maximum.")
        return benefits


class CompanyLogoForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['logo']

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo:
            # Validate file type
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            extension = logo.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("Unsupported file format. Please upload JPG, PNG, or GIF.")

            # Validate file size (5MB max)
            if logo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return logo


class CompanyCoverPhotoForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['cover_photo']

    def clean_cover_photo(self):
        cover_photo = self.cleaned_data.get('cover_photo')
        if cover_photo:
            # Validate file type
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            extension = cover_photo.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("Unsupported file format. Please upload JPG, PNG, or GIF.")

            # Validate file size (5MB max)
            if cover_photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return cover_photo


class CompanyBasicInfoForm(forms.ModelForm):
    """Form for company basic information (from Company model)"""

    class Meta:
        model = Company
        fields = ['company_name', 'email', 'phone_number', 'company_type']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': '+880 XXXX-XXXXXX'
            }),
            'company_type': forms.TextInput(attrs={
                'placeholder': 'e.g., Technology, Finance, Healthcare...'
            })
        }


# Add to forms.py

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'work_hours', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your bio...'}),
            'work_hours': forms.TextInput(attrs={'placeholder': 'e.g., Saturday-Thursday, 8.00 am to 7.00 pm'}),
        }


class AdminProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['profile_picture']

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")

            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            extension = profile_picture.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("Unsupported file extension. Supported: JPG, JPEG, PNG, GIF")
        return profile_picture


class AdminCoverPhotoForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['cover_photo']

    def clean_cover_photo(self):
        cover_photo = self.cleaned_data.get('cover_photo')
        if cover_photo:
            if cover_photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")

            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            extension = cover_photo.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("Unsupported file extension. Supported: JPG, JPEG, PNG, GIF")
        return cover_photo
