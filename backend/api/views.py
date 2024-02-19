from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from wsgiref.util import FileWrapper

from api.tasks import generate_pdf_with_wkhtmltopdf
from core.models import Check, Printer


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
    if check_exist:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'error': 'Check allready exists'})

    # создать для данного заказа чеки для всех принтеров
    Check.objects.bulk_create(
        [
            Check.objects.create(
                printer_id=printer,
                type=printer.check_type,
                order=request.data,
            )
            for printer in printers
        ]
    )

    # вызвать воркера для создания pdf
    generate_pdf_with_wkhtmltopdf.delay(
        point_id=point_id, requst_data=request.data)
    return Response(status=status.HTTP_200_OK,
                    data={"ok": "Чеки успешно созданы"})


@api_view(['GET'])
def get_new_checks(request):
    api_key = request.query_params.get('api_key')
    checks = Check.objects.select_related(
        'printer_id').filter(status='RN')
    list_of_id = []
    for check in checks:
        if check.printer_id.api_key != api_key:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={"error": "Ошибка авторизации"})
        list_of_id.append({'id': check.pk})
    return Response({'checks': list_of_id})


@api_view(['GET'])
def get_check(request):
    api_key = request.query_params.get('api_key')
    check_id = request.query_params.get('check_id')
    check = Check.objects.select_related(
        'printer_id').filter(pk=check_id).first()
    if not check or check.status != 'RN':
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"error": "string"})
    if api_key != check.printer_id.api_key:
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={"error": "Ошибка авторизации"})
    response = FileResponse(
        FileWrapper(check.pdf_file),
        content_type='application/pdf',
        status=status.HTTP_200_OK,
        as_attachment=True
    )
    return response
