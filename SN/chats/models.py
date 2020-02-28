from django.db import models
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify

# from django.contrib.postgres.fields import ArrayField


from markdown_deux import markdown
# from .utils import get_read_time


from sn_mixins import functions
from accounts.models import Profile


from datetime import timedelta, datetime
from django.db.models import Q
from django.db.models import Case, When

# just to gather all of related chats ( that doubled data for each user simultaniuosly )
class ChatUnion(models.Model):

    # people_in_chat = models.ManyToManyField(Profile, related_name='own_union_chats')

    # except self chats
    def get_related_chats(self, own_chat_instance):
        # own_chats_ids = own_chats.values_list('id', flat=True)
        # own_chat_id = own_chat_instance.values_list('id', flat=True)
        return self.relative_chats.exclude(id=own_chat_instance.id)
    

    def create_chats_for_relative_users(self, initiated_user, rel_profiles, chat_name):
        try:
            for prof in rel_profiles:
                if len(rel_profiles) > 1: # equals to if len(rel_profiles) > 1 - . cause chat_name cant be created for all ident if it not mult (it will be like user0_and_user1)
                    # mult
                    Chat.objects.create(chat_union=self, chat_owner=prof, chat_name=chat_name) 
                else: # if len(rel_profiles) == 1
                    # one-to-one
                    Chat.objects.create(chat_union=self, chat_owner=prof, chat_name=f'{initiated_user.slug}')#f'{prof.slug}_to_{initiated_user.slug}'
        except Exception as ex:
            print(f'ERROR in def create_chats_for_relative_users() details:\n{ex}\n')
            return False
        return True

    def copy_chat_msgs(self, own_chat_instance, m_i):
        """ message_instance === m_i """
        # print('00')
        # print(own_chat_instance)
        # print(m_i)
        # print(self.get_related_chats(own_chat_instance))
        # print('01')
        for chat in self.get_related_chats(own_chat_instance):
            Message.objects.create(content=m_i.content, image=m_i.image, sender=m_i.sender, chat=chat)
            

# # to create other user chats and add in C_U
# @receiver(post_save, sender=ChatUnion)
# def post_save_chatunion_receiver(sender, instance, created, *args, **kwargs):
#     """
#     Method pre_save receiver of Chat model to generate slug
#     """
    
#     if not instance.slug:
#         instance.slug = create_slug(instance)
  

# Chat.objects.sort_by_msgs(request.user)

class ChatManager(models.Manager):

    def undelete_chats(self, user):
        # print('Undele chats')
        own_chats = user.profile.own_chats.filter(deleted=True)
        [chat.check_undelete_chat() for chat in own_chats]

    def get_own_chats(self, user):
        self.undelete_chats(user)
        own_chats = user.profile.own_chats.filter(deleted=False)
        reduced_own_chats = list(filter(lambda elem: elem.msgs_exists, own_chats))
        chat_ids = [elem.id for elem in reduced_own_chats]
        return self.filter(id__in=chat_ids)

    def sort_by_msgs(self, user):
        """ Sorted chats query by newest messages """
        own_chats = self.get_own_chats(user)
        # for chat in own_chats:
        chat_id_and_last_msg_date = [[chat.id, chat.last_created_msg.created] for chat in own_chats]
        sorted_chats = sorted(chat_id_and_last_msg_date, key=lambda l:l[1], reverse=True) # list of lists
        sorted_chats = [chat[0] for chat in sorted_chats]# ids of chats

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(sorted_chats)])
        queryset = self.filter(pk__in=sorted_chats).order_by(preserved)

        return queryset

class Chat(models.Model):
    # relative_chats_common_id = ArrayField(models.IntegerField(), blank=True)
    chat_union = models.ForeignKey(ChatUnion, on_delete=models.CASCADE, related_name='relative_chats')
    # people_in_chat = models.ManyToManyField(Profile, related_name='own_chats')
    chat_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='own_chats')
    chat_name = models.TextField()
    # topic = models.CharField(max_length=60, default='Nothing') # 2
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    deleted = models.BooleanField(default=False)

    objects = ChatManager()

    # chat_image = models.ImageField(upload_to=functions.upload_location, \
    #     null=True, \
    #     blank=True, \
    #     width_field="width_field", \
    #     height_field="height_field")
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)


    # new_messages = models.IntegerField(default=0)#( unreaded yet )

    def delete_chat(self):
        try:
            self.deleted = True

            self.get_inner_msgs.delete()
            
            self.save()

            return True
        except Exception as ex:
            print(f'\n\nError in Chat.delete_chat:\n {ex}')
            return False

    def check_undelete_chat(self):
        if self.deleted == True and self.count_new_messages > 0:
            self.deleted = False
            self.save()
        

    def __str__(self):
        return f'chat {self.slug}'


    @property
    def read_new_messages(self): # num of new messages
        # self.new_messages = self.get_inner_msgs.filter(readed=False).count()
        # return self.new_messages
        try:
            self.get_inner_msgs.filter(readed=False).update(readed=True)
            return True
        except Exception as ex:
            print(f'\nError Chat.read_new_messages:\n {ex}')
            return None


    @property
    def count_new_messages(self): # num of new messages
        # self.new_messages = self.get_inner_msgs.filter(readed=False).count()
        # return self.new_messages
        return self.get_inner_msgs.filter(readed=False).count()

    @property
    def create_msg(self):
        return reverse("chats:message_create", kwargs={"slug": self.slug})  # chat slug
        # return Message.objects.create(chat=self, sender=self.chat_owner, image=image)

    @property
    def get_inner_msgs(self):
        return self.inner_msgs.all()#.select_related('inner_msgs')

    @property
    def msgs_exists(self):
        return True if self.get_inner_msgs.count() > 0 else False

    @property
    def last_created_msg(self):
        return self.get_inner_msgs.order_by('created').last()


    # @property
    # def last_updated_msg(self):
    #     return self.get_inner_msgs.order_by('-updated').first()
    
    @property
    def get_absolute_url(self):
        """built-in method to get url of Chat object"""
        return reverse("chats:chat_detail", kwargs={"slug": self.slug})

    @property
    def get_delete_url(self):
        """built-in method to get delete url of Chat object"""
        return reverse("chats:chat_delete", kwargs={"slug": self.slug})

    # @classmethod
    # def get_user_msgs(cls, user):
    #     return cls.objects.filter(Q(sender__user=user)|
	# 					Q(receivers__user=user))

    # def sort_by_inner_msgs(self):
    #     self.get_inner_msgs.order_by('created').last()

    class Meta:
        ordering = ["-created"] #  "-updated"
        
# Create your models here.
class Message(models.Model):
    """ Main model of Chat for the SN """
    # receivers = models.ManyToManyField(Profile, related_name='received_messages')#, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sended_msgs') # TODO delete duplication ( there and in owner in CHAT)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='inner_msgs')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # read_time = models.IntegerField(default=0)
    image = models.ImageField(upload_to=functions.upload_location, \
        null=True, \
        blank=True, \
        width_field="width_field", \
        height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    readed = models.BooleanField(default=False)


    def is_msg_updated(self):
        return True if self.updated != self.created else False

    def __str__(self):
        return f'message {self.id}'

    # @property
    # def get_receivers(self):
    #     return self.receivers.all()

    # @property
    # def get_absolute_url(self):
    #     """built-in method to get url of message object"""
    #     return reverse("chats:message_detail", kwargs={"id": self.id})

    @property
    def get_delete_url(self):
        """built-in method to get delete url of message object"""
        return reverse("chats:message_delete", kwargs={"id": self.id})
        

    def get_markdown(self):
        """
        change content field to appropriate
        html display using markdown lib
        """
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    class Meta:
        ordering = ["created"] # "-updated"
        


def create_slug(instance, new_slug=None):
    """ create slug to url, from title or title with adding to it the id"""
    print(f'\n\nChat inst:\n{instance}')
    print(f'\n\nChat inst name:\n{instance.__dict__}')
    slug = slugify(instance.chat_name)
    if new_slug is not None:
        slug = new_slug
    qs = Chat.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    print(f'\n\nChat inst slug:\n{slug}')
    return slug


@receiver(pre_save, sender=Chat)
def pre_save_chat_receiver(sender, instance, *args, **kwargs):
    """
    Method pre_save receiver of Chat model to generate slug
    """
    # print(f'\n\ninstance.slug{instance.slug}')
    print(instance)
    if not instance.slug:
        instance.slug = create_slug(instance)

#if not hasattr(instance, "purchase"):