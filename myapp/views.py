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
            return redirect("dashboard")  # replace with your dashboard/homepage
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
    # Fetch all jobs (or apply filters as needed)
    jobs = Job.objects.all()

    # Pass jobs to the template
    context = {
        'jobs': jobs,
    }
    return render(request, 'myapp/browseoppurtunity.html', context)

def search_jobs(request):
    query = request.GET.get('q', '')
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')
    posted = request.GET.get('posted', '')

    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(title__icontains=query) | jobs.filter(company__icontains=query)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if posted :
        jobs = jobs.filter(posted__icontains=posted)


    jobs_data = [
        {
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'posted': job.posted,
            'deadline': job.deadline.strftime('%B %d, %Y'),
            'is_new': job.is_new,
        }
        for job in jobs
    ]

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
