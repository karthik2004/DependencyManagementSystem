from django.views.generic import ListView,DetailView
from .models import Application,Service
from django.http import HttpResponseRedirect

from django.shortcuts import render

# Create your views here.
class ApplicationList(ListView):
    model = Application
    template_name = 'application_list.html'
    queryset = Application.objects.all().order_by('appok')
class ServiceList(ListView):
    model = Application
    template_name = 'service_list.html'
    queryset = Application.objects.order_by('appok')

def StatusUpdate(request):
    app_object = Application.objects.get(id = request.POST.get("application"))
    app_object.failreason = request.POST.get("reason", "")
    app_object.appok = not app_object.appok
    app_object.save()
    return HttpResponseRedirect('/dashboard/')

class ServiceInfo(DetailView):
    model = Application
    template_name = 'service_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceInfo, self).get_context_data(**kwargs)
        return context