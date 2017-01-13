from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from .models import Job,Status,History,Address
from accounts.models import Profile

from .forms import RepairQuotationForm, AddressForm

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'repairs/index.html'
    context_object_name = 'latest_repair_list'

    def get_queryset(self):
        """
        Return the last five jobs (not including those set to be
        published in the future).
        """
        return Job.objects.all()


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Job
    template_name = 'repairs/detail.html'

    def get_queryset(self):
        """
        Excludes any jobs that aren't published yet.
        """
        return Job.objects.filter(entry_date__lte=timezone.now())
        
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['address_histories'] = Address.objects.filter(job__user=self.request.user).distinct()
        return context


def index_view(request):
    jobs = []
    if request.user.is_authenticated:
        print "user is authenticated"
        jobs = Job.objects.filter(user=request.user)
    
    return render(request, 'repairs/index.html', {
        'jobs': jobs
    })

def repair_quotation(request):
    if request.method == 'POST':
        print "POST"
        form = RepairQuotationForm(request.POST)
        if form.is_valid():
            problem = form.cleaned_data['problem']
            product = form.cleaned_data['product']
            serial_number = form.cleaned_data['serial_number']
            username = form.cleaned_data['customer_name']
            if request.user.is_authenticated:
                # Do something for authenticated users.
                job_obj = Job(user = request.user,
                                problem=problem,
                                product=product,
                                entry_date = timezone.now())
                
                job_obj.save()
                #messages.success(request, 'Your repair quotation has been submitted!')
                messages.info(request, 'Please select an address for collection.')
                return HttpResponseRedirect(reverse('repairs:address'))
            else:
                messages.error(request, 'Please signin to make a repair quotation.')
                # Do something for anonymous users.
                # Redirect to login or register page, copy the repair_quotation form as hidden input
                #request.session['problem'] = problem
                return HttpResponseRedirect(reverse('accounts:signup'))
        else:
            messages.error(request, ('Please correct the error below.'))
            return render(request, 'repairs/repair_quotation.html', {'form': form})

    else:
        if request.user.is_authenticated:
            form = RepairQuotationForm()
            address_form = AddressForm()
            return render(request, 'repairs/repair_quotation.html', {'form': form,'address_form': address_form})
        else:
            messages.error(request, 'Please signin to make a repair quotation.')
            return HttpResponseRedirect(reverse('repairs:index'))
    
def thanks(request):
    if request.user.is_authenticated:
        message = request.user
    else:
        message = request.user
    return render(request, 'repairs/thanks.html')

@login_required
def request_update(request,job_id):
    job = Job.objects.get(pk=job_id)
    if not job.address:
        messages.warning(request, 'Please add an address to your repair request.')
    elif customer_request_update(job_id):
        messages.success(request, '%s Your request has been recorded, customer service will contact you in 24 hours.' % job_id)
    else:
        messages.error(request, '%s You already made an request in last 24 hours. Please allow upto 24 hours' % job_id)
    return HttpResponseRedirect(reverse('repairs:detail', args=[job_id]))


def customer_request_update(job_id):
    job = Job.objects.get(pk=job_id)
    if not job.was_customer_request_update_recentlly():
        status = Status.objects.filter(status_text__startswith="Customer request")[0]
        history = History(date=timezone.now(),status=status,job=job)
        history.save()
        return True
    else:
        return False

@login_required
def address_view(request,job_id):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address_form.save()
        return HttpResponseRedirect(reverse('repairs:detail', args=[job_id]))
    else:
        address_form = AddressForm()
        address_histories= Address.objects.filter(job__user=request.user).distinct()
        print '####',address_histories
        print '\n'.join(str(p) for p in address_histories) 
        return render(request, 'repairs/address.html', {'job_id': job_id,'address_form': address_form, 'address_histories':address_histories})

def payment_view(request,job_id):
    pass
