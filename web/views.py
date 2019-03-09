from django.shortcuts import render,redirect
from .models import TodoList
import datetime
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from .forms import NewUserForm

def index(request):
	if not request.user.is_authenticated:
	 	return redirect("main:login")
	todos = TodoList.objects.all(pk=request.user_id)
	if request.method == "POST": 
		if "taskAdd" in request.POST: 
			title = request.POST["description"]
			date = str(request.POST["date"])
			content = title + " -- " + date
			Todo = TodoList(title=title, content=content, due_date=date)
			Todo.save()  
			return redirect("/")
		
		if "taskDelete" in request.POST:
			checkedlist = request.POST["checkedbox"] 
			for todo_id in checkedlist:
				todo = TodoList.objects.get(id=int(todo_id))
				todo.delete()

	return render(request, "web/index.html", {"todos": todos})

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user=form.save()
			username=form.cleaned_data.get('username')
			messages.success(request, f"You are loggedin as: {username}")
			login(request,user)
			return redirect("/")

		else :
			for msg in form.error.messages :
				messages.error(request, f"{msg}: {form.error_messages[msg]}")
			return render(request = request,template_name = "web/register.html",context={"form":form})

	form=NewUserForm

	return render(request = request,template_name = "web/register.html",context={"form":form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "web/login.html",
                    context={"form":form})


def logout_request(request):
	logout(request)
	messages.info(request,"Logged out successfully")
	return redirect("main:index")
