# # forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# # from django.contrib.auth.models import User
# from .models import CustomUser


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserChangeForm

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


class RealizedDateForm(forms.Form):
    realized_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))



class GetOtpForm(forms.Form):
    admission_number = forms.CharField(max_length=20, required=True)
    mobile_number = forms.CharField(max_length=15, required=True)

class VerifyOtpForm(forms.Form):
    otp_1 = forms.CharField(max_length=1, required=True)
    otp_2 = forms.CharField(max_length=1, required=True)
    otp_3 = forms.CharField(max_length=1, required=True)
    otp_4 = forms.CharField(max_length=1, required=True)

    def clean(self):
        cleaned_data = super().clean()
        otp = cleaned_data.get('otp_1') + cleaned_data.get('otp_2') + cleaned_data.get('otp_3') + cleaned_data.get('otp_4')
        cleaned_data['otp'] = otp
        return cleaned_data


# working


class CustomUserCreationForm(forms.ModelForm):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Super Admin'),
    )

    # Use a dropdown to select role and map it to `is_staff` and `is_superuser`
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    username = forms.CharField(label="Teacher Name", required=True)
    first_name = forms.CharField(
        label="Mobile Number",
        required=True,
        max_length=10,
        min_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Enter mobile number'})
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'role', 'password')  # Customize fields here

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Modify field labels for mobile number (first_name)
        self.fields['first_name'].label = "Mobile Number"
        self.fields['email'].required = True

        # Customize the teacher_name field to allow spaces
        self.fields['username'].widget.attrs.update({
            'pattern': r'^[A-Za-z ]+$',  # Regular expression to allow only letters and spaces
            'title': "Teacher name should contain only letters and spaces"
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Ensure teacher name contains only valid characters (letters and spaces)
        if not all(c.isalpha() or c.isspace() for c in username):
            raise ValidationError("Teacher name can only contain letters and spaces.")
        
        return username
    
    def clean_first_name(self):
        mobile_number = self.cleaned_data.get('first_name')

        # Ensure that the mobile number is exactly 10 digits long
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits long.")
        
        if User.objects.filter(first_name=mobile_number).exists():
            raise ValidationError("A user with that mobile number already exists.")

        return mobile_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        """ Save the user data with custom handling for role and password. """
        user = super().save(commit=False)

        # Map the role field to is_staff and is_superuser
        role = self.cleaned_data.get('role')
        print('role -----------',role)
        if role == '1':  # Super Admin
            user.is_staff = True
            user.is_superuser = True
        else:  # Admin
            user.is_staff = True
            user.is_superuser = False

        # Set the password
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user



class CustomUserChangeForm(UserChangeForm):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Super Admin'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role", required=True)
    first_name = forms.CharField(
        label="Mobile Number",
        required=True,
        max_length=10,
        min_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Enter mobile number'})
    )
    # teacher_name = forms.CharField(label="Teacher Name", required=True)
    username = forms.CharField(label="Teacher Name", required=True)

    class Meta:
        model = User
        # fields = ('email', 'username', 'first_name', 'role', 'teacher_name')
        fields = ('email', 'username', 'first_name', 'role', 'password') 

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

        # Set initial role based on is_superuser
        if self.instance:
            self.fields['role'].initial = '1' if self.instance.is_superuser else '0'

    def clean_first_name(self):
        mobile_number = self.cleaned_data.get('first_name')

        # Ensure that the mobile number is exactly 10 digits long
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits long.")
        
        if User.objects.filter(first_name=mobile_number).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with that mobile number already exists.")

        return mobile_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with that email already exists.")
        return email
    
    def save(self, commit=True):
        """ Save the user data with custom handling for role. """
        user = super().save(commit=False)

        # Map the role field to is_staff and is_superuser
        role = self.cleaned_data.get('role')
        user.is_staff = role == '1'  # Super Admin
        user.is_superuser = role == '1'

        # Update the additional fields
        user.first_name = self.cleaned_data.get('first_name')
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')

        if commit:
            user.save()
        return user
    

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='Enter OTP', max_length=6, required=True)

