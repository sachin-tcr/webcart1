"""
URL configuration for webcart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from webapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('about',views.about),
    path('services',views.services),
    path('contact',views.contact),
    path('login',views.login),
    path('userregister',views.userregister),
    path('admin1',views.admin),
    path('viewusers',views.viewusers),
    path('viewemployee',views.viewemployee),
    path('addemp',views.addemp),
    path('Add_work_categories',views.Add_work_categories),
    path('Verify_workers',views.Verify_workers),
    path('workers',views.workers),
    path('View_profile',views.View_profile),
    path('customers',views.customers),
    path('cust_View_profile',views.cust_View_profile),
    path('emp_register',views.empregister),
    path('signin',views.signin),
    path('signout',views.signout),
    path('approve_item/<int:id>',views.approve_item),
    path('a_emp_dele/<int:id>',views.a_emp_dele),
    path('emp_block_dele/<int:id>',views.emp_block_dele),
    path('user_profile_edit/<int:id>/', views.pro_edit, name='user_profile_edit'),
    path('emp_profile_edit/<int:id>/',views.emp_pro_edit , name='emp_profile_edit'),
    path('forgot_password',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='reset_password'),
    path('sendreviews',views.send_reviews),
    path('show_review',views.show_reviews),
    path('send_review_form/<int:id>/',views.send_review_form),
    path('emp_show_reviews',views.emp_show_reviews),
    path('all_show_reviews',views.all_show_reviews),
    path('block_emp/<int:id>',views.block_emp),
    path('unblock_emp/<int:id>',views.unblock_emp),
    path('viewblock_emp',views.viewblock_emp),
    path('veri_emp_dele/<int:id>',views.veri_emp_dele),
    path('service_del/<int:id>',views.service_del),
    path('service_edit/<int:id>/',views.service_edit,name='service_edit'),
    path('dek',views.dek),
    path('booking/<int:id>',views.book),
    path('service_up_form/<int:id>',views.service_up_form),
    path('user_dele',views.user_dele),
    path('emp_dele',views.emp_dele),
    path('payment/<int:price>/<int:pk>/',views.payment),
    path('a_booking',views.a_booking),
    path('a_book_cancel/<int:id>',views.a_book_cancel),
    path('single_razor/<int:id>',views.single_razor,name='single_razor'),
    path('razor',views.razor),
    path('razor_pay/<int:s_price>/<int:pk>/',views.razorpaycheck,name='razorpay'),
    path('success/<int:id>/', views.success, name='success'),
    path('statusup/<int:booking_id>',views.statusup,name="statusup"),
    path('statusup2/<int:booking_id>',views.statusup2,name="statusup2"),
    path('u_bookreq',views.u_bookreq),
    path('conf_bookreq',views.conf_bookreq),
    path('u_bookreq_cancel/<int:id>',views.u_bookreq_cancel),
    path('emp_status',views.emp_status),
    path('u_dis_bookings',views.u_dis_bookings),
    path('a_book_send/<int:id>/',views.a_book_send)









]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

