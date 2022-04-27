from django.contrib import admin
from .models import DagligaInkomster, DagligaUtgifter, TheDay
admin.site.register(TheDay)
admin.site.register(DagligaInkomster)
admin.site.register(DagligaUtgifter)