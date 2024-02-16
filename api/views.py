from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Printer, Check
from rest_framework import status

from django.template.loader import get_template


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
        if check_type == 'CL':
            template = get_template('client_check.html')
        else:
            template = get_template('kitchen_check.html')
        html = template.render({'data': data})

        Check.objects.create(
            printer_id=printer,
            type=check_type,
            order=request.data,
            # pdf_file ?
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


@csrf_exempt
def func(request):
    data = request.data
    order_id = data.get('id')
    point_id = data.get('point_id')

    printers = Printer.objects.filter(point_id=point_id)

    for printer in printers:
        check_type = printer.check_type
        if check_type == 'client':
            template = get_template('client_check.html')
        else:
            template = get_template('kitchen_check.html')

        context = request.data

        html = template.render(context)
        return html
