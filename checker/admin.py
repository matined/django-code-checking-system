from django.contrib import admin

from .models import Language, CodeSample, Note


admin.site.register(Language)
admin.site.register(CodeSample)
admin.site.register(Note)
