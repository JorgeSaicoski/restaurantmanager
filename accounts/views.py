from django.shortcuts import  render, redirect
from .forms import NewUserForm, NewCustomerForm
from django.contrib.auth import login
from django.contrib import messages
from accounts.models import Customer

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		# If anything is alright
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("customer_register")
		# If the password is wrong (the another test is checked in front)
		return render(request=request, template_name="accounts/register.html", context={"register_form": form, "message": "Las contraseñas no son iguales"})
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="accounts/register.html", context={"register_form":form})
# Create a profile
def customer_request(request):
	if request.method == "POST":
		form = NewCustomerForm(request.POST)
		if form.is_valid():
			user = request.user
			form.save()
			email = request.POST["email"]
			name = request.POST["name"]
			try:
				customer = Customer.objects.get(email=email)
			except:
				return render(request=request, template_name="accounts/customer.html", context={"register_form": form, "message": "Este email ya esta en uso"})
			customer.user = user
			customer.save()

			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewCustomerForm(request.POST)
	return render (request=request, template_name="accounts/customer.html", context={"register_form":form})
