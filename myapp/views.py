
import json
from django.db.models.fields import related
from django.http import request
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import State,City,Area,User

from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# for flash massages
from django.contrib import messages


# Create your views here.
def dashboard(request):
    return render(request,'dashboard.html')

def user_profile(request):
    return render(request,'user_profile.html')


def state(request):
    allStates = State.objects.filter(is_deleted=1)
    params = {"allStates": allStates}
    return render(request,'state/state.html', params)       

def add_state(request):
    if request.method=="POST":
        try:
            active_status = "active" if request.POST['is_active'] == 'on' else "deactive"
        except Exception as e:
            active_status = "deactive"
        s = State()
        s.name = request.POST['name']
        s.desc = request.POST['desc']
        s.is_active=active_status
        s.save()
        # State.objects.create(
        #     name=request.POST['name'],
        #     desc=request.POST['desc']
        #     )
        msg="Your State Added Successfully"
        # state=State.objects.all()
        # print(state, "All States..")
        #return redirect('/')
        return render(request,'state/add_state.html',{'state':state,'msg':msg})
    else:
        return render(request,'state/add_state.html')    

def edit_state(request,state_id = None):
    if request.method=="POST":
        s=State.objects.get(id=request.POST['state_id'],is_deleted = 1)
        s.name=request.POST['name']
        s.desc=request.POST['desc']
        s.save()
        msg="Your State Updated Successfully"
        return redirect('/state',{'msg':msg})
    else:
        s=State.objects.get(id=state_id,is_deleted = 1)
        params = {'state': s}
        return render(request,'state/edit_state.html', params) 
        
def delete_state(request, st_id):
    s=State.objects.get(id=st_id)
    s.is_deleted=0
    s.save()
    return redirect('/state')




def city(request):
    allcitys=City.objects.filter(is_deleted=1)
    params={'allcitys': allcitys}
    return render(request,'city/city.html', params)  
    
@csrf_exempt
def change_status_city(request):
    if request.method == "POST":
        city = City.objects.get(id=request.POST['is_active'])
        active_status = "active" if request.POST['checked'] == 'true' else "deactive"
        city.is_active=active_status
        city.save()
        return JsonResponse({'success': True, 'message': 'Update Changed.'}, safe=False)
    else:
        return JsonResponse({'success': False, 'message': 'Something went wrong.!'}, safe=False)




def add_city(request):
    if request.method == "POST":
        try:
            active_status = "active" if request.POST['is_active'] == 'on' else "deactive"
        except Exception as e:
            active_status = "deactive"

        c = City()
        c.state_id = State.objects.get(id=request.POST['state_id'])
        c.name = request.POST['name']
        c.desc = request.POST['desc']
        c.is_active=active_status
        c.save()
        
        return redirect('/city')
    else:
        allStates = State.objects.all()
        allcitys=City.objects.all()
        parmas = {'allStates': allStates,'allcitys':allcitys}
        return render(request,'city/add_city.html', parmas) 


def edit_city(request,city_id=None):
    if request.method=="POST":
        c=City.objects.get(id=request.POST['city_id'],is_deleted = 1)
        c.name=request.POST['name']
        c.desc=request.POST['desc']
        c.save()
        return redirect('/city')
    else:
        c=City.objects.get(id=city_id,is_deleted = 1)
        params={'city':c}
        return render(request,'city/edit_city.html',params)


def delete_city(request,ct_id):
    c=City.objects.get(id=ct_id)
    c.is_deleted=0
    c.save()
    return redirect('/city')


def area(request):
    allareas=Area.objects.filter(is_deleted=1)
    params={'allareas':allareas}
    return render(request,'area/area.html',params)  

def add_area(request):
    if request.method=="POST":
        try:
            active_status="active" if request.POST['is_active'] == 'on' else "deactive"
        except Exception as e:
            active_status="deactive"
        a=Area()
        a.city_id=City.objects.get(id=request.POST['city_id'])
        a.name=request.POST['name']
        a.desc=request.POST['desc']
        a.is_active=active_status
        a.save()
        return redirect('/area')
    else:
        allcitys=City.objects.all()
        params={'allcitys':allcitys}   
        return render(request,'area/add_area.html',params)   


def edit_area(request,area_id=None):     
    if request.method=="POST":
        a=Area.objects.get(id=request.POST['area_id'],is_deleted = 1)
        a.name=request.POST['name']
        a.desc=request.POST['desc']
        a.save()
        return redirect('/area')
    else:
        a=Area.objects.get(id=area_id,is_deleted = 1)
        params={'area':a}
        return render(request,'area/edit_area.html',params)

def delete_area(request,at_id):
    a=Area.objects.get(id=at_id)
    a.is_deleted=0
    a.save()
    return redirect('/area')


def user(request):
    allusers=User.objects.filter(is_deleted = 1)
    params={'allusers':allusers}
    return render(request,'user/user.html',params)  
   

def add_user(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="This Email already Registred.."
            return render(request,'user/add_user.html',{'msg':msg}) 
        except User.DoesNotExist as ex:    
            u=User()
            u.fname = request.POST['fname']
            u.lname = request.POST['lname']
            u.email= request.POST['email']
            u.phone = request.POST['phone']
            u.address = request.POST['address']
            u.user_type = request.POST['user_type']
            u.state_id = State.objects.get(id = request.POST['state_id'])
            u.city_id = City.objects.get(id = request.POST['city_id'])
            u.area_id = Area.objects.get(id = request.POST['area_id'])
            if(request.POST['is_active'] == 'on'):
                u.is_active="active"
            else:
                u.is_active="deactive"
            u.save()
            return redirect('/user')
    else:
        allStates = State.objects.all()
        allcitys=City.objects.all()
        allareas=Area.objects.all()
        parmas = {'allStates': allStates,'allcitys':allcitys,'allareas':allareas}
        return render(request,'user/add_user.html', parmas) 


def edit_user(request,user_id=None): 
    if request.method=="POST":
        u=User.objects.get(id=request.POST['user_id'], is_deleted = 1)
        u.fname=request.POST['fname']
        u.lname=request.POST['lname']
        u.email=request.POST['email']
        u.phone=request.POST['phone']
        u.address=request.POST['address']
        u.user_type = request.POST['user_type']
        u.state_id = State.objects.get(id = request.POST['state_id'])
        u.city_id = City.objects.get(id = request.POST['city_id'])
        u.area_id = Area.objects.get(id = request.POST['area_id'])
        u.save()
        messages.success(request, "Success: This is the sample success Flash message.")
        return redirect('/user')
    else:
        u=User.objects.get(id=user_id, is_deleted = 1)
        allStates=State.objects.all()
        allcitys=City.objects.all()
        allareas=Area.objects.all()
        params={'user':u,'allStates': allStates,'allcitys':allcitys,'allareas':allareas}
        return render(request,'user/edit_user.html',params)  

def delete_user(request,ur_id):
    d=User.objects.get(id=ur_id)
    #soft delete
    d.is_deleted=0
    d.save()
    return redirect('/user')
    #d.delete()
    
@csrf_exempt 
def getcity(request):
    if request.method=="POST":
        gtstate=State.objects.get(id=request.POST['state_id'])
        gtcity=City.objects.filter(state_id=gtstate.id)
        #create list of all city data
        finalCitys = []  
        for i in gtcity:
            finalCitys.append({'name': i.name, 'id': i.id})  
        return JsonResponse({'status':'save','finalCitys':finalCitys}, safe = False)  
        #return JsonResponse(serializers.serialize('json', gtcity), safe = False)
    else:
        return JsonResponse({'status':0})


@csrf_exempt
def getarea(request):
    if request.method=="POST":
        gtcity=City.objects.get(id=request.POST['city_id'])
        gtarea=Area.objects.filter(city_id=gtcity.id)

        finalarea = []
        for i in gtarea:
            finalarea.append({'name':i.name,'id':i.id})
        return JsonResponse({'status':'save','finalarea':finalarea}, safe=False)
    else:
        return JsonResponse({'status':0})
    
    

        
        
        
       
        










    