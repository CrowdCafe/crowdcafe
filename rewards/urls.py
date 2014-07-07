from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
import views

urlpatterns = patterns('',
    #-------------------------------------------------------------------------------
    # Vendors
    url(r'accounts/(?P<account_pk>\d+)/vendors/$', login_required(views.VendorListView.as_view()), name='vendor-list'),
    url(r'accounts/(?P<account_pk>\d+)/vendors/create/$', login_required(views.VendorCreateView.as_view()), name='vendor-create'),
    url(r'vendors/(?P<vendor_pk>\d+)/update/$', login_required(views.VendorUpdateView.as_view()), name='vendor-update'),
    #-------------------------------------------------------------------------------
    # Rewards
    url(r'vendors/(?P<vendor_pk>\d+)/rewards/$', login_required(views.RewardListView.as_view()), name='reward-list'),
    url(r'vendors/(?P<vendor_pk>\d+)/rewards/create/$', login_required(views.RewardCreateView.as_view()), name='reward-create'),
    url(r'rewards/(?P<reward_pk>\d+)/update/$', login_required(views.RewardUpdateView.as_view()), name='reward-update'),
    #-------------------------------------------------------------------------------
    # Coupons
    url(r'rewards/(?P<reward_pk>\d+)/coupons/$', login_required(views.CouponListView.as_view()), name='coupon-list'),
    url(r'coupons/(?P<coupon_pk>\d+)/update/$', login_required(views.CouponUpdateView.as_view()), name='coupon-update'),
)
