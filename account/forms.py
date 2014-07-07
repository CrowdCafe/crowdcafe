from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from crispy_forms.layout import Submit, Fieldset, Layout, Button, HTML
from django import forms
from models import Profile, Account, Membership
from django.forms.forms import Form
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

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
                    <div class="col-sm-2">
                      <a href="{% url 'socialauth_begin' 'dropbox' %}" class="btn-block btn btn-dropbox-inversed"><i class="fa fa-dropbox"></i> Dropbox </a>
                    </div>
                    
             </div>
                """),
            )
        )
        #self.helper.add_input(Submit('submit', 'Login'))
        super(LoginForm, self).__init__(*args, **kwargs)

class UserUpdate(ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(pk=self.request.id).count():
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

    class Meta:
        model = Membership
        exclude = ('date_created')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-vertical'
        self.helper.add_input(Submit('submit', 'Save'))
        super(MembershipForm, self).__init__(*args, **kwargs)