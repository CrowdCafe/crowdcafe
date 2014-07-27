# Create your views here.
import logging
import random

from django.contrib.auth.models import User, Group
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login
from django.core.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.views.generic.list import ListView
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView

from CrowdCafe.settings_credentials import MC_KEY
from forms import LoginForm, UserCreateForm, AccountForm, MembershipForm, UserUpdate, PayPalForm, FundTransferForm
from models import Account, Membership, FundTransfer


log = logging.getLogger(__name__)

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
                login(request, user)
                return redirect('account-list')
        return render(request,
                      template_name,
                      {'form': user_form})
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreateForm()
    return render(request, template_name, args)


#TODO - does not work
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
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        log.debug('logged user ' + str(user))
        if user is not None:
            login(request, user)
            return redirect('account-list')
    form = LoginForm()
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))


# -------------------------------------------------------------
# Accounts
# -------------------------------------------------------------

class AccountListView(ListView):
    model = Account
    template_name = "account/account_list.html"

    def get_queryset(self):
        return Account.objects.filter(users__in=[self.request.user.id])  #TODO make sure it is correct

    def get_context_data(self, **kwargs):
        context = super(AccountListView, self).get_context_data(**kwargs)
        context['token'] = Token.objects.get(user=self.request.user)
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
        log.debug(form.errors)
        return CreateView.form_invalid(self, form)

    def form_valid(self, form):
        log.debug("saved")
        account = form.save()
        account.save()
        membership, created = Membership.objects.get_or_create(user=self.request.user, permission='AN', account=account)

        return redirect(reverse('account-list'))


class AccountUpdateView(UpdateView):
    model = Account
    template_name = "kitchen/crispy.html"
    form_class = AccountForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        log.debug(form.errors)
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        return get_object_or_404(Account, pk=self.kwargs.get('account_pk', None), users__in=[self.request.user.id])

    def form_valid(self, form):
        log.debug("updated")
        account = form.save()
        return redirect(reverse('account-list'))


class PayPalPayment(FormView):
    template_name = "kitchen/crispy.html"
    form_class = PayPalForm

    def get_initial(self):
        initial = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "currency_code": "EUR",
            "item_name": "CrowdCafe Credit",
            "invoice": str(self.kwargs.get('account_pk', None)) + '|' + str(random.randint(1000000, 9999999)),
            "notify_url": settings.APP_URL + reverse('paypal-ipn'),
            "return_url": settings.APP_URL + reverse('account-payment-accept'),
            "cancel_return": settings.APP_URL + reverse('account-list'),
            "custom": self.kwargs.get('account_pk', None)
        }
        return initial


@csrf_exempt
def acceptPayment(request):
    log.debug(request.POST)
    return redirect(reverse('account-list'))


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
        membership, created = Membership.objects.get_or_create(user=self.request.user, permission='AN', account=account)

        return redirect(reverse('account-list'))


# -------------------------------------------------------------
# Membership
# -------------------------------------------------------------

class MembershipCreateView(CreateView):
    #TODO fix - preselection of users to select from
    model = Membership
    template_name = "kitchen/crispy.html"
    form_class = MembershipForm

    def get_initial(self):
        initial = {}
        initial['account'] = get_object_or_404(Account, pk=self.kwargs.get('account_pk', None),
                                               users__in=[self.request.user.id])
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
        log.debug(form.errors)
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        return get_object_or_404(Membership, pk=self.kwargs.get('member_pk', None),
                                 account__users__in=[self.request.user.id])

    def form_valid(self, form):
        log.debug("updated")
        membership = form.save()
        return redirect(reverse('member-list', kwargs={'account_pk': membership.account.id}))


class MembershipListView(ListView):
    template_name = "account/membership_list.html"
    model = Membership

    def get_queryset(self):
        account = get_object_or_404(Account, pk=self.kwargs.get('account_pk', None), users__in=[self.request.user.id])
        return Membership.objects.filter(account=account)

    def get_context_data(self, **kwargs):
        context = super(MembershipListView, self).get_context_data(**kwargs)
        context['account'] = get_object_or_404(Account, pk=self.kwargs.get('account_pk', None))
        return context


# -------------------------------------------------------------
# Fund Transfers
# -------------------------------------------------------------
class FundTransferCreateView(CreateView):
    model = FundTransfer
    template_name = "kitchen/crispy.html"
    form_class = FundTransferForm

    def get_initial(self):
        initial = {}
        initial['creator'] = self.request.user
        return initial

    def form_invalid(self, form):
        log.debug("form is not valid")
        return CreateView.form_invalid(self, form)

    def form_valid(self, form):
        log.debug("saved")
        #TODO test it
        if self.request.user in form['from_account'].members and form['from_account'].balance >= form['amount']:
            form.save()
        return redirect(reverse('account-list'))


class FundTransferListView(ListView):
    model = FundTransfer
    template_name = "account/fundtransfer_list.html"

    def get_queryset(self):
        account = get_object_or_404(Account, pk=self.kwargs.get('account_pk', None), users__in=[self.request.user.id])

        return FundTransfer.objects.filter(
            Q(from_account=account) | Q(to_account=account))  #TODO make sure it is correct

    def get_context_data(self, **kwargs):
        context = super(FundTransferListView, self).get_context_data(**kwargs)
        return context


@require_http_methods(["POST","GET"])
@csrf_exempt
#TODO test me when online
#FIXME set a consistent key and specify it in mailchimp
#FIXME test this, only in production or on server that can be accesssed by mailchimp
def webHookSuperUser(request):
    '''
    this view handles the webhook from mailchimp, pls refer to this for details
    http://apidocs.mailchimp.com/webhooks/#email-address-changes
    '''
    if request.method == 'GET':
        return HttpResponse(status=200)
    else:
        # get beacuse it's from url
        url_key = request.GET['key']
        log.debug("key %s",url_key)
        if url_key != MC_KEY:
            log.warning('wrong key, someone trying to mess up?')
            return Http404('Nope')
        else:
            event_type = request.POST['type']
            log.debug("Type %s",event_type)
            # not sure it's but should work
            data = request.POST['data']
            log.debug("data %s",data)
            email = request.POST['data[merges][EMAIL]']
            log.debug("email: %s",email)
            user = get_object_or_404(User, email=email)
            g = Group.objects.get(name='superuser')
            if event_type == 'subscribe':
                g.user_set.add(user)
                g.save()
                log.debug('added')
            elif event_type == 'unsubscribe':
                g.user_set.remove(user)
                log.debug('removed')
                g.save()
                #else nothign
            return HttpResponse(status=200)
            # subscribe or unsubscibe
