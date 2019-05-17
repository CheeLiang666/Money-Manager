from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
import pyrebase
import json

config = {
    'apiKey': "...",
    'authDomain': "...",
    'databaseURL': "...",
    'projectId': "...",
    'storageBucket': "...",
    'messagingSenderId': "...",
    'appId': "..."
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

# Create your views here.
@csrf_protect
def index(request):
    return render(request, 'mySite/account.html')

@csrf_protect
def signUp(request):
    parsed_data = json.loads(request.body.decode("utf-8"))
    username = parsed_data.get("username")
    email = parsed_data.get("email")
    passw = parsed_data.get("password")
    resp = {}
    try:
        user = auth.create_user_with_email_and_password(email, passw)
    except Exception as e:
        print(f"Firebase Authentication sign up exception: {e}")
        resp = {"status": 0, "message": "Email already in use, please sign up with different account."}
    else:
        uid = user["localId"]
        data = {"name": username, "email": email}
        database.child("users").child(uid).child("details").set(data)
        resp = {"status": 1, "message": f"{username}, you've successfully registered an account. Let's rock!!!"}
    return JsonResponse({"response": resp})