from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('registration/',views.register,name='registration'),
    path('about/',views.about,name='about'),
    path('course/',views.course,name='course'),
    path('coursedetail/<int:id>/',views.coursedetail,name='coursedetail'),
    path('login/',views.login_enter,name='login'),
    path('success/',views.success,name='success'),
    path('failure/',views.failure,name='failure'),
    path('firsttime/',views.firsttime,name='first'),
    path('otp/',views.otp,name='otp'),
    path('setpassword/',views.password,name='setpass'),
    path('logout/',views.logout_out,name='logout'),
    path('forgotpassword/',views.forgotpassword,name='forgot'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('profile/',views.profile,name='profile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('studentcourse/',views.studcourse,name='studcourse'),
    path('editprofile/',views.editprofile,name='editprofile')
]