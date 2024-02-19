from django.db import models


class Printer(models.Model):
    class CHOICES_TYPE(models.TextChoices):
        KT = 'KT', 'kitchen'
        CL = 'CL', 'client'

    name = models.CharField(
        max_length=50, help_text='название принтера')
    api_key = models.CharField(
        max_length=50, help_text='ключ доступа к API')
    check_type = models.CharField(
        max_length=50,
        choices=CHOICES_TYPE.choices,
        help_text='тип чека которые печатает принтер'
    )
    point_id = models.IntegerField(
        help_text='точка к которой привязан принтер')

    def __str__(self) -> str:
        return self.name


class Check(models.Model):
    class CHOICES_TYPE(models.TextChoices):
        KT = 'KT', 'kitchen'
        CL = 'CL', 'client'

    class CHOICES_STATUS(models.TextChoices):
        NW = 'NW', 'new'
        RN = 'RN', 'rendered'
        PR = 'PR', 'printed'

    printer_id = models.ForeignKey(
        Printer,
        on_delete=models.CASCADE,
        related_name='printers',
        help_text='принтер')
    type = models.CharField(max_length=50, choices=CHOICES_TYPE.choices,
                            help_text='тип чека')
    order = models.JSONField(help_text='информация о заказе')
    status = models.CharField(
        max_length=50,
        choices=CHOICES_STATUS.choices,
        default=CHOICES_STATUS.NW,
        help_text='статус чека',
    )
    pdf_file = models.FileField(
        upload_to='', help_text='ссылка на созданный PDF-файл', blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.printer_id.name} +{self.printer_id.check_type}'
