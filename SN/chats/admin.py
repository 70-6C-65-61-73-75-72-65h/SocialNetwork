from django.contrib import admin
from .models import ChatUnion, Chat, Message

admin.site.register(ChatUnion)
admin.site.register(Chat)

class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(Message, MessageAdmin)

# Register your models here.
