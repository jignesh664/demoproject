from django.db import models


# Create your models here.

class State(models.Model):
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)

    def __str__(self):
        return self.name+" "+self.desc
        
    
class City(models.Model):
    state_id=models.ForeignKey(State,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)

    def __str__(self):
        return self.name+" "+self.desc
     
class Area(models.Model):
    city_id=models.ForeignKey(City,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)

    def __str__(self):
        return self.name+" "+self.desc
     
class User(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)    
    email=models.EmailField()    
    phone=models.CharField(max_length=300)
    address=models.CharField(max_length=300)
    state_id=models.ForeignKey(State,on_delete=models.CASCADE)
    city_id=models.ForeignKey(City,on_delete=models.CASCADE)
    area_id=models.ForeignKey(Area,on_delete=models.CASCADE)

    def __str__(self):
        return self.name+" "+self.desc
