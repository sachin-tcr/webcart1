from django import forms
from .models import *

class UserProfileForm(forms.Form):
    name=models.CharField(max_length=20)
    frimg=models.FileField()
    email=models.EmailField(max_length=20)
    address=models.CharField(max_length=500)
    number=models.IntegerField()
    user_name=models.CharField(max_length=20)
    password=models.CharField(max_length=20,unique=True)
    c_password=models.CharField(max_length=20,unique=True)


class w_categories_form(forms.Form):
    name=models.CharField(max_length=20)
    frimg=models.FileField()
    price=models.IntegerField()
    content=models.CharField(max_length=100)

class u_review1(forms.ModelForm):
    class Meta:
        model = u_review
        fields = ['Message','user_name','email','s_name']
        # name = models.CharField(max_length=20)
        # email = models.EmailField(max_length=20)
        # number = models.IntegerField()
        # Message= models.CharField(max_length=200)

class ReplyForm(forms.Form):
    review_id = forms.IntegerField(widget=forms.HiddenInput)
    reply = forms.CharField(label='Reply', widget=forms.Textarea)
    user_name = forms.CharField(label='Your Name', max_length=200)
    email = forms.EmailField(label='Your Email')

class emp_regform(forms.Form):
    name = models.CharField(max_length=20)
    image = models.FileField()
    job = models.CharField(max_length=20)
    job1 = (
        ('carpenter', 'carpenter'),
        ('Furniture Mover', 'Furniture Mover'),
        ('tank cleaner', 'tank cleaner'),
        ('Plumber', 'Plumber'),
        ('cctv technician', 'cctv technician')

    )
    job_status = models.CharField(max_length=150, choices=job1, null=True)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=20)
    number = models.IntegerField()
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20, unique=True)
    c_password = models.CharField(max_length=20, unique=True)


