from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
import logging
from logging import Formatter,FileHandler
import os
import re
import csv

ALLOWED_EXTENSIONS = {'sol'}
OPERATIONS = {'function', 'contract', 'return', 'require'}

def allowed_file(filename):
    print(filename.rsplit('.')[1])
    if(filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS):
        return True
    return False 

def searchfunction(file, operation):
    return sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(operation), str(file)))

def home(request):
    return render(request,'home.html')

def filePost(request):
    if 'solFile' not in request.FILES:
        messages.error(request, 'No File!.')
        return redirect('/')
    file = request.FILES['solFile']
    if file.name == '':
        messages.error(request,'No file Selected')
    if file and allowed_file(file.name):
        f = file.read()
        # count = searchfunction(f,operation)
        # print(operation + ',' + str(count))
        messages.success(request,'Download Complete')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="eagle.csv"'
        writer = csv.writer(response)
        writer.writerow(['Keyword','Number of times it is used'])
        for operation in OPERATIONS:
            count = searchfunction(f,operation)
            writer.writerow([operation,str(count)])
        # print(writer)
        # writer.writerow([operation,str(count)])
        messages.success(request,'Download Complete')
        return response        
        return redirect('/')

    