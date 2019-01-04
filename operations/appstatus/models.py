from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Application(models.Model):
    name= models.CharField(max_length=50, unique=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    url=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True,max_length=1024)
    dependencies=models.ManyToManyField('self',symmetrical=False,blank=True)
    appok=models.BooleanField(default=True)
    failreason=models.TextField(blank=True,max_length=1024)



    def __str__(self):
        return '%s'%self.name


    def appok_rel(self):
        return self.appok and not any(self.services.filter(serviceok=False))

    def app_updated(self):
        return self.services.latest('date_modified').date_modified or self.date_modified


class Service(models.Model):
    name=models.CharField(max_length=50,unique=False)
    application=models.ForeignKey(Application,related_name='services',null=True,on_delete='CASCADE')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    service_url = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=1024)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True, related_name="services")
    serviceok = models.BooleanField(default=True)
    failreason = models.TextField(blank=True, max_length=1024)

    def __str__(self):
        return '%s' % self.name + ' (' + str(self.application) + ')'

    def serviceok_rel(self):
        return self.application.appok and self.serviceok

    def get_all_deps(self,include_self=False):
        dep_list= []
        if include_self:
            dep_list.append(self)
        for service in Service.object.filter(dependencies=self):
            _dep_list=service.get_all_deps(include_self=True)
            if 0 < len(_dep_list):
                dep_list.extend(_dep_list)
        return dep_list
@receiver(post_save,sender=Service,dispatch_uid="update_serviceok")
def update_status(sender,instance,**kwargs):
    if not Service.objects.filter(dependencies=instance):

        pass
    for service in Service.objects.filter(dependencies=instance):
        if service==instance or service.serviceok==instance.serviceok:

            pass
        else:
            service.serviceok=instance.serviceok
            service.failreason='Dependency on %s' %instance.name + '(' + instance.application.name + ')'
            service.save()
@receiver(post_save,sender=Application,dispatch_uid="Update all Services")
def update_services(sender,instance,**kwargs):
    print(instance)
    for service in Service.objects.all():
        print(service.name)
        service.serviceok=instance.serviceok
        service.save()

