# from allauth.account.forms import SignupForm, LoginForm, AddEmailForm, ChangePasswordForm, SetPasswordForm, ResetPasswordForm
# from allauth.socialaccount.forms import SignupForm, DisconnectForm
from django.forms import ModelForm
from django.contrib.auth.models import User
# class MyCustomLoginForm(LoginForm):
#
#     def __init__(self, *args, **kwargs):
#         super(MyCustomLoginForm, self).__init__(*args, **kwargs)
#         self.fields["login"].widget.attrs.update({
#             'style': "color:black;"
#         })
#
#
# class MyCustomSignupForm(SignupForm):
#
#     def __init__(self, *args, **kwargs):
#         super(MyCustomSignupForm
# , self).__init__(*args, **kwargs)
#         for fieldname, field in self.fields.item():
#             field.widget.attrs.update(
#                 {
#                     'style': "color:black;"
#                 }
#             )
class UserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name",  "username")
