from django.db import models
from django.urls import reverse_lazy
from .signal import parsed_tags
from django.db.models.signals import pre_save
from halls.models import Hall
# Create your models here.
class Tags(models.Model):
    tag = models.CharField(max_length=20, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    tagTimes = models.IntegerField(blank=True)

    def __str__(self):
        return self.tag
    
    def get_halls(self):
        return Hall.objects.filter(tags__icontains=self.tag)
        # query_tag=self.tag
        # print(self.tag)
        # return Hall.objects.extra(where=['FIND_IN_SET(tags,dfd)'])


def parsed_tags_receiver(sender, tags_list, *args, **kwargs):
    if len(tags_list)>0:
        for tag_var in tags_list:
            new_tag, create = Tags.objects.get_or_create(tag=tag_var)

parsed_tags.connect(parsed_tags_receiver)


def tag_save_receiver(sender, instance, *args, **kwargs):
        instance.tagTimes = len(instance.get_halls())

pre_save.connect(tag_save_receiver, sender = Tags)  