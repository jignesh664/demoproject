from django.db import models


# Create your models here.

class State(models.Model):
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
    is_deleted = models.IntegerField(default=1)
    is_active = models.CharField(max_length=300,default="inactive")

    def __str__(self):
        return self.name+" "+self.desc
        
    
class City(models.Model):
    state_id=models.ForeignKey(State,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
    is_deleted = models.IntegerField(default=1)
    is_active = models.CharField(max_length=300,default="inactive")
    def __str__(self):
        return self.name+" "+self.desc
     
class Area(models.Model):
    city_id=models.ForeignKey(City,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
    is_deleted = models.IntegerField(default=1)
    is_active = models.CharField(max_length=300,default="inactive")

    def __str__(self):
        return self.name+" "+self.desc
     
class User(models.Model):
    user_type=models.CharField(max_length=100)
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)    
    email=models.EmailField()    
    phone=models.CharField(max_length=300)
    address=models.CharField(max_length=300)
    state_id=models.ForeignKey(State,on_delete=models.PROTECT,null=True,blank=True)
    city_id=models.ForeignKey(City,on_delete=models.PROTECT,null=True,blank=True)
    area_id=models.ForeignKey(Area,on_delete=models.PROTECT,null=True,blank=True)
    is_deleted = models.IntegerField(default=1)
    is_active = models.CharField(max_length=300,default="inactive")
    is_login=models.BooleanField(default=False)



    def __str__(self):
        return self.name+" "+self.desc


class Customer(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=8)
    mobile=models.CharField(max_length=13)
    address=models.TextField()
    date=models.DateField()
    state=models.CharField(max_length=100,default='')
    city=models.CharField(max_length=100,default='')
    is_active=models.BooleanField(default=False)


    def __str__(self):
        return self.fname+" "+self.lname

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    product_model=models.CharField(max_length=100)
    product_price=models.CharField(max_length=100)
    product_model_year=models.CharField(max_length=100)
    product_color=models.CharField(max_length=100)
    date=models.DateField()   

    def __str__(self):
        return self.product_name+" "+self.product_model

class Order(models.Model):
    customer_id=models.ForeignKey(Customer,on_delete=models.PROTECT,null=True,blank=True)
    product_id=models.ForeignKey(Product,on_delete=models.PROTECT,null=True,blank=True)
    order_date=models.DateField() 
    order_number=models.CharField(max_length=100)
    order_price=models.CharField(max_length=100)

    def __str__(self):
        return self.order_price+" "+self.order_number



