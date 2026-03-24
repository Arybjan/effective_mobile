from django.contrib import admin
from .models import Role, BusinessElement, AccessRoleRule

admin.site.register(Role)
admin.site.register(BusinessElement)
admin.site.register(AccessRoleRule)
