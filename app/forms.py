# # forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# # from django.contrib.auth.models import User
# from .models import CustomUser

# # class CustomUserCreationForm(UserCreationForm):
# #     class Meta:
# #         model = User
# #         fields = ('username', 'email', 'password1', 'password2')

# # class CustomUserChangeForm(UserChangeForm):
# #     class Meta:
# #         model = User
# #         fields = ('username', 'email', 'first_name', 'last_name')


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'mobile', 'role', 'password1', 'password2')

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'mobile', 'role', 'first_name', 'last_name')

from django import forms

class FeeNotApplicableForm(forms.Form):
    MONTH_CHOICES = [
        ('', 'Please Select Month'),
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]
    
    # Use ChoiceField instead of IntegerField
    fee_not_applicable_in_months = forms.ChoiceField(choices=MONTH_CHOICES, label="Fee Not Applicable in Months")
