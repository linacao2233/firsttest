from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
class VideoInline(admin.StackedInline):
	model = Videos

class ChapterInline(admin.StackedInline):
	model = Chapters

class SubjectAdmin(admin.ModelAdmin):
	inlines = [ChapterInline]
	search_fields = ['name', 'description']

class ChapterAdmin(admin.ModelAdmin):
	inlines = [VideoInline]
	search_fields = ['name']

admin.site.register(Subjects, SubjectAdmin)
admin.site.register(Videos)
admin.site.register(Chapters, ChapterAdmin)
