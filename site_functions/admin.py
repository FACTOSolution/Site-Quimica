from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Minicurso)
admin.site.register(Article)


"""
user: superuser
password: pass1234
"""
