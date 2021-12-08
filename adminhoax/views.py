from django.shortcuts import render, redirect
import datetime
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

    today = datetime.date.today()

    monthlyClassroomSubscriptionCount = ClassroomSubscription.objects.filter(
        dateCreated__month=today.month, dateCreated__year=today.year
    ).count()
    monthlyInstitutionSubscriptionCount = InstitutionSubscription.objects.filter(
        dateCreated__month=today.month, dateCreated__year=today.year
    ).count()

    totalMonthlyClassroomSubscriptionCount = Plan.objects.filter(
        pk=ClassroomSubscription.objects.filter(dateCreated__month=today.month, dateCreated__year=today.year)
    )
    totalMonthlyInstitutionSubscriptionCount = Plan.objects.filter(
        pk=InstitutionSubscription.objects.filter(dateCreated__month=today.month, dateCreated__year=today.year)
    )

    total = monthlyClassroomSubscriptionCount + monthlyInstitutionSubscriptionCount

    institutionVerification = InstitutionVerification.objects.all()

    contain = {
        "userslist": users,
        "usersCount": usersCount,
        "transactionlistClassroom": transactionsClassroom,
        "transactionlistInsitution": transactionsInstituion,
        "classroomsCount": classroomsCount,
        "institutionsCount": instituionsCount,
        "subscriptionList": subscription,
        "subscriptionTotal": total,
        "institutionVerification": institutionVerification,
    }

    return render(request, "adminhoax/index.html", contain)

def institutionVerify(request, pk_instv):
    institutionVerification = InstitutionVerification.objects.get(id=pk_instv)

    contain = {'data':institutionVerification, }
    return render(request, "adminhoax/verifyPage.html", contain)
