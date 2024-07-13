from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import *
from django.http import HttpResponse
import razorpay
from collections import defaultdict
import re
from django.db.models import Q
from django.template import loader
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .forms import *
import os
def userregister(request):
    if request.method=='POST':
        name=request.POST['name']
        frimg1=request.FILES['frimg1']
        email=request.POST['email']
        number=request.POST['number']
        state=request.POST['state']
        district=request.POST['district']
        pin_code=request.POST['pin_code']
        address=request.POST['address']
        user_name = request.POST['user_name']
        password=request.POST['password']
        c_password=request.POST['c_password']

        if password != c_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'registration.html')

            # Password strength conditions
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return render(request, 'registration.html')

        special_char_pattern = r'[!@#$%^&*()_+=\-[\]{};:\'"\\|,.<>/?]'
        alph_pattern = r'[A-Za-z]'
        number_pattern = r'[0-9]'


        if not re.search(special_char_pattern, password):
            messages.error(request, "Password must contain at least one special character")
            return render(request, 'registration.html')
        
        if not re.search(alph_pattern, password):
            messages.error(request, "Password must contain at least one uppercase letter")
            return render(request, 'registration.html')

        if not re.search(number_pattern, password):
            messages.error(request, "Password must contain at least one number")
            return render(request, 'registration.html')

        try:
            d=register(name=name, frimg=frimg1,state=state,district=district,pin_code=pin_code,email=email,number=number,address=address,user_name=user_name,password=password,c_password=c_password)
            d.save()
            messages.success(request, "Registration completed")
        except Exception as e:
            messages.error(request, f"Failed to save registration: {str(e)}")

        return redirect(login)
    return render(request,'registration.html')
def empregister(request):
    if request.method=='POST':
        name=request.POST['emp_name']
        image=request.FILES['image']
        cv = request.FILES['cv']
        email=request.POST['emp_email']
        number=request.POST['emp_number']
        address=request.POST['emp_address']
        user_name = request.POST['emp_user_name']
        password=request.POST['emp_password']
        c_password=request.POST['emp_c_password']

        if password != c_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'emp_registration.html')

            # Password strength conditions
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return render(request, 'emp_registration.html')

        special_char_pattern = r'[!@#$%^&*()_+=\-[\]{};:\'"\\|,.<>/?]'
        alph_pattern = r'[A-Za-z]'
        number_pattern = r'[0-9]'

        if not re.search(special_char_pattern, password):
            messages.error(request, "Password must contain at least one special character")
            return render(request, 'emp_registration.html')

        if not re.search(alph_pattern, password):
            messages.error(request, "Password must contain at least one uppercase letter")
            return render(request, 'emp_registration.html')

        if not re.search(number_pattern, password):
            messages.error(request, "Password must contain at least one number")
            return render(request, 'emp_registration.html')

        job=request.POST.get('work1')

        try:
            d=verify_emp(cv=cv,job=job,name=name,image=image,email=email,number=number,address=address,user_name=user_name,password=password,c_password=c_password)
            d.save()
            messages.success(request,"Employee Registration completed")
        except Exception as e:
            messages.error(request, f"Failed to save registration: {str(e)}")


        return redirect(login)

    return render(request,'emp_registration.html')
def addemp(request):
    if 'aid' in request.session:
        if request.method=='POST':
            name=request.POST['emp_name']
            image=request.FILES['image']
            cv = request.FILES['cv']
            email=request.POST['emp_email']
            number=request.POST['emp_number']
            address=request.POST['emp_address']
            user_name = request.POST['emp_user_name']
            password=request.POST['emp_password']
            c_password=request.POST['emp_c_password']
            if password != c_password:
                messages.error(request, "Passwords do not match")
                return render(request, 'emp_registration.html')

                # Password strength conditions
            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long")
                return render(request, 'emp_registration.html')

            special_char_pattern = r'[!@#$%^&*()_+=\-[\]{};:\'"\\|,.<>/?]'
            alph_pattern = r'[A-Za-z]'
            number_pattern = r'[0-9]'

            if not re.search(special_char_pattern, password):
                messages.error(request, "Password must contain at least one special character")
                return render(request, 'emp_registration.html')

            if not re.search(alph_pattern, password):
                messages.error(request, "Password must contain at least one uppercase letter")
                return render(request, 'emp_registration.html')

            if not re.search(number_pattern, password):
                messages.error(request, "Password must contain at least one number")
                return render(request, 'emp_registration.html')

            job=request.POST.get('work1')
            try:
                d=verify_emp(cv=cv,job=job,name=name,image=image,email=email,number=number,address=address,user_name=user_name,password=password,c_password=c_password)
                d.save()
                messages.success(request,"Employee Registration completed")
            except Exception as e:
                messages.error(request, f"Failed to save registration: {str(e)}")
    return render(request,'Add Employee.html')
def Add_work_categories(re):
    if re.method=='POST':
        name=re.POST['s_name']
        re.session['s_id']=name
        frimg1=re.FILES['s_img']
        price=re.POST['s_price']
        content=re.POST['s_content']
        d= w_categories.objects.create(s_name=name,frimg=frimg1,s_price=price,content=content)
        d.save()
        return redirect(admin)
    return render(re,'Add work categories.html')

def login(re):
    if re.method == 'POST':
        u = re.POST['user_name']
        p = re.POST['password']
        try:
            data = register.objects.get(user_name=u)
            if u == data.user_name and p == data.password:
                re.session['uid']=u
                return redirect(customers)
            else:
                messages.error(re,'invalid username or password')
        except Exception:
            try:
                data=emp_reg.objects.get(user_name=u)
                if u == data.user_name and p== data.password:
                    re.session['empid']=u
                    return redirect(workers)
                else:
                    messages.error(re, 'invalid username or password')
            except:
                if u=='admin' and p=='admin':
                    re.session['aid']=u
                    return redirect(admin)
                else:
                    messages.error(re, 'invalid username or password')
    return render(re,'login.html')

def viewusers(re):
    d=register.objects.all()
    return render(re,'viewusers.html',{'d':d})

def Verify_workers(re):
    data=verify_emp.objects.all()
    return render(re,'Verify workers.html',{'da':data})

def approve_item(request, id):
    rev_item = verify_emp.objects.get(pk=id)
    item = emp_reg(cv=rev_item.cv,job=rev_item.job,name=rev_item.name,image=rev_item.image,email=rev_item.email,number=rev_item.number,address=rev_item.address,user_name=rev_item.user_name,password=rev_item.password,c_password=rev_item.c_password)
    item.save()
    rev_item.delete()
    return redirect(Verify_workers)
def viewemployee(request):
    data=emp_reg.objects.all()
    return render(request,'view_employee.html',{'da':data})
    # return render(request,'view_employee.html',{'da':data})
def cust_View_profile(re):
    if 'uid' in re.session:
        u=register.objects.get(user_name=re.session['uid'])
        return render(re,'cust_View profile.html',{'user':u})
    return render(re, 'login.html')
def View_profile(re):
    if 'empid' in re.session:
        u = emp_reg.objects.get(user_name=re.session['empid'])
        return render(re, 'View profile.html', {'user': u})
    return render(re, 'login.html')
def pro_edit(re,id):
    if 'uid' in re.session:
        u=register.objects.get(pk=id)
        if re.method == 'POST':
            u.name = re.POST['name']
            u.email = re.POST['email']
            u.number = re.POST['number']
            u.address = re.POST['address']
            if 'frimg1' in re.FILES:
                u.frimg= re.FILES['frimg1']
                if os.path.exists(u.frimg.path):
                    os.remove(u.frimg.path)
            try:
                u.save()
            except:
                return redirect(update_profile,id)
            messages.success(re, '...Profile Updated Successfully...')
            return redirect(cust_View_profile)

        return render(re,'update_u_profile.html',{'d':u})





def emp_pro_edit(re,id):
    if 'empid' in re.session:
        u=emp_reg.objects.get(pk=id)
        if re.method == 'POST':
            u.name = re.POST['name']
            u.email = re.POST['email']
            u.number = re.POST['number']
            u.address = re.POST['address']
            u.job=re.POST['job']
            if 'image' in re.FILES:
                u.image= re.FILES['image']
                if os.path.exists(u.image.path):
                    os.remove(u.image.path)
            try:
                u.save()
            except:
                return redirect(emp_update_profile,id)
            messages.success(re, '...Profile Updated Successfully...')
            return redirect(View_profile)
        return render(re,'update_emp_profile.html',{'d':u})
    return redirect(View_profile)



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = register.objects.get(email=email)
        except register.DoesNotExist:
            user = None

        try:
            emp = emp_reg.objects.get(email=email)
        except emp_reg.DoesNotExist:
            emp = None

        if not user and not emp:
            messages.info(request, "Email id not registered")
            return redirect('forgot_password')

        if user:
            # Generate and save a unique token for the user
            token = get_random_string(length=4)
            PasswordReset.objects.create(user=user, token=token)
        else:
            # Generate and save a unique token for the employee
            token = get_random_string(length=4)
            PasswordReset.objects.create(emp=emp, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request, "Network connection failed")
            return redirect('forgot_password')

    return render(request, 'forget_password.html')
    # --------------------------------------------------


def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            try:
                password_reset.user.password=new_password
                password_reset.user.save()
            except:
                password_reset.emp.password = new_password
                password_reset.emp.save()

            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html',{'token':token})


def send_review_form(re,id):
    if 'uid' in re.session:
        u = register.objects.get(user_name=re.session['uid'])
        s = bookings.objects.get(pk=id)
        return render(re, 'send_reviews.html', {'user': u, 's': s})


def send_reviews(re):
    if 'uid' in re.session:
        u = register.objects.get(user_name=re.session['uid'])
        s=w_categories.objects.all()
        if re.method == 'POST':
            email=re.POST['email']
            Message=re.POST['Message']
            radio_c=re.POST['select5']
            user_name = re.POST['Name']
            s.s_name=re.POST.get('s_name')
            data=u_review(s_name=s.s_name,email=email,radio_c=radio_c,Message=Message,user_name=user_name)
            data.save()
        return redirect(show_reviews)
    return render(re, 'send_reviews.html')


def show_reviews(re):
    Very_Bad = 0
    Bad = 0
    Very_Good = 0
    Good = 0
    Excellent = 0
    l = []

    # Retrieve all items from u_review model
    items = u_review.objects.all()

    # Count occurrences of each rating category
    for i in items:
        if i.radio_c == 'Very Bad':
            Very_Bad += 1
        elif i.radio_c == 'Bad':
            Bad += 1
        elif i.radio_c == 'Very Good':
            Very_Good += 1
        elif i.radio_c == 'Good':
            Good += 1
        elif i.radio_c == 'Excellent':
            Excellent += 1
    for i in items:
        l.append(i.radio_c)

    d = u_review.objects.all()
    return render(re,'show_reviews.html',{'user1':d,
        'Vb': Very_Bad,
        'Bd': Bad,
        'Vg': Very_Good,
        'Gd': Good,
        'Ex': Excellent,})

def emp_show_reviews(re):
    if 'empid' in re.session:
        u = emp_reg.objects.get(user_name=re.session['empid'])
        d = u_review.objects.filter(s_name= u.job)
        return render(re, 'emp_show_reviews.html', {'user1': d})



def all_show_reviews(re):
    d = u_review.objects.all()
    return render(re, 'all_show_reviews.html', {'user1': d})






def dek(re):
    data=u_review.objects.all()
    data.delete()
    return redirect(show_reviews)
def block_emp(request,id):
    rev_item = emp_reg.objects.get(pk=id)
    item =block_employee(cv=rev_item.cv,name=rev_item.name, image=rev_item.image, job=rev_item.job, email=rev_item.email,
                   number=rev_item.number, address=rev_item.address, user_name=rev_item.user_name,
                   password=rev_item.password, c_password=rev_item.c_password)
    item.save()
    rev_item.delete()
    return redirect(viewemployee)
def viewblock_emp(re):
    data=block_employee.objects.all()
    return render(re,'view_blocked_employee.html',{'da':data})
def unblock_emp(request,id):
    rev_item = block_employee.objects.get(pk=id)
    item =emp_reg(cv=rev_item.cv,name=rev_item.name, image=rev_item.image, job=rev_item.job, email=rev_item.email,
                   number=rev_item.number, address=rev_item.address, user_name=rev_item.user_name,
                   password=rev_item.password, c_password=rev_item.c_password)
    item.save()
    rev_item.delete()
    return redirect(viewblock_emp)
def a_emp_dele(request,id):
    data=emp_reg.objects.get(pk=id)
    data.delete()
    return redirect(viewemployee)
def user_dele(request):
    if 'uid' in request.session:
        data=register.objects.get(user_name=request.session['uid'])
        data.delete()
    return redirect(login)
def emp_dele(request):
    if 'empid' in request.session:
        data=emp_reg.objects.get(user_name=request.session['empid'])
        data.delete()
    return redirect(login)


def emp_block_dele(request,id):
    data=block_employee.objects.get(pk=id)
    data.delete()
    return redirect(viewblock_emp)

def veri_emp_dele(re,id):
    data = verify_emp.objects.get(pk=id)
    data.delete()
    return redirect(Verify_workers)

def service_del(request,id):
    if 'aid' in request.session:
        data=w_categories.objects.get(pk=id)
        data.delete()
        return redirect(admin)

def service_up_form(re,id):
    if 'aid' in re.session:
        u = w_categories.objects.get(pk=id)
        return render(re, 'update_service.html', {'d': u})



def service_edit(request,id):
        if 'aid' in request.session:
            u = w_categories.objects.get(pk=id)
            if request.method == 'POST':
                u.s_name = request.POST['s_name']
                u.s_price = request.POST['s_price']
                u.content = request.POST['s_content']
                if 's_img' in request.FILES:
                    u.frimg = request.FILES['s_img']
                    if os.path.exists(u.frimg.path):
                        os.remove(u.frimg.path)
                try:
                    u.save()
                except:
                    return redirect(update_service,id)
                return redirect(admin)
        return render(request, 'update_service.html')


def book(re,id):
    if 'uid' in re.session:
        u = register.objects.get(user_name=re.session['uid'])
        s=w_categories.objects.get(pk=id)
        return render(re, 'booking.html', {'user': u, 's': s})
    return redirect(customers)

def payment(request,price,pk):
        if 'uid' in request.session:
            u = register.objects.get(user_name=request.session['uid'])
            s = bookings.objects.filter(b_name=u)
            t = int(price) * 100
            return render(request, "payment.html", {'amount': t,'pk':pk})
        return render(request, "payment.html")


def single_razor(re,id):
    service = get_object_or_404(w_categories,pk=id)
    user = get_object_or_404(register, user_name=re.session['uid'])
    if re.method == "POST":
        name = re.POST['name']
        address = re.POST['address']
        email = re.POST['email']
        number = re.POST['number']
        state = re.POST['state']
        district = re.POST['district']
        pin_code = re.POST['pin_code']
        date=re.POST['s_date']
        s_name = re.POST.get('s_name')
        s_price = re.POST.get('s_price')
        booking1 = bookings.objects.create(
            w=service,
            email=email,
            state=state,
            district=district,
            pin_code=pin_code,
            b_name=name,
            address=address,
            number=number,
            date=date,
        )
        booking1.save()
        messages.success(re,'booking request sended')
        # return redirect(razorpaycheck,service.s_price)
        return redirect(u_bookreq)
    #     return JsonResponse({'status': 'Your order has been placed successfully'})
    #
    return redirect(customers)

def  u_bookreq(re):
    if 'uid' in re.session:
        u = register.objects.get(user_name=re.session['uid'])
        data = bookings.objects.filter(b_name=u.user_name)
        e = emp_reg.objects.all()
        c = booked.objects.all()
        d = adminpassbookings.objects.all()
        b = booked.objects.values_list('booked_name', flat=True)
        booked_services = booked.objects.values_list('b_s_name', flat=True)
        booked_ids = set(booked.objects.values_list('booking_id', flat=True))

        booked_details = []
        for booking in data:
            if booking.booking_id in booked_ids:
                status = "Cash Paid"
                bookings.objects.filter(booking_id=booking.booking_id).update(payment_status=status)
            else:
                status = "Cash Not-paid"
                bookings.objects.filter(booking_id=booking.booking_id).update(payment_status=status)
            booked_details.append({'booking': booking, 'status': status})
        return render(re, 'u_book_req.html', {'da': data, 'e': e, 'b': b,'booked_details': booked_details,'c':c,'d':d})



# def u_bookreq(re):
#     if 'uid' in re.session:
#         u = register.objects.get(user_name=re.session['uid'])
#         data = bookings.objects.filter(b_name=u.user_name)
#         c=booked.objects.all()
#         v=adminpassbookings.objects.all()
#         booked_ids = set(booked.objects.values_list('booking_id', flat=True))
#
#         booked_details = []
#         for booking in data:
#             if booking.booking_id in booked_ids:
#                 status = "Cash Paid"
#                 bookings.objects.filter(booking_id=booking.booking_id).update(payment_status=status)
#             else:
#                 status = "Cash Not-paid"
#                 bookings.objects.filter(booking_id=booking.booking_id).update(payment_status=status)
#             booked_details.append({'booking': booking, 'status': status})
#
#         return render(re, 'u_book_req.html', {'v':v,'da': data,'c':c,'booked_details': booked_details})
#     return render(re, 'u_book_req.html')
def u_bookreq_cancel(re,id):
    if 'uid' in re.session:
        data = bookings.objects.get(pk=id)
        data.delete()
    return redirect(u_bookreq)









    #












def razor(re):
    return render(re, "payment.html")


def razorpaycheck(request,s_price,pk):
    if 'uid' in request.session:
        u = register.objects.get(user_name=request.session['uid'])
        s = bookings.objects.filter(b_name=u)
        t = s_price*100
        return render(request, "payment.html", {'amount': t, 'pk':pk})


    return redirect(razor)


def success(re,id):
    if 'uid' in re.session:
        r=register.objects.get(user_name=re.session['uid'])
        data = bookings.objects.get(pk=id)
        a = booked.objects.create(booked_name=data.b_name,
                                            email=data.email,
                                            address=data.address,
                                            number=data.number,
                                            state=data.state,
                                            b_s_name=data.w.s_name,
                                            b_s_price=data.w.s_price,
                                            district=data.district,
                                            pin_code=data.pin_code,
                                            date=data.date,
                                  booking_id=data.booking_id)
        # v=booked.objects.filter(booked_name=r.user_name)
        return render(re,'success.html')

def u_dis_bookings(re):
    if 'uid' in re.session:
        data=register.objects.get(user_name=re.session['uid'])
        u=booked.objects.filter(booked_name=data.user_name)
        return render(re,'u_dis_bookings.html',{'d':u})




def a_booking(re):
    data = bookings.objects.all()
    e = emp_reg.objects.all()
    c = booked.objects.all()
    d = adminpassbookings.objects.all()
    b = booked.objects.values_list('booked_name', flat=True)
    booked_services = booked.objects.values_list('b_s_name', flat=True)
    booked_ids = set(booked.objects.values_list('booking_id', flat=True))

    booked_details = []
    for booking in data:
        if booking.booking_id in booked_ids:
            status = "Cash Paid"
        else:
            status = "Cash Not-paid"
        booked_details.append({'booking': booking, 'status': status})
    return render(re, 'a_booking.html', {'da': data, 'e': e, 'b': b,'booked_details': booked_details,'c':c,'d':d})



def a_book_send(re,id):
    if 'aid' in re.session:
        data = bookings.objects.filter(pk=id)
        booking=data.first()
        a = adminpassbookings.objects.create(booked_name=booking.b_name,
                                  email=booking.email,
                                  address=booking.address,
                                  number=booking.number,
                                  state=booking.state,
                                  b_s_name=booking.w.s_name,
                                  b_s_price=booking.w.s_price,
                                  district=booking.district,
                                  pin_code=booking.pin_code,
                                  date=booking.date,
                                  booking_id=booking.booking_id,
                                  created_at=booking.created_at)
        a.save()
        messages.success(re,'work sended')
    return redirect(a_booking)
        # return render(re,'view_emp_work.html',{'d':data})


def conf_bookreq(request):
    if 'empid' in request.session:
        emp=emp_reg.objects.get(user_name=request.session['empid'])
        data = adminpassbookings.objects.filter(b_s_name=emp.job)
        return render(request, 'view_emp_work.html', {'da': data,'s':emp})
    return redirect(workers)



def workers(request):
    if 'empid' in request.session:
        data = emp_reg.objects.get(user_name=request.session['empid'])
        u = w_categories.objects.filter(s_name=data.job)
        return render(request, 'workers.html', {'da': u})
    return redirect(login)






def a_book_cancel(re,id):
    if 'aid' in re.session:
        data = bookings.objects.get(pk=id)
        data.delete()
        return redirect(a_booking)

def statusup(re, booking_id):
    if re.method == "POST":
        st = bookings.objects.get( booking_id=booking_id)
        st.status = re.POST.get('status')
        st.save()
    return redirect(a_booking)

def statusup2(re, booking_id):
    if re.method == "POST":
        st = adminpassbookings.objects.get( booking_id=booking_id)
        st.status = re.POST.get('status')
        st.save()
    return redirect(conf_bookreq)

# def work_status(request):
#     data=emp_reg.objects.all()
#     return render(request,'work status.html',{'da':data})
def emp_status(re):
    if 'empid' in re.session:
        if re.method == "POST":
            st = emp_reg.objects.get(user_name=re.session['empid'])
            st. status = re.POST.get('status')
            st.save()
        return redirect(conf_bookreq)



def signout(request):
    if 'uid' in request.session or 'empid' in request.session or 'aid' in request.session:
        request.session.flush()
        return redirect(login)
    return render(request,'index.html')
def signin(request):
    if 'uid' in request.session or 'empid' in request.session or 'aid' in request.session:
        logged_in = True
    else:
        logged_in = False
    return render(request, 'login.html', {'data': logged_in})








def index(re):
    return render(re,'index.html')

def about(request):
    if 'id' in request.session:
        logged_in = True
    else:
        logged_in = False
    return render(request, 'about.html', {'data': logged_in})

def services(re):
    return render(re,'services.html')
def contact(re):
    return render(re,'contact.html')


def admin(request):
    data=w_categories.objects.all()
    return render(request,'admin.html',{"da":data})

def dele(re,id):
    data=emp_register.objects.get(pk=id)
    data.delete()
    return redirect(viewemployee)




def customers(request):
    data = w_categories.objects.all()
    return render(request,'customers.html', {'da': data})





