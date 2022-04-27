from operator import mod
from django.db import models
import datetime 
from taggit.managers import TaggableManager

current_date = datetime.date.today()


class TheDay(models.Model):
    date=models.DateField( null=False, blank=False, unique=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
    def save(self, *args, **kwargs):

       # make sure `id` is set to current date
        old_pk=self.pk
        day=int(self.date.day)
        month=int(self.date.month) * 100
        year=int(self.date.year)* 10000
        self.pk=year+month+day
        super(TheDay, self).save(*args, **kwargs)
        instance=TheDay.objects.get(id=old_pk)
        if instance:
            instance.delete()
        return super(TheDay, self).save(*args, **kwargs)

       
class DagligaUtgifter(models.Model):
    name=models.CharField(max_length=100, blank=False, null=False)
    amount=models.IntegerField(default=0)
    the_day=models.ForeignKey(TheDay, on_delete=models.CASCADE)
    
class DagligaInkomster(models.Model):
    amount=models.IntegerField(default=0)
    the_day=models.ForeignKey(TheDay, on_delete=models.CASCADE)
    klient=TaggableManager()
    kommentar=models.TextField(blank=True, null=True)



