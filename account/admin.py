from django.contrib import admin
from account.models import CustomUser, Debit


admin.site.register(CustomUser)
admin.site.register(Debit)