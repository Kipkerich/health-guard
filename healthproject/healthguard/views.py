from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from . forms import PatientForm
from .models import Patient
import speech_recognition as sr
import pyttsx3
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
def diagnosis(request):
    if request.method == "GET":
        query = request.GET.get('q', '')  # Get search query from request
        if query:
            patients = Patient.objects.filter(name__icontains=query)  # Search by name
        else:
            patients = Patient.objects.all()  # Fetch all patients if no search query

        return render(request, "../templates/diagnosis.html", {"patients": patients, "query": query})
    else:
        return render(request, "../templates/diagnosis.html")
@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        selected_symptoms = request.POST.getlist("symptoms")  # Get selected symptoms
        patient.symptoms = ", ".join(selected_symptoms)  # Store as comma-separated values
        patient.save()
        print(patient)
        return redirect("patient_detail", patient_id=patient.id)  # Refresh the page

    return render(request, "../templates/patient_details.html", {"patient": patient})
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient

STI_SYMPTOMS = [
    "painful_urination", "abnormal_discharge", "pain_during_sex", "abdominal_pain",
    "Abnormal_Bleeding_Women", "Sore_Throat", "Swelling_Testicles", 
    "rash_palms_soles", "flu_like_symptoms", "genital_warts"
]

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, "patient_details.html", {"patient": patient, "sti_symptoms": STI_SYMPTOMS})

@login_required
def update_patient_symptoms(request, patient_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_symptoms = data.get("symptoms", [])
            patient = get_object_or_404(Patient, id=patient_id)
            patient.symptoms = ", ".join(selected_symptoms)
            patient.save()
            return JsonResponse({"success": True, "updated_symptoms": patient.symptoms})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I will ask if you have certain symptoms. Please answer yes or no.")
        symptoms = []
        
        for symptom in STI_SYMPTOMS:
            speak(f"Do you have {symptom.replace('_', ' ')}?")
            print(f"Do you have {symptom.replace('_', ' ')}? (yes/no)")
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                
                if text == "yes":
                    symptoms.append(symptom)
            except sr.UnknownValueError:
                speak("Sorry, I did not understand. Please repeat.")
            except sr.RequestError:
                speak("Could not request results, please check your internet connection.")
    return symptoms

def predict_sti(symptoms):
    url = "http://127.0.0.1:5000/predict_sti"
    data = {"symptoms": symptoms, "user": "voice_user"}
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        prediction = response.json().get("predicted_sti", "No prediction available")
        return prediction
    else:
        return "Error fetching prediction."

@csrf_exempt
def voice_sti_prediction(request):
    if request.method == "POST":
        symptoms = recognize_speech()
        if symptoms:
            speak("Predicting STI based on your symptoms.")
            result = predict_sti(symptoms)
            speak(f"Based on your symptoms, the predicted STI is {result}")
            return JsonResponse({"predicted_sti": result})
        else:
            return JsonResponse({"error": "No symptoms provided."}, status=400)
    return render(request, "voice_interface.html")
