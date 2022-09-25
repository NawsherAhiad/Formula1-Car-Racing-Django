from django.shortcuts import redirect, render
from django.db import connection
from formula1.models import driver, participation
from formula1.models import team
from formula1.models import merch
from formula1.models import circuit 
from formula1.models import schedule
from formula1.models import standings
from formula1.models import users
from django.contrib import messages
from django.http import HttpResponse
import random

# Create your views here.
def index(request):
    schedules = schedule.objects.all()
    standing = standings.objects.raw('select * from standings, schedule where standings.schedule_id = schedule.schedule_id')
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        user_values = {
            'current_user': current_user,
            'user_rank' : user_rank,
            'schedules' : schedules,
            'standings' : standing
        }   
        return render(request, "index.html", user_values)  
    return render(request, "index.html",{'schedules' : schedules, 'standings' : standing})

def signup(request):
    schedules = schedule.objects.all()
    standing = standings.objects.raw('select * from standings, schedule where standings.schedule_id = schedule.schedule_id')
    values = {
        'schedules' : schedules,
        'standings' : standing
    }
    if request.method =="POST":
        text = ""
        for i in range(5):
            text += str(random.randint(0,9))

        user_name = request.POST['user_name']
        user_id = user_name + text
        user_email= request.POST['user_email']

        user_password= request.POST['user_password']
        user_phone= request.POST['user_phone']
        rank = "user"
        if users.objects.filter(user_email=user_email).count() > 0:
            messages.success(request, "Email Already Exists!")
            return render(request, "signup.html",values)
        else:
            saverecord = users()

            saverecord.user_id = user_id
            saverecord.user_name = user_name
            saverecord.user_email = user_email
            saverecord.user_password = user_password
            saverecord.user_phone = user_phone
            saverecord.rank = rank
            saverecord.save()

            messages.success(request, "Succesful")
            return render(request, "signup.html", values)
    
    else:
        return render(request, "signup.html", values)
  
def signin(request):
    schedules = schedule.objects.all()
    standing = standings.objects.raw('select * from standings, schedule where standings.schedule_id = schedule.schedule_id')
    values = {
        'schedules' : schedules,
        'standings' : standing
    }
    if request.method == "POST":
        value= users.objects.get(user_email=request.POST['user_email'])
        if value.user_password==request.POST['user_password']:
            request.session['user_id']=value.user_id
            request.session['user_name'] = value.user_name
            request.session['rank'] = value.rank
            return redirect("../index")
    else:
        return render(request, "signin.html", values)

def signout(request):
    try:
        del request.session['user_id']
        del request.session['user_name']
        del request.session['rank']
    except KeyError:
        pass
    return redirect("../signin")

def admin(request):
    schedules = schedule.objects.all()
    standing = standings.objects.raw('select * from standings, schedule where standings.schedule_id = schedule.schedule_id')
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        if user_rank == "admin":
            user_values = {
                'current_user': current_user,
                'user_rank' : user_rank,
                'schedules' : schedules,
                'standings' : standing
            }
            return render(request, "admin_page.html", user_values)
        else:
            return HttpResponse("You don't have the permission to view this page")
    else:
        return redirect("../signin")


def input_driver(request):
    teams = team.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        if user_rank == "admin":
            values = {
                'current_user': current_user,
                'user_rank' : user_rank,
                'teams':teams

            }
            return render(request, "input_driver.html", values)
        else:
            return HttpResponse("You don't have the permission to view this page")

def insert_driver(request):
    if request.method =="POST":
        driver_id= request.POST['driver_id']
        driver_name = request.POST['driver_name']
        sex= request.POST['sex']
        age = request.POST['age']
        country= request.POST['country']
        total_points= request.POST['total_points']
        team_id= request.POST['team_id']
        if len(request.FILES) != 0:
            image = request.FILES['image']

        saverecord = driver()

        saverecord.driver_id = driver_id
        saverecord.driver_name = driver_name
        saverecord.sex = sex
        saverecord.age = age
        saverecord.country = country
        saverecord.total_points = total_points
        saverecord.team_team_id = team_id
        saverecord.image = image
        saverecord.save()
        messages.success(request, "Succesful")
        return render(request, "input_driver.html")
    


def report_driver(request):
    schedules = schedule.objects.all()
    standing = standings.objects.raw('select * from standings, schedule where standings.schedule_id = schedule.schedule_id')
    drivers = driver.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        values = {
            'current_user': current_user,
            'user_rank' : user_rank,
            'drivers':drivers,
            'schedules' : schedules,
            'standings' : standing
        }
        return render(request,"report_driver.html",values)
    else:
        return render(request,"report_driver.html",{'drivers':drivers, 'schedules' : schedules, 'standings' : standing})

def edit_driver(request, driver_id):
    drivers = driver.objects.get(driver_id = driver_id)
    return render(request,"edit_driver.html",{'drivers':drivers})

def update_driver(request, driver_id):
    drivers = driver.objects.get(driver_id = driver_id)
    update = connection.cursor()
    if request.method =="POST":
        driver_id= request.POST['driver_id']
        driver_name = request.POST['driver_name']
        sex= request.POST['sex']
        age = request.POST['age']
        country= request.POST['country']
        total_points= request.POST['total_points']
        team_id= request.POST['team_id']
        update.execute("update driver set driver_name = %s, sex = %s, age = %s, country = %s, total_points = %s, team_team_id = %s where driver_id = %s", [driver_name, sex, age, country, total_points, team_id, driver_id])
        drivers_new = driver.objects.get(driver_id = driver_id)
        messages.success(request, "Record Updated!")
        return render(request,"edit_driver.html",{'drivers':drivers_new})
    messages.success(request, "Record Not Updated!")
    return render(request,"edit_driver.html",{'drivers':drivers})


def delete_driver(request, driver_id):
    delete = connection.cursor()
    delete.execute("delete from driver where driver_id = %s", [driver_id])
    return redirect("../report_driver")
    

def input_team(request):
    if request.method == "POST":
       team_id = request.POST['team_id']
       team_name = request.POST['team_name']
       base = request.POST['base']
       pole_position = request.POST['pole_position']
       world_championship = request.POST['world_championship']
       if len(request.FILES) != 0:
            image = request.FILES['image']

       saverecord = team()
       saverecord.team_id = team_id
       saverecord.team_name = team_name
       saverecord.base = base
       saverecord.pole_position =pole_position
       saverecord.world_championship = world_championship
       saverecord.image = image
       saverecord.save()
       messages.success(request, "Succesful")
       return render(request, "input_team.html")
    else:
           
        return render(request, "input_team.html")

def report_team(request):
    schedules = schedule.objects.all()
    standing = standings.objects.raw('select * from standings, schedule where standings.schedule_id = schedule.schedule_id')
    teams = team.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        values = {
            'current_user': current_user,
            'user_rank' : user_rank,
            'teams':teams,
            'schedules' : schedules,
            'standings' : standing
        }
        return render(request,"report_team.html",values)
    else:
        return render(request,"report_team.html",{'teams':teams, 'schedules' : schedules, 'standings' : standing})

def edit_team(request, team_id):
    teams = team.objects.get(team_id = team_id)
    return render(request,"edit_team.html",{'teams':teams})

def update_team(request, team_id):
    teams = team.objects.get(team_id = team_id)
    update = connection.cursor()
    if request.method == "POST":
        team_id = request.POST['team_id']
        team_name = request.POST['team_name']
        base = request.POST['base']
        pole_position = request.POST['pole_position']
        world_championship = request.POST['world_championship']
        update.execute("update team set team_name = %s, base = %s, pole_position = %s, world_championship = %s where team_id = %s", [team_name, base, pole_position, world_championship, team_id])
        team_new = team.objects.get(team_id = team_id)
        messages.success(request, "Record Updated!")
        return render(request,"edit_team.html",{'teams':team_new})
    messages.success(request, "Record Not Updated!")
    return render(request,"edit_team.html",{'teams':teams})

def delete_team(request, team_id):
    delete = connection.cursor()
    delete.execute("delete from participation where team_id = %s", [team_id])
    delete.execute("delete from driver where team_team_id = %s", [team_id])
    delete.execute("delete from merch where team_id = %s", [team_id])
    delete.execute("delete from team where team_id = %s", [team_id])
    return redirect("../report_team")



       
def input_merch(request):
    teams = team.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        if user_rank == "admin":
            values = {
                'current_user': current_user,
                'user_rank' : user_rank,
                'teams':teams

            }
            return render(request, "input_merch.html", values)
        else:
            return HttpResponse("You don't have the permission to view this page")

def insert_merch(request):
    if request.method == "POST":
        product_id = request.POST['product_id']
        category = request.POST['category']
        size = request.POST['size']
        price = request.POST['price']
        quantity = request.POST['quantity']
        team_id = request.POST['team_id']
        
        saverecord = merch()
        saverecord.product_id = product_id
        saverecord.category = category
        saverecord.size = size
        saverecord.price = price
        saverecord.quantity = quantity
        saverecord.team_id = team_id
        saverecord.save()
        messages.success(request, "Succesful")
        return render(request, "input_merch.html")
    
    
def report_merch(request):
    merchandise = merch.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        values = {
            'current_user': current_user,
            'user_rank' : user_rank,
            'merchandise':merchandise
        }
        return render(request,"report_merch.html",values)
    else:
        return render(request,"report_merch.html",{'merchandise':merchandise})

def edit_merch(request, product_id):
    products = merch.objects.get(product_id = product_id)
    return render(request,"edit_merch.html",{'products':products})

def update_merch(request, product_id):
    products = merch.objects.get(product_id = product_id)
    update = connection.cursor()
    if request.method == "POST":
        product_id = request.POST['product_id']
        category = request.POST['category']
        size = request.POST['size']
        price = request.POST['price']
        quantity = request.POST['quantity']
        team_id = request.POST['team_id']

        update.execute("update merch set category = %s, size = %s, price = %s, quantity = %s, team_id = %s where product_id = %s", [category, size, price, quantity, team_id, product_id])
        product_new = merch.objects.get(product_id = product_id)
        messages.success(request, "Record Updated!")
        return render(request,"edit_merch.html",{'products':product_new})
    messages.success(request, "Record Not Updated!")
    return render(request,"edit_merch.html",{'products':products})


def delete_merch(request, product_id):
    delete = connection.cursor()
    delete.execute("delete from merch where product_id = %s", [product_id])
    return redirect("../report_merch")


def input_circuit(request):
    if request.method == "POST":
        circuit_serial= request.POST['circuit_serial']
        circuit_name= request.POST['circuit_name']
        circuit_location= request.POST['circuit_location']
        circuit_length= request.POST['circuit_length']
        circuit_description= request.POST['circuit_description']
        
        saverecord = circuit()
        saverecord.circuit_serial = circuit_serial
        saverecord.circuit_name = circuit_name
        saverecord.circuit_location = circuit_location
        saverecord.circuit_length = circuit_length
        saverecord.circuit_description = circuit_description
        saverecord.save()
        messages.success(request, "Successful")
        return render(request, "inpput_circuit.html")
    else:
        
        return render(request, "input_circuit.html")

def report_circuit(request):
    schedules = schedule.objects.all()
    standing = standings.objects.raw('select * from standings, schedule where standings.schedule_id = schedule.schedule_id')
    circuits = circuit.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        values = {
            'current_user': current_user,
            'user_rank' : user_rank,
            'circuits':circuits,
            'schedules' : schedules,
            'standings' : standing
        }
        return render(request,"report_circuit.html",values)
    else:
        return render(request,"report_circuit.html",{'circuits':circuits, 'schedules' : schedules, 'standings' : standing})

def edit_circuit(request, circuit_serial):
    circuits = circuit.objects.get(circuit_serial = circuit_serial)
    return render(request,"edit_circuit.html",{'circuits':circuits})

def update_circuit(request, circuit_serial):
    circuits = circuit.objects.get(circuit_serial = circuit_serial)
    update = connection.cursor()
    if request.method == "POST":
        circuit_serial= request.POST['circuit_serial']
        circuit_name= request.POST['circuit_name']
        circuit_location= request.POST['circuit_location']
        circuit_length= request.POST['circuit_length']
        circuit_description= request.POST['circuit_description']

        update.execute("update circuit set circuit_name = %s, circuit_location = %s, circuit_length = %s, circuit_description = %s where circuit_serial = %s", [circuit_name, circuit_location, circuit_length, circuit_description, circuit_serial])
        circuit_new = circuit.objects.get(circuit_serial = circuit_serial)
        messages.success(request, "Record Updated!")
        return render(request,"edit_circuit.html",{'circuits':circuit_new})
    messages.success(request, "Record Not Updated!")
    return render(request,"edit_circuit.html",{'circuits':circuits})


def delete_circuit(request, circuit_serial):
    delete = connection.cursor()
    delete.execute("delete from schedule where circuit_serial = %s", [circuit_serial])
    delete.execute("delete from circuit where circuit_serial = %s", [circuit_serial])
    return redirect("../report_circuit")


def input_schedule(request):
    circuits = circuit.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        if user_rank == "admin":
            values = {
                'current_user': current_user,
                'user_rank' : user_rank,
                'circuits':circuits

            }
            return render(request, "input_schedule.html", values)
        else:
            return HttpResponse("You don't have the permission to view this page")

def insert_schedule(request):
    if request.method == "POST":
        schedule_id = request.POST['schedule_id']
        schedule_name = request.POST['schedule_name']
        duration = request.POST['duration']
        schedule_date = request.POST['schedule_date']
        year = request.POST['year']
        circuit_serial = request.POST['circuit_serial']

        saverecord = schedule()
        saverecord.schedule_id = schedule_id
        saverecord.schedule_name = schedule_name
        saverecord.duration = duration
        saverecord.schedule_date = schedule_date
        saverecord.year = year 
        saverecord.circuit_serial = circuit_serial
        saverecord.save()

        messages.success(request, "Successful")
        return render(request, "input_schedule.html")
    else:
        
        return render(request, "input_schedule.html")

def report_schedule(request,years):
    standing = standings.objects.raw('select * from standings, schedule where standings.schedule_id = schedule.schedule_id')
    if years == 'all':
        schedules = schedule.objects.all()
    else:
        schedules = schedule.objects.filter(year = years)
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        values = {
            'current_user': current_user,
            'user_rank' : user_rank,
            'schedules':schedules,
            'standings' : standing
        }
        return render(request,"report_schedule.html",values)
    else:
        return render(request,"report_schedule.html",{'schedules':schedules, 'standings' : standing})

def edit_schedule(request, schedule_id):
    schedules = schedule.objects.get(schedule_id = schedule_id)
    return render(request,"edit_schedule.html",{'schedules':schedules})

def update_schedule(request, schedule_id):
    schedules = schedule.objects.get(schedule_id = schedule_id)
    update = connection.cursor()
    if request.method == "POST":
        schedule_id = request.POST['schedule_id']
        schedule_name = request.POST['schedule_name']
        duration = request.POST['duration']
        schedule_date = request.POST['schedule_date']
        year = request.POST['year']
        circuit_serial = request.POST['circuit_serial']
        update.execute("update schedule set schedule_name = %s, duration = %s, schedule_date = %s, year = %s, circuit_serial = %s where schedule_id = %s", [schedule_name, duration, schedule_date, year, circuit_serial, schedule_id])
        schedule_new = schedule.objects.get(schedule_id = schedule_id)
        messages.success(request, "Record Updated!")
        return render(request,"edit_schedule.html",{'schedules':schedule_new})
    messages.success(request, "Record Not Updated!")
    return render(request,"edit_schedule.html",{'schedules':schedules})


def delete_schedule(request, schedule_id):
    delete = connection.cursor()
    delete.execute("delete from participation where schedule_id = %s", [schedule_id])
    delete.execute("delete from ticket where schedule_id = %s", [schedule_id])
    delete.execute("delete from schedule where schedule_id = %s", [schedule_id])
    return redirect("../report_schedule")

def input_standings(request):
    drivers = driver.objects.all()
    schedules = schedule.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        if user_rank == "admin":
            values = {
                'current_user': current_user,
                'user_rank' : user_rank,
                'drivers':drivers,
                'schedules': schedules

            }
            return render(request, "input_standings.html", values)
        else:
            return HttpResponse("You don't have the permission to view this page")

def insert_standings(request):
    if request.method == "POST":
        standing_id = request.POST["standing_id"]
        time = request.POST.get("time")
        avg_speeds = request.POST.get("avg_speeds")
        laps= request.POST.get("laps")
        points = request.POST.get("points")
        driver_id = request.POST.get("driver_id")
        schedule_id = request.POST.get("schedule_id")
        

        saverecord = standings()
        saverecord.standing_id= standing_id
        saverecord.time= time
        saverecord.avg_speeds = avg_speeds
        saverecord.laps= laps
        saverecord.points = points
        saverecord.schedule_id = schedule_id
        saverecord.driver_id = driver_id
        saverecord.save()

        messages.success(request, "Successful")
        return render(request, "input_standings.html")
    else:
        
        return render(request, "input_standings.html")


def report_standing(request, schedule_ids):
    schedules = schedule.objects.all()
    if schedule_ids == 'all':
        standing = standings.objects.all()
    else:
        standing = standings.objects.filter(schedule_id = schedule_ids)
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        values = {
            'current_user': current_user,
            'user_rank' : user_rank,
            'standing':standing,
            'schedules':schedules

        }
        return render(request,"report_standing.html",values)
    else:
        return render(request,"report_standing.html",{'standing':standing, 'schedules':schedules})

def edit_standings(request, standing_id):
    standing = standings.objects.get(standing_id = standing_id)
    return render(request,"edit_standings.html",{'standings':standing})

def update_standings(request, standing_id):
    standing = standings.objects.get(standing_id = standing_id)
    update = connection.cursor()
    if request.method == "POST":
        standing_id = request.POST["standing_id"]
        time = request.POST.get("time")
        avg_speeds = request.POST.get("avg_speeds")
        laps= request.POST.get("laps")
        points = request.POST.get("points")
        driver_id = request.POST.get("driver_id")
        schedule_id = request.POST.get("schedule_id")
        update.execute("update standings set time = %s, avg_speeds = %s, laps = %s, points = %s, driver_id = %s, schedule_id = %s where standing_id = %s", [time, avg_speeds, laps, points, driver_id, schedule_id, standing_id])
        standing_new = standings.objects.get(standing_id = standing_id)
        messages.success(request, "Record Updated!")
        return render(request,"edit_standings.html",{'standings':standing_new})
    messages.success(request, "Record Not Updated!")
    return render(request,"edit_standings.html",{'standings':standing})


def delete_standings(request, standing_id):
    delete = connection.cursor()
    delete.execute("delete from standings where standing_id = %s", [standing_id])
    return redirect("../report_standing")


def input_participation(request):
    teams = team.objects.all()
    schedules = schedule.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        if user_rank == "admin":
            values = {
                'current_user': current_user,
                'user_rank' : user_rank,
                'teams':teams,
                'schedules': schedules

            }
            return render(request, "input_participation.html", values)
        else:
            return HttpResponse("You don't have the permission to view this page")

def insert_participation(request):
    if request.method == "POST":
        team_id = request.POST.get("team_id")
        schedule_id = request.POST.get("schedule_id")
        

        saverecord = participation()
        saverecord.team_id = team_id
        saverecord.schedule_id = schedule_id
        saverecord.save()

        messages.success(request, "Successful")
        return render(request, "input_participation.html")
    else:
        
        return render(request, "input_participation.html")


def report_participation(request, schedule_id):
    participants = participation.objects.raw('select * from participation, schedule, team where participation.schedule_id = schedule.schedule_id and participation.team_id = team.team_id and participation.schedule_id = %s', [schedule_id])
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        values = {
            'current_user': current_user,
            'user_rank' : user_rank,
            'participants':participants

        }
        return render(request,"report_participation.html",values)
    else:
        return render(request,"report_participation.html",{'participants':participants})

def report_users(request):
    user = users.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        user_rank = request.session['rank']
        if user_rank == "admin":
            values = {
                'current_user': current_user,
                'user_rank' : user_rank,
                'user':user
            }
            return render(request,"report_users.html",values)
        else:
            return HttpResponse("You don't have the permission to view this page")
    else:
        return redirect("../signin")




