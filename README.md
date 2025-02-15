# 🏥 HealthGuard

HealthGuard is a Django-based healthcare application that helps users manage patient records and diagnoses for STIs using the recommendation sytem. 
It includes user authentication, a patient registration system, and diagnostic tools to enhance healthcare management.

## 🚀 Features

- 🔐 **User Authentication** (Login & Registration)
- 🏥 **Patient Management** (Name, Age, Gender)
- 📊 **Diagnosis System** 
- 📑 **Secure & Scalable** using Django

---

## 📌 Installation

### 🔹 Prerequisites
Ensure you have the following installed:
- [Python](https://www.python.org/) (3.12+ recommended)
- [Git](https://git-scm.com/)
- [Django](https://www.djangoproject.com/)
- A virtual environment manager (optional but recommended)

### 🔹 Steps to Run Locally
1️⃣ Clone the repository:
sh
git clone https://github.com/Kipkerich/healthguard.git
cd healthguard

2️⃣ Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies:
pip install -r requirements.txt

4️⃣ Apply migrations:
python manage.py makemigrations
python manage.py migrate

5️⃣ Create a superuser (for admin access):
python manage.py createsuperuser

6️⃣ Run the development server:
python manage.py runserver

📌 Usage
Register/Login before accessing the homepage.
Add Patients by filling in their name, age, and gender.
Diagnosis Feature.

📌 Contributing
Want to improve HealthGuard? 🚀

Fork this repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m "Added new feature").
Push to your fork (git push origin feature-branch).
Submit a Pull Request for review.

📌 License
This project is licensed under the MIT License.

📌 Contact
💬 Have questions or suggestions? Reach out!
📧 Email: jaykipkerich@gmail.com
