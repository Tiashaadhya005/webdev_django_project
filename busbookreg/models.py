from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, TimeField
from django.core.exceptions import ValidationError
from svariable import *

# Create your models here.
class Bus_booking(models.Model):
    StartingLocation=CharField(max_length=30)
    EndLocation=CharField(max_length=30)
    Bus_book_tool=models.Manager()

    def __str__(self):
        return self.StartingLocation+"  "+self.EndLocation
    
    


