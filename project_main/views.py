from django.shortcuts import render, redirect

def register_page(request):
    return render(request,'register.html')
def login_page(request):
    return render(request, 'login.html')
def home_page(request):
    return render(request, 'home.html')
