from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . forms import PatientForm
from .models import Patient

@login_required
#Homepage view
def home(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()  # Save the data to the database
            return redirect("home")  # Refresh the page to show updated list
    else:
        form = PatientForm()

    patients = Patient.objects.all()  # Fetch all patients
    return render(request, "../templates/index.html", {"form": form, "patients": patients})


@login_required
#Diagnosis view
def diagnosis(request):
    return render(request, "../templates/diagnosis.html")