from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, ReportUploadForm
from .models import Student, Report
from django.contrib.auth.models import User
from django.http import HttpResponse

# Student registration view
def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)

            # Create and link student
            student = form.save(commit=False)
            student.user = user
            student.save()

            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboard
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student, Report
from .forms import ReportUploadForm  # <-- import your form

@login_required
def dashboard(request):
    if request.user.is_superuser:
        # Prefetch reports to reduce queries
        students = Student.objects.all().prefetch_related('report_set')
        programs = {}
        for student in students:
            programs.setdefault(student.program, []).append(student)
        return render(request, 'student_dashboard.html', {'programs': programs})
    else:
        student = Student.objects.get(user=request.user)
        reports = Report.objects.filter(student=student)
        form = ReportUploadForm()  # <-- create a new form instance
        return render(request, 'student_dashboard.html', {
            'student': student,
            'reports': reports,
            'form': form,  # <-- pass form to template
        })



# Upload report
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ReportUploadForm

@login_required
def upload_report(request):
    if request.method == 'POST':
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.student = request.user.student
            report.save()
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Report submitted successfully!'})
            else:
                # Render a template showing the success message and OK button
                return render(request, 'upload_success.html', {'message': 'Report submitted successfully!'})
        else:
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return redirect('dashboard')
    else:
        return redirect('dashboard')




@login_required
def student_info_view(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return HttpResponse("Student record not found.", status=404)

    return render(request, 'student_info.html', {
        'student': student,
        
    })
# myapp/views.py

from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CompanyLoginForm
from django.contrib import messages
from datetime import datetime

def company_login(request):
    if request.method == 'POST':
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            user = authenticate(username=company_name, password=company_name)
            if user:
                login(request, user)
                current_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
                messages.success(request, f"Login successful. {company_name} - {current_time}")
                return redirect('company_login')  # Show message before redirecting elsewhere
            else:
                messages.error(request, "Invalid company name.")
    else:
        form = CompanyLoginForm()

    return render(request, 'company_login.html', {'form': form})



from django.http import JsonResponse
from .models import Student, Evaluation
from .forms import EvaluationForm

def submit_evaluation(request):
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            selected_company = form.cleaned_data['company']  # From the EvaluationForm

            if Evaluation.objects.filter(student=student).exists():
                return JsonResponse({
                    'success': False,
                    'message': f"{student.full_name} has already been evaluated."
                }, status=400)

            if str(student.company_placement) != selected_company:
                return JsonResponse({
                    'success': False,
                    'message': f"{student.full_name} is not assigned to {selected_company}."
                }, status=400)

            form.save()
            return JsonResponse({'success': True, 'message': 'Evaluation submitted successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    form = EvaluationForm()
    return render(request, 'submit_evaluation.html', {'form': form})



def get_students_by_company(request):
    company = request.GET.get('company', '')
    students = Student.objects.filter(company_placement__icontains=company)
    student_data = [{'id': s.id, 'full_name': s.full_name} for s in students]
    return JsonResponse({'students': student_data})


