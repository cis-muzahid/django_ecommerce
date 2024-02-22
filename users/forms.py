
from django import forms
from users.models import CustomUser, Role, Permission


class CutomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password']


    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)



class UserRoleForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = ['name', 'permissions']


class UserPermissionForm(forms.ModelForm):

    class Meta:
        model = Permission
        fields = ['name']