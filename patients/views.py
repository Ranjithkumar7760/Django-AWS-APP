from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Patient
from .forms import PatientForm
from django.core.cache import cache

def patient_list(request):
    patients = cache.get('all_patients')
    
    if not patients:
        patients = Patient.objects.all()
        cache.set('all_patients', patients, timeout=300)  # Cache for 5 minutes

    return render(request, 'patients/patient_list.html', {'patients': patients})



# ✅ Dashboard View (Requires Login)
@login_required
def dashboard(request):
    patients = Patient.objects.filter(user=request.user)  # Show only current user's patients
    return render(request, 'patients/dashboard.html', {'patients': patients})

# ✅ User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Use `.get()` to prevent KeyErrors
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")  # Redirect to dashboard after login
        else:
            return render(request, "patients/login.html", {"error": "Invalid username or password"})
    return render(request, "patients/login.html")

# ✅ User Logout View
def user_logout(request):
    logout(request)
    return redirect("/login/")  # Redirect to login page after logout

# ✅ User Signup View
def user_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "patients/signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "patients/signup.html", {"error": "Username already exists"})

        if User.objects.filter(email=email).exists():
            return render(request, "patients/signup.html", {"error": "Email already registered"})

        # Create and save the new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Auto-login after signup
        login(request, user)
        return redirect("/")  # Redirect to dashboard

    return render(request, "patients/signup.html")

# ✅ Create Patient View
@login_required
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user  # Assign the logged-in user
            patient.save()
            return redirect('dashboard')
    else:
        form = PatientForm()
    return render(request, 'patients/create_patient.html', {'form': form})

# ✅ Update Patient View
@login_required
def update_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/update_patient.html', {'form': form})

# ✅ Delete Patient View
@login_required
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('dashboard')
    return render(request, 'patients/delete_patient.html', {'patient': patient})





# ✅ Create Patient View
@login_required
def create_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user  # Assign the logged-in user
            patient.save()
            return redirect('dashboard')  # Redirect to dashboard
    else:
        form = PatientForm()
    
    return render(request, 'patients/create_patient.html', {'form': form})
