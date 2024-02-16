from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Printer, Check
from rest_framework import status


@api_view(['POST'])
def simple_view(request):
    data = request.data
    point_id = data.get('point_id')

    # получить все принтеры на точке

    printers = Printer.objects.filter(point_id=point_id)

    # проверить наличие принтеров на точке

    if not printers:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'No printers on that address'})

    # проверить, что чек не создавался

    # создать для данного заказа чеки для всех принтеров

    for printer in printers:
        check_type = printer.check_type
        Check.objects.create(
            printer_id=printer,
            type=check_type,
            order=request.data,
            # pdf_file ?
        )

    # генерация ПДФ через воркеров ?

    return Response({'data': point_id})


@api_view(['GET'])
def get_all_checks(request):
    checks = Check.objects.all().first()

    return Response({'checks': 1})
