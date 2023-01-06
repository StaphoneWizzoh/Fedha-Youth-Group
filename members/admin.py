from django.contrib import admin

from .models import Registration, Guarantor, MemberExit


# class RegAdmin(admin.AdminSite):
#     list_display = ('first_name', 'date_joined')
#     list_filter = ('publisher', 'publication_date')


admin.site.register(Registration)
admin.site.register(Guarantor)
admin.site.register(MemberExit)
