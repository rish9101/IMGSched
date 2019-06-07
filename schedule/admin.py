from django.contrib import admin
from .models import User, Users, MeetingsTable, CommentsTable
# Register your models here.

admin.site.register(User)
admin.site.register(Users)
admin.site.register(MeetingsTable)
admin.site.register(CommentsTable)
