from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    EVENT_TYPES = (
        ('Concert', 'Concert'),
        ('Workshop', 'Workshop'),
        ('Sport', 'Sport'),
        ('Theatre', 'Theatre'),
    )
    
    TYPE_COLORS = {
        'Concert': '#582BAC',
        'Workshop': '#B31A4D',
        'Sport': '#E48E2C',
        'Theatre': '#4A920F',
    }

    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=EVENT_TYPES)
    image = models.ImageField(upload_to='event_images/')
    time = models.DateTimeField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_type_color(self):
        return self.TYPE_COLORS.get(self.type, '#000000')  # Default color if type not found

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')


class UserAction(models.Model):
    ACTION_TYPES = (
        ('like', 'Like'),
        ('share_whatsapp', 'Share on WhatsApp'),
        ('share_twitter', 'Share on Twitter'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
