from django.db import models


# Create your models here.

class State(models.Model):
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
    is_deleted = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)

    def __str__(self):
        return self.name+" "+self.desc
        
    
class City(models.Model):
    state_id=models.ForeignKey(State,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
    is_deleted = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)

    def __str__(self):
        return self.name+" "+self.desc
     
class Area(models.Model):
    city_id=models.ForeignKey(City,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
    is_deleted = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)


    def __str__(self):
        return self.name+" "+self.desc
     
class User(models.Model):
    user_type=models.CharField(max_length=100,default="user")
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)    
    email=models.EmailField()    
    phone=models.CharField(max_length=300)
    address=models.CharField(max_length=300)
    state_id=models.ForeignKey(State,on_delete=models.PROTECT,null=True,blank=True)
    city_id=models.ForeignKey(City,on_delete=models.PROTECT,null=True,blank=True)
    area_id=models.ForeignKey(Area,on_delete=models.PROTECT,null=True,blank=True)
    is_deleted = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)

    def __str__(self):
        return self.name+" "+self.desc
