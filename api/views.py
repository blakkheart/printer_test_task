import json
import base64
import requests
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Printer, Check
from rest_framework import status
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.core.files.uploadedfile import SimpleUploadedFile


@api_view(['POST'])
def create_checks(request):

    data = request.data
    order_id = data.get('id')
    point_id = data.get('point_id')

    # получить все принтеры на точке

    printers = Printer.objects.filter(point_id=point_id)

    # проверить наличие принтеров на точке

    if not printers:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'error': 'No printers on that address'})

    # проверить, что чек не создавался

    check_exist = Check.objects.filter(order__id=order_id)
    # if check_exist:
    #     return Response(status=status.HTTP_400_BAD_REQUEST,
    #                     data={'error': 'Check allready exists'})
    # создать для данного заказа чеки для всех принтеров

    for printer in printers:
        check_type = printer.check_type
        print(check_type)
        if check_type == 'CL':
            html = render_to_string(
                '../templates/client_check.html', context={'data_client': request.data})
            # template = get_template('client_check.html')
        else:
            html = render_to_string(
                '../templates/kitchen_check.html', context={'data_kitchen': request.data})
            # template = get_template('kitchen_check.html')
        # html = template.render({'data': data})

        # print(type(html))

        # pdf
        # print(html)

        url = 'http://127.0.0.1:7771/'
        content = base64.b64encode(html.encode('utf-8')).decode("utf-8")
        data = {
            'contents': content,
        }

        headers = {
            'Content-Type': 'application/json',    # This is important
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        pdf_file = SimpleUploadedFile(
            'file.pdf', response.content, content_type='application/pdf')
        # Save the response contents to a file
        # print(response.content)
        # pdf
        # dir = str(settings.BASE_DIR) + '/templates/file.pdf'
        # with open(dir, 'wb') as f:
        #     f.write(response.content)
        Check.objects.create(
            printer_id=printer,
            type=check_type,
            order=request.data,
            pdf_file=pdf_file
        )

    # генерация ПДФ через воркеров ?

    return Response(status=status.HTTP_200_OK,
                    data={"ok": "Чеки успешно созданы"})


@api_view(['GET'])
def get_new_cheks(request):
    checks = Check.objects.all().first()

    return Response({'checks': 1})


@api_view(['GET'])
def get_check(request):
    checks = Check.objects.all().first()

    return Response({'checks': 1})
