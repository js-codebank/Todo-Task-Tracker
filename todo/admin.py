from django.contrib import admin
from .models import TodoNote

#created by default is hidden, add it as read_only field
class TodoNoteAdmin(admin.ModelAdmin):
    fields= ('created','title','category','description','completed','user',)
    readonly_fields= ('created',)


admin.site.register(TodoNote, TodoNoteAdmin)

