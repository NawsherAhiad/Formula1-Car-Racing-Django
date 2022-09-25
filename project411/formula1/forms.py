from django import forms  
from formula1.models import driver
from formula1.models import team
from formula1.models import merch
from formula1.models import circuit 
from formula1.models import schedule
from formula1.models import standings
from formula1.models import users

class DriverForm(forms.ModelForm):  
    class Meta:  
        model = driver  
        fields = "__all__"