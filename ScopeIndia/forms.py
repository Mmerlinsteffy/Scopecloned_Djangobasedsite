from django import forms
from .models import Registration
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'fullname',
            'gender',
            'eduqual',
            'mobile',
            'email',
            'guardname',
            'address',
            'city',
            'state',
            'country',
            'pin'
        ]
        labels={
            'fullname':'Full Name',
            'gender':'Gender',
            'eduqual':'Educational Qualification',
            'mobile':'Mobile Number',
            'email':'Email ID',
            'guardname':'Guardian Name',
            'address':'Address',
            'city':'City',
            'state':'State',
            'country':'Country',
            'pin':'Pincode'
        }