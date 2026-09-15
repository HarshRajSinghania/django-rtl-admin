from django.db import models


class Thing(models.Model):
    name = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)
    reference = models.CharField(max_length=60, blank=True)
    note = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    published_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "testapp"
        ordering = ("name",)

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return self.name.lower().replace(" ", "-")
