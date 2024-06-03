from django.contrib import admin
from users.models import CustomUser, Customer, Staff
from django import forms
from backend.enums.user import User as UserEnum


class UserTypeFilter(admin.SimpleListFilter):
    title = 'User Type'
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return CustomUser.USER_TYPE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_type=self.value())
        return queryset


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = (UserTypeFilter,)


class CustomerForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['password'].initial = self.instance.user.password

    def save(self, commit=True):
        instance = super(CustomerForm, self).save(commit=False)
        return instance


class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)


class StaffAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Staff, StaffAdmin)
