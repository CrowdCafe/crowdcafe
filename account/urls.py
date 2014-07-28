from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    #url(r'^', include(router.urls)),
    #url(r'^user/$',create_user),
    
    #url(r'^auth/$',views.auth,name='auth'),
    url(r'^$',views.home),

    #TODO - we need to find a consistent way to call functions and classes
    url(r'^user/login/$',views.login_user,name='login'),
    url(r'^user/update/$',login_required(views.update_user),name='user-update'),
    url(r'^user/register/$', views.register_user, name='register'),
    url(r'^user/logout/$', login_required(views.logout_user), name='logout'),
    url(r'^user/mandrill$', views.webHookSuperUser, name = 'user-mandrill'),

    

    url(r'^accounts/$', login_required(views.AccountListView.as_view()), name='account-list'),
    url(r'^fundtransfers/create/$', login_required(views.FundTransferCreateView.as_view()), name='fundtransfer-create'),
    url(r'^accounts/create/$', login_required(views.AccountCreateView.as_view()), name='account-create'),
    url(r'^accounts/(?P<account_pk>\d+)/update/$', login_required(views.AccountUpdateView.as_view()), name='account-update'),
    url(r'^accounts/(?P<account_pk>\d+)/payment/request/$', login_required(views.PayPalPayment.as_view()), name='account-payment-request'),

    url(r'^accounts/payment/accept/$', login_required(views.acceptPayment), name='account-payment-accept'),
    url(r'^accounts/paypal/', include('paypal.standard.ipn.urls')),

    url(r'^accounts/(?P<account_pk>\d+)/transfers/$', login_required(views.FundTransferListView.as_view()), name='fundtransfer-list'),

    url(r'^accounts/(?P<account_pk>\d+)/members/$', login_required(views.MembershipListView.as_view()), name='member-list'),
    url(r'^accounts/(?P<account_pk>\d+)/members/create/$', login_required(views.MembershipCreateView.as_view()), name='member-create'),
    url(r'^members/(?P<member_pk>\d+)/update/$', login_required(views.MembershipUpdateView.as_view()), name='member-update'),

)
