from django.db import models
from django_mysql.models import ListCharField
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from tags.signal import parsed_tags
from django.conf import settings


# Create your models here.

class HallManager(models.Manager):
    def savehall(self,user,parent_obj):
        qs = self.get_queryset().filter(user=user,parent=parent_obj)
        if qs.exists():
            return None
        obj = self.model(
            parent = parent_obj,
            user = user,
            title = parent_obj.title,
            tags = parent_obj.tags
        )
        obj.save()

        return obj
    
    def save_toggle(self, user, hall_obj):
        if user in hall_obj.saved.all():
            print("saved")
            is_liked = True
            hall_obj.saved.remove(user)
        else:
            is_liked = False
            print("unsaved")
            hall_obj.saved.add(user)
        return is_liked


class Hall(models.Model):
    parent = models.ForeignKey("self",blank=True,null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_halls')
    saved = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='saved')
    # tags = ListCharField(
    #     base_field=models.CharField(max_length=20),
    #     blank=True,
    #     size=5,
    #     max_length=(5 * 21)  # 6 * 10 character nominals, plus commas
    # )
    tags = models.CharField(max_length=255, blank=True)

    objects = HallManager()
    def __str__(self):
        return self.title

# def hall_save_receiver2(sender, instance, *args, **kwargs):
#         instance.tags = instance.tags.split(",")

# pre_save.connect(hall_save_receiver2, sender = Hall)  

def hall_save_receiver(sender, instance, created, *args, **kwargs):
    # if created:
    parsed_tags.send(sender=instance.__class__,tags_list=instance.tags.split(","))

post_save.connect(hall_save_receiver, sender = Hall)  




    

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    hall = models.ForeignKey(Hall,related_name='videos',on_delete=models.CASCADE)



