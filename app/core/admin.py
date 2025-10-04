from django.contrib import admin
from core.models import User, UserProfile, Session, Message

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Session)
admin.site.register(Message)
