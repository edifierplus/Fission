from django.db import models

class Argument(models.Model):
    pub_date = models.DateTimeField('date published')
    A = models.DecimalField(max_digits=19, decimal_places=10)
    k = models.DecimalField(max_digits=19, decimal_places=10)
    phy = models.DecimalField(max_digits=19, decimal_places=10)
    x_min = models.DecimalField(max_digits=19, decimal_places=10)
    x_max = models.DecimalField(max_digits=19, decimal_places=10)
    y_min = models.DecimalField(max_digits=19, decimal_places=10)
    y_max = models.DecimalField(max_digits=19, decimal_places=10)
    delta_x = models.DecimalField(max_digits=19, decimal_places=10)

