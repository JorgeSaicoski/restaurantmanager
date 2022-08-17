from django.shortcuts import  render, redirect
from .forms import NewUserForm, NewCustomerForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from accounts.models import Customer

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		form_customer = NewCustomerForm(request.POST)
		email = request.POST["email"]
		# If anything is alright
		if form.is_valid():
			user = form.save()
			customer = form_customer.save()
			customer.user = user
			customer.email = email
			customer.save()
			login(request, user)
			return redirect("/")

		# If the password is wrong (the another test is checked in front)
		try:
			Customer.objects.get(email=email)
			return render(request=request, template_name="accounts/register.html", context={"register_form": form, "form_customer": form_customer, "message": "Este email ya esta en uso"})
		except:
			print(request.POST)
			if request.POST["password1"] != request.POST["password2"]:
				return render(request=request, template_name="accounts/register.html", context={"register_form": form, "form_customer":form_customer, "message": "Las contraseñas no son iguales"})
			return render(request=request, template_name="accounts/register.html", context={"register_form": form, "form_customer": form_customer, "message": "La contraseña no cumple los requisitos"})
	form = NewUserForm()
	form_customer = NewCustomerForm()
	return render (request=request, template_name="accounts/register.html", context={"register_form":form, "form_customer":form_customer})
# Create a profile
def customer_request(request):
	if request.method == "POST":
		form = NewCustomerForm(request.POST)
		if form.is_valid():
			user = request.user
			email = request.POST["email"]
			try:
				customer = Customer.objects.get(email=email)
			except:
				return render(request=request, template_name="accounts/customer.html", context={"register_form": form, "message": "Este email ya esta en uso"})
			customer.user = user
			customer.save()

			return redirect("/")
	form = NewCustomerForm(request.POST)
	return render (request=request, template_name="accounts/customer.html", context={"register_form":form})


def login_request(request):

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