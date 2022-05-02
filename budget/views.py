from asyncio.windows_events import NULL
import datetime
import json
from pyexpat import model
from django.shortcuts import redirect, render
from django.views.generic import View,CreateView, UpdateView, TemplateView
from datetime import timedelta
from budget.models import DagligaInkomster, Klient, TheDay, DagligaUtgifter
current_date = datetime.date.today()
week = current_date + timedelta(days=-6)

day=int(current_date.day)
month=int(current_date.month) * 100
year=int(current_date.year)* 10000


class IdagsnyautgiftenVIew(CreateView):
    model=DagligaUtgifter
    fields=['amount', 'name']
    template_name="budget/idags-nya-utgift-view.html"

    def post(self, request):
        amount = request.POST['amount']
        name = request.POST['name']
        the_day = TheDay.objects.get(date=current_date)
        instance= DagligaUtgifter(name=name, amount=amount, the_day=the_day)
        instance.save()
        return redirect("budget:idag-nya-ut")

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            idag=TheDay.objects.get(date=current_date)
            context['idag']= idag
            if  idag.totalUtgift+idag.totalInkomst==0:
                context['perut']= int((idag.totalUtgift /(idag.totalUtgift+idag.totalInkomst))*100)
                context['perin']= int((idag.totalInkomst /(idag.totalUtgift+idag.totalInkomst))*100)
            else:
                context['perut']= int(100)
                context['perin']= int(100)
            context['utgifter'] = DagligaUtgifter.objects.filter(the_day__date=current_date).order_by('amount')
            context['inkomster'] = DagligaInkomster.objects.filter(the_day__date__contains=current_date)
            context['indata'] =json.dumps( [
                {
                    'id': obj.id,
                    'amount': obj.amount,
                    'date': current_date.strftime("%A"),
                }
                for obj in DagligaInkomster.objects.filter(the_day__date__contains=current_date)
            ])
            context['utdata'] = json.dumps([
                {
                    'id': obj.id,
                    'amount': obj.amount,
                    'name': obj.name
                }
                for obj in DagligaUtgifter.objects.filter(the_day__date=current_date)
            ])
            context['veckoutdata'] = json.dumps([
                {
                    'id': obj.id,
                    'totalUtgift': obj.totalUtgift,
                    'totalInkomst': obj.totalInkomst
                }
                for obj in TheDay.objects.filter(date__lte=current_date , date__gte=week)
            ])
            return context


class IdagsnyainkomstenVIew(CreateView):
    model=DagligaInkomster
    fields=['amount', 'klient', 'kommentar']
    template_name="budget/idags-nya-inkomst-view.html"

    def post(self, request):
        amount = request.POST['amount']
        kommentar = request.POST['kommentar']
        klient = request.POST['klient']
        the_day = TheDay.objects.get(date=current_date)

        instance=DagligaInkomster(kommentar=kommentar, amount=amount, the_day=the_day)

        try:
            obj = Klient.objects.get(name__iexact=klient)
        except Klient.DoesNotExist:
            obj = Klient(name=klient)
            obj.save()
        instance.klient=obj
        instance.save()

        return redirect("budget:idag-nya-in")

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        this_date=TheDay.objects.get(id=year+month+day)
        dags_inkomster=DagligaInkomster.objects.filter(the_day=this_date).order_by('klient')
        context['dags_inkomster']=dags_inkomster
        context["dags_utgifter"] = DagligaUtgifter.objects.filter(the_day=this_date).order_by('amount')
        return context

class IdagsView(TemplateView):
    template_name="budget/idag-template.html"
    def get(self, request, *args, **kwargs):
        
        if not TheDay.objects.filter(date=current_date).exists():
            instance=TheDay(date=current_date)
            instance.save()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idag=TheDay.objects.get(date=current_date)
        context['idag']= idag
        if  idag.totalUtgift+idag.totalInkomst==0:
            context['perut']= int((idag.totalUtgift /(idag.totalUtgift+idag.totalInkomst))*100)
            context['perin']= int((idag.totalInkomst /(idag.totalUtgift+idag.totalInkomst))*100)
        else:
            context['perut']= int(100)
            context['perin']= int(100)
        context['utgifter'] = DagligaUtgifter.objects.filter(the_day__date=current_date).order_by('amount')
        context['inkomster'] = DagligaInkomster.objects.filter(the_day__date__contains=current_date)
        context['indata'] =json.dumps( [
            {
                'id': obj.id,
                'amount': obj.amount,
                'date': current_date.strftime("%A"),
            }
            for obj in DagligaInkomster.objects.filter(the_day__date__contains=current_date)
        ])
        context['utdata'] = json.dumps([
            {
                'id': obj.id,
                'amount': obj.amount,
                'name': obj.name
            }
            for obj in DagligaUtgifter.objects.filter(the_day__date=current_date)
        ])
        context['veckoutdata'] = json.dumps([
            {
                'id': obj.id,
                'totalUtgift': obj.totalUtgift,
                'totalInkomst': obj.totalInkomst
            }
            for obj in TheDay.objects.filter(date__lte=current_date , date__gte=week)
        ])
        return context

class EditInkomstView(UpdateView):
    model=DagligaInkomster
    fields='__all__'
    template_name="budget/edit-specific-inkomst.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        id=self.kwargs['pk']
        the_form=DagligaInkomster.objects.get(id=id)
        this_date=the_form.the_day
        dags_inkomster=DagligaInkomster.objects.filter(the_day=this_date).order_by('klient')
        context['dags_inkomster']=dags_inkomster
        context["dags_utgifter"] = DagligaUtgifter.objects.filter(the_day=this_date).order_by('amount')
        return context

class EditUtgiftView(UpdateView):
    model=DagligaUtgifter
    fields='__all__'
    template_name="budget/edit-specific-utgift.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        id=self.kwargs['pk']
        the_form=DagligaUtgifter.objects.get(id=id)
        this_date=the_form.the_day
        dags_inkomster=DagligaInkomster.objects.filter(the_day=this_date).order_by('klient')
        context['dags_inkomster']=dags_inkomster
        context["dags_utgifter"] = DagligaUtgifter.objects.filter(the_day=this_date).order_by('amount')
        return context



            

