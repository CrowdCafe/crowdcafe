# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login
import logging
from django.contrib.auth.models import User
from django.core.context_processors import csrf 
from forms import LoginForm, UserCreateForm, AccountForm, MembershipForm, UserUpdate
from models import Account, Profile, Membership
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render
from django.http import HttpResponseRedirect    

from rest_framework.authtoken.models import Token
from django.views.generic.list import ListView

log = logging.getLogger(__name__)

from utils import initUser
# -------------------------------------------------------------
# Users
# -------------------------------------------------------------
def home(request):
    
    if request.user.is_authenticated():
        return redirect('account-list')
    else:
        return redirect('login')

def register_user(request):
    
    template_name = 'kitchen/crispy.html'

    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            
            user = authenticate(username=username,
                                password=password)
            if user:
                # save extra parameters - email
                user.email = user_form.data['email']
                user.save()
                #ASK - may be we should init it only in one place - on login?
                initUser(user)
                login(request, user)
                return redirect('account-list')
        return render(request,
                      template_name,
                      { 'form' : user_form })
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreateForm()
    print args
    return render(request, template_name, args)

def update_user(request):
    args = {}
    template_name = 'kitchen/crispy.html'

    if request.method == 'POST':
        form = UserUpdate(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account-list')
    else:
        form = UserUpdate(instance=request.user)

    args['form'] = form
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))

def logout_user(request):
    
    logout(request)
    return redirect('/')    

def login_user(request):
    
    template_name = 'kitchen/crispy.html'

    if request.method == 'POST':
        #TODO - need to fix this part
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print user
        if user is not None:
            login(request, user)
            initUser(user)
            #token = Token.objects.get_or_create(user=user)
            return redirect('account-list')
    form = LoginForm()
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))

# -------------------------------------------------------------
# Accounts
# -------------------------------------------------------------

class AccountListView(ListView):
    
    model = Account

    def get_queryset(self):
        return Account.objects.filter(users__in=[self.request.user.id]) #TODO make sure it is correct
    def get_context_data(self, **kwargs):
        context = super(AccountListView, self).get_context_data(**kwargs)
        return context

class AccountCreateView(CreateView):
    
    model = Account
    template_name = "kitchen/crispy.html"
    form_class = AccountForm

    def get_initial(self):
        initial = {}
        initial['creator'] = self.request.user
        return initial
    
    def form_invalid(self, form):
        log.debug("form is not valid")
        print (form.errors)
        return CreateView.form_invalid(self, form)
    
    def form_valid(self, form):
        log.debug("saved")
        account = form.save()
        account.save()
        membership, created = Membership.objects.get_or_create(user = self.request.user, permission = 'AN', account = account)

        return redirect(reverse('account-list'))

class AccountUpdateView(UpdateView):
    
    model = Account
    template_name = "kitchen/crispy.html"
    form_class = AccountForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        print (form.errors)
        return UpdateView.form_invalid(self, form)
    
    def get_object(self):
        return get_object_or_404(Account, pk = self.kwargs.get('account_pk', None), users__in = [self.request.user.id])
   
    def form_valid(self, form):
        log.debug("updated")
        account = form.save()
        return redirect(reverse('account-list'))

# -------------------------------------------------------------
# Membership
# -------------------------------------------------------------

class MembershipCreateView(CreateView):
    
    model = Membership
    template_name = "kitchen/crispy.html"
    form_class = MembershipForm

    def get_initial(self):
        initial = {}
        initial['account'] = get_object_or_404(Account, pk = self.kwargs.get('account_pk', None), users__in = [self.request.user.id])
        return initial
    
    def form_invalid(self, form):
        log.debug("form is not valid")
        print (form.errors)
        return CreateView.form_invalid(self, form)
    
    def form_valid(self, form):
        log.debug("saved")
        membership = form.save()

        return redirect(reverse('member-list', kwargs={'account_pk': membership.account.id}))

class MembershipUpdateView(UpdateView):
    
    model = Membership
    template_name = "kitchen/crispy.html"
    form_class = MembershipForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        print (form.errors)
        return UpdateView.form_invalid(self, form)
    def get_object(self):
        return get_object_or_404(Membership, pk = self.kwargs.get('member_pk', None), account__users__in = [self.request.user.id])
   
    def form_valid(self, form):
        log.debug("updated")
        membership = form.save()
        return redirect(reverse('member-list', kwargs={'account_pk': membership.account.id}))

class MembershipListView(ListView):

    model = Membership

    def get_queryset(self):
        account = get_object_or_404(Account, pk = self.kwargs.get('account_pk', None), users__in = [self.request.user.id])
        return Membership.objects.filter(account = account)
    
    def get_context_data(self, **kwargs):
        context = super(MembershipListView, self).get_context_data(**kwargs)
        context['account'] = get_object_or_404(Account, pk = self.kwargs.get('account_pk', None))
        return context