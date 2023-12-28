from django.contrib import admin

from .models import CodeSample, Comment


admin.site.register(CodeSample)
admin.site.register(Comment)
