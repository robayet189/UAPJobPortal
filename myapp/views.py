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
            company = form.save(commit=False)
            company.is_verified = False  # Companies start unverified
            company.save()
            messages.success(request, "Registration successful! Please wait for admin verification.")
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
            # ✅ FORCE SESSION CREATION
            if not request.session.session_key:
                request.session.create()

            # ✅ SET SESSION DATA
            request.session["student_id"] = student.id
            request.session.set_expiry(86400)

            # ✅ DEBUG
            print(f"✅ LOGIN SUCCESS: Session created - {request.session.session_key}")
            print(f"✅ Session data: {dict(request.session)}")

            messages.success(request, "Login successful!")
            return redirect("dashboard")
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
            return redirect("faculty_dashboard")  # replace with your dashboard/homepage
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

        print(f"Admin login attempt: {email}")  # Debug print

        try:
            admin = Administrator.objects.get(email=email)

            if check_password(password, admin.password):
                request.session["admin_id"] = admin.id
                print(f"✅ ADMIN LOGIN SUCCESS: Session created - {request.session.session_key}")  # Debug print
                print(f"✅ Admin session data: {dict(request.session)}")  # Debug print

                messages.success(request, "Login successful!")
                return redirect("custom_admin_dashboard")
            else:
                messages.error(request, "Invalid email or password.")
                return redirect("adminlog")

        except Administrator.DoesNotExist:
            messages.error(request, "Invalid email or password or not registered yet.")
            return redirect("adminlog")

    return render(request, "myapp/adminlogin.html")



from django.http import JsonResponse
from django.shortcuts import render
from .models import Job


def browse_opportunities(request):
    alumni_jobs = Job.objects.filter(status='active').order_by('-created_at')
    faculty_opportunities = FacultyOpportunity.objects.filter(status='active').order_by('-created_at')
    company_jobs = CompanyJob.objects.filter(status='active').order_by('-created_at')  # NEW

    all_opportunities = list(alumni_jobs) + list(faculty_opportunities) + list(company_jobs)
    all_opportunities.sort(key=lambda x: x.created_at, reverse=True)

    context = {'opportunities': all_opportunities}
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

    alumni_jobs = Job.objects.filter(status='active')  # CHANGED
    faculty_opportunities = FacultyOpportunity.objects.filter(status='active')  # CHANGED
    company_jobs = CompanyJob.objects.filter(status='active')  # CHANGED


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


def job_detail(request, job_id):
    """Dynamic job detail page"""
    try:
        # Try to find the job in different models
        job = None
        job_type = None

        # Check alumni jobs
        if Job.objects.filter(id=job_id).exists():
            job = Job.objects.get(id=job_id)
            job_type = 'alumni_job'
        # Check faculty opportunities
        elif FacultyOpportunity.objects.filter(id=job_id).exists():
            job = FacultyOpportunity.objects.get(id=job_id)
            job_type = 'faculty_opportunity'
        # Check company jobs
        elif CompanyJob.objects.filter(id=job_id).exists():
            job = CompanyJob.objects.get(id=job_id)
            job_type = 'company_job'

        if job:
            # Get similar jobs for the sidebar
            similar_jobs = get_similar_jobs(job, job_type)

            context = {
                'job': job,
                'job_type': job_type,
                'similar_jobs': similar_jobs,
            }
            return render(request, 'myapp/job_id.html', context)
        else:
            return render(request, 'myapp/job_id.html', {'error': 'Job not found'})

    except Exception as e:
        return render(request, 'myapp/job_id.html', {'error': str(e)})


def get_similar_jobs(main_job, job_type):
    """Get similar jobs based on the main job"""
    similar_jobs = []

    if job_type == 'alumni_job':
        # Get other alumni jobs with similar titles
        similar = Job.objects.filter(
            status='active'
        ).exclude(id=main_job.id).order_by('-created_at')[:2]

        for job in similar:
            similar_jobs.append({
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'deadline': job.deadline.strftime('%B %d, %Y'),
                'type': 'alumni_job'
            })

    elif job_type == 'faculty_opportunity':
        # Get other faculty opportunities
        similar = FacultyOpportunity.objects.filter(
            status='active'
        ).exclude(id=main_job.id).order_by('-created_at')[:2]

        for opportunity in similar:
            similar_jobs.append({
                'id': opportunity.id,
                'title': opportunity.title,
                'company': opportunity.department,
                'deadline': opportunity.deadline.strftime('%B %d, %Y'),
                'type': 'faculty_opportunity'
            })

    elif job_type == 'company_job':
        # Get other company jobs
        similar = CompanyJob.objects.filter(
            status='active'
        ).exclude(id=main_job.id).order_by('-created_at')[:2]

        for job in similar:
            similar_jobs.append({
                'id': job.id,
                'title': job.title,
                'company': job.company.company_name,
                'deadline': job.deadline.strftime('%B %d, %Y'),
                'type': 'company_job'
            })

    return similar_jobs

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
    """Student dashboard page"""
    # ✅ ADD THIS SESSION CHECK
    if 'student_id' not in request.session:
        print("❌ DASHBOARD: No student_id in session, redirecting to login")
        return redirect('stdlog')

    # ✅ DEBUG: Print session info
    print(f"✅ DASHBOARD: Student ID in session: {request.session.get('student_id')}")
    print(f"✅ DASHBOARD: Session key: {request.session.session_key}")

    return render(request, 'myapp/studentdashboard.html')

from django.http import JsonResponse
from .models import Job, Application
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page


def get_student_dashboard_data(request):
    """API to get student data for dashboard profile section"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])

        return JsonResponse({
            'success': True,
            'student': {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'full_name': f"{student.first_name} {student.last_name}",
                'email': student.email,
                'student_id': student.student_id,
                'graduation_year': student.graduation_year,
                'profile_picture_url': student.profile_picture.url if student.profile_picture else '/static/default-profile.png',
            }
        })
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_jobs_for_students(request):
    """Active & approved only: alumni jobs, faculty opps, company jobs WITH applied status"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])

        # Get applied job IDs for this student
        applied_job_ids = set(Application.objects.filter(student=student).values_list('job_id', flat=True))
        applied_faculty_opportunity_ids = set(
            FacultyApplication.objects.filter(student=student).values_list('opportunity_id', flat=True))
        applied_company_job_ids = set(
            CompanyApplication.objects.filter(student=student).values_list('job_id', flat=True))

        alumni_jobs = Job.objects.filter(status='active').order_by('-created_at')
        company_jobs = CompanyJob.objects.filter(status='active').order_by('-created_at')
        faculty_opportunities = FacultyOpportunity.objects.filter(status='active').order_by('-created_at')

        jobs_data = []

        # Alumni jobs
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
                'posted_by_name': 'Alumni',
                'applied': job.id in applied_job_ids  # ADD THIS LINE
            })

        # Company jobs
        from datetime import timedelta
        from django.utils import timezone
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
                'posted_by_name': job.company.company_name,
                'applied': job.id in applied_company_job_ids  # ADD THIS LINE
            })

        # Faculty opportunities
        for opportunity in faculty_opportunities:
            jobs_data.append({
                'id': opportunity.id,
                'title': opportunity.title,
                'company': opportunity.department,
                'location': "University Campus",
                'posted_date': opportunity.posted_date.strftime('%B %d, %Y'),
                'deadline': opportunity.deadline.strftime('%B %d, %Y'),
                'job_type': opportunity.opportunity_type,
                'description': opportunity.description,
                'salary': 'University Stipend',
                'requirements': opportunity.requirements.split('\n') if opportunity.requirements else [],
                'is_new': opportunity.posted_date >= timezone.now().date() - timedelta(days=7),
                'type': 'faculty_opportunity',
                'posted_by_name': f"{opportunity.posted_by.first_name} {opportunity.posted_by.last_name}",
                'applied': opportunity.id in applied_faculty_opportunity_ids  # ADD THIS LINE
            })

        return JsonResponse(jobs_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
                status='pending'  # <-- FORCE pending
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

            # Create the application
            application = Application.objects.create(student=student, job=job)

            # Return success with application data
            return JsonResponse({
                'success': True,
                'application_id': application.id,
                'message': 'Application submitted successfully!'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


def get_applied_jobs(request):
    """Get all jobs that the student has applied to (all types)"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])

        applied_jobs_data = []

        # 1. Get applied alumni jobs
        alumni_applications = Application.objects.filter(student=student).select_related('job')
        for application in alumni_applications:
            job = application.job
            applied_jobs_data.append({
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'deadline': job.deadline.strftime('%B %d, %Y'),
                'job_type': job.job_type,
                'description': job.description,
                'salary': job.salary,
                'requirements': job.requirements.split('\n') if job.requirements else [],
                'is_new': job.is_new,
                'type': 'job',  # alumni job
                'applied': True,
                'applied_at': application.applied_at.strftime('%B %d, %Y %H:%M'),
            })

        # 2. Get applied faculty opportunities
        faculty_applications = FacultyApplication.objects.filter(student=student).select_related('opportunity')
        for application in faculty_applications:
            opportunity = application.opportunity
            applied_jobs_data.append({
                'id': opportunity.id,
                'title': opportunity.title,
                'company': opportunity.department,
                'location': "University Campus",
                'deadline': opportunity.deadline.strftime('%B %d, %Y'),
                'job_type': opportunity.opportunity_type,
                'description': opportunity.description,
                'salary': 'University Stipend',
                'requirements': opportunity.requirements.split('\n') if opportunity.requirements else [],
                'is_new': False,
                'type': 'faculty_opportunity',
                'applied': True,
                'applied_at': application.applied_at.strftime('%B %d, %Y %H:%M'),
            })

        # 3. Get applied company jobs
        company_applications = CompanyApplication.objects.filter(student=student).select_related('job')
        for application in company_applications:
            job = application.job
            applied_jobs_data.append({
                'id': job.id,
                'title': job.title,
                'company': job.company.company_name,
                'location': job.location,
                'deadline': job.deadline.strftime('%B %d, %Y'),
                'job_type': job.job_type,
                'description': job.description,
                'salary': job.salary,
                'requirements': job.requirements.split('\n') if job.requirements else [],
                'is_new': job.posted_date >= timezone.now().date() - timedelta(days=7),
                'type': 'company_job',
                'applied': True,
                'applied_at': application.applied_at.strftime('%B %d, %Y %H:%M'),
            })

        return JsonResponse(applied_jobs_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
@require_POST
def update_job(request, job_id):
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        payload = json.loads(request.body or "{}")
        new_status = payload.get('status')

        # Alumni cannot self-activate or set pending
        if new_status and new_status not in ['draft', 'closed']:
            return JsonResponse({'error': 'Forbidden status change'}, status=403)

        job = Job.objects.get(id=job_id, posted_by_id=request.session['alumni_id'])
        if new_status:
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
    print(f"🔍 DELETE JOB: Attempting to delete job {job_id}")

    if 'alumni_id' not in request.session:
        print("❌ DELETE JOB: No alumni session found")
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        alumni_id = request.session['alumni_id']
        print(f"🔍 DELETE JOB: Alumni ID from session: {alumni_id}")

        # Get the job and verify ownership
        job = Job.objects.get(id=job_id, posted_by_id=alumni_id)
        job_title = job.title

        print(f"🔍 DELETE JOB: Found job '{job_title}' owned by alumni {alumni_id}")

        # Delete the job
        job.delete()

        print(f"✅ DELETE JOB: Successfully deleted job '{job_title}'")

        return JsonResponse({
            'success': True,
            'message': f'Job "{job_title}" has been deleted successfully'
        })

    except Job.DoesNotExist:
        print(f"❌ DELETE JOB: Job {job_id} not found or not owned by alumni {alumni_id}")
        return JsonResponse({
            'error': 'Job not found or you do not have permission to delete this job'
        }, status=404)
    except Exception as e:
        print(f"❌ DELETE JOB: Unexpected error: {str(e)}")
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
                requirements='\n'.join(data.get('requirements', [])),  # Handle requirements
                expected_applicants=data.get('expected_applicants', 0),
                deadline=data['deadline'],
                posted_by=faculty,
                status=data.get('status', 'pending')
            )

            return JsonResponse({'success': True, 'opportunity_id': opportunity.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)

@require_POST
def update_opportunity(request, opportunity_id):
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        payload = json.loads(request.body or "{}")
        new_status = payload.get('status')

        # Faculty cannot self-activate
        if new_status and new_status not in ['closed', 'pending']:
            return JsonResponse({'error': 'Forbidden status change'}, status=403)

        opportunity = FacultyOpportunity.objects.get(id=opportunity_id, posted_by_id=request.session['faculty_id'])
        if new_status:
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

            # Check if company is verified
            if not company.is_verified:
                return JsonResponse({'error': 'Company not verified. Please wait for admin verification.'}, status=400)

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
                status='pending'  # CHANGED: Needs admin approval
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


@require_POST
def update_company_job(request, job_id):
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        company = Company.objects.get(id=request.session['company_id'])
        job = CompanyJob.objects.get(id=job_id, company=company)

        # Restrict status changes
        if 'status' in data:
            if data['status'] not in ['closed', 'draft']:
                return JsonResponse({'error': 'Forbidden status change'}, status=403)
            job.status = data['status']

        # Allow safe field edits
        for f in ['title', 'location', 'description', 'salary', 'deadline']:
            if f in data:
                setattr(job, f, data[f])

        job.save()
        return JsonResponse({'success': True})
    except CompanyJob.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


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


# In get_jobs_for_students function - UPDATE filter
def get_jobs_for_students(request):
    """Active & approved only: alumni jobs, faculty opps, company jobs"""
    alumni_jobs = Job.objects.filter(status='active').order_by('-created_at')
    company_jobs = CompanyJob.objects.filter(status='active').order_by('-created_at')
    faculty_opportunities = FacultyOpportunity.objects.filter(status='active').order_by('-created_at')

    jobs_data = []

    # Alumni jobs
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

    # Company jobs
    from datetime import timedelta
    from django.utils import timezone
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

    # Faculty opportunities (expose alongside jobs)
    for opportunity in faculty_opportunities:
        jobs_data.append({
            'id': opportunity.id,
            'title': opportunity.title,
            'company': opportunity.department,  # or 'CSE Department'
            'location': "University Campus",
            'posted_date': opportunity.posted_date.strftime('%B %d, %Y'),
            'deadline': opportunity.deadline.strftime('%B %d, %Y'),
            'job_type': opportunity.opportunity_type,
            'description': opportunity.description,
            'salary': 'University Stipend',
            'requirements': opportunity.requirements.split('\n') if opportunity.requirements else [],
            'is_new': opportunity.posted_date >= timezone.now().date() - timedelta(days=7),
            'type': 'faculty_opportunity',
            'posted_by_name': f"{opportunity.posted_by.first_name} {opportunity.posted_by.last_name}"
        })

    return JsonResponse(jobs_data, safe=False)

# Add to views.py

# Admin Dashboard APIs
from .models import ActivityLog

def admin_stats(request):
    """Get admin dashboard statistics"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    total_users = (Student.objects.count() + Alumni.objects.count() +
                   Faculty.objects.count() + Company.objects.count())
    active_jobs = (Job.objects.filter(status='active').count() +
                   FacultyOpportunity.objects.filter(status='active').count() +
                   CompanyJob.objects.filter(status='active').count())
    pending_reviews = (Job.objects.filter(status='pending').count() +
                       FacultyOpportunity.objects.filter(status='pending').count() +
                       CompanyJob.objects.filter(status='pending').count())
    total_companies = Company.objects.count()

    # Calculate new signups (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    new_signups = (Student.objects.filter(created_at__gte=week_ago).count() +
                   Alumni.objects.filter(created_at__gte=week_ago).count() +
                   Faculty.objects.filter(created_at__gte=week_ago).count() +
                   Company.objects.filter(created_at__gte=week_ago).count())

    total_applications = (Application.objects.count() +
                          FacultyApplication.objects.count() +
                          CompanyApplication.objects.count())

    return JsonResponse({
        'total_users': total_users,
        'active_jobs': active_jobs,
        'pending_reviews': pending_reviews,
        'total_companies': total_companies,
        'new_signups': new_signups,
        'total_applications': total_applications
    })


def pending_approvals(request):
    """Get all pending approvals for admin dashboard"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    pending_data = []

    # Alumni jobs pending approval
    alumni_jobs = Job.objects.filter(status='pending')
    for job in alumni_jobs:
        pending_data.append({
            'id': job.id,
            'type': 'job',
            'title': job.title,
            'submitted_by': f"{job.posted_by.first_name} {job.posted_by.last_name}",
            'submitted_by_type': 'Alumni',
            'location': job.location,
            'job_type': job.job_type,
            'description': job.description,
            'submitted_at': job.created_at.strftime('%B %d, %Y'),
            'deadline': job.deadline.strftime('%B %d, %Y')
        })

    # Faculty opportunities pending approval
    faculty_opportunities = FacultyOpportunity.objects.filter(status='pending')
    for opportunity in faculty_opportunities:
        pending_data.append({
            'id': opportunity.id,
            'type': 'faculty_opportunity',
            'title': opportunity.title,
            'submitted_by': f"{opportunity.posted_by.first_name} {opportunity.posted_by.last_name}",
            'submitted_by_type': 'Faculty',
            'location': "University Campus",
            'opportunity_type': opportunity.opportunity_type,
            'description': opportunity.description,
            'submitted_at': opportunity.created_at.strftime('%B %d, %Y'),
            'deadline': opportunity.deadline.strftime('%B %d, %Y')
        })

    # Company jobs pending approval
    company_jobs = CompanyJob.objects.filter(status='pending')
    for job in company_jobs:
        pending_data.append({
            'id': job.id,
            'type': 'company_job',
            'title': job.title,
            'submitted_by': job.company.company_name,
            'submitted_by_type': 'Company',
            'location': job.location,
            'job_type': job.job_type,
            'description': job.description,
            'submitted_at': job.created_at.strftime('%B %d, %Y'),
            'deadline': job.deadline.strftime('%B %d, %Y')
        })

    return JsonResponse(pending_data, safe=False)


def company_verification(request):
    """Get companies pending verification"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    companies = Company.objects.filter(is_verified=False)
    companies_data = []

    for company in companies:
        companies_data.append({
            'id': company.id,
            'company_name': company.company_name,
            'email': company.email,
            'company_type': company.company_type,
            'phone_number': company.phone_number,
            'created_at': company.created_at.strftime('%B %d, %Y')
        })

    return JsonResponse(companies_data, safe=False)


def admin_users(request):
    """Get all users for admin management"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    users_data = []

    # Students
    students = Student.objects.all()
    for student in students:
        users_data.append({
            'id': student.id,
            'user_type': 'student',
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'student_id': student.student_id,
            'graduation_year': student.graduation_year,
            'is_verified': student.is_verified,
            'created_at': student.created_at.strftime('%B %d, %Y')
        })

    # Alumni
    alumni = Alumni.objects.all()
    for alum in alumni:
        users_data.append({
            'id': alum.id,
            'user_type': 'alumni',
            'first_name': alum.first_name,
            'last_name': alum.last_name,
            'email': alum.email,
            'student_id': alum.student_id,
            'graduation_year': alum.graduation_year,
            'is_verified': alum.is_verified,
            'created_at': alum.created_at.strftime('%B %d, %Y')
        })

    # Faculty
    faculty = Faculty.objects.all()
    for faculty_member in faculty:
        users_data.append({
            'id': faculty_member.id,
            'user_type': 'faculty',
            'first_name': faculty_member.first_name,
            'last_name': faculty_member.last_name,
            'email': faculty_member.email,
            'position': faculty_member.position,
            'is_verified': faculty_member.is_verified,
            'created_at': faculty_member.created_at.strftime('%B %d, %Y')
        })

    return JsonResponse(users_data, safe=False)


from django.views.decorators.http import require_POST

@require_POST
def approve_item(request, item_type, item_id):
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    try:
        if item_type == 'job':
            item = Job.objects.get(id=item_id)
        elif item_type == 'faculty_opportunity':
            item = FacultyOpportunity.objects.get(id=item_id)
        elif item_type == 'company_job':
            item = CompanyJob.objects.get(id=item_id)
        else:
            return JsonResponse({'error': 'Invalid item type'}, status=400)

        if getattr(item, 'status') != 'pending':
            return JsonResponse({'error': 'Only pending items can be approved'}, status=400)

        item.status = 'active'
        item.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def reject_item(request, item_type, item_id):
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    try:
        if item_type == 'job':
            item = Job.objects.get(id=item_id)
        elif item_type == 'faculty_opportunity':
            item = FacultyOpportunity.objects.get(id=item_id)
        elif item_type == 'company_job':
            item = CompanyJob.objects.get(id=item_id)
        else:
            return JsonResponse({'error': 'Invalid item type'}, status=400)

        if getattr(item, 'status') != 'pending':
            return JsonResponse({'error': 'Only pending items can be rejected'}, status=400)

        item.status = 'rejected'
        item.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def verify_company(request, company_id):
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    try:
        company = Company.objects.get(id=company_id)
        company.is_verified = True
        company.save()
        return JsonResponse({'success': True})
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)

@require_POST
def reject_company(request, company_id):
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    try:
        company = Company.objects.get(id=company_id)
        company.delete()  # or set a rejected flag
        return JsonResponse({'success': True})
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)


def add_user(request):
    """Add a new user (admin functionality)"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_type = data['user_type']

            if user_type == 'student':
                user = Student.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    student_id=data.get('student_id', ''),
                    graduation_year=data.get('graduation_year', 2024),
                    is_verified=True
                )
                user.set_password(data['password'])
                user.save()

            elif user_type == 'alumni':
                user = Alumni.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    student_id=data.get('student_id', ''),
                    graduation_year=data.get('graduation_year', 2024),
                    is_verified=True
                )
                user.set_password(data['password'])
                user.save()

            elif user_type == 'faculty':
                user = Faculty.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    position=data.get('position', 'Professor'),
                    is_verified=True
                )
                user.set_password(data['password'])
                user.save()

            else:
                return JsonResponse({'error': 'Invalid user type'}, status=400)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


def delete_user(request, user_type, user_id):
    """Delete a user"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        if user_type == 'student':
            user = Student.objects.get(id=user_id)
        elif user_type == 'alumni':
            user = Alumni.objects.get(id=user_id)
        elif user_type == 'faculty':
            user = Faculty.objects.get(id=user_id)
        else:
            return JsonResponse({'error': 'Invalid user type'}, status=400)

        user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def activity_log(request):
    """Get activity log for admin"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    # This would typically come from an ActivityLog model
    # For now, return mock data
    activities = [
        {
            'action': 'Job Approved',
            'timestamp': '2024-01-20 14:30:25',
            'details': 'Approved "Software Developer" position from TechCorp'
        },
        {
            'action': 'Company Verified',
            'timestamp': '2024-01-20 13:15:42',
            'details': 'Verified company "Innovate Solutions"'
        },
        {
            'action': 'User Added',
            'timestamp': '2024-01-20 12:05:18',
            'details': 'Added new faculty member Dr. Robert Chen'
        }
    ]

    return JsonResponse(activities, safe=False)


def log_activity(request):
    """Log admin activity"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    # This would save to an ActivityLog model
    # For now, just return success
    return JsonResponse({'success': True})


def admin_profile(request):
    """Get admin profile data"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        admin = Administrator.objects.get(id=request.session['admin_id'])
        return JsonResponse({
            'name': f"{admin.first_name} {admin.last_name}",
            'email': admin.email,
            'phone_number': admin.phone_number,
            'last_login': 'Just now'  # You might want to add last_login field to your model
        })
    except Administrator.DoesNotExist:
        return JsonResponse({'error': 'Admin not found'}, status=404)


def system_health(request):
    """Get system health status"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    # Mock data - you can implement actual health checks
    return JsonResponse({
        'server_status': 'operational',
        'database_status': 'healthy',
        'storage_used': 72,
        'last_checked': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    })


def recent_activity(request):
    """Get recent signup activity"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    # Get recent signups (last 5)
    recent_activities = []

    # Recent students
    recent_students = Student.objects.order_by('-created_at')[:2]
    for student in recent_students:
        recent_activities.append({
            'name': f"{student.first_name} {student.last_name}",
            'type': 'student',
            'time': student.created_at.strftime('%H:%M'),
            'date': student.created_at.strftime('%b %d, %Y')
        })

    # Recent alumni
    recent_alumni = Alumni.objects.order_by('-created_at')[:1]
    for alumni in recent_alumni:
        recent_activities.append({
            'name': f"{alumni.first_name} {alumni.last_name}",
            'type': 'alumni',
            'time': alumni.created_at.strftime('%H:%M'),
            'date': alumni.created_at.strftime('%b %d, %Y')
        })

    # Recent faculty
    recent_faculty = Faculty.objects.order_by('-created_at')[:1]
    for faculty in recent_faculty:
        recent_activities.append({
            'name': f"{faculty.first_name} {faculty.last_name}",
            'type': 'faculty',
            'time': faculty.created_at.strftime('%H:%M'),
            'date': faculty.created_at.strftime('%b %d, %Y')
        })

    # Recent companies
    recent_companies = Company.objects.order_by('-created_at')[:1]
    for company in recent_companies:
        recent_activities.append({
            'name': company.company_name,
            'type': 'company',
            'time': company.created_at.strftime('%H:%M'),
            'date': company.created_at.strftime('%b %d, %Y')
        })

    return JsonResponse(recent_activities, safe=False)

def admin_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('adminlog')
    return render(request, 'myapp/admindashboard.html')

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student, StudentEducation, StudentExperience, StudentProject, StudentSkill, ProjectTechnology
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect


def student_profile(request):
    """Student profile page"""
    if 'student_id' not in request.session:
        return redirect('stdlog')

    return render(request, 'myapp/studentprofile.html')


def get_student_profile(request):
    """API endpoint to get student profile data"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])

        # Get related data properly
        education = student.education.all().values('degree', 'institution', 'period')
        experience = student.experience.all().values('job_title', 'company', 'period', 'description')
        projects_data = []

        for project in student.projects.all():
            technologies = list(project.technologies.all().values_list('name', flat=True))
            projects_data.append({
                'title': project.title,
                'description': project.description,
                'technologies': technologies
            })

        skills = list(student.skills.all().values_list('name', flat=True))

        return JsonResponse({
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'student_id': student.student_id,
            'graduation_year': student.graduation_year,
            'phone_number': student.phone_number or '',
            'bio': student.bio or '',
            'profile_picture_url': student.profile_picture.url if student.profile_picture else '',
            'education': list(education),
            'experience': list(experience),
            'projects': projects_data,
            'skills': skills,
        })
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_student_profile(request):
    """API endpoint to update student profile"""
    try:
        data = json.loads(request.body)
        student = Student.objects.get(id=request.session['student_id'])

        # Update basic fields
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.email = data.get('email', student.email)
        student.phone_number = data.get('phone_number', student.phone_number)
        student.student_id = data.get('student_id', student.student_id)
        student.bio = data.get('bio', student.bio)

        # Add graduation_year if needed
        if 'graduation_year' in data:
            student.graduation_year = data['graduation_year']

        student.save()

        return JsonResponse({'success': True, 'message': 'Profile updated successfully'})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_student_education(request):
    """Update student education"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])
        data = json.loads(request.body)

        # Clear existing education
        student.education.all().delete()

        # Add new education entries
        for edu_data in data.get('education', []):
            StudentEducation.objects.create(
                student=student,
                degree=edu_data.get('degree', ''),
                institution=edu_data.get('institution', ''),
                period=edu_data.get('period', '')
            )

        return JsonResponse({'success': True, 'message': 'Education updated successfully'})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def update_student_experience(request):
    """Update student experience"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])
        data = json.loads(request.body)

        # Clear existing experience
        student.experience.all().delete()

        # Add new experience entries
        for exp_data in data.get('experience', []):
            StudentExperience.objects.create(
                student=student,
                job_title=exp_data.get('job_title', ''),
                company=exp_data.get('company', ''),
                period=exp_data.get('period', ''),
                description=exp_data.get('description', '')
            )

        return JsonResponse({'success': True, 'message': 'Experience updated successfully'})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def update_student_projects(request):
    """Update student projects"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])
        data = json.loads(request.body)

        # Clear existing projects and technologies
        student.projects.all().delete()

        # Add new projects with technologies
        for project_data in data.get('projects', []):
            project = StudentProject.objects.create(
                student=student,
                title=project_data.get('title', ''),
                description=project_data.get('description', '')
            )

            # Add technologies for this project
            for tech_name in project_data.get('technologies', []):
                ProjectTechnology.objects.create(
                    project=project,
                    name=tech_name
                )

        return JsonResponse({'success': True, 'message': 'Projects updated successfully'})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def update_student_skills(request):
    """Update student skills"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])
        data = json.loads(request.body)

        # Clear existing skills
        student.skills.all().delete()

        # Add new skills
        for skill_name in data.get('skills', []):
            StudentSkill.objects.create(
                student=student,
                name=skill_name
            )

        return JsonResponse({'success': True, 'message': 'Skills updated successfully'})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import os
from django.conf import settings
from django.core.files.storage import default_storage

@csrf_exempt
@require_http_methods(["POST"])
@require_POST
def upload_profile_picture(request):
    try:
        if 'profile_picture' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No file provided'})

        profile_picture = request.FILES['profile_picture']

        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if profile_picture.content_type not in allowed_types:
            return JsonResponse({'success': False, 'error': 'Invalid file type. Please upload JPEG, PNG, or GIF.'})

        # Validate file size (5MB max)
        if profile_picture.size > 5 * 1024 * 1024:
            return JsonResponse({'success': False, 'error': 'File size must be less than 5MB'})

        # Save the file
        file_path = f'profile_pictures/{request.user.username}_{profile_picture.name}'
        saved_path = default_storage.save(file_path, profile_picture)

        # Get the URL for the saved file
        file_url = default_storage.url(saved_path)

        # Update user's profile picture in database (if you have a UserProfile model)
        # Example:
        # profile = request.user.userprofile
        # profile.profile_picture = saved_path
        # profile.save()

        return JsonResponse({
            'success': True,
            'profile_picture_url': file_url,
            'message': 'Profile picture updated successfully'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# views.py - Add this function
@require_POST
def upload_cover_photo(request):
    try:
        if 'cover_photo' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No file provided'})

        cover_photo = request.FILES['cover_photo']

        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if cover_photo.content_type not in allowed_types:
            return JsonResponse({'success': False, 'error': 'Invalid file type. Please upload JPEG, PNG, or GIF.'})

        # Validate file size (5MB max)
        if cover_photo.size > 5 * 1024 * 1024:
            return JsonResponse({'success': False, 'error': 'File size must be less than 5MB'})

        # Save the file
        file_path = f'cover_photos/{request.user.username}_cover_{cover_photo.name}'
        saved_path = default_storage.save(file_path, cover_photo)

        # Get the URL for the saved file
        file_url = default_storage.url(saved_path)

        # Update user's cover photo in database (if you have a UserProfile model)
        # Example:
        # profile = request.user.userprofile
        # profile.cover_photo = saved_path
        # profile.save()

        return JsonResponse({
            'success': True,
            'cover_photo_url': file_url,
            'message': 'Cover photo updated successfully'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def upload_resume(request):
    """Upload resume"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])

        if 'resume' in request.FILES:
            student.resume = request.FILES['resume']
            student.save()

            return JsonResponse({
                'success': True,
                'message': 'Resume updated successfully',
                'resume_url': student.resume.url,
                'resume_name': student.resume.name.split('/')[-1]
            })
        else:
            return JsonResponse({'error': 'No file provided'}, status=400)

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



from django.http import FileResponse, Http404
import os


def download_resume(request):
    """Download student resume"""
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        student = Student.objects.get(id=request.session['student_id'])

        if not student.resume:
            return JsonResponse({'error': 'No resume uploaded'}, status=404)

        # Serve the file for download
        response = FileResponse(student.resume.open(), as_attachment=True, filename=student.resume.name.split('/')[-1])
        return response

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Alumni Profile Views
from .models import Alumni, AlumniEducation, AlumniExperience, AlumniProject, AlumniSkill, AlumniProjectTechnology

def alumni_profile(request):
    """Alumni profile page"""
    if 'alumni_id' not in request.session:
        return redirect('almlog')
    return render(request, 'myapp/alumniprofile.html')

# Alumni Profile APIs
@csrf_exempt
@require_http_methods(["GET"])
def get_alumni_profile_api(request):
    """API endpoint to get complete alumni profile data"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        alumni = Alumni.objects.get(id=request.session['alumni_id'])

        # Get education data
        education = []
        for edu in alumni.education.all():
            education.append({
                'degree': edu.degree,
                'institution': edu.institution,
                'period': edu.period
            })

        # Get experience data
        experience = []
        for exp in alumni.experience.all():
            experience.append({
                'job_title': exp.job_title,
                'company': exp.company,
                'period': exp.period,
                'description': exp.description
            })

        # Get projects data
        projects = []
        for project in alumni.projects.all():
            technologies = [tech.name for tech in project.technologies.all()]
            projects.append({
                'title': project.title,
                'description': project.description,
                'technologies': technologies
            })

        # Get skills
        skills = [skill.name for skill in alumni.skills.all()]

        return JsonResponse({
            'success': True,
            'first_name': alumni.first_name,
            'last_name': alumni.last_name,
            'email': alumni.email,
            'phone_number': alumni.phone_number or '',
            'student_id': alumni.student_id or '',
            'graduation_year': alumni.graduation_year or '',
            'bio': alumni.bio or '',
            'current_position': alumni.current_position or '',
            'company': alumni.company or '',
            'linkedin_url': alumni.linkedin_url or '',
            'profile_picture_url': alumni.profile_picture.url if alumni.profile_picture else '',
            'education': education,
            'experience': experience,
            'projects': projects,
            'skills': skills,
        })
    except Alumni.DoesNotExist:
        return JsonResponse({'error': 'Alumni not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def update_alumni_profile_api(request):
    """API endpoint to update alumni profile basic info"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        alumni = Alumni.objects.get(id=request.session['alumni_id'])

        # Update basic profile fields
        if 'first_name' in data:
            alumni.first_name = data['first_name']
        if 'last_name' in data:
            alumni.last_name = data['last_name']
        if 'email' in data:
            alumni.email = data['email']
        if 'phone_number' in data:
            alumni.phone_number = data['phone_number']
        if 'student_id' in data:
            alumni.student_id = data['student_id']
        if 'bio' in data:
            alumni.bio = data['bio']
        if 'current_position' in data:
            alumni.current_position = data['current_position']
        if 'company' in data:
            alumni.company = data['company']
        if 'linkedin_url' in data:
            alumni.linkedin_url = data['linkedin_url']

        alumni.save()

        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully'
        })

    except Alumni.DoesNotExist:
        return JsonResponse({'error': 'Alumni not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_alumni_education_api(request):
    """API endpoint to update alumni education"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        alumni = Alumni.objects.get(id=request.session['alumni_id'])

        # Clear existing education
        alumni.education.all().delete()

        # Add new education entries
        education_data = data.get('education', [])
        for edu in education_data:
            AlumniEducation.objects.create(
                alumni=alumni,
                degree=edu.get('degree', ''),
                institution=edu.get('institution', ''),
                period=edu.get('period', '')
            )

        return JsonResponse({
            'success': True,
            'message': 'Education updated successfully'
        })

    except Alumni.DoesNotExist:
        return JsonResponse({'error': 'Alumni not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_alumni_experience_api(request):
    """API endpoint to update alumni experience"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        alumni = Alumni.objects.get(id=request.session['alumni_id'])

        # Clear existing experience
        alumni.experience.all().delete()

        # Add new experience entries
        experience_data = data.get('experience', [])
        for exp in experience_data:
            AlumniExperience.objects.create(
                alumni=alumni,
                job_title=exp.get('job_title', ''),
                company=exp.get('company', ''),
                period=exp.get('period', ''),
                description=exp.get('description', '')
            )

        return JsonResponse({
            'success': True,
            'message': 'Experience updated successfully'
        })

    except Alumni.DoesNotExist:
        return JsonResponse({'error': 'Alumni not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_alumni_projects_api(request):
    """API endpoint to update alumni projects"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        alumni = Alumni.objects.get(id=request.session['alumni_id'])

        # Clear existing projects
        alumni.projects.all().delete()

        # Add new projects with technologies
        projects_data = data.get('projects', [])
        for proj in projects_data:
            project = AlumniProject.objects.create(
                alumni=alumni,
                title=proj.get('title', ''),
                description=proj.get('description', '')
            )

            # Add technologies
            technologies = proj.get('technologies', [])
            for tech in technologies:
                AlumniProjectTechnology.objects.create(
                    project=project,
                    name=tech
                )

        return JsonResponse({
            'success': True,
            'message': 'Projects updated successfully'
        })

    except Alumni.DoesNotExist:
        return JsonResponse({'error': 'Alumni not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_alumni_skills_api(request):
    """API endpoint to update alumni skills"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        alumni = Alumni.objects.get(id=request.session['alumni_id'])

        # Clear existing skills
        alumni.skills.all().delete()

        # Add new skills
        skills_data = data.get('skills', [])
        for skill in skills_data:
            AlumniSkill.objects.create(
                alumni=alumni,
                name=skill
            )

        return JsonResponse({
            'success': True,
            'message': 'Skills updated successfully'
        })

    except Alumni.DoesNotExist:
        return JsonResponse({'error': 'Alumni not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def upload_alumni_profile_picture_api(request):
    """API endpoint to upload alumni profile picture"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        alumni = Alumni.objects.get(id=request.session['alumni_id'])

        if 'profile_picture' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        profile_picture = request.FILES['profile_picture']

        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if profile_picture.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid file type'}, status=400)

        # Validate file size (5MB max)
        if profile_picture.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'File size must be less than 5MB'}, status=400)

        # Save the file
        alumni.profile_picture = profile_picture
        alumni.save()

        return JsonResponse({
            'success': True,
            'message': 'Profile picture updated successfully',
            'profile_picture_url': alumni.profile_picture.url
        })

    except Alumni.DoesNotExist:
        return JsonResponse({'error': 'Alumni not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Add this to your views.py in the alumni section
@require_http_methods(["GET"])
def get_alumni_dashboard_data(request):
    """API to get alumni data for dashboard"""
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        alumni = Alumni.objects.get(id=request.session['alumni_id'])

        # Count alumni's jobs by status
        total_jobs = Job.objects.filter(posted_by=alumni).count()
        active_jobs = Job.objects.filter(posted_by=alumni, status='active').count()
        draft_jobs = Job.objects.filter(posted_by=alumni, status='draft').count()
        closed_jobs = Job.objects.filter(posted_by=alumni, status='closed').count()

        # Count total applicants across all jobs
        total_applicants = Application.objects.filter(job__posted_by=alumni).count()

        # Count hired (you might want to track this differently)
        total_hired = Application.objects.filter(
            job__posted_by=alumni,
            status='accepted'
        ).count()

        return JsonResponse({
            'success': True,
            'alumni': {
                'id': alumni.id,
                'first_name': alumni.first_name,
                'last_name': alumni.last_name,
                'full_name': f"{alumni.first_name} {alumni.last_name}",
                'email': alumni.email,
                'student_id': alumni.student_id,
                'graduation_year': alumni.graduation_year,
                'current_position': alumni.current_position or '',
                'company': alumni.company or '',
            },
            'stats': {
                'total_jobs': total_jobs,
                'active_jobs': active_jobs,
                'draft_jobs': draft_jobs,
                'closed_jobs': closed_jobs,
                'total_applicants': total_applicants,
                'total_hired': total_hired
            }
        })
    except Alumni.DoesNotExist:
        return JsonResponse({'error': 'Alumni not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from .models import Faculty, FacultyEducation, FacultyExperience, FacultyProject, FacultyResearchInterest, FacultyCourse,ProjectResearchArea

def faculty_profile(request):
    """Faculty profile page"""
    if 'faculty_id' not in request.session:
        return redirect('fcltlog')
    return render(request, 'myapp/facultyprofile.html')

def get_faculty_profile(request):
    """Get faculty profile data for dashboard"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        faculty = Faculty.objects.get(id=request.session['faculty_id'])
        return JsonResponse({
            'success': True,
            'faculty': {
                'id': faculty.id,
                'first_name': faculty.first_name,
                'last_name': faculty.last_name,
                'full_name': f"{faculty.first_name} {faculty.last_name}",
                'email': faculty.email,
                'position': faculty.position,
                'office': faculty.office or '7th floor, CSE dept. university campus',
                'contact': faculty.phone_number or '+88-0167593251',
                'profile_picture_url': faculty.profile_picture.url if faculty.profile_picture else '',
            }
        })
    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_faculty_opportunities_with_applicants(request):
    """Get faculty opportunities with applicant counts"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        faculty_id = request.session['faculty_id']
        opportunities = FacultyOpportunity.objects.filter(posted_by_id=faculty_id).order_by('-created_at')

        opportunities_data = []
        for opportunity in opportunities:
            # Count applicants for this opportunity
            applicants_count = FacultyApplication.objects.filter(opportunity=opportunity).count()

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
                'applicants_count': applicants_count,
            })

        return JsonResponse(opportunities_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_recent_applicants_faculty(request):
    """Get recent applicants for faculty dashboard"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        faculty_id = request.session['faculty_id']

        # Get recent applications for this faculty's opportunities
        recent_applications = FacultyApplication.objects.filter(
            opportunity__posted_by_id=faculty_id
        ).select_related('student', 'opportunity').order_by('-applied_at')[:5]

        applicants_data = []
        for application in recent_applications:
            applicants_data.append({
                'name': f"{application.student.first_name} {application.student.last_name}",
                'position': application.opportunity.title,
                'time': application.applied_at.strftime('%H:%M'),
                'date': application.applied_at.strftime('%b %d, %Y'),
                'student_id': application.student.student_id,
                'email': application.student.email
            })

        return JsonResponse(applicants_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Faculty Profile APIs
@csrf_exempt
@require_http_methods(["GET"])
def get_faculty_profile_api(request):
    """API endpoint to get complete faculty profile data"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        faculty = Faculty.objects.get(id=request.session['faculty_id'])

        # Get education data
        education = []
        for edu in faculty.education.all():
            education.append({
                'degree': edu.degree,
                'institution': edu.institution,
                'period': edu.period
            })

        # Get experience data
        experience = []
        for exp in faculty.experience.all():
            experience.append({
                'job_title': exp.job_title,
                'company': exp.company,
                'period': exp.period,
                'description': exp.description
            })

        # Get projects data
        projects = []
        for project in faculty.projects.all():
            research_areas = [area.name for area in project.research_areas.all()]
            projects.append({
                'title': project.title,
                'description': project.description,
                'research_areas': research_areas
            })

        # Get research interests
        research_interests = [interest.name for interest in faculty.research_interests.all()]

        # Get courses
        courses = [course.name for course in faculty.courses.all()]

        return JsonResponse({
            'success': True,
            'first_name': faculty.first_name,
            'last_name': faculty.last_name,
            'email': faculty.email,
            'phone_number': faculty.phone_number or '',
            'position': faculty.position,
            'office': faculty.office or '',
            'bio': faculty.bio or '',
            'profile_picture_url': faculty.profile_picture.url if faculty.profile_picture else '',
            'education': education,
            'experience': experience,
            'projects': projects,
            'research_interests': research_interests,
            'courses': courses,
        })
    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def update_faculty_profile_api(request):
    """API endpoint to update faculty profile basic info"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        faculty = Faculty.objects.get(id=request.session['faculty_id'])

        # Update basic profile fields
        if 'first_name' in data:
            faculty.first_name = data['first_name']
        if 'last_name' in data:
            faculty.last_name = data['last_name']
        if 'email' in data:
            faculty.email = data['email']
        if 'phone_number' in data:
            faculty.phone_number = data['phone_number']
        if 'position' in data:
            faculty.position = data['position']
        if 'office' in data:
            faculty.office = data['office']
        if 'bio' in data:
            faculty.bio = data['bio']

        faculty.save()

        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully'
        })

    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_faculty_education_api(request):
    """API endpoint to update faculty education"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        faculty = Faculty.objects.get(id=request.session['faculty_id'])

        # Clear existing education
        faculty.education.all().delete()

        # Add new education entries
        education_data = data.get('education', [])
        for edu in education_data:
            FacultyEducation.objects.create(
                faculty=faculty,
                degree=edu.get('degree', ''),
                institution=edu.get('institution', ''),
                period=edu.get('period', '')
            )

        return JsonResponse({
            'success': True,
            'message': 'Education updated successfully'
        })

    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_faculty_experience_api(request):
    """API endpoint to update faculty experience"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        faculty = Faculty.objects.get(id=request.session['faculty_id'])

        # Clear existing experience
        faculty.experience.all().delete()

        # Add new experience entries
        experience_data = data.get('experience', [])
        for exp in experience_data:
            FacultyExperience.objects.create(
                faculty=faculty,
                job_title=exp.get('job_title', ''),
                company=exp.get('company', ''),
                period=exp.get('period', ''),
                description=exp.get('description', '')
            )

        return JsonResponse({
            'success': True,
            'message': 'Experience updated successfully'
        })

    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_faculty_projects_api(request):
    """API endpoint to update faculty projects"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        faculty = Faculty.objects.get(id=request.session['faculty_id'])

        # Clear existing projects
        faculty.projects.all().delete()

        # Add new projects with research areas
        projects_data = data.get('projects', [])
        for proj in projects_data:
            project = FacultyProject.objects.create(
                faculty=faculty,
                title=proj.get('title', ''),
                description=proj.get('description', '')
            )

            # Add research areas
            research_areas = proj.get('research_areas', [])
            for area in research_areas:
                ProjectResearchArea.objects.create(
                    project=project,
                    name=area
                )

        return JsonResponse({
            'success': True,
            'message': 'Projects updated successfully'
        })

    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_faculty_research_interests_api(request):
    """API endpoint to update faculty research interests"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        faculty = Faculty.objects.get(id=request.session['faculty_id'])

        # Clear existing research interests
        faculty.research_interests.all().delete()

        # Add new research interests
        research_interests_data = data.get('research_interests', [])
        for interest in research_interests_data:
            FacultyResearchInterest.objects.create(
                faculty=faculty,
                name=interest
            )

        return JsonResponse({
            'success': True,
            'message': 'Research interests updated successfully'
        })

    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_faculty_courses_api(request):
    """API endpoint to update faculty courses"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        faculty = Faculty.objects.get(id=request.session['faculty_id'])

        # Clear existing courses
        faculty.courses.all().delete()

        # Add new courses
        courses_data = data.get('courses', [])
        for course in courses_data:
            FacultyCourse.objects.create(
                faculty=faculty,
                name=course
            )

        return JsonResponse({
            'success': True,
            'message': 'Courses updated successfully'
        })

    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def upload_faculty_profile_picture_api(request):
    """API endpoint to upload faculty profile picture"""
    if 'faculty_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        faculty = Faculty.objects.get(id=request.session['faculty_id'])

        if 'profile_picture' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        profile_picture = request.FILES['profile_picture']

        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if profile_picture.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid file type'}, status=400)

        # Validate file size (5MB max)
        if profile_picture.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'File size must be less than 5MB'}, status=400)

        # Save the file
        faculty.profile_picture = profile_picture
        faculty.save()

        return JsonResponse({
            'success': True,
            'message': 'Profile picture updated successfully',
            'profile_picture_url': faculty.profile_picture.url
        })

    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



from .models import Company, CompanyProfile
from .forms import CompanyLogoForm,CompanyCoverPhotoForm

# Company Profile Page
def company_profile_page(request):
    """Company profile page"""
    if 'company_id' not in request.session:
        return redirect('comlog')
    return render(request, 'myapp/companyprofile.html')


def get_company_profile(request):
    """Get company profile data - COMPLETE VERSION"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])

        # Get or create company profile
        profile, created = CompanyProfile.objects.get_or_create(company=company)

        return JsonResponse({
            'id': company.id,
            'company_name': company.company_name,
            'email': company.email,
            'phone_number': company.phone_number,
            'company_type': company.company_type,
            'is_verified': company.is_verified,
            'address': company.address if hasattr(company, 'address') else '',

            # PROFILE DATA - This might be missing!
            'profile': {
                'description': profile.description,
                'industry': profile.industry,
                'company_size': profile.company_size,
                'founded_year': profile.founded_year,
                'website': profile.website,
                'logo_url': profile.logo.url if profile.logo else '',
                'cover_photo_url': profile.cover_photo.url if profile.cover_photo else '',
                'linkedin_url': profile.linkedin_url,
                'twitter_url': profile.twitter_url,
                'facebook_url': profile.facebook_url,
                'mission_statement': profile.mission_statement,
                'company_values': profile.company_values,
                'benefits': profile.get_benefits_list(),  # This returns a list
                'city': profile.city,
                'country': profile.country,
            }
        })

    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Company Profile APIs
@csrf_exempt
@require_http_methods(["GET"])
def get_company_profile_api(request):
    """API endpoint to get complete company profile data"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])

        # Get or create company profile
        profile, created = CompanyProfile.objects.get_or_create(company=company)

        # Get company jobs for stats
        active_jobs = CompanyJob.objects.filter(company=company, status='active').count()
        total_jobs = CompanyJob.objects.filter(company=company).count()

        return JsonResponse({
            'success': True,
            'company': {
                'id': company.id,
                'company_name': company.company_name,
                'email': company.email,
                'phone_number': company.phone_number,
                'company_type': company.company_type,
                'is_verified': company.is_verified,
            },
            'profile': {
                'description': profile.description or '',
                'industry': profile.industry or '',
                'company_size': profile.company_size or '',
                'founded_year': profile.founded_year or '',
                'website': profile.website or '',
                'address': profile.address or '',
                'city': profile.city or '',
                'country': profile.country or '',
                'mission_statement': profile.mission_statement or '',
                'company_values': profile.company_values or '',
                'benefits': profile.get_benefits_list(),
                'linkedin_url': profile.linkedin_url or '',
                'twitter_url': profile.twitter_url or '',
                'facebook_url': profile.facebook_url or '',
                'logo_url': profile.logo.url if profile.logo else '',
                'cover_photo_url': profile.cover_photo.url if profile.cover_photo else '',
            },
            'stats': {
                'active_jobs': active_jobs,
                'total_jobs': total_jobs,
            }
        })
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_company_profile_api(request):
    """Update company profile information"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        company = Company.objects.get(id=request.session['company_id'])
        profile = CompanyProfile.objects.get(company=company)

        print(f"📝 Updating profile for: {company.company_name}")
        print(f"📦 Received data: {data}")

        # Update Company model fields
        if 'company_name' in data:
            company.company_name = data['company_name']
        if 'email' in data:
            company.email = data['email']
        if 'phone_number' in data:
            company.phone_number = data['phone_number']
        if 'address' in data:
            # If you have address in Company model, otherwise handle in profile
            company.address = data['address']

        company.save()

        # Update CompanyProfile fields
        update_fields = [
            'description', 'industry', 'company_size', 'founded_year',
            'website', 'linkedin_url', 'twitter_url', 'facebook_url',
            'address', 'city', 'country', 'mission_statement', 'company_values'
        ]

        for field in update_fields:
            if field in data:
                setattr(profile, field, data[field])

        # Handle benefits specifically
        if 'benefits' in data and isinstance(data['benefits'], list):
            profile.benefits = '\n'.join(data['benefits'])

        profile.save()

        print(f"✅ Successfully updated profile for: {company.company_name}")

        return JsonResponse({
            'success': True,
            'message': 'Company profile updated successfully'
        })

    except Exception as e:
        print(f"❌ Error updating profile: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def update_company_basic_info_api(request):
    """API endpoint to update company basic information"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        company = Company.objects.get(id=request.session['company_id'])

        # Update basic company fields
        if 'company_name' in data:
            company.company_name = data['company_name']
        if 'email' in data:
            company.email = data['email']
        if 'phone_number' in data:
            company.phone_number = data['phone_number']
        if 'company_type' in data:
            company.company_type = data['company_type']

        company.save()

        return JsonResponse({
            'success': True,
            'message': 'Company information updated successfully'
        })

    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def upload_company_logo_api(request):
    """API endpoint to upload company logo"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])
        profile = CompanyProfile.objects.get(company=company)

        if 'logo' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        logo = request.FILES['logo']

        # Validate file using form
        form = CompanyLogoForm(files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Logo updated successfully',
                'logo_url': profile.logo.url
            })
        else:
            return JsonResponse({'error': form.errors}, status=400)

    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)
    except CompanyProfile.DoesNotExist:
        return JsonResponse({'error': 'Company profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def upload_company_cover_photo_api(request):
    """API endpoint to upload company cover photo"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])
        profile = CompanyProfile.objects.get(company=company)

        if 'cover_photo' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        cover_photo = request.FILES['cover_photo']

        # Validate file using form
        form = CompanyCoverPhotoForm(files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Cover photo updated successfully',
                'cover_photo_url': profile.cover_photo.url
            })
        else:
            return JsonResponse({'error': form.errors}, status=400)

    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)
    except CompanyProfile.DoesNotExist:
        return JsonResponse({'error': 'Company profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def get_company_dashboard_data(request):
    """API to get company data for dashboard with profile info"""
    if 'company_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        company = Company.objects.get(id=request.session['company_id'])
        profile, created = CompanyProfile.objects.get_or_create(company=company)

        # Count company's jobs by status
        total_jobs = CompanyJob.objects.filter(company=company).count()
        active_jobs = CompanyJob.objects.filter(company=company, status='active').count()
        pending_jobs = CompanyJob.objects.filter(company=company, status='pending').count()
        closed_jobs = CompanyJob.objects.filter(company=company, status='closed').count()
        draft_jobs = CompanyJob.objects.filter(company=company, status='draft').count()

        # Count total applicants across all jobs
        total_applicants = CompanyApplication.objects.filter(job__company=company).count()

        return JsonResponse({
            'success': True,
            'company': {
                'id': company.id,
                'company_name': company.company_name,
                'email': company.email,
                'phone_number': company.phone_number,
                'company_type': company.company_type,
                'is_verified': company.is_verified,
                'logo_url': profile.logo.url if profile.logo else '/static/default-company-logo.png',
                'description': profile.description or 'Welcome to our company profile!',
            },
            'stats': {
                'total_jobs': total_jobs,
                'active_jobs': active_jobs,
                'pending_jobs': pending_jobs,
                'closed_jobs': closed_jobs,
                'draft_jobs': draft_jobs,
                'total_applicants': total_applicants,
            }
        })
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Add to views.py - Admin Profile Section

def admin_profile_page(request):
    """Admin profile page"""
    if 'admin_id' not in request.session:
        return redirect('adminlog')
    return render(request, 'myapp/adminprofile.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def get_admin_profile_api(request):
    """API endpoint to get complete admin profile data for the profile page"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        admin = Administrator.objects.get(id=request.session['admin_id'])

        # Get admin stats for activity overview
        total_jobs_reviewed = Job.objects.filter(status__in=['active', 'rejected']).count()
        total_companies_reviewed = Company.objects.filter(is_verified=True).count()
        total_accounts_managed = (
                Student.objects.count() +
                Alumni.objects.count() +
                Faculty.objects.count() +
                Company.objects.count()
        )

        # Count total issues resolved (you might need to implement this)
        total_issues_resolved = ActivityLog.objects.filter(
            admin=admin,
            action_type__in=['approval', 'rejection']
        ).count() if hasattr(admin, 'activitylog_set') else 42

        # Get recent activities
        recent_activities = []
        if hasattr(admin, 'activitylog_set'):
            activities = admin.activitylog_set.all().order_by('-created_at')[:5]
            for activity in activities:
                recent_activities.append({
                    'title': activity.action,
                    'description': activity.details,
                    'time': activity.created_at.strftime('%H hours ago') if activity.created_at else 'Recently'
                })
        else:
            # Fallback mock data
            recent_activities = [
                {
                    'title': 'Approved Job Posting',
                    'description': 'Lab Assistant at University Campus',
                    'time': '5 hours ago'
                },
                {
                    'title': 'Verified Company Account',
                    'description': 'TechInnovate',
                    'time': '3 hours ago'
                }
            ]

        return JsonResponse({
            'success': True,
            'admin': {
                'first_name': admin.first_name,
                'last_name': admin.last_name,
                'email': admin.email,
                'phone_number': admin.phone_number or '+880 1827-483267',
                'work_hours': admin.work_hours or 'Saturday-Thursday, 8.00 am to 7.00 pm',
                'bio': admin.bio or 'CSE Job Portal Administrator responsible for reviewing job postings, verifying company accounts, and ensuring the platform provides a safe and valuable experience for all users.',
                'profile_picture_url': admin.profile_picture.url if admin.profile_picture else '',
                'cover_photo_url': admin.cover_photo.url if admin.cover_photo else '',
            },
            'stats': {
                'jobs_reviewed': total_jobs_reviewed,
                'companies_reviewed': total_companies_reviewed,
                'accounts_managed': total_accounts_managed,
                'issues_resolved': total_issues_resolved,
            },
            'activities': recent_activities,
            'system_health': {
                'server_status': 100,
                'database_health': 91,
                'storage_usage': 72
            }
        })
    except Administrator.DoesNotExist:
        return JsonResponse({'error': 'Admin not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_admin_profile_api(request):
    """API endpoint to update admin profile basic info"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        admin = Administrator.objects.get(id=request.session['admin_id'])

        # Update basic profile fields
        if 'first_name' in data:
            admin.first_name = data['first_name']
        if 'last_name' in data:
            admin.last_name = data['last_name']
        if 'email' in data:
            admin.email = data['email']
        if 'phone_number' in data:
            admin.phone_number = data['phone_number']
        if 'work_hours' in data:
            admin.work_hours = data['work_hours']
        if 'bio' in data:
            admin.bio = data['bio']

        admin.save()

        # Log the activity
        ActivityLog.objects.create(
            admin=admin,
            action='Updated Profile',
            action_type='user_management',
            details=f'{admin.first_name} updated their profile information',
            ip_address=get_client_ip(request)
        )

        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully'
        })

    except Administrator.DoesNotExist:
        return JsonResponse({'error': 'Admin not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def upload_admin_profile_picture_api(request):
    """API endpoint to upload admin profile picture"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        admin = Administrator.objects.get(id=request.session['admin_id'])

        if 'profile_picture' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        profile_picture = request.FILES['profile_picture']

        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if profile_picture.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid file type'}, status=400)

        # Validate file size (5MB max)
        if profile_picture.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'File size must be less than 5MB'}, status=400)

        # Save the file
        admin.profile_picture = profile_picture
        admin.save()

        # Log the activity
        ActivityLog.objects.create(
            admin=admin,
            action='Updated Profile Picture',
            action_type='user_management',
            details=f'{admin.first_name} updated their profile picture',
            ip_address=get_client_ip(request)
        )

        return JsonResponse({
            'success': True,
            'message': 'Profile picture updated successfully',
            'profile_picture_url': admin.profile_picture.url
        })

    except Administrator.DoesNotExist:
        return JsonResponse({'error': 'Admin not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def upload_admin_cover_photo_api(request):
    """API endpoint to upload admin cover photo"""
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        admin = Administrator.objects.get(id=request.session['admin_id'])

        if 'cover_photo' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        cover_photo = request.FILES['cover_photo']

        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if cover_photo.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid file type'}, status=400)

        # Validate file size (5MB max)
        if cover_photo.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'File size must be less than 5MB'}, status=400)

        # Save the file
        admin.cover_photo = cover_photo
        admin.save()

        # Log the activity
        ActivityLog.objects.create(
            admin=admin,
            action='Updated Cover Photo',
            action_type='user_management',
            details=f'{admin.first_name} updated their cover photo',
            ip_address=get_client_ip(request)
        )

        return JsonResponse({
            'success': True,
            'message': 'Cover photo updated successfully',
            'cover_photo_url': admin.cover_photo.url
        })

    except Administrator.DoesNotExist:
        return JsonResponse({'error': 'Admin not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Helper function to get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def post_job_page(request):
    """Dedicated page for posting new jobs"""
    if 'alumni_id' not in request.session:
        return redirect('almlog')
    return render(request, 'myapp/post_job.html')

def post_job(request):
    if 'alumni_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            alumni = Alumni.objects.get(id=request.session['alumni_id'])

            job = Job.objects.create(
                title=data['title'],
                company=data['company'],
                location=data.get('location', 'Dhaka, Bangladesh'),  # Added location
                deadline=data['deadline'],
                job_type=data['job_type'],
                description=data['description'],
                salary=data.get('salary', ''),
                requirements='\n'.join(data.get('requirements', [])),
                posted_by=alumni,
                status=data.get('status', 'pending')  # Now accepts status parameter
            )

            return JsonResponse({'success': True, 'job_id': job.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)

def post_opportunity_page(request):
    """Dedicated page for posting new opportunities"""
    if 'faculty_id' not in request.session:
        return redirect('fcltlog')
    return render(request, 'myapp/post_opportunity.html')

def post_company_job_page(request):
    """Dedicated page for posting new company jobs"""
    if 'company_id' not in request.session:
        return redirect('comlog')
    return render(request, 'myapp/post_company_job.html')