from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserItemForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import *


# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        return redirect("basic_user_home")
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        context = {"form": form}
        return render(request, "register.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("basic_user_home")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")
    else:
        return render(request, "login.html")


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect("login")


@login_required
def basic_home(request):
    user_items = UserItem.objects.filter(user=request.user)
    return render(request, "basic_user_home.html", {"user_items": user_items})

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def admin_home(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method=="POST":
        user_id = request.POST.get('user_id')
        try:
            user_delete= User.objects.get(id=user_id)
            user_delete.delete()
            messages.success(request, f"User {user_delete.username} deleted!")
        except User.DoesNotExist:
            messages.error(request, "No User by ye name, traveller.")
    context = {'users':users}   
    return render(request, "admin_home.html", context)


@login_required
def create_item(request):
    if request.method == "POST":
        form = UserItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, "Item Created successfully.")
            return redirect("basic_user_home")
    else:
        form = UserItemForm()

    return render(request, "create_item.html", {"form": form})


@login_required
def update_item(request, item_id):
    item = get_object_or_404(UserItem, id=item_id)

    if request.method == "POST":
        form = UserItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully.")
            return redirect("basic_user_home")
        else:
            messages.error(request, "Error updating item.")
    else:
        form = UserItemForm(instance=item)

    return render(request, "update_item.html", {'form':form, 'item':item})


@login_required
def delete_item(request, item_id):
    UserItem.objects.filter(id=item_id, user=request.user).delete()
    messages.success(request, "Item deleted successfully.")
    return redirect("basic_user_home")

@login_required
def read_items(request):
    query= request.GET.get('q', '')
    user_items = UserItem.objects.filter(title__icontains=query)
    return render(request, 'read_items.html', {'user_items': user_items, 'query':query})