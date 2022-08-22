from django.shortcuts import  render, redirect
from .forms import NewUserForm, NewCustomerForm, LoginForm, UpdateCustomerForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from accounts.models import Customer
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		form_customer = NewCustomerForm(request.POST)
		email = request.POST["email"]
		username = request.POST["username"]
		#first of all, check if the email is already in use
		try:
			customer_check = Customer.objects.get(email=email)
			if customer_check.user:
				return render(request=request, template_name="accounts/register.html", context={"register_form": form, "form_customer": form_customer, "message": "Este email ya esta en uso"})
		except:
			pass
		# If anything is alright
		if form.is_valid():
			user = form.save()
			#if it already have some order
			try:
				customer = Customer.objects.get(email=email)
			except:
				customer = form_customer.save()
			customer.user = user
			customer.email = email
			customer.save()
			login(request, user)
			return redirect("/")

		# If the password is wrong (the another test is checked in front)

		try:
			User.objects.get(username=username)
			return render(request=request, template_name="accounts/register.html", context={"register_form": form, "form_customer": form_customer, "message": "Este nombre ya esta en uso"})
		except:
			if request.POST["password1"] != request.POST["password2"]:
				return render(request=request, template_name="accounts/register.html", context={"register_form": form, "form_customer":form_customer, "message": "Las contraseñas no son iguales"})
			for i in username:
				if i == " ":
					return render(request=request, template_name="accounts/register.html", context={"register_form": form, "form_customer": form_customer, "message": "El nombre no puede tener espacio"})
			return render(request=request, template_name="accounts/register.html", context={"register_form": form, "form_customer": form_customer, "message": "La contraseña no cumple los requisitos"})
	form = NewUserForm()
	form_customer = NewCustomerForm()
	return render (request=request, template_name="accounts/register.html", context={"register_form":form, "form_customer":form_customer})
# Update profile
def customer_request(request):
	if request.user.is_authenticated:
		user = request.user
		customer = Customer.objects.get(user=user)
		return render(request=request, template_name="accounts/customer.html", context={"user":user, 'customer':customer})
	return redirect("/account/register/")

def login_request(request):
	if request.user.is_authenticated:
		logout(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, f' wecome {username} !!')
			return redirect("/")
		else:
			messages.info(request, f'account done not exit plz sign in')
	form = LoginForm()

	return render(request, 'accounts/login.html', {'form': form})

def logout_request(request):
	logout(request)
	return redirect("/account/login/")
def updateCustomer(request):
	user = request.user
	customer = Customer.objects.get(user=user)
	data = json.loads(request.body)
	form = data["form"]
	name = form["name"]
	email = form["email"]
	phone = form["phone"]
	username = form["username"]

	try:
		customer_check = Customer.objects.get(name=name)
		if customer_check != customer:

			return JsonResponse('name', safe=False)
	except:
		pass
	try:
		customer_check = Customer.objects.get(email=email)
		if customer_check != customer:
			return JsonResponse('email', safe=False)
	except:
		pass
	try:
		user_check = User.objects.get(username=username)
		if user_check != user:
			return JsonResponse('login', safe=False)
	except:
		pass

	customer.email = email
	customer.name = name
	customer.phone = phone
	user.username = username
	user.email = email
	customer.save()
	user.save()

	return JsonResponse('success', safe=False)