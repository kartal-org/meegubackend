from django.forms import ModelForm 
import datetime
from .models import *
from users.models import *
from subscriptions.models import *
from classrooms.models import *
from institutions.models import Institution, Department, StaffType, Staff, InstitutionVerification

class InstitutionVerifyForm(ModelForm):
	class Meta:
		model = InstitutionVerification
		fields = ['status']