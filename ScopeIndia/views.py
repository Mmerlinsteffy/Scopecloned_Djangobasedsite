from django.core.mail.message import email
from django.shortcuts import render,redirect
from . models import *
from django.core.mail import EmailMessage
from django.conf import settings
import random,hashlib
from . forms import ProfileForm
# Create your views here.
def home(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'aboutus.html')

def course(request):
    couses=Maincourse.objects.all()
    return render(request,'courses.html',{"courses":couses})

def coursedetail(request,id):
    detail=Subcourse.objects.get(id=id)
    syllabus = CourseContent.objects.filter(subcourse=detail)
    return render(request, 'coursedetail.html', {
        'detail': detail,
        'syllabus': syllabus
    })

def register(request):
    if request.method=='POST':
       fullname=request.POST['name']
       dob=request.POST['date']
       gender=request.POST['gender']
       eduqual=request.POST['edu']
       mobile=request.POST['mob']
       email=request.POST['email'] 
       guard_name=request.POST['guard']
       guard_occu=request.POST['guardoccu']
       guard_mob=request.POST['guardmob']
       course=request.POST['course']
       trainmode=request.POST['mode']
       location=request.POST['place']
       time=request.POST['time']
       Address=request.POST['add']
       Country=request.POST['country']
       state=request.POST['state']
       city=request.POST['city']
       pin=request.POST['post']
       if Registration.objects.filter(email=email).exists():
            return redirect('failure')
       scoperegister=Registration()
       scoperegister.fullname=fullname
       scoperegister.dob=dob
       scoperegister.gender=gender
       scoperegister.eduqual=eduqual
       scoperegister.mobile=mobile
       scoperegister.email=email
       scoperegister.guardname=guard_name
       scoperegister.guard_occu=guard_occu
       scoperegister.guard_mob=guard_mob
       scoperegister.course=course
       scoperegister.train_mode=trainmode
       scoperegister.location=location
       scoperegister.timing=time
       scoperegister.address=Address
       scoperegister.country=Country
       scoperegister.state=state
       scoperegister.city=city
       scoperegister.pin=pin
       scoperegister.save()
       frommail=settings.EMAIL_HOST_USER
       sub='Registration Successfull'
       message=f"Hello {fullname}  Thank you for registering at SCOPE INDIA."
       mail=EmailMessage(sub,message,frommail,[email])
       mail.send()
       return redirect('success')
    return render(request,'registration.html')

def login_enter(request):
    if 'student' in request.session:
        return redirect('dashboard')
    if request.method=='POST':
        uname=request.POST['uname']
        pword=request.POST['pword']
        encrypt_pword=hashlib.md5(pword.encode())
        check_pword=encrypt_pword.hexdigest()
        check_login=StudentLogin.objects.filter(username=uname,password=check_pword)
        keep_logged = request.POST.get('keep')
        if check_login.exists():
            request.session['student'] = uname
            if keep_logged:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
            return redirect('dashboard')
        else:
            return render(request,'login.html',{'error':'Invalid username or password'})
    return render(request,'login.html')

def logout_out(request):
      request.session.flush()
      return redirect('login')

def success(request):
    return render(request,'success.html')

def failure(request):
    return render(request,'failure.html')
    
def firsttime(request):
    if request.method=='POST':
        mail=request.POST['email']
        match=Registration.objects.filter(email=mail)
        request.session['Email_id']=mail
        if match.exists():
            login_exist = StudentLogin.objects.filter(username=mail)
            if login_exist.exists():
                return render(request,'firsttime.html',{'error':'Password already created. Please login or use forgot password.'})
            else:
                otp=random.randrange(1000,9999)
                request.session['otp']=str(otp)
                request.session['Email_id'] = mail
                request.session['purpose'] = 'create'
                sub='OTP'
                msg=f'Your OTP is {otp}'
                email_sent=EmailMessage(sub,msg,settings.EMAIL_HOST_USER,[mail])
                email_sent.send()
                return redirect('otp')
        else:
            return render(request,'firstlogin.html',{'error':'Not a registered mail'})
    return render(request,'firstlogin.html')
    
def otp(request):
    if request.method=="POST":
        getotp=request.POST['otp']
        value_otp=request.session['otp']
        if getotp==value_otp:
            return redirect('setpass')
        else:
            return render(request,'otp.html',{'error':'Wrong otp'})
    return render(request,'otp.html')
    
def password(request):
    if request.method=='POST':
        newpword=request.POST['password']
        encyrptpword=hashlib.md5(newpword.encode())
        newencodepword=encyrptpword.hexdigest()
        confpword=request.POST['confirm_password']
        encryptconf=hashlib.md5(confpword.encode())
        newconfpword=encryptconf.hexdigest()
        if newencodepword==newconfpword:
            purpose = request.session.get('purpose')
            if purpose=='create':
                username=request.session['Email_id']
                student = Registration.objects.get(email=username)
                newlogin=StudentLogin()
                newlogin.password=newconfpword
                newlogin.student_id=student
                newlogin.username=username
                newlogin.save()
                return redirect('login')
            elif purpose=='reset':
                get_user=request.session['forgotEmail_id']
                studentlogin = StudentLogin.objects.get( username=get_user)
                studentlogin.password = newconfpword
                studentlogin.save()
                request.session.pop('otp',None)
                request.session.pop('Email_id',None)
                request.session.pop('purpose',None)
                return redirect('login')
        else:
            return render(request,'setpassword.html',{'error':'Password doesnt match'})
    return render(request,'setpassword.html')

def forgotpassword(request):
    if request.method=='POST':
        mail=request.POST['email']
        match=Registration.objects.filter(email=mail)
        request.session['forgotEmail_id']=mail
        if match.exists():
                otp = random.randrange(1000,9999)
                request.session['otp'] = str(otp)
                request.session['Email_id'] = mail
                request.session['purpose'] = 'reset'
                Sub='Forgot Password OTP'
                msg=f'Your OTP is {otp}'
                forgot_mail=EmailMessage(Sub,msg,settings.EMAIL_HOST_USER,[mail])
                forgot_mail.send()
                return redirect('otp')
        else:
            return render(request,'firstlogin.html',{'error':'Email not found'})
    return render(request,'firstlogin.html')

def dashboard(request):
    if 'student' not in request.session:
        return redirect('login')
    get_user = request.session['student']
    student = StudentLogin.objects.get( username=get_user)
    if request.method == 'POST':
        if 'image' in request.FILES:
            student.file = request.FILES['image']
            student.save()
            return redirect('dashboard')
    return render(request,'dashboard.html',{ 'student':student,'page':'dashboard'} )

def profile(request):
    if 'student' not in request.session:
        return redirect('login')
    get_user = request.session['student']
    student = StudentLogin.objects.get( username=get_user)
    return render( request,'profile.html',{'student':student,'page':'profile'})

def studcourse(request):
    if 'student' not in request.session:
        return redirect('login')
    get_user = request.session['student']
    student = StudentLogin.objects.get(username=get_user)
    search_course = None
    search = request.GET.get('search')
    if search:
        search_course = Subcourse.objects.filter(subcourse_name__icontains=search )
    return render(request,'studcourse.html',{'student':student,'search_course':search_course,'page':'studcourse'})

def changepassword(request):
    if 'student' not in request.session:
        return redirect('login')
    get_user = request.session['student']
    student = StudentLogin.objects.get(username=get_user)
    msg=''
    if request.method=='POST':
        oldpword=request.POST['oldpassword']
        enc_old=hashlib.md5(oldpword.encode())
        encrypt_oldpword=enc_old.hexdigest()
        newpword=request.POST['newpassword']
        enc_new=hashlib.md5(newpword.encode())
        encrypt_newpword=enc_new.hexdigest()
        confpword=request.POST['confirmpassword']
        enc_change=hashlib.md5(confpword.encode())
        encrypt_confpword=enc_change.hexdigest()
        password_check=StudentLogin.objects.filter(username=get_user,password=encrypt_oldpword)
        if password_check.exists():
            if encrypt_newpword==encrypt_confpword:
                student.password = encrypt_confpword
                student.save()
                request.session.flush()
                return redirect('login')
            else:
                msg=' Newpassword and Confirm password does not match'
        else:
            msg='Old Password is incorrect  go to forgot password'
    return render(request,'changepassword.html',{'student':student,
            'page':'password',
            'error':msg})

def editprofile(request):
    if 'student' not in request.session:
        return redirect('login')
    get_user = request.session['student']
    student = StudentLogin.objects.get(username=get_user)
    profile = student.student_id
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
    return render(request, 'editprofile.html',{'form':form,'student':student,'page':'editprofile'})