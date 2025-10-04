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

        # ✅ Check the password
        if check_password(password, student.password):
            # store session info
            request.session["student_id"] = student.id
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # replace with your dashboard/homepage
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("stdlog")

    return render(request, "myapp/studentlogin.html")


def alumnilogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            alumni = Alumni.objects.get(email=email)
        except Alumni.DoesNotExist:
            messages.error(request, "Invalid email or password or not registered yet.")
            return redirect("almlog")

        # ✅ Check the password
        if check_password(password, alumni.password):
            # store session info
            request.session["alumni_id"] = alumni.id
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # replace with your dashboard/homepage
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

        # ✅ Check the password
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

        # ✅ Check the password
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

        # ✅ Check the password
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
