
import json
from django.db import connection, reset_queries
from django.db.models import query
from django.db.models.fields import related
from django.http import request
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import State,City,Area,User,Customer,Order,Product

from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# for flash massages
from django.contrib import messages

# for check session first only chech_session function call
from mysite.project_session import check_session

# for check all as per requirnment function call
# from mysite.project_session import *

from django.views.decorators.cache import cache_control

def runsql(q):
    cursor=connection.cursor()
    cursor.execute(q)
    if (cursor.description!=None):
        columns=[col [0] for  col in cursor.description]
        return[
            dict(zip(columns,row))
            for row in cursor.fetchall()
        ]
    else:
        return True    


@csrf_exempt
@check_session
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def dashboard(request):
    c=Customer.objects.all()
    o=Order.objects.all()
    # for remove dublicates values add distinct() method
    records = Customer.objects.filter().values('state').distinct()
    records = [x['state'] for x in records]
    #citys =Customer.objects.filter().values('city')
    #citys=[y['city'] for y in citys]
    #print(records)
    params={'c':c,'o':o,'records': records}
    return render (request,'dashboard.html',params)


@csrf_exempt
def get_city(request):
    if request.method=="POST":
        allconditions=""
        city=request.POST.getlist('state[]')
        #print(city)
        finalcity=str(tuple(city)) if len(city) > 1 else str(tuple(city)).replace(',','') 
        if (city):
            allconditions +=f" AND state in {finalcity}"
        querys=f"SELECT DISTINCT city FROM myapp_customer WHERE 1 = 1 {allconditions};"
        data=runsql(querys)
        #print(data)
        return JsonResponse({'status':'save','data':data},safe=False)
    else:
        return JsonResponse({'status':0,})  



@csrf_exempt
def get_data(request):
    if request.method=="POST":
        allconditions=""
        state=request.POST.getlist('state[]')
       
        finalstate=str(tuple(state)) if len(state) > 1 else str(tuple(state)).replace(',','')
        if (state):
            allconditions +=f" AND c.state in {finalstate}"

        city=request.POST.getlist('city[]')
        finalcity=str(tuple(city)) if len(city) > 1 else str(tuple(city)).replace(',','')
        if (city):
            allconditions +=f"AND c.city in {finalcity}"

        tdate=request.POST['tdate']    
        date=request.POST['fdate']
        if (date):
            allconditions+=f"AND DATE(c.date) BETWEEN DATE('{date}') AND DATE ('{tdate}')"


        querys=f"select c.fname, c.mobile, c.state, c.city, o.order_number, o.order_date, o.order_price, p.product_name, p.product_price from myapp_customer  as c  LEFT JOIN myapp_order as o ON c.id=o.id LEFT JOIN myapp_product as p ON p.id=c.id  WHERE 1 = 1 {allconditions} ORDER BY c.state ASC;"
        data=runsql(querys) 
        return JsonResponse({'status':'save','data':data},safe=False)
    else:
        return JsonResponse({'status':0})    



@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)            
def user_profile(request):
    return render(request,'user_profile.html')

   
@check_session  
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True) 
def state(request):
    allStates = State.objects.filter(is_deleted=1)
    params = {"allStates": allStates}
    return render(request,'state/state.html', params)   


@csrf_exempt
@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)  
def change_status_state(request):
    if request.method == "POST":
        state = State.objects.get(id=request.POST['is_active'])
        active_status = "active" if request.POST['checked'] == 'true' else "deactive"
        print(active_status)
        state.is_active=active_status
        state.save()
        return JsonResponse({'success': True, 'message': 'Update Changed.'}, safe=False)
    else:
        return JsonResponse({'success': False, 'message': 'Something went wrong.!'}, safe=False)
    

@check_session  
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True) 
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
        messages.add_message(request, messages.SUCCESS,"State added successfully.")
        # state=State.objects.all()
        # print(state, "All States..")
        #return redirect('/')
        return redirect('/state')
    else:
        return render(request,'state/add_state.html') 
                 

@check_session  
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True) 
def edit_state(request,state_id = None):
    if request.method=="POST":
        s=State.objects.get(id=request.POST['state_id'],is_deleted = 1)
        s.name=request.POST['name']
        s.desc=request.POST['desc']
        s.save()
        messages.add_message(request, messages.SUCCESS,"State Edit successfully.")
        return redirect('/state')
    else:
        s=State.objects.get(id=state_id,is_deleted = 1)
        params = {'state': s}
        return render(request,'state/edit_state.html', params) 
    

@check_session  
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True) 
def delete_state(request, st_id):
    s=State.objects.get(id=st_id)
    s.is_deleted=0
    s.save()
    messages.add_message(request, messages.WARNING,"State Delete successfully.")
    return redirect('/state')
    

@check_session  
def city(request):
    allcitys=City.objects.filter(is_deleted=1)
    params={'allcitys': allcitys}
    return render(request,'city/city.html', params)  
   
  
@csrf_exempt
@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)  
def change_status_city(request):
    if request.method == "POST":
        city = City.objects.get(id=request.POST['is_active'])
        active_status = "active" if request.POST['checked'] == 'true' else "deactive"
        city.is_active=active_status
        city.save()
        return JsonResponse({'success': True, 'message': 'Update Changed.'}, safe=False)
    else:
        return JsonResponse({'success': False, 'message': 'Something went wrong.!'}, safe=False)



@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)  
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
        messages.add_message(request, messages.SUCCESS, "City Added Successfully !!")
        return redirect('/city')
    else:
        allStates = State.objects.all()
        allcitys=City.objects.all()
        parmas = {'allStates': allStates,'allcitys':allcitys}
        return render(request,'city/add_city.html', parmas) 
    

@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)  
def edit_city(request,city_id=None):
    if request.method=="POST":
        c=City.objects.get(id=request.POST['city_id'],is_deleted = 1)
        c.name=request.POST['name']
        c.desc=request.POST['desc']
        c.save()
        messages.add_message(request, messages.SUCCESS,"City Edit successfully!!")
        return redirect('/city')
    else:
        c=City.objects.get(id=city_id,is_deleted = 1)
        params={'city':c}
        return render(request,'city/edit_city.html',params)


@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)  
def delete_city(request,ct_id):
    c=City.objects.get(id=ct_id)
    c.is_deleted=0
    c.save()
    messages.add_message(request, messages.WARNING,"City Delete successfully.")
    return redirect('/city')
   

@check_session
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)   
def area(request):
    allareas=Area.objects.filter(is_deleted=1)
    params={'allareas':allareas}
    return render(request,'area/area.html',params) 


@csrf_exempt
@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)  
def change_status_area(request):
    if request.method == "POST":
        area = Area.objects.get(id=request.POST['is_active'])
        active_status = "active" if request.POST['checked'] == 'true' else "deactive"
        area.is_active=active_status
        area.save()
        return JsonResponse({'success': True, 'message': 'Update Changed.'}, safe=False)
    else:
        return JsonResponse({'success': False, 'message': 'Something went wrong.!'}, safe=False)


@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)  
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
        messages.add_message(request, messages.SUCCESS,"Area added successfully.")
        return redirect('/area')
    else:
        allcitys=City.objects.all()
        params={'allcitys':allcitys}   
        return render(request,'area/add_area.html',params)   


@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)  
def edit_area(request,area_id=None): 
    if request.method=="POST":
        a=Area.objects.get(id=request.POST['area_id'],is_deleted = 1)
        a.name=request.POST['name']
        a.desc=request.POST['desc']
        a.save()
        messages.add_message(request, messages.SUCCESS,"Area Edit successfully.")
        return redirect('/area')
    else:
        a=Area.objects.get(id=area_id,is_deleted = 1)
        params={'area':a}
        return render(request,'area/edit_area.html',params)




@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)  
def delete_area(request,at_id):
    a=Area.objects.get(id=at_id)
    a.is_deleted=0
    a.save()
    messages.add_message(request, messages.WARNING,"Area Delete successfully.")
    return redirect('/area')
     

@check_session  
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True) 
def user(request):
    allusers=User.objects.filter(is_deleted = 1)
    params={'allusers':allusers}
    return render(request,'user/user.html',params)  


@csrf_exempt
@check_session 
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)   
def change_status_user(request):
    if request.method=="POST":
        user=User.objects.get(id=request.POST['is_active'])
        active_status="active"  if request.POST['checked'] == 'true'  else "deactive"
        user.is_active=active_status
        user.save()
        return JsonResponse({'success': True ,'massage':'Updated Successfully !'},safe=False)
    else:
        return JsonResponse({'success': False , 'massage':'something went wrong'},safe=False)
       

@check_session
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)   
def add_user(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            messages.success(request, "User Email is already Registred !! Please use another.")
            return render(request,'user/add_user.html') 
        except User.DoesNotExist as ex:    
            u=User()
            u.fname = request.POST['fname']
            print(u.fname)
            u.lname = request.POST['lname']
            print(u.lname)
            u.email= request.POST['email']
            print(u.email)
            u.phone = request.POST['phone']
            print(u.phone)
            u.address = request.POST['address']
            print(u.address)
            u.user_type = request.POST['user_type']
            print(u.user_type)
            u.state_id = State.objects.get(id = request.POST['state_id'])
            u.city_id = City.objects.get(id = request.POST['city_id'])
            u.area_id = Area.objects.get(id = request.POST['area_id'])
            if(request.POST['is_active'] == 'on'):
                u.is_active="active"
            else:
                u.is_active="deactive"
            u.save()
            messages.add_message(request, messages.SUCCESS,"User added successfully.")
            return redirect('/user')
    else:
        allStates = State.objects.all()
        allcitys=City.objects.all()
        allareas=Area.objects.all()
        parmas = {'allStates': allStates,'allcitys':allcitys,'allareas':allareas}
        return render(request,'user/add_user.html', parmas) 
    

@check_session
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
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
        messages.add_message(request, messages.SUCCESS,"User Edit successfully.")
        return redirect('/user')
    else:
        u=User.objects.get(id=user_id, is_deleted = 1)
        allStates=State.objects.all()
        allcitys=City.objects.all()
        allareas=Area.objects.all()
        params={'user':u,'allStates': allStates,'allcitys':allcitys,'allareas':allareas}
        return render(request,'user/edit_user.html',params)  


@check_session
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def delete_user(request,ur_id):
    d=User.objects.get(id=ur_id)
    #soft delete
    d.is_deleted=0
    d.save()
    messages.add_message(request, messages.WARNING,"User Delete successfully.")
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
    

@cache_control(no_cache=True ,must_revalidate=True ,no_store=True) 
def admin_login(request):
    if request.method=="POST":
        try:    
            user=User.objects.get(email=request.POST['email'],phone=request.POST['phone'])
            if user:
                request.session['email']=user.email
                request.session['fname']=user.fname
                #request.session['user]=serialisers.serialze('json,user)
                user.is_login=True
                user.save()
                messages.add_message(request, messages.SUCCESS,"Hi U have Login Successfully")

                return redirect('dashboard')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR,"Email and Password does not exist.")
            return redirect('/')    
        
    else:
        return render(request,'admin_login.html')

@check_session
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def logout(request):
    user=User.objects.get(email=request.session['email'])
    user.is_login=False
    user.save()
    request.session.clear()
    messages.add_message(request, messages.WARNING,"Logout successfully.")
    return redirect('/')

def forgot_pass(request):
    return render(request,'forgot_pass.html')



             
       
        











    