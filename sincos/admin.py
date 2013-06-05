from django.contrib import admin
from sincos.models import Argument

class ArgumentAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'A', 'k', 'phy', 'x_min', 'x_max', 'y_min', 'y_max', 'delta_x')

admin.site.register(Argument, ArgumentAdmin)
