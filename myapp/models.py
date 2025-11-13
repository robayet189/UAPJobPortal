from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Add these fields to your existing Student model
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    student_id = models.CharField(max_length=20, unique=True)
    graduation_year = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ADD THESE PROFILE FIELDS:
    bio = models.TextField(blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


# Add these new models for education, experience, projects, and skills
# Add these models for student profile data
class StudentEducation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class StudentExperience(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class StudentProject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class StudentSkill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'name']

class ProjectTechnology(models.Model):
    project = models.ForeignKey(StudentProject, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Alumni(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    student_id = models.CharField(max_length=20, unique=True)
    graduation_year = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ADD THESE PROFILE FIELDS (Same as Student):
    bio = models.TextField(blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    profile_picture = models.ImageField(upload_to='alumni_profile_pics/', blank=True, null=True)
    resume = models.FileField(upload_to='alumni_resumes/', blank=True, null=True)
    current_position = models.CharField(max_length=200, blank=True, default='')
    company = models.CharField(max_length=200, blank=True, default='')
    linkedin_url = models.URLField(blank=True, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


# Add Alumni Profile Models (Similar to Student)
class AlumniEducation(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class AlumniExperience(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class AlumniProject(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class AlumniSkill(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['alumni', 'name']


class AlumniProjectTechnology(models.Model):
    project = models.ForeignKey(AlumniProject, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Faculty(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    position = models.CharField(max_length=100)

    # ADD THESE NEW FIELDS:
    office = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='faculty_profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, default='')

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


# Add Faculty Profile Models
class FacultyEducation(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class FacultyExperience(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class FacultyProject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class FacultyResearchInterest(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='research_interests')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['faculty', 'name']


class FacultyCourse(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class ProjectResearchArea(models.Model):
    project = models.ForeignKey(FacultyProject, on_delete=models.CASCADE, related_name='research_areas')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    company_type = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)  # For admin verification
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name  # FIXED: Was using first_name/last_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Administrator(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20)
    work_hours = models.TextField(blank=True, default='Saturday-Thursday, 8.00 am to 7.00 pm')
    bio = models.TextField(blank=True, default='')
    profile_picture = models.ImageField(upload_to='admin_profile_pics/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='admin_cover_photos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


from django.db import models


class Job(models.Model):
    JOB_STATUS = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('draft', 'Draft'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    ]

    JOB_TYPES = [
        ('full', 'Full Time'),
        ('part', 'Part Time'),
        ('intern', 'Internship'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    posted = models.CharField(max_length=50, default="Recently")
    deadline = models.DateField()
    is_new = models.BooleanField(default=False)
    job_type = models.CharField(max_length=50, choices=JOB_TYPES)
    description = models.TextField(blank=True)

    # Add these new fields
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='pending')
    posted_by = models.ForeignKey(Alumni, on_delete=models.CASCADE, null=True, blank=True)
    applicants = models.ManyToManyField(Student, through='Application', blank=True)
    salary = models.CharField(max_length=100, blank=True)
    requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending, reviewed, rejected, accepted

    class Meta:
        unique_together = ['student', 'job']


# Add this to your models.py after the Job model

class FacultyOpportunity(models.Model):
    OPPORTUNITY_STATUS = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    ]

    OPPORTUNITY_TYPES = [
        ('teaching', 'Teaching Assistant'),
        ('research', 'Research Assistant'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=200)
    department = models.CharField(max_length=200, default="CSE Department • University Campus")
    opportunity_type = models.CharField(max_length=50, choices=OPPORTUNITY_TYPES)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    expected_applicants = models.IntegerField(default=0)
    posted_date = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=OPPORTUNITY_STATUS, default='pending')
    posted_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    applicants = models.ManyToManyField(Student, through='FacultyApplication', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FacultyApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(FacultyOpportunity, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        unique_together = ['student', 'opportunity']

class CompanyJob(models.Model):
    JOB_STATUS = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
        ('rejected', 'Rejected'),
    ]

    JOB_TYPES = [
        ('full', 'Full Time'),
        ('part', 'Part Time'),
        ('intern', 'Internship'),
        ('contract', 'Contract'),
    ]

    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    salary = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='pending')  # keep THIS one
    expected_applicants = models.IntegerField(default=0)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"

class CompanyApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(CompanyJob, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        unique_together = ['student', 'job']


# Add to models.py
class ActivityLog(models.Model):
    ACTION_TYPES = [
        ('approval', 'Approval'),
        ('rejection', 'Rejection'),
        ('verification', 'Verification'),
        ('user_management', 'User Management'),
        ('system', 'System'),
    ]

    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=255)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class CompanyProfile(models.Model):
    COMPANY_SIZES = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1000+', '1000+ employees'),
    ]

    INDUSTRIES = [
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('other', 'Other'),
    ]

    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(blank=True, default='')
    industry = models.CharField(max_length=100, choices=INDUSTRIES, blank=True, default='')
    company_size = models.CharField(max_length=50, choices=COMPANY_SIZES, blank=True, default='')
    founded_year = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True, default='')
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='company_covers/', blank=True, null=True)

    # Social Media
    linkedin_url = models.URLField(blank=True, default='')
    twitter_url = models.URLField(blank=True, default='')
    facebook_url = models.URLField(blank=True, default='')

    # Contact Information
    address = models.TextField(blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')

    # Company Details
    mission_statement = models.TextField(blank=True, default='')
    company_values = models.TextField(blank=True, default='')
    benefits = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.company_name} Profile"

    def get_benefits_list(self):
        """Convert benefits text to list"""
        if self.benefits:
            return [benefit.strip() for benefit in self.benefits.split('\n') if benefit.strip()]
        return []

    # REMOVE the problematic save() method entirely
    # Don't override the save method for auto-creation

from django.db.models.signals import post_save
from django.dispatch import receiver

# Keep the signal but make it simpler
@receiver(post_save, sender=Company)
def create_company_profile(sender, instance, created, **kwargs):
    """Auto-create company profile when a new company is created"""
    if created:
        # Use get_or_create to avoid duplicates
        CompanyProfile.objects.get_or_create(company=instance)
        print(f"✅ Created CompanyProfile for {instance.company_name}")