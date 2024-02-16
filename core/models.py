from django.db import models


class Printer(models.Model):
    CHOICES_TYPE = (
        ('KT', 'kitchen'),
        ('CL', 'client'),
    )

    name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=50)
    check_type = models.CharField(max_length=50, choices=CHOICES_TYPE)
    point_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Check(models.Model):
    CHOICES_TYPE = (
        ('KT', 'kitchen'),
        ('CL', 'client'),
    )
    CHOICES_STATUS = (
        ('NW', 'new'),
        ('RN', 'rendered'),
        ('PR', 'printed'),
    )

    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=CHOICES_TYPE)
    order = models.JSONField()
    status = models.CharField(max_length=50, choices=CHOICES_STATUS)
    pdf_file = models.FileField(upload_to='pdf')

    def __str__(self) -> str:
        return self.order
