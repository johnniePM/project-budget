from django.contrib import admin

# Register your models here.
from .models import DagligaInkomster, DagligaUtgifter, Klient, TheDay
admin.site.register(DagligaInkomster)
admin.site.register(DagligaUtgifter)

class TheDateAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(TheDay,TheDateAdmin)
admin.site.register(Klient)