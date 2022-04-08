from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.db import connection
# Create your views here.
from django.template import RequestContext

# def Donarlogin(request):
#     return render(request,"Donor_login.html")
def Donarsignup(request):
    return render(request,"donor_signup.html")
def Donarsignin(request):
    email=request.GET["email"]
    Password=request.GET["psw"]
    cursor=connection.cursor()
    Query="select * from Donar where email='"+email+"'"
    cursor.execute(Query)
    data=cursor.fetchall()
    if len(data)>0:
        data={"email":"Already exist! use another email id."}
        return render(request,"donunsuccesfulpopup.html",data)
    else:
        FirstName=request.GET["fname"]
        LastName=request.GET["lname"]
        Mobile=request.GET["mob"]
        Address=request.GET["Add"]
        cursor=connection.cursor()
        Query1="insert into Donar(FirstName,LastName,email,mobile,Pass,address) values (%s,%s,%s,%s,%s,%s)"
        value=(FirstName,LastName,email,Mobile,Password,Address)
        cursor.execute(Query1,value)
        query3 = "insert into dashboard (email) values ('" + email + "')"
        cursor.execute(query3)
    return render(request,"donsuccessfulpopup.html")
def Donarverify(request):
    email=request.GET["email"]
    psw=request.GET["psw"]
    cursor=connection.cursor()
    Query2="select email,pass,FirstName,LastName from Donar where email='"+email+"'"
    cursor.execute(Query2)
    data=cursor.fetchall()
    if len(data)==0:
        data={"email":"Donar doesn't exist"}
        return render(request,"donunsuccesfulpopup.html",data)

    else:
        if email==data[0][0] and psw==data[0][1]:
            global val
            def val():
                return data[0][0]
            fname=data[0][2]
            lname=data[0][3]
            query3 = "select * from dashboard where email='"+email+"'"
            cursor.execute(query3)
            das_data = cursor.fetchall()
            totaldon=das_data[0][1]
            acceptdon=das_data[0][2]
            rejectdon=das_data[0][3]
            pendingdon=das_data[0][4]
            successdon=das_data[0][5]
            d_data={"fname":fname,"lname":lname,"tdon":totaldon,"accdon":acceptdon,"rejdon":rejectdon,"pendon":pendingdon,"sucdon":successdon}
            return render(request,"donordashboard.html",d_data)
        else:
            data = {"email": "Donar doesn't exist"}
            return render(request, "donunsuccesfulpopup.html", data)

def donordashboard(request):
    glo_email=val()
    cursor = connection.cursor()
    Query4 = "select * from dashboard left join donar on dashboard.email=donar.email where dashboard.email='"+glo_email+"'"
    cursor.execute(Query4)
    data = cursor.fetchall()
    totaldon = data[0][1]
    acceptdon = data[0][2]
    rejectdon = data[0][3]
    pendingdon = data[0][4]
    successdon = data[0][5]
    fname=data[0][8]
    lname=data[0][9]
    d_data = {"fname": fname, "lname": lname, "tdon": totaldon, "accdon": acceptdon, "rejdon": rejectdon,
              "pendon": pendingdon, "sucdon": successdon}
    return render(request, "donordashboard.html", d_data)
def donatenow(request):
    return render(request, "donate_now.html")
def logout(request):
    return render(request, "Donor_login.html")
def profile(request):
    glo_email = val()
    cursor = connection.cursor()
    Query2 = "select FirstName,LastName,email,mobile,address from Donar where email='"+glo_email+"'"
    cursor.execute(Query2)
    data = cursor.fetchall()
    fname = data[0][0]
    lname = data[0][1]
    email = data[0][2]
    mobile = data[0][3]
    address=data[0][4]
    pro_data={"fname": fname, "lname": lname,"email":email,"mobile":mobile,"address":address}
    return render(request, "profile.html",pro_data)

def editprofile(request):
    glo_email = val()
    cursor = connection.cursor()
    Query2 = "select FirstName,LastName,email,mobile,address from Donar where email='"+glo_email+"'"
    cursor.execute(Query2)
    data = cursor.fetchall()
    fname = data[0][0]
    lname = data[0][1]
    email = data[0][2]
    mobile = data[0][3]
    address=data[0][4]
    pro_data={"fname": fname, "lname": lname,"email":email,"mobile":mobile,"address":address}
    return render(request, "editprofile.html",pro_data)


def updateProfile(request):
    glo_email = val()
    fname = request.GET["fname"]
    lname = request.GET["lname"]
    email = request.GET["email"]
    mob = request.GET["contact"]
    add = request.GET["Add"]
    cursor = connection.cursor()
    Query5 = "update donar set FirstName='"+fname+"',LastName='"+lname+"',email='"+email+"',mobile='"+mob+"',address='"+add+"' where email='"+glo_email+"'"
    Query6 = "update dashboard set email='"+email+"' where email='"+glo_email+"'"
    cursor.execute(Query5)
    cursor.execute(Query6)
    dic={"email":"Your profile is successfully updated."}
    return render(request, "donsuccessfulpopup.html",dic)

def readytodonate(request):
    glo_email = val()
    optionname = request.GET["option"]
    ico = request.GET["ico"]
    dco = request.GET["dco"]
    city = request.GET["city"]
    dsn = request.GET["dsn"]
    cursor = connection.cursor()
    Query20 = "insert into itemdonate(optionname,ico,dco,city,dsn,donar_email) values (%s,%s,%s,%s,%s,%s)"
    value20=(optionname,ico,dco,city,dsn,glo_email)
    cursor.execute(Query20, value20)
    Query21 = "select pendingdonation from dashboard where email='" + glo_email + "'"
    cursor.execute(Query21)
    data = cursor.fetchone()
    pendingdonation=data[0]
    Query6 = "update dashboard set pendingdonation='"+str((pendingdonation+1))+"' where email='"+glo_email+"'"
    cursor.execute(Query6)
    dic={"email":"Thank you! We appereciate your move. We are processing you request."}
    return render(request, "donsuccessfulpopup.html",dic)

# admin activity
def adminverify(request):
    email = request.GET["email"]
    psw = request.GET["psw"]
    cursor = connection.cursor()
    Query2 = "select email,adminpassword from admintable where email='" + email + "'"
    cursor.execute(Query2)
    data = cursor.fetchall()
    if len(data) == 0:
        data = {"email": "admin doesn't exist"}
        return render(request, "exist.html", data)

    else:
        if email == data[0][0] and psw == data[0][1]:
            query3 = "select pendingdonation from dashboard"
            cursor.execute(query3)
            ad_data = cursor.fetchall()
            sum=0
            for i in range(len(ad_data)):
                sum=sum+ad_data[i][0]
            data={"email":sum}
            return render(request, "admindashboard.html", data)
        else:
            data = {"email": "Admin doesn't exist"}
            return render(request, "exist.html", data)


#request allocate
def alocaterequest(request):
    cursor = connection.cursor()
    Query30 = "select email,pendingdonation from dashboard where pendingdonation=1"
    cursor.execute(Query30)
    data=cursor.fetchall()
    email=data[0][0]
    pendingdonation=data[0][1]
    Query31 = "select address from donar where email='" +email+ "'"
    cursor.execute(Query31)
    data=cursor.fetchall()
    donar_city=data[0][0]
    Query32 = "select username,phonenumber,email,isavailable from donationmanagementsiteapp_volunteer where city='" + donar_city + "'"
    cursor.execute(Query32)
    vol_data=cursor.fetchall()
    for i in range(len(vol_data)):
        if vol_data[i][3]=='Yes':
            req_email=vol_data[i][2]
            Query33="update donationmanagementsiteapp_volunteer set isavailable='No' where email='"+req_email+ "'"
            cursor.execute(Query33)
            Query35 = "update donationmanagementsiteapp_volunteer set donrequest=1,donaremail='"+email+"' where email='" + req_email + "'"
            cursor.execute(Query35)
            Query34 = "update dashboard set pendingdonation=0 where email='"+email+"'"
            cursor.execute(Query34)
            break
        else:
            data = {"email": "No volunteer Available right now."}
            return render(request, "exist.html", data)
    data = {"email": "Volunteer assigned."}
    return render(request, "exist.html", data)



