from django.shortcuts import render

def home(request):
    return render(request, 'myapp/herosection.html')
def login(request):
    return render(request, 'myapp/login.html')

def register(request):
    return render(request, 'myapp/register.html')


def success(request):
    came_from = request.GET.get('from')

    back_urls = {
        "studentregistration": "/register/studentregistration/",
        "alumniregistration": "/register/alumniregistration/",
        "facultyregistration": "/register/facultyregistration/",
        "companyregistration": "/register/companyregistration/",
        "adminregistration": "/register/adminregistration/",
    }

    login_urls = {
        "studentregistration": "/login/studentlogin/",
        "alumniregistration": "/login/alumnilogin/",
        "facultyregistration": "/login/facultylogin/",
        "companyregistration": "/login/companylogin/",
        "adminregistration": "/login/adminlogin/",
    }

    back_url = back_urls.get(came_from, "/")
    login_url = login_urls.get(came_from, "/login/")

    return render(request, "myapp/success.html", {
        "back_url": back_url,
        "login_url": login_url})



from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentRegistrationForm, FacultyRegistrationForm
from .forms import AlumniRegistrationForm,CompanyRegistrationForm,AdminRegistrationForm
from .models import Student
from .models import Faculty
from .models import Alumni
from .models import Company
from .models import Administrator

def studentregistration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please check your email for verification.")
            return redirect('/success/?from=studentregistration')
    else:
        form = StudentRegistrationForm()

    return render(request, 'myapp/studentregistration.html', {'form': form})


def alumniregistration(request):
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please check your email for verification.")
            return redirect('/success/?from=alumniregistration')
    else:
        form = AlumniRegistrationForm()

    return render(request, 'myapp/alumniregistration.html', {'form': form})



def facultyregistration(request):
    if request.method == 'POST':
        form = FacultyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please check your email for verification.")
            return redirect('/success/?from=facultyregistration')
    else:
        form = FacultyRegistrationForm()

    return render(request, 'myapp/facultyregistration.html', {'form': form})

def companyregistration(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please check your email for verification.")
            return redirect('/success/?from=companyregistration')
    else:
        form = CompanyRegistrationForm()

    return render(request, 'myapp/companyregistration.html', {'form': form})


def adminregistration(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please check your email for verification.")
            return redirect('/success/?from=adminregistration')
    else:
        form = AdminRegistrationForm()

    return render(request, 'myapp/adminregistration.html', {'form': form})



def studentlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            messages.error(request, "Invalid email or password or not registered yet.")
            return redirect("stdlog")

        if check_password(password, student.password):
            # store session info
            request.session["student_id"] = student.id
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # replace with your dashboard/homepage
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("stdlog")

    return render(request, "myapp/studentlogin.html")


# views.py
def alumnilogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            alumni = Alumni.objects.get(email=email)
        except Alumni.DoesNotExist:
            messages.error(request, "Invalid email or password or not registered yet.")
            return redirect("almlog")

        if check_password(password, alumni.password):
            request.session["alumni_id"] = alumni.id
            messages.success(request, "Login successful!")
            return redirect("alumni_dashboard")  # <— go to alumni dashboard
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("almlog")

    return render(request, "myapp/alumnilogin.html")

def facultylogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            faculty = Faculty.objects.get(email=email)
        except Faculty.DoesNotExist:
            messages.error(request, "Invalid email or password or not registered yet.")
            return redirect("fcltlog")

        if check_password(password, faculty.password):
            # store session info
            request.session["faculty_id"] = faculty.id
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # replace with your dashboard/homepage
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("fcltlog")

    return render(request, "myapp/facultylogin.html")


def companylogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            company = Company.objects.get(email=email)
        except Company.DoesNotExist:
            messages.error(request, "Invalid email or password or not registered yet.")
            return redirect("comlog")

        if check_password(password, company.password):
            # store session info
            request.session["company_id"] = company.id
            messages.success(request, "Login successful!")
            return redirect("company_dashboard")  # replace with your dashboard/homepage
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("comlog")

    return render(request, "myapp/companylogin.html")


def adminlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            admin = Administrator.objects.get(email=email)
        except Administrator.DoesNotExist:
            messages.error(request, "Invalid email or password or not registered yet.")
            return redirect("adminlog")

        if check_password(password, admin.password):
            # store session info
            request.session["admin_id"] = admin.id
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # replace with your dashboard/homepage
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("adminlog")

    return render(request, "myapp/adminlogin.html")




from django.http import JsonResponse
from django.shortcuts import render
from .models import Job


def browse_opportunities(request):
    # Fetch alumni jobs
    alumni_jobs = Job.objects.filter(status='active').order_by('-created_at')

    # Fetch faculty opportunities
    faculty_opportunities = FacultyOpportunity.objects.filter(status='active').order_by('-created_at')

    # Combine both for the template
    all_opportunities = list(alumni_jobs) + list(faculty_opportunities)

    # Sort by creation date (newest first)
    all_opportunities.sort(key=lambda x: x.created_at, reverse=True)

    context = {
        'opportunities': all_opportunities,
    }
    return render(request, 'myapp/browseoppurtunity.html', context)


from django.db.models import Q  # Add this import
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import json
from .models import (
    Student, Alumni, Faculty, Company, Administrator,
    Job, Application, FacultyOpportunity, FacultyApplication,
    CompanyJob, CompanyApplication
)


def search_jobs(request):
    query = request.GET.get('q', '')
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')
    posted = request.GET.get('posted', '')

    # Search alumni jobs
    alumni_jobs = Job.objects.filter(status='active')
    # Search faculty opportunities
    faculty_opportunities = FacultyOpportunity.objects.filter(status='active')
    # Search company jobs - NEW
    company_jobs = CompanyJob.objects.filter(status='active')

    if query:
        alumni_jobs = alumni_jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(description__icontains=query)
        )
        faculty_opportunities = faculty_opportunities.filter(
            Q(title__icontains=query) |
            Q(department__icontains=query) |
            Q(description__icontains=query)
        )
        company_jobs = company_jobs.filter(  # NEW
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(requirements__icontains=query)
        )

    if job_type:
        # Map frontend job types to model values
        type_mapping = {
            'full': 'full',
            'part': 'part',
            'intern': 'intern'
        }
        mapped_type = type_mapping.get(job_type)
        if mapped_type:
            alumni_jobs = alumni_jobs.filter(job_type=mapped_type)
            faculty_opportunities = faculty_opportunities.filter(opportunity_type=mapped_type)
            company_jobs = company_jobs.filter(job_type=mapped_type)  # NEW

    if location:
        alumni_jobs = alumni_jobs.filter(location__icontains=location)
        company_jobs = company_jobs.filter(location__icontains=location)  # NEW

    # Handle posted date filter
    if posted:
        today = timezone.now().date()
        if posted == 'today':
            alumni_jobs = alumni_jobs.filter(created_at__date=today)
            faculty_opportunities = faculty_opportunities.filter(created_at__date=today)
            company_jobs = company_jobs.filter(created_at__date=today)  # NEW
        elif posted == 'week':
            week_ago = today - timedelta(days=7)
            alumni_jobs = alumni_jobs.filter(created_at__date__gte=week_ago)
            faculty_opportunities = faculty_opportunities.filter(created_at__date__gte=week_ago)
            company_jobs = company_jobs.filter(created_at__date__gte=week_ago)  # NEW
        elif posted == 'month':
            month_ago = today - timedelta(days=30)
            alumni_jobs = alumni_jobs.filter(created_at__date__gte=month_ago)
            faculty_opportunities = faculty_opportunities.filter(created_at__date__gte=month_ago)
            company_jobs = company_jobs.filter(created_at__date__gte=month_ago)  # NEW

    # Combine results
    jobs_data = []

    # Add alumni jobs
    for job in alumni_jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'posted': job.posted,
            'deadline': job.deadline.strftime('%B %d, %Y'),
            'is_new': job.is_new,
            'type': 'job',
            'job_type': job.job_type,
            'description': job.description,
            'salary': job.salary,
            'requirements': job.requirements.split('\n') if job.requirements else [],
            'posted_by': 'Alumni',
            'posted_date': job.created_at.strftime('%B %d, %Y')
        })

    # Add faculty opportunities
    for opportunity in faculty_opportunities:
        jobs_data.append({
            'id': opportunity.id,
            'title': opportunity.title,
            'department': opportunity.department,
            'location': "University Campus",
            'posted_date': opportunity.posted_date.strftime('%B %d, %Y'),
            'deadline': opportunity.deadline.strftime('%B %d, %Y'),
            'is_new': False,
            'type': 'faculty_opportunity',
            'opportunity_type': opportunity.opportunity_type,
            'description': opportunity.description,
            'requirements': opportunity.requirements.split('\n') if opportunity.requirements else [],
            'posted_by': f"{opportunity.posted_by.first_name} {opportunity.posted_by.last_name}",
            'salary': 'University Stipend'
        })

    # ADD COMPANY JOBS - NEW
    for job in company_jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company.company_name,
            'location': job.location,
            'type': 'company_job',
            'job_type': job.job_type,
            'description': job.description,
            'salary': job.salary,
            'requirements': job.requirements.split('\n') if job.requirements else [],
            'deadline': job.deadline.strftime('%B %d, %Y'),
            'posted_date': job.posted_date.strftime('%B %d, %Y'),
            'posted_by': job.company.company_name,
            'is_new': job.posted_date >= timezone.now().date() - timedelta(days=7)
        })

    return JsonResponse(jobs_data, safe=False)

def job_id(request):
    return render(request, 'myapp/job_id.html')

def forgotpassword(request, source):
    # Map source to login URL names
    login_urls = {
        'student': 'stdlog',
        'alumni': 'almlog',
        'faculty': 'fcltlog',
        'company': 'comlog',
        'admin': 'adminlog',
    }

    back_to_login = login_urls.get(source, 'login')

    return render(request, 'myapp/forgetpassword.html', {
        'back_to_login': back_to_login,
        'source': source
    })


def sendrecoverycode(request, source):
    login_urls = {
        'student': 'stdlog',
        'alumni': 'almlog',
        'faculty': 'fcltlog',
        'company': 'comlog',
        'admin': 'adminlog',
    }

    back_to_login = login_urls.get(source, 'login')

    # ADD THIS ENTIRE BLOCK ↓
    if request.method == 'POST':
        email = request.POST.get('email')

        model_map = {
            'student': Student,
            'alumni': Alumni,
            'faculty': Faculty,
            'company': Company,
            'admin': Administrator,
        }

        model = model_map.get(source)

        if model:
            try:
                user = model.objects.get(email=email)
                request.session['recovery_email'] = email
                request.session['recovery_source'] = source

                messages.success(request, "Verification code sent to your email!")
                return render(request, 'myapp/sendrecoverycode.html', {
                    'back_to_login': back_to_login,
                    'source': source
                })

            except model.DoesNotExist:
                messages.error(request, "Email not found. Please register first or try a different email.")
                return redirect('forgotpass', source=source)
        else:
            messages.error(request, "Invalid user type.")
            return redirect('forgotpass', source=source)
    # ADD BLOCK ENDS HERE ↑

    return render(request, 'myapp/sendrecoverycode.html', {
        'back_to_login': back_to_login,
        'source': source
    })


def tryanotheremail(request, source):
    login_urls = {
        'student': 'stdlog',
        'alumni': 'almlog',
        'faculty': 'fcltlog',
        'company': 'comlog',
        'admin': 'adminlog',
    }

    back_to_login = login_urls.get(source, 'login')

    return render(request, 'myapp/tryanotheremail.html', {
        'back_to_login': back_to_login,
        'source': source
    })



def sendcodenewmail(request, source):
    login_urls = {
        'student': 'stdlog',
        'alumni': 'almlog',
        'faculty': 'fcltlog',
        'company': 'comlog',
        'admin': 'adminlog',
    }

    back_to_login = login_urls.get(source, 'login')

    return render(request, 'myapp/send_code_to_new_mail.html', {
        'back_to_login': back_to_login,
        'source': source
    })


def resetpassword(request, source):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match (frontend also validates, but double-check on backend)
        if new_password and confirm_password and new_password == confirm_password:
            # TODO: Add your password update logic here
            # Example:
            # email = request.session.get('verified_email')
            # user = YourModel.objects.get(email=email)
            # user.password = make_password(new_password)
            # user.save()

            # Redirect to success page
            return redirect('resetpasswordsuccess', source=source)
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('resetpassword', source=source)

    login_urls = {
        'student': 'stdlog',
        'alumni': 'almlog',
        'faculty': 'fcltlog',
        'company': 'comlog',
        'admin': 'adminlog',
    }

    back_to_login = login_urls.get(source, 'login')

    return render(request, 'myapp/resetpassword.html', {
        'back_to_login': back_to_login,
        'source': source
    })


def resetpasswordsuccess(request, source):
    login_urls = {
        'student': 'stdlog',
        'alumni': 'almlog',
        'faculty': 'fcltlog',
        'company': 'comlog',
        'admin': 'adminlog',
    }

    back_to_login = login_urls.get(source, 'login')

    return render(request, 'myapp/RecoverPasswordSuccesfully.html', {
        'back_to_login': back_to_login,
        'source': source
    })


def verify_code(request, source):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        # TODO: Add your OTP verification logic here
        # Example:
        # if otp == request.session.get('recovery_code'):
        #     request.session['otp_verified'] = True
        #     return redirect('resetpassword', source=source)
        # else:
        #     messages.error(request, "Invalid verification code!")
        #     return redirect('sendrecoverycode', source=source)

        # For now, just redirect to reset password
        return redirect('resetpassword', source=source)

    return redirect('sendrecoverycode', source=source)

from django.http import JsonResponse

def dashboard(request):
    return render(request, 'myapp/studentdashboard.html')


from django.http import JsonResponse
from .models import Job, Application
import json


def get_jobs_for_students(request):
    """Get active jobs for student dashboard"""
    jobs = Job.objects.filter(status='active').order_by('-created_at')

    jobs_data = []
    for job in jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'posted': job.posted,
            'deadline': job.deadline.strftime('%B %d, %Y'),
            'job_type': job.job_type,
            'description': job.description,
            'salary': job.salary,
            'requirements': job.requirements.split('\n') if job.requirements else [],
            'is_new': job.is_new,
        })

    return JsonResponse(jobs_data, safe=False)


def get_alumni_jobs(request):
    """Get jobs for alumni dashboard (all jobs posted by this alumni)"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    alumni_id = request.session['alumni_id']
    jobs = Job.objects.filter(posted_by_id=alumni_id).order_by('-created_at')

    jobs_data = []
    for job in jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'posted': job.posted,
            'deadline': job.deadline.strftime('%B %d, %Y'),
            'status': job.status,
            'job_type': job.job_type,
            'applicants_count': job.applicants.count(),
            'description': job.description,
            'salary': job.salary,
            'requirements': job.requirements.split('\n') if job.requirements else [],
        })

    return JsonResponse(jobs_data, safe=False)


def post_job(request):
    """Handle job posting from alumni dashboard"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            alumni = Alumni.objects.get(id=request.session['alumni_id'])

            job = Job.objects.create(
                title=data['title'],
                company=data['company'],
                location=data['location'],
                deadline=data['deadline'],
                job_type=data['job_type'],
                description=data['description'],
                salary=data.get('salary', ''),
                requirements='\n'.join(data.get('requirements', [])),
                posted_by=alumni,
                status=data.get('status', 'active')
            )

            return JsonResponse({'success': True, 'job_id': job.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


def apply_to_job(request):
    """Handle job applications from students"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = Student.objects.get(id=request.session['student_id'])
            job = Job.objects.get(id=data['job_id'])

            # Check if already applied
            if Application.objects.filter(student=student, job=job).exists():
                return JsonResponse({'error': 'Already applied to this job'}, status=400)

            Application.objects.create(student=student, job=job)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)

# views.py
def alumni_dashboard(request):
    if 'alumni_id' not in request.session:
        return redirect('almlog')  # or wherever your alumni login is
    return render(request, 'myapp/alumnidashboard.html')

# views.py (add near your other job APIs)
from django.views.decorators.http import require_POST
import json
from .models import Job

@require_POST
def update_job(request, job_id):
    """Update a job (e.g., status=closed) owned by the logged-in alumni"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        payload = json.loads(request.body or "{}")
        new_status = payload.get('status')

        if new_status not in ['active', 'draft', 'closed']:
            return JsonResponse({'error': 'Invalid status'}, status=400)

        job = Job.objects.get(id=job_id, posted_by_id=request.session['alumni_id'])
        job.status = new_status
        job.save()
        return JsonResponse({'success': True})
    except Job.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def delete_job(request, job_id):
    """Delete a job owned by the logged-in alumni"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        job = Job.objects.get(id=job_id, posted_by_id=request.session['alumni_id'])
        job.delete()
        return JsonResponse({'success': True})
    except Job.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


from .models import FacultyOpportunity,FacultyApplication

def faculty_dashboard(request):
    if 'faculty_id' not in request.session:
        return redirect('fcltlog')
    return render(request, 'myapp/facultydashboard.html')


def get_faculty_opportunities(request):
    """Get opportunities for faculty dashboard"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    faculty_id = request.session['faculty_id']
    opportunities = FacultyOpportunity.objects.filter(posted_by_id=faculty_id).order_by('-created_at')

    opportunities_data = []
    for opportunity in opportunities:
        opportunities_data.append({
            'id': opportunity.id,
            'title': opportunity.title,
            'department': opportunity.department,
            'opportunity_type': opportunity.opportunity_type,
            'description': opportunity.description,
            'requirements': opportunity.requirements.split('\n') if opportunity.requirements else [],
            'expected_applicants': opportunity.expected_applicants,
            'posted_date': opportunity.posted_date.strftime('%B %d, %Y'),
            'deadline': opportunity.deadline.strftime('%B %d, %Y'),
            'status': opportunity.status,
            'applicants_count': opportunity.applicants.count(),
        })

    return JsonResponse(opportunities_data, safe=False)


def post_opportunity(request):
    """Handle opportunity posting from faculty dashboard"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            faculty = Faculty.objects.get(id=request.session['faculty_id'])

            opportunity = FacultyOpportunity.objects.create(
                title=data['title'],
                department=data['department'],
                opportunity_type=data['opportunity_type'],
                description=data['description'],
                requirements='\n'.join(data.get('requirements', [])),
                expected_applicants=data.get('expected_applicants', 0),
                deadline=data['deadline'],
                posted_by=faculty,
                status=data.get('status', 'active')
            )

            return JsonResponse({'success': True, 'opportunity_id': opportunity.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


@require_POST
def update_opportunity(request, opportunity_id):
    """Update an opportunity (e.g., status=closed)"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        payload = json.loads(request.body or "{}")
        new_status = payload.get('status')

        if new_status not in ['active', 'pending', 'closed']:
            return JsonResponse({'error': 'Invalid status'}, status=400)

        opportunity = FacultyOpportunity.objects.get(id=opportunity_id, posted_by_id=request.session['faculty_id'])
        opportunity.status = new_status
        opportunity.save()
        return JsonResponse({'success': True})
    except FacultyOpportunity.DoesNotExist:
        return JsonResponse({'error': 'Opportunity not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def delete_opportunity(request, opportunity_id):
    """Delete an opportunity"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        opportunity = FacultyOpportunity.objects.get(id=opportunity_id, posted_by_id=request.session['faculty_id'])
        opportunity.delete()
        return JsonResponse({'success': True})
    except FacultyOpportunity.DoesNotExist:
        return JsonResponse({'error': 'Opportunity not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def get_opportunity_applicants(request, opportunity_id):
    """Get applicants for a specific opportunity"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        opportunity = FacultyOpportunity.objects.get(id=opportunity_id, posted_by_id=request.session['faculty_id'])
        applications = FacultyApplication.objects.filter(opportunity=opportunity).select_related('student')

        applicants_data = []
        for application in applications:
            applicants_data.append({
                'id': application.student.id,
                'name': f"{application.student.first_name} {application.student.last_name}",
                'email': application.student.email,
                'student_id': application.student.student_id,
                'graduation_year': application.student.graduation_year,
                'applied_at': application.applied_at.strftime('%B %d, %Y %H:%M'),
                'status': application.status
            })

        return JsonResponse(applicants_data, safe=False)
    except FacultyOpportunity.DoesNotExist:
        return JsonResponse({'error': 'Opportunity not found'}, status=404)


def get_faculty_stats(request):
    """Get statistics for faculty dashboard"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    faculty_id = request.session['faculty_id']

    # Count total students (you might want to adjust this based on your logic)
    total_students = Student.objects.count()

    # Count faculty opportunities
    total_opportunities = FacultyOpportunity.objects.filter(posted_by_id=faculty_id).count()

    # Count students hired (you might want to track this differently)
    total_hired = FacultyApplication.objects.filter(
        opportunity__posted_by_id=faculty_id,
        status='accepted'
    ).count()

    # Count total applications
    total_applied = FacultyApplication.objects.filter(
        opportunity__posted_by_id=faculty_id
    ).count()

    return JsonResponse({
        'total_students': total_students,
        'total_opportunities': total_opportunities,
        'total_hired': total_hired,
        'total_applied': total_applied
    })


# Add to views.py

def get_faculty_opportunities_for_students(request):
    """Get active faculty opportunities for student dashboard"""
    opportunities = FacultyOpportunity.objects.filter(status='active').order_by('-created_at')

    opportunities_data = []
    for opportunity in opportunities:
        opportunities_data.append({
            'id': opportunity.id,
            'title': opportunity.title,
            'department': opportunity.department,
            'opportunity_type': opportunity.opportunity_type,
            'description': opportunity.description,
            'posted_date': opportunity.posted_date.strftime('%B %d, %Y'),
            'deadline': opportunity.deadline.strftime('%B %d, %Y'),
            'posted_by': f"{opportunity.posted_by.first_name} {opportunity.posted_by.last_name}",
        })

    return JsonResponse(opportunities_data, safe=False)


def apply_to_faculty_opportunity(request):
    """Handle student applications to faculty opportunities"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = Student.objects.get(id=request.session['student_id'])
            opportunity = FacultyOpportunity.objects.get(id=data['opportunity_id'])

            # Check if already applied
            if FacultyApplication.objects.filter(student=student, opportunity=opportunity).exists():
                return JsonResponse({'error': 'Already applied to this opportunity'}, status=400)

            FacultyApplication.objects.create(student=student, opportunity=opportunity)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


def company_dashboard(request):
    if 'company_id' not in request.session:
        return redirect('comlog')
    return render(request, 'myapp/companydashboard.html')


def get_company_profile(request):
    """Get company profile data"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])
        return JsonResponse({
            'id': company.id,
            'company_name': company.company_name,
            'email': company.email,
            'phone_number': company.phone_number,
            'company_type': company.company_type
        })
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)


def get_company_stats(request):
    """Get company dashboard statistics"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])

        # Count jobs by status
        active_jobs = CompanyJob.objects.filter(company=company, status='active').count()
        pending_jobs = CompanyJob.objects.filter(company=company, status='pending').count()
        closed_jobs = CompanyJob.objects.filter(company=company, status='closed').count()
        draft_jobs = CompanyJob.objects.filter(company=company, status='draft').count()
        total_jobs = CompanyJob.objects.filter(company=company).count()

        # Count total applicants across all jobs
        total_applicants = CompanyApplication.objects.filter(job__company=company).count()

        return JsonResponse({
            'active_jobs': active_jobs,
            'pending_jobs': pending_jobs,
            'closed_jobs': closed_jobs,
            'draft_jobs': draft_jobs,
            'total_applicants': total_applicants,
            'total_jobs': total_jobs
        })
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)


def get_company_jobs(request):
    """Get all jobs for a company"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])
        jobs = CompanyJob.objects.filter(company=company).order_by('-created_at')

        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'id': job.id,
                'title': job.title,
                'location': job.location,
                'job_type': job.job_type,
                'status': job.status,
                'description': job.description,
                'requirements': job.requirements.split('\n') if job.requirements else [],
                'salary': job.salary,
                'expected_applicants': job.expected_applicants,
                'deadline': job.deadline.strftime('%Y-%m-%d'),
                'posted_date': job.posted_date.strftime('%B %d, %Y'),
                'applicants_count': CompanyApplication.objects.filter(job=job).count()
            })

        return JsonResponse(jobs_data, safe=False)
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)


def post_company_job(request):
    """Handle job posting from company dashboard"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company = Company.objects.get(id=request.session['company_id'])

            job = CompanyJob.objects.create(
                title=data['title'],
                company=company,
                location=data['location'],
                description=data['description'],
                requirements='\n'.join(data.get('requirements', [])),
                salary=data.get('salary', ''),
                job_type=data['job_type'],
                expected_applicants=data.get('expected_applicants', 0),
                deadline=data['deadline'],
                status=data.get('status', 'active')
            )

            return JsonResponse({'success': True, 'job_id': job.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


def get_job_applicants(request, job_id):
    """Get applicants for a specific company job"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])
        job = CompanyJob.objects.get(id=job_id, company=company)
        applications = CompanyApplication.objects.filter(job=job).select_related('student')

        applicants_data = []
        for application in applications:
            applicants_data.append({
                'id': application.student.id,
                'name': f"{application.student.first_name} {application.student.last_name}",
                'email': application.student.email,
                'student_id': application.student.student_id,
                'graduation_year': application.student.graduation_year,
                'applied_at': application.applied_at.strftime('%B %d, %Y %H:%M'),
                'status': application.status
            })

        return JsonResponse(applicants_data, safe=False)
    except CompanyJob.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)


def update_company_job(request, job_id):
    """Update a company job"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company = Company.objects.get(id=request.session['company_id'])
            job = CompanyJob.objects.get(id=job_id, company=company)

            # Update fields if provided
            if 'status' in data:
                job.status = data['status']
            if 'title' in data:
                job.title = data['title']
            if 'location' in data:
                job.location = data['location']
            if 'description' in data:
                job.description = data['description']
            if 'salary' in data:
                job.salary = data['salary']
            if 'deadline' in data:
                job.deadline = data['deadline']

            job.save()
            return JsonResponse({'success': True})
        except CompanyJob.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


def delete_company_job(request, job_id):
    """Delete a company job"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])
        job = CompanyJob.objects.get(id=job_id, company=company)
        job.delete()
        return JsonResponse({'success': True})
    except CompanyJob.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def get_recent_applicants(request):
    """Get recent applicants for company dashboard"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])

        # Get recent applications (last 5)
        recent_applications = CompanyApplication.objects.filter(
            job__company=company
        ).select_related('student', 'job').order_by('-applied_at')[:5]

        applicants_data = []
        for application in recent_applications:
            applicants_data.append({
                'name': f"{application.student.first_name} {application.student.last_name}",
                'position': application.job.title,
                'time': application.applied_at.strftime('%H:%M'),
                'date': application.applied_at.strftime('%b %d, %Y')
            })

        return JsonResponse(applicants_data, safe=False)
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)


def apply_to_company_job(request):
    """Handle applications to company jobs from students"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = Student.objects.get(id=request.session['student_id'])
            job = CompanyJob.objects.get(id=data['job_id'])

            # Check if already applied
            if CompanyApplication.objects.filter(student=student, job=job).exists():
                return JsonResponse({'error': 'Already applied to this job'}, status=400)

            CompanyApplication.objects.create(student=student, job=job)
            return JsonResponse({'success': True})
        except CompanyJob.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


# Update student jobs API to include company jobs
def get_jobs_for_students(request):
    """Get active jobs for student dashboard - UPDATED to include company jobs"""
    # Alumni jobs
    alumni_jobs = Job.objects.filter(status='active').order_by('-created_at')
    # Company jobs - NEW
    company_jobs = CompanyJob.objects.filter(status='active').order_by('-created_at')

    jobs_data = []

    # Add alumni jobs
    for job in alumni_jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'posted': job.posted,
            'deadline': job.deadline.strftime('%B %d, %Y'),
            'job_type': job.job_type,
            'description': job.description,
            'salary': job.salary,
            'requirements': job.requirements.split('\n') if job.requirements else [],
            'is_new': job.is_new,
            'type': 'job',
            'posted_by_name': 'Alumni'
        })

    # Add company jobs - NEW
    for job in company_jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company.company_name,
            'location': job.location,
            'posted_date': job.posted_date.strftime('%B %d, %Y'),
            'deadline': job.deadline.strftime('%B %d, %Y'),
            'job_type': job.job_type,
            'description': job.description,
            'salary': job.salary,
            'requirements': job.requirements.split('\n') if job.requirements else [],
            'is_new': job.posted_date >= timezone.now().date() - timedelta(days=7),
            'type': 'company_job',
            'posted_by_name': job.company.company_name
        })

    return JsonResponse(jobs_data, safe=False)