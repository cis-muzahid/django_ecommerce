from django import forms
from users.models import CustomUser, Role, Permission


class CutomUserForm(forms.ModelForm):
    user_role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Select a role"
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_role', 'password']
    # role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)



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