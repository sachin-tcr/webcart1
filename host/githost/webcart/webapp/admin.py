from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(register)
admin.site.register(emp_reg)
admin.site.register(w_categories)
admin.site.register(verify_emp)
admin.site.register(u_review)
admin.site.register(PasswordReset)
admin.site.register(block_employee)
admin.site.register(bookings)
admin.site.register(adminpassbookings)
admin.site.register(booked)
