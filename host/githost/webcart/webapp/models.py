from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.

class register(models.Model):
    name=models.CharField(max_length=20)
    frimg=models.FileField()
    email=models.EmailField(max_length=200,unique=True)
    state = models.CharField(max_length=200,null=True)
    district = models.CharField(max_length=200,null=True)
    pin_code = models.IntegerField(null=True)
    address=models.CharField(max_length=500)
    number=models.IntegerField()
    user_name=models.CharField(max_length=20,unique=True)
    password=models.CharField(max_length=20,unique=True)
    c_password=models.CharField(max_length=20,unique=True)




class verify_emp(models.Model):
    name=models.CharField(max_length=20)
    image=models.FileField()
    cv = models.FileField(upload_to='pdfs/', null=True, blank=True)
    job = models.CharField(max_length=20)
    email=models.EmailField(max_length=100,unique=True)
    address=models.CharField(max_length=20)
    number=models.IntegerField()
    user_name=models.CharField(max_length=20,unique=True)
    password=models.CharField(max_length=20,unique=True)
    c_password=models.CharField(max_length=20,unique=True)

class block_employee(models.Model):
    name=models.CharField(max_length=20)
    image=models.FileField()
    cv = models.FileField(upload_to='pdfs/', null=True, blank=True)
    job= models.CharField(max_length=20)
    email=models.EmailField(max_length=100,unique=True)
    address=models.CharField(max_length=20)
    number=models.IntegerField()
    user_name=models.CharField(max_length=20,unique=True)
    password=models.CharField(max_length=20,unique=True)
    c_password=models.CharField(max_length=20,unique=True)


class u_review(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE, null=True)
    Message= models.CharField(max_length=200)
    radio_c=models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    user_name = models.CharField(max_length=200,null=True)
    s_name = models.CharField(max_length=200,null=True)

class w_categories(models.Model):
    s_name=models.CharField(max_length=20)
    frimg=models.FileField()
    s_price=models.IntegerField()
    content=models.CharField(max_length=50)


class emp_reg(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField()
    cv = models.FileField(upload_to='pdfs/', null=True, blank=True)
    job_choice = (
        ('carpenter', 'carpenter'),
        ('Furniture Mover', 'Furniture Mover'),
        ('tank cleaner', 'tank cleaner'),
        ('Plumber', 'Plumber'),
        ('cctv technician', 'cctv technician')

    )
    job= models.CharField(max_length=150, choices=job_choice, default='select',  null=True)
    email = models.EmailField(max_length=200,unique=True)
    address = models.CharField(max_length=20)
    number = models.IntegerField()
    user_name = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20, unique=True)
    c_password = models.CharField(max_length=20, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)
    orderstatus = (
        ('Free', 'Free'),
        ('In work', 'In work'),
        ('Off duty', 'Off duty')

    )
    status = models.CharField(max_length=150, choices=orderstatus, default='Free', null=True)




class booked(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE, null=True)
    emp = models.ForeignKey(emp_reg, on_delete=models.CASCADE, null=True)
    booking_id = models.IntegerField(unique=True)
    booked_name= models.CharField(max_length=500)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=500)
    number = models.IntegerField()
    state = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    pin_code = models.IntegerField(null=True)
    date = models.DateField(default=datetime.datetime.today, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    b_s_name = models.CharField(max_length=200, null=True)
    b_s_price = models.IntegerField(null=True)
    payment_mode = models.CharField(max_length=200, default='Razor_pay', null=True)

class bookings(models.Model):

    booking_id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(register, on_delete=models.CASCADE, null=True)
    emp = models.ForeignKey(emp_reg, on_delete=models.CASCADE, null=True)
    b_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=500)
    number = models.IntegerField()
    state = models.CharField(max_length=200,null=True)
    district = models.CharField(max_length=200,null=True)
    pin_code = models.IntegerField(null=True)
    date = models.DateField(default=datetime.datetime.today,null=True)
    w=models.ForeignKey(w_categories,on_delete=models.CASCADE,null=True)
    review = models.ForeignKey(u_review, on_delete=models.CASCADE, null=True)
    orderstatus = (
        ('Accepted', 'Accepted'),
        ('Finished', 'Finished'),
        ('pending', 'pending'),
        ('Cancelled', 'Cancelled')
    )



    status = models.CharField(max_length=150, choices=orderstatus, default='pending', null=True)


    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)
    payment_status=models.CharField(max_length=200,null=True)












class adminpassbookings(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE, null=True)
    emp = models.ForeignKey(emp_reg, on_delete=models.CASCADE, null=True)
    booking_id = models.IntegerField(unique=True)
    booked_name = models.CharField(max_length=500)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=500)
    number = models.IntegerField()
    state = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    pin_code = models.IntegerField(null=True)
    date = models.DateField(default=datetime.datetime.today, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    b_s_name = models.CharField(max_length=200, null=True)
    b_s_price = models.IntegerField(null=True)
    payment_mode = models.CharField(max_length=200, default='Razor_pay', null=True)
    orderstatus = (

        ('Finished', 'Finished'),
        ('pending', 'pending'),
        ('Cancelled', 'Cancelled')
    )

    status = models.CharField(max_length=150, choices=orderstatus, default='pending', null=True)






class PasswordReset(models.Model):
    user=models.ForeignKey(register,on_delete=models.CASCADE,null=True, blank=True)
    emp = models.ForeignKey(emp_reg, on_delete=models.CASCADE, null=True, blank=True)
    #security
    token=models.CharField(max_length=4)

