from django.contrib import admin
from real.models import Reactor, Stage

class ReactorAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'V', 'N', 'element', 'gamaI',
     'gamaXe', 'gamaPm')

class StageAdmin(admin.ModelAdmin):
    list_display = ('myreactor', 'reactor_id', 'sn', 'power', 'phy')

admin.site.register(Reactor, ReactorAdmin)
admin.site.register(Stage, StageAdmin)