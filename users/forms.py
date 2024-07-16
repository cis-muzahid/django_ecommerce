from django import forms
from users.models import CustomUser, Role, Permission, UserAddress


class CutomUserForm(forms.ModelForm):
    """ Form for user """
    user_role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Select a role"
    )
    class Meta:
        model = CustomUser
        fields = ['mobile_no', 'email', 'first_name', 'last_name', 'user_role', 'password', 'user_image']


class UserRoleForm(forms.ModelForm):
    """ Form for user's role """
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False  # Set to True if a role must have at least one permission
    )
    class Meta:
        model = Role
        fields = ['name', 'permissions']


class UserPermissionForm(forms.ModelForm):
    """ Form for user's permission """
    class Meta:
        model = Permission
        fields = ['name']

class LoginForm(forms.Form):
    """ Form for user's login """
    email = forms.EmailField(label='Your email', max_length=100)
    password = forms.CharField(label='Your password', max_length=100,widget=forms.PasswordInput()) 

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email):
            raise forms.ValidationError('Email does not exists!')
        return email

class AddressForm(forms.ModelForm):
    """ Form for user's address """
    class Meta:
        model = UserAddress
        fields = ['street', 'city', 'state', 'postal_code', 'country', 'is_default']