from django import forms

# from pagedown.widgets import PagedownWidget

from .models import Message, Chat
from accounts.models import Profile



#extend form https://stackoverflow.com/questions/2229039/django-modelform-with-extra-fields-that-are-not-in-the-model
# class ChatForm(forms.ModelForm): # for creation by other users ( using already created chatunion )

#     # people_in_chat = forms.ModelMultipleChoiceField(Profile.objects.all()) # profile.user.email

#     class Meta:
#         model = Chat
#         fields = (
#             # "people_in_chat",
#             "chat_name",
#         )


# # when we create chatunion (firstly created chat by 1 user for others)

# class ChatUnionForm(ChatForm): # not boundings to ChatUnion

#     people_in_chat = forms.ModelMultipleChoiceField(Profile.objects.all())

#     class Meta(ChatForm.Meta):
#         fields = ChatForm.Meta.fields + ('people_in_chat',)

class ChatUnionForm(forms.ModelForm): # not boundings to ChatUnion

    def __init__(self, *args, **kwargs):
        self.people_in_chat = kwargs.pop('people_in_chat', None)
        self.chat_name = kwargs.pop('chat_name', None)
        super().__init__(*args, **kwargs)

    people_in_chat = forms.ModelMultipleChoiceField(Profile.objects.all())

    class Meta:
        model = Chat
        fields = (
            # "people_in_chat",
            "chat_name",
        )


class MessageForm(forms.ModelForm):
    # content = forms.CharField(widget=PagedownWidget(attrs={"show_preview":False}))

    # content = forms.CharField(widget=PagedownWidget()) # show preview

    class Meta:
        model = Message
        fields = [
            "content",
            "image",
            # "sender",
        ]