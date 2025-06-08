# meetings/admin.py
from django.contrib import admin
from .models import Meeting, Subject, Owner, Comment

admin.site.register(Meeting)
admin.site.register(Subject)
admin.site.register(Owner)
admin.site.register(Comment)