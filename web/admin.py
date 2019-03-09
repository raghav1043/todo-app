from django.contrib import admin

# Register your models here.
from . import models

class TodoListAdmin(admin.ModelAdmin):
	list_display = ("title", "created", "due_date")


admin.site.register(models.TodoList, TodoListAdmin)