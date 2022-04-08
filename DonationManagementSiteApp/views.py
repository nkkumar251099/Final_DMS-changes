import sys

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse
from django.db import connection
from .models import Volunteer
import os

val = ''


# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')


def loginOptions(request):
    return render(request, 'loginOptions.html')


def signup_page(request):
    return render(request, 'signup.html')


def vol_signed_up(request):
    username = request.POST['user-name']
    phonenumber = request.POST['user-phone-number']
    email = request.POST['user-email']

    cursor = connection.cursor()
    query1 = "select * from donationmanagementsiteapp_volunteer where email= '" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchall()

    if len(data) > 0:
        return render(request, 'Unsuccessfulpopup.html')
        sys.exit()

    else:
        password = request.POST['user-password']

        aadhar_image = request.FILES['user-aadhar-image']
        fss = FileSystemStorage()
        file = fss.save(aadhar_image.name, aadhar_image)  # this is for saving image in media folder
        aadhar_image_path = fss.url(file)  # this is for getting image path

        address = request.POST['user-address']
        city = request.POST['city-name']
        state = request.POST['state-name']

        new_volunteer = Volunteer(username=username, phonenumber=phonenumber, email=email, password=password,
                                  aadhar_image_path=aadhar_image_path, address=address, city=city, state=state)
        new_volunteer.save()

        return render(request, 'Successfulpopup.html')


def vol_loged_in(request):
    global val
    email = request.POST['email']
    password = request.POST['password']

    cursor = connection.cursor()
    query1 = "select * from donationmanagementsiteapp_volunteer where email= '" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()

    if data is not None:
        if password == data[4]:
            if email not in val:
                for i in email:
                    val = val + i
            data = {"username": data[1],"donrequest":data[10]}
            return render(request, 'dashboard.html', data)
        else:
            return HttpResponse('Your password is wrong')

def donrequest(request):
    global val
    gl_email = val
    cursor = connection.cursor()
    query1 = "select donrequest,donaremail from donationmanagementsiteapp_volunteer where email= '" + gl_email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data[0]==0 or data[0]=='0':
        return render(request, 'norequest.html')
    else:
        query2 = "select FirstName,LastName,mobile from donar where email= '" + data[1] + "'"
        cursor.execute(query2)
        data1 = cursor.fetchall()
        query3 = "select optionname,dco from itemdonate where donar_email= '" + data[1] + "'"
        cursor.execute(query3)
        data2=cursor.fetchall()
        fname=data1[0][0]
        lname=data1[0][1]
        mob=data1[0][2]
        dname=data2[0][0]
        dcarea=data2[0][1]
        data = {"fname":fname, "lname": lname,"mob":mob,"dname":dname,"dcarea":dcarea}
        return render(request, 'request.html', data)



def vol_profile_info(request):
    global val
    gl_email = val

    cursor = connection.cursor()
    query1 = "select * from donationmanagementsiteapp_volunteer where email= '" + gl_email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data is not None:
        info={
            "username": data[1],
            "phonenumber": data[2],
            "email": data[3],
            "aadhar_image_path": data[5],
            "address": data[6],
            "city": data[7],
            "state": data[8],
        }
        return render(request,'profileinfo.html',info)
    else:
        return HttpResponse('no data')

def delivered(request):
    global val
    gl_email = val
    cursor = connection.cursor()
    query1 = "update donationmanagementsiteapp_volunteer set donrequest=0,isavailable='Yes',donaremail=NULL where email= '" + gl_email + "'"
    cursor.execute(query1)
    data = {"email":"Thank you for your kindness!"}
    return render(request, 'donsuccessfulpopup.html', data)
