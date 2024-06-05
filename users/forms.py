from django import forms
from users.models import CustomUser, Role, Permission, UserAddress


class CutomUserForm(forms.ModelForm):
    user_role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Select a role"
    )
    class Meta:
        model = CustomUser
        fields = ['mobile_no', 'email', 'first_name', 'last_name', 'user_role', 'password']


class UserRoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False  # Set to True if a role must have at least one permission
    )
    class Meta:
        model = Role
        fields = ['name', 'permissions']


class UserPermissionForm(forms.ModelForm):

    class Meta:
        model = Permission
        fields = ['name']

class LoginForm(forms.Form):
    email = forms.EmailField(label='Your email', max_length=100)
    password = forms.CharField(label='Your password', max_length=100,widget=forms.PasswordInput()) 

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email):
            raise forms.ValidationError('Email does not exists!')
        return email

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['street', 'city', 'state', 'postal_code', 'country']