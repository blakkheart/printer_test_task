from django.db import models


class Printer(models.Model):
    '''Модель принтера.'''
    class CHOICES_TYPE(models.TextChoices):
        KT = 'KT', 'kitchen'
        CL = 'CL', 'client'

    name = models.CharField(
        max_length=50, help_text='Название принтера')
    api_key = models.CharField(
        max_length=50, help_text='Ключ доступа к API')
    check_type = models.CharField(
        max_length=50,
        choices=CHOICES_TYPE.choices,
        help_text='Тип чека, которые печатает принтер.'
    )
    point_id = models.IntegerField(
        help_text='Точка, к которой привязан принтер')

    def __str__(self) -> str:
        return self.name


class Check(models.Model):
    '''Модель чека.'''
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
        help_text='Принтер')
    type = models.CharField(max_length=50, choices=CHOICES_TYPE.choices,
                            help_text='Тип чека')
    order = models.JSONField(help_text='Информация о заказе')
    status = models.CharField(
        max_length=50,
        choices=CHOICES_STATUS.choices,
        default=CHOICES_STATUS.NW,
        help_text='Статус чека',
    )
    pdf_file = models.FileField(
        upload_to='',
        help_text='Ссылка на созданный PDF-файл',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f'{self.printer_id.name} + {self.printer_id.check_type}'
