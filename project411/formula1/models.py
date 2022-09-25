from django.db import models
import datetime
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('media/', filename)




# Create your models here.
class driver(models.Model):
    driver_id = models.CharField(max_length=50 )
    driver_name = models.CharField(max_length=50 )
    sex = models.CharField(max_length=10)
    age = models.CharField(max_length=4)
    country = models.CharField(max_length=50)
    total_points = models.CharField(max_length=5)
    team_team_id = models.CharField(max_length=50)
    image = models.ImageField(upload_to=filepath, null=True, blank=True,default='media/default.jpg')
    class Meta: 
        db_table ="driver"


class team(models.Model):
    team_id= models.CharField(max_length=50)
    team_name = models.CharField(max_length=20)
    base = models.CharField(max_length=20)
    pole_position = models.CharField (max_length=20)
    world_championship = models.CharField(max_length=20)
    image = models.ImageField(upload_to=filepath, null=True, blank=True,default='media/default.png')
    class Meta:
        db_table = "team"

class  merch (models.Model):
     product_id = models.CharField(max_length=20)
     category= models.CharField(max_length=30)
     size= models.CharField(max_length=20)
     price =models.CharField(max_length=5)
     quantity = models.CharField(max_length=10)
     team_id = models.CharField(max_length=50)
     image = models.ImageField(upload_to=filepath, null=True, blank=True,default='media/default.png')
     class Meta:
         db_table ="merch" 
    

class circuit (models.Model):
    circuit_serial= models.CharField(max_length=50)
    circuit_name = models.CharField(max_length=30)
    circuit_location= models.CharField(max_length=30)
    circuit_length= models.CharField(max_length=3)
    circuit_description = models.CharField(max_length=10000)
    image = models.ImageField(upload_to=filepath, null=True, blank=True,default='media/default.png')
    class Meta:
        db_table ="circuit"

class users (models.Model):
    user_id= models.CharField(max_length=50)
    user_name= models.CharField(max_length=50)
    user_email=models.CharField(max_length=50)
    user_password = models.CharField(max_length=30)
    user_phone =models.CharField(max_length=20)
    rank = models.CharField(max_length=20)
    class Meta:
        db_table = "users" 

class schedule (models.Model):
    schedule_id = models.CharField(max_length=50)
    schedule_name = models.CharField(max_length=30)
    duration = models.CharField(max_length=100)
    schedule_date =models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    circuit_serial = models.CharField(max_length=50)
    class Meta:
        db_table = "schedule"

class standings (models.Model):
    standing_id =models.CharField(max_length=50)
    time = models.CharField(max_length=30)
    avg_speeds = models.CharField(max_length=30)
    laps= models.CharField(max_length=5)
    points = models.CharField(max_length=5)
    driver_id= models.CharField(max_length=50)
    schedule_id = models.CharField(max_length=50)
    class Meta:
        db_table ="standings" 
    
class participation(models.Model):
    team_id = models.CharField(max_length=50)
    schedule_id = models.CharField(max_length=50)
    class Meta:
        db_table="participation"

class ticket(models.Model):
    ticket_id = models.CharField(max_length=50)
    type= models.CharField(max_length=30)
    price= models.CharField(max_length=5)
    schedule_id = models.CharField(max_length=50)
    class Meta:
        db_table="ticket"

