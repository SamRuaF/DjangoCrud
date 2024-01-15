from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True) #Si no me pasan nada el campo va a estar vacio
    created = models.DateTimeField(auto_now_add= True) #Fecha y hora
    datecompleted = models.DateTimeField(null = True, blank = True) 
    important = models.BooleanField(default = False) #Por defecto no todas las tareas son importantes
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title + '- by ' + self.user.username


