# -*- coding: UTF-8 -*-
from django.db import models

class Reactor(models.Model):
    pub_date = models.DateTimeField('datetime built')
    #反应堆体积(m^3)
    V = models.DecimalField(max_digits=50, decimal_places=8)
    #核密度(10^28m^-3)
    N = models.DecimalField(max_digits=50, decimal_places=8)
    #元素种类(U-233, U-235, Pu-239)
    element = models.CharField(max_length = 10)
    #I裂变产额
    gamaI = models.DecimalField(max_digits=10, decimal_places=8)
    #Xe裂变产额
    gamaXe = models.DecimalField(max_digits=10, decimal_places=8)
    #Pm裂变产额
    gamaPm = models.DecimalField(max_digits=10, decimal_places=8)
    #元素微观裂变截面
    sigmaf = models.DecimalField(max_digits=50, decimal_places=8)
    #元素微观吸收截面
    sigmaa = models.DecimalField(max_digits=50, decimal_places=8)
    
    def __unicode__(self):
        return "reactor"+str(self.id)

class Stage(models.Model):
    #关于反应堆的外键
    myreactor = models.ForeignKey(Reactor)
    #该阶段所属反应堆的id
    reactor_id = models.IntegerField()
    #该阶段编号
    sn = models.IntegerField()
    #持续时间(h)
    t = models.DecimalField(max_digits=50, decimal_places=8)
    #反应堆功率(MW)
    power = models.DecimalField(max_digits=50, decimal_places=8)
    #中子通量密度10^28m^-2s^-1(m^3, /m, MW)
    phy = models.DecimalField(max_digits=50, decimal_places=30)
    #I核密度(10^28m^-3)
    dens_I = models.DecimalField(max_digits=50, decimal_places=8)
    #Xe核密度(10^28m^-3)
    dens_Xe = models.DecimalField(max_digits=50, decimal_places=8)
    #Pm核密度(10^28m^-3)
    dens_Pm = models.DecimalField(max_digits=50, decimal_places=8)
    #Sm核密度(10^28m^-3)
    dens_Sm = models.DecimalField(max_digits=50, decimal_places=8)

    def __unicode__(self):
        return "reactor"+str(self.reactor_id)+"_stage"+str(self.sn)