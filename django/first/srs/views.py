from django.shortcuts import render
from django.http import HttpResponse

import sys
from subprocess import run,PIPE
# Create your views here.

def index(request):
    return render(request,"index.html")

def ask(request):

    name=request.GET['name']
    service=request.GET['service']
    out=run([sys.executable,'//home//ganesh1bns//Desktop//SR_Asst//main.py'],shell=False,stdout=PIPE)
    return render(request,'index.html');
