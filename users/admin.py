from django.contrib import admin
from .models import User
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    #is_student = forms.BooleanField(label='is student', required=False, widget=forms.CheckboxInput)
    #is_teacher = forms.BooleanField(label='is teacher', required=False, widget=forms.CheckboxInput)

    class Meta:
        model = User
        fields = ('__all__')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        return password2
    
   # def usertype(self):
   #     is_student=self.get("is_student")
   #     is_teacher=self.get("is_teacher")
   #     if (user.is_teacher==True) and (user.is_student==True):
   #         raise forms.ValidationError('user cant be both teacher and student ')
   #     return is_teacher

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser','is_student','is_teacher')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
   # def usertype(self):
   #     is_student=self.get("is_student")
   #     is_teacher=self.get("is_teacher")
   #     if user.is_teacher and user.is_student:
   #         raise forms.ValidationError('user cant be both teacher and student ')

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_teacher','is_student')
    list_filter = ('is_teacher','is_student')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser','is_student','is_teacher',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
