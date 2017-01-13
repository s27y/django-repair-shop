import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Address(models.Model):
    full_name = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    town_city = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=50,default='Ireland')
    contact_number = models.CharField(max_length=20)
    
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s"% (self.full_name,
            self.address_line_1,
            self.address_line_2,
            self.town_city,
            self.county,
            self.postcode,
            self.country,
            self.contact_number)
    
    
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    problem = models.CharField(max_length=500,default='n/a')
    entry_date = models.DateTimeField('date of entry')
    serial_number = models.CharField(max_length=100,default='n/a')
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.problem
    
    def was_customer_request_update_recentlly(self):
        flag = False
        one_day_ago = timezone.now() - datetime.timedelta(days=1)
        if len(self.history_set.filter(date__gte=one_day_ago).order_by('-date')) > 0:
            latest_history = self.history_set.filter(date__gte=one_day_ago).order_by('-date')[0]
            if latest_history.status.status_text.startswith("Customer request"):
                flag = True
        return flag
    
    def get_latest_history(self):
        job_history_set = self.history_set.order_by('-date')
        if job_history_set:
            return job_history_set[0]
        else:
            return None


class Status(models.Model):
    status_text = models.CharField(max_length=100)
    index = models.FloatField()
    
    class Meta:
        verbose_name_plural = "status"
    def __str__(self):
        return self.status_text


class History(models.Model):
    date = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500,blank=True)

    def __str__(self):
        return str(self.date)



