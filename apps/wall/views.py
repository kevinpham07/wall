from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User, Message, Comment
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
	return render(request, "wall/index.html")

def register(request):
	if request.method == "POST":

		count = 0
		if len(request.POST["first_name"]) < 1:
			messages.add_message(request, messages.INFO, "First name can not be blank!", extra_tags = "danger")
			count +=1

		if str.isalpha(request.POST["first_name"]) == False:
			messages.add_message(request, messages.INFO, "First name can only be letters!", extra_tags = "danger")
			count +=1

		if len(request.POST["last_name"]) < 1:
			messages.add_message(request, messages.INFO, "Last name can not be blank!", extra_tags = "danger")
			count +=1

		if str.isalpha(request.POST["last_name"]) == False:
			messages.add_message(request, messages.INFO, "Last name can only be letters!", extra_tags = "danger")
			count +=1

		if len(request.POST["email"]) < 1:
			messages.add_message(request, messages.INFO, "Email can no be blank", extra_tags = "danger")
			count +=1

		if not EMAIL_REGEX.match(request.POST["email"]):
			messages.add_message(request, messages.INFO, "Email is not valid!", extra_tags = "danger")
			count +=1

		if len(request.POST["password"]) < 1:
			messages.add_message(request, messages.INFO, "Password can not be blank", extra_tags = "danger")
			count +=1

		if request.POST["password"] != request.POST["confirmation"]:
			messages.add_message(request, messages.INFO, "Passwords do not match", extra_tags = "danger")
			count +=1

		if count == 0:
			User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST["email"], password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()))
			messages.add_message(request, messages.INFO, "CONGRATULATIONS ON REGISTERING", extra_tags = "success")
			return redirect(reverse("wall:index"))

	return redirect(reverse("wall:index"))

def login(request):
	if request.method == "POST":

		user = User.objects.filter(email = request.POST["email"])
		count = 0

		if len(user) < 1:
			print
			messages.add_message(request, messages.INFO, "Wrong login info")
			count += 1
			redirect(reverse("wall:index"))
		if count == 0:
			if bcrypt.checkpw(request.POST["password"].encode(), User.objects.get(email = request.POST["email"]).password.encode()):
				request.session["name"] = User.objects.get(email = request.POST["email"]).first_name
				request.session["id"] = User.objects.get(email = request.POST["email"]).id
				request.session["logged.in"] = True
				return redirect(reverse("wall:wall"))
			else:
				messages.add_message(request, messages.INFO, "Wrong login info")
				return redirect(reverse("wall:index"))

	return redirect(reverse("wall:index"))

def simplewall(request):
	if "name" not in request.session:
		return redirect(reverse("wall:index"))
	if "id" not in request.session:
		return redirect(reverse("wall:index"))
	if request.session["logged.in"] != True:
		return redirect(reverse("wall:index"))
	return render(request, "wall/simplewall.html", {"messages": Message.objects.all().order_by("-created_at")})

def message(request):
	if request.method == "POST":
		user = User.objects.get(id=request.session["id"])

		if request.POST["message"]:
			Message.objects.create(content = request.POST["message"], user = user)
		return redirect(reverse("wall:wall"))

def comment(request):
	if request.method == "POST":
		user = User.objects.get(id=request.session["id"])
		message = Message.objects.get(id=request.POST["msg.id"])

		if request.POST["comment"]:
			Comment.objects.create(content = request.POST["comment"], message = message, creator = user)
		return redirect(reverse("wall:wall"))

def logout(request):
	request.session.clear()
	return redirect(reverse("wall:index"))
