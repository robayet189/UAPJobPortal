from django.db import models

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



class Company(models.Model):
    company_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Always store hashed passwords!
    company_type = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
        ('active', 'Active'),
        ('draft', 'Draft'),
        ('closed', 'Closed'),
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