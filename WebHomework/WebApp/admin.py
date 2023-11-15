import django.contrib.admin
from django.contrib import admin

# Register your models here.
from .models import Answer, Tag, Question, Profile

admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Profile)