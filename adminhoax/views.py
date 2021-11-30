from django.shortcuts import render, redirect  
 
from .models import *
from users.models import *
from subscriptions.models import *
from classrooms.models import *
from institutions.models import * 

# Create your views here.  
def home(request):
    users = NewUser.objects.all()
    usersCount = users.count() 

    classroomsCount = Classroom.objects.count()
    instituionsCount = Institution.objects.count() 

    transactionsClassroom = ClassroomSubscription.objects.all()
    transactionsInstituion = InstitutionSubscription.objects.all()

    subscription = Plan.objects.all()


    #monthly nga query dre dapit start
    #plan = Plan.objects.filter(name=transactionsClassroom)
    planCount = ClassroomSubscription.objects.filter(plan=subscription).count()
    total = Plan.price * planCount
    #end
    
    contain = {'userslist':users, 'usersCount':usersCount,
                'transactionlistClassroom':transactionsClassroom,  
                'transactionlistInsitution':transactionsInstituion,
                'classroomsCount':classroomsCount,
                'instituionsCount':instituionsCount,
                'subscriptionList':subscription,
                'subscriptionTotal':total,}         #'subscriptionTotal':total nga variable para ma pass sa html

    return render(request, 'adminhoax/index.html', contain)