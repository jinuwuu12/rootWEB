from django.shortcuts import render

def index(request):
    return render(request, 'IC_Main.html')
# Create your views here.
