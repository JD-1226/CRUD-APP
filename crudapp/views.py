from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages 
from .forms import SignUpForm, AddRecordForm 
from .models import Record 

# Create your views here.
records = Record.objects.all()

def home(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')
    else: 
        records = Record.objects.all()       
        return render(request, 'home.html',{'records':records})

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})


def student_record(request, pk):
    if request.user.is_authenticated:
        student_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'student_record': student_record})
    else:
        messages.error(request, 'You must be logged in to view that page.')
        return redirect('home')
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record has been deleted successfully.')
        return redirect('home')
    else:
        return redirect('home')
    

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record has been added successfully.')
                return redirect('home')
        
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, 'you must be logged in for that.')
        return redirect('home') 
    

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been updated successfully.')
            return redirect('home')
        
        return render(request, 'update_record.html', {'form':form}) 
    
    else:
        messages.success(request, 'you must be logged in for that.')
        return redirect('home')