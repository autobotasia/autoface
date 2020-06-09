# from allauth.account.forms import SignupForm, LoginForm, AddEmailForm, ChangePasswordForm, SetPasswordForm, ResetPasswordForm
# from allauth.socialaccount.forms import SignupForm, DisconnectForm
#
#
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
