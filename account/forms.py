from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from crispy_forms.layout import Submit, Fieldset, Layout, Button, HTML
from django import forms
from models import Profile, Account, Membership, FundTransfer
from django.forms.forms import Form
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from paypal.standard import conf

class SubmitButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return '<input type="submit" name="%s" value="%s">' % (html.escape(name), html.escape(value))


class SubmitButtonField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = SubmitButtonWidget

        super(SubmitButtonField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return value

class PayPalForm(PayPalPaymentsForm):
    action_url = conf.POSTBACK_ENDPOINT
    if settings.PAYPAL_TEST:
        action_url = conf.SANDBOX_POSTBACK_ENDPOINT
    payment_amounts = ((10.0,'10 euro'),(25.0,'25 euro'),(100.0,'100 euro'))
    amount = forms.ChoiceField(choices=payment_amounts, widget=forms.Select(), label=(u'Amount to pay'), required=True)
    
    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_action = action_url
    helper.add_input(Submit('submit', 'Pay via PayPal'))

class UserCreateForm(UserCreationForm):

    email = forms.EmailField(label=(u'Email'))
    #first_name = forms.CharField(label=(u'First name'))
    #last_name = forms.CharField(label=(u'Last name'))
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(Fieldset('Registration', 'email','password1','password2'))
        self.helper.add_input(Submit('submit', 'Register'))
        self.helper.form_class = 'form-vertical'
        super(UserCreateForm, self).__init__(*args, **kwargs)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-vertical'
        self.helper.layout = Layout(
            Fieldset(
            'Login',
            'username',
            'password',
            HTML("""
                 <div class="row">
                    <div class="col-sm-2">
                    <input type = 'submit' value='Login' class='btn-block btn btn-primary'>
                    </div>
                    <div class="col-sm-4">
                    <a href="{% url 'register' %}" class="">Don't have an account? Register</a>
                    </div>
                 </div>
                 <div class="row">
                  <div class="col-sm-2">
                 <p>or login with:</p>
                 </div>
                 </div>
                 <div class="row">
                    <div class="col-sm-2">
                    <a href="{% url 'socialauth_begin' 'facebook' %}" class="btn-block btn btn-facebook-inversed"><i class="fa fa-facebook"></i> Facebook </a>
                    </div>
                    <div class="col-sm-2">
                    <a href="{% url 'socialauth_begin' 'google-oauth2' %}" class="btn-block btn btn-googleplus-inversed"><i class="fa fa-google-plus"></i> Google+ </a>
                                        </div>
                    <div class="col-sm-2">
                    <a href="{% url 'socialauth_begin' 'github' %}" class="btn-block btn btn-github-inversed"><i class="fa fa-github"></i> Github </a>
                    </div>
             </div>
                """),
            )
        )
        #self.helper.add_input(Submit('submit', 'Login'))
        super(LoginForm, self).__init__(*args, **kwargs)

class UserUpdate(ModelForm):
    username = forms.CharField(required=True, widget=forms.HiddenInput)
    #first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    #last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
    
    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        print User.objects.filter(email=email).exclude(username=username).count()
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update'))
        self.helper.form_class = 'form-vertical'
        super(UserUpdate, self).__init__(*args, **kwargs)

class AccountForm(ModelForm):
    
    creator = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = Account
        exclude = ('deleted','users','total_earnings','total_spendings','personal')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-vertical'
        self.helper.add_input(Submit('submit', 'Save'))
        super(AccountForm, self).__init__(*args, **kwargs)



class MembershipForm(ModelForm):
    
    account = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.HiddenInput)
    #TODO att here autocomplete
    class Meta:
        model = Membership
        exclude = ('date_created')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-vertical'
        self.helper.add_input(Submit('submit', 'Save'))
        super(MembershipForm, self).__init__(*args, **kwargs)

class FundTransferForm(ModelForm):
    
    class Meta:
        model = FundTransfer
        exclude = ('date_created')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        #TODO Filter accounts - show only the ones belonging to this user
     
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-vertical'
        self.helper.add_input(Submit('submit', 'Transfer funds'))
        super(FundTransferForm, self).__init__(*args, **kwargs)
