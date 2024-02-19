import json
import base64
import requests

from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string
from django.core.files.uploadedfile import SimpleUploadedFile
from celery import shared_task

from core.models import Check, Printer


@shared_task
@transaction.atomic
def generate_pdf_with_wkhtmltopdf(point_id: int, requst_data: dict) -> None:
    '''Функция для генерации pdf с помощью wkhtmltopdf.'''
    printers = Printer.objects.filter(point_id=point_id)
    for printer in printers:
        check_type = printer.get_check_type_display()

        if check_type == 'client':
            html = render_to_string(
                '../templates/client_check.html',
                context={'data_client': requst_data})
        elif check_type == 'kitchen':
            html = render_to_string(
                '../templates/kitchen_check.html',
                context={'data_kitchen': requst_data})
        else:
            raise ValueError('No such check_type!')

        url = 'http://wkhtmltopdf:8001/'
        content = base64.b64encode(html.encode('utf-8')).decode('utf-8')
        data = {
            'contents': content,
        }
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        pdf_file = SimpleUploadedFile(
            f'{requst_data.get("id")}_{check_type}.pdf',
            response.content,
            content_type='application/pdf'
        )
        with open(f'{settings.MEDIA_ROOT}/{requst_data.get("id")}_{check_type}.pdf', 'wb') as file:
            file.write(response.content)
        Check.objects.filter(
            printer_id=printer,
            type=printer.check_type,
            order=requst_data,
        ).update(pdf_file=pdf_file, status='RN')
