from typing import (
    List,
    Union
)
from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet


def ganerate_new_number(model: Model) -> int:
    """Вычисляет максимальный (последний) номер документа для модели model
    и возвращает следующий. Если последний номер 345, то вернет 346.
    """
    last_order = model.objects.all().order_by("number").last()
    if last_order:
        return last_order.number + 1
    return 1


def fetch_queryset_from_request_data(
        request: HttpRequest,
        model: Model) -> Union[QuerySet, List[Model]]:
    obj_id = request.GET.get("id")
    if obj_id:
        obj = get_object_or_404(model, id=obj_id)
        queryset = [obj]
    else:
        queryset = model.objects.all()
    return queryset
