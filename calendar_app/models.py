import random
import string

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


User = get_user_model()

class Group(models.Model):
    name   = models.CharField(unique=True , max_length=255)
    code   = models.CharField(max_length=255 , null= True , blank= True)
    user   = models.ManyToManyField(User )
    slug   = models.SlugField(unique=True , null= True , blank=True)

    def save(self, *args , **kwargs):
        self.code  = id_generator()
        self.slug = slugify(self.name)
        super().save(*args , **kwargs)

    def __str__(self):
        return self.name

 

 
class Event(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    title         = models.CharField(max_length=200)
    description   = models.TextField()
    date          = models.DateField()
    start_time    = models.TimeField()
    end_time      = models.TimeField()
    created_date  = models.DateTimeField(auto_now_add=True)
    group        = models.ForeignKey(Group , on_delete= models.CASCADE , null= True , blank=True)
    priority        = models.ForeignKey('Priority' , on_delete= models.CASCADE , null= True , blank=True)

    class Meta:
        unique_together = ('start_time', 'end_time',)
  

    
    @property
    def get_html_url(self):
        url = reverse('event-detail', args=(self.id,))
        return f' <a href="{url}"> {self.title} </a>'

    def create_event(slef):
        return f"http://localhost:800/event/create/"

    # def get_event_in_current_date(self):
    #     # print(Event.objects.filter(date= self.date))
    #     return Event.objects.filter(date= self.date)
    @property
    def get_all_events(self):
        if Event.objects.filter(date= self.date).count() >1:
            url = reverse('event-all', args=(self.date, ))
            return f' <a href="{url}"> ... </a>'
        return ""

    @property
    def get_all_events_by_group(self):
        print(self.group)
        if Event.objects.filter(date= self.date , group= self.group ).count() >1:
            url = reverse('event-all-group', args=(self.date, self.group.name ))
            return f' <a href="{url}"> ... </a>'
        return ""



    def __str__(self):
        # print(self.date)
        return str(self.date)


class  Priority(models.Model):
    scale   = models.IntegerField()

    def __str__(self):
        return f"{self.scale}"