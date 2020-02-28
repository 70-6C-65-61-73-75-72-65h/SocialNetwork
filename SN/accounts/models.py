""" Use main django-framework libs """
from django.db import models

from django.conf import settings

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdown_deux import markdown
# Create your models here.

from sn_mixins import functions

class Profile(models.Model): # user.date_joined - date of registration
    """ Model relative to each User model that have some add-in fields """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=functions.upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __str__(self):
        return f'profile {self.user.username}'

    # i dont need to do (reverse_lazy) cause it function and not an class attribute/ so i can use (reverse) 
    @property
    def get_chat_url(self):
        """built-in method to get delete url of Profile object"""
        return reverse("chats:chat_create")#, kwargs={"slug": self.slug}) # , "auto": 1


    @property
    def get_absolute_url(self):
        """built-in method to get url of Profile object"""
        return reverse("accounts:profile", kwargs={"slug": self.slug})

    @property
    def get_delete_url(self):
        """built-in method to get delete url of Profile object"""
        return reverse("accounts:delete", kwargs={"slug": self.slug})

    @property
    def get_update_url(self):
        """
        built-in method to get url of updating self
        account info for Profile model
        """
        return reverse("accounts:update", kwargs={"slug": self.slug})

    @property
    def get_password_reset(self):
        """
        built-in method to get url of updating self
        password for Profile model
        """
        return reverse("password_reset:password_reset_recover")

    def get_markdown(self):
        """
        change content field to appropriate
        html display using markdown lib
        """
        content = self.bio
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    class Meta:
        ordering = ["-user__date_joined"]


def create_slug(instance, new_slug=None):
    """ create slug to url, from title or title with adding to it the id"""
    slug = slugify(instance.user.username)
    if new_slug is not None:
        slug = new_slug
    qs = Profile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


# creation slug right before PROFILE creation
@receiver(pre_save, sender=Profile)
def pre_save_profile_receiver(sender, instance, *args, **kwargs):
    """
    Method pre_save receiver of Profile model to generate
    slug
    """
    if not instance.slug:
        slug = create_slug(instance)

        instance.slug = slug


# creation profile right after USER creation
@receiver(post_save, sender=User)
def update_create_user_profile(instance, created, *args, **kwargs):
    """
    Method post_save receiver of User model to create
    Profile relative model
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()