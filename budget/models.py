from operator import mod
from statistics import mode
from django.db import models
import datetime 
from datetime import timedelta

current_date = datetime.date.today()
datetime_tomorrow = current_date + timedelta(days=1)

class TheDay(models.Model):
    date=models.DateField( null=False, blank=False, unique=True, auto_now=False)
    totalInkomst=models.IntegerField(default=0, blank=True, null=True )
    totalUtgift=models.IntegerField(default=0, blank=True, null=True )
    
    def __str__(self) -> str:
        return str(self.date)
    
    def save(self, *args, **kwargs):
        day=int(current_date.day)
        month=int(current_date.month) * 100
        year=int(current_date.year)* 10000  
        try:
            if TheDay.objects.get(date=self.date).date == current_date:
                self.pk=year+month+day
            self.totalInkomst=0
            self.totalUtgift=0
            for item in DagligaUtgifter.objects.filter(the_day__date__contains=self.date):
                self.totalUtgift+= item.amount
            for item in DagligaInkomster.objects.filter(the_day__date__contains=self.date):
                self.totalInkomst+= item.amount
        except:
                pass
            

        return super(TheDay, self).save(*args, **kwargs)

       
class DagligaUtgifter(models.Model):
    name=models.CharField(max_length=100, blank=False, null=False)
    amount=models.IntegerField(default=0)
    the_day=models.ForeignKey(TheDay, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def __str__(self) -> str:
        return f"{self.the_day} | {self.name}"
    
class DagligaInkomster(models.Model):
    amount=models.IntegerField(default=0)
    the_day=models.ForeignKey(TheDay, on_delete=models.CASCADE)
    kommentar=models.TextField(blank=True, null=True)
    name=models.CharField(default="no", blank=False, null=False, max_length=150)
    klient=models.ForeignKey('Klient', on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.the_day} | {self.amount}"


class Klient(models.Model):
    name=models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name
    



