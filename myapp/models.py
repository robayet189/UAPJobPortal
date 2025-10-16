from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Always store hashed passwords!
    student_id = models.CharField(max_length=20, unique=True)
    graduation_year = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)



class Alumni(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Always store hashed passwords!
    student_id = models.CharField(max_length=20, unique=True)
    graduation_year = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


class Faculty(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Always store hashed passwords!
    position = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


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
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


from django.db import models


class Job(models.Model):
    JOB_STATUS = [
        ('pending', 'Pending'),  # ADD THIS
        ('active', 'Active'),
        ('draft', 'Draft'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),  # ADD THIS
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
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='active')
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
        ('pending', 'Pending'),  # ADD THIS
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),  # ADD THIS
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
    status = models.CharField(max_length=20, choices=OPPORTUNITY_STATUS, default='active')
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
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='pending')
    expected_applicants = models.IntegerField(default=0)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='pending')

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