from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GymUser  # Import your model
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")  # Redirect to the home page or dashboard after login
        else:
            return render(request, "signin.html", {"error": "Invalid username or password"})
    return render(request, "signin.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = make_password(request.POST.get("password"))
        plan = request.POST.get("plan")
        
         # Check if the email is already registered
        if GymUser.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email is already registered."})

        # Extract the price from the selected plan
        try:
            amount = int(plan.split("-")[-1].strip().replace(",", ""))
        except (IndexError, ValueError):
            return render(request, "register.html", {"error": "Invalid plan selection."})

        # Save user details to the database
        GymUser.objects.create(username=username, email=email, password=password, plan=plan)

        # Redirect to PhonePe payment gateway
        phonepe_url = generate_phonepe_payment_url(amount)
        return redirect(phonepe_url)

    return render(request, "register.html") #to put succesful payment page

def generate_phonepe_payment_url(amount):
    """
    Generates the PhonePe payment URL.
    Replace the placeholder URL and parameters with actual PhonePe API details.
    """
    base_url = "https://phonepe.com/payment"  # Replace with actual gateway URL
    callback_url = "https://yourwebsite.com/payment/callback"  # Your callback endpoint
    merchant_id = "MERCHANT_ID"  # Replace with your PhonePe merchant ID
    payload = f"{base_url}?merchantId={merchant_id}&amount={amount}&callbackUrl={callback_url}"
    return payload

def payment_callback(request):
    """
    Handle the callback from PhonePe after payment.
    """
    if request.method == "POST":
        # Process the payment response here
        payment_status = request.POST.get("status")
        transaction_id = request.POST.get("transactionId")
        # Handle success or failure
        if payment_status == "SUCCESS":
            return HttpResponse("Payment successful!")
        else:
            return HttpResponse("Payment failed. Please try again.")
    return HttpResponse("Invalid request.")
