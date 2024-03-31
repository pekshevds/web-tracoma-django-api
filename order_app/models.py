from django.db import models
from django.utils.dateformat import format
from main_app.base import Directory, Document
from main_app.services import ganerate_new_number


class Contractor(Directory):
    address1 = models.CharField(verbose_name="Адрес", max_length=255,
                                null=True, blank=True, default="")
    address2 = models.CharField(verbose_name="Адрес", max_length=255,
                                null=True, blank=True, default="")
    address3 = models.CharField(verbose_name="Адрес", max_length=255,
                                null=True, blank=True, default="")
    phone1 = models.CharField(verbose_name="Телефон", max_length=25,
                              null=True, blank=True, default="")
    phone2 = models.CharField(verbose_name="Телефон", max_length=25,
                              null=True, blank=True, default="")
    phone3 = models.CharField(verbose_name="Телефон", max_length=25,
                              null=True, blank=True, default="")

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        ordering = ["name"]


class Order(Document):

    sender = models.ForeignKey(
        Contractor, on_delete=models.PROTECT,
        verbose_name="Отправитель", related_name="sender",
        null=True, blank=True)
    sender_name = models.CharField(
        verbose_name="Наименование отправителя", max_length=150, default="")
    sender_address = models.CharField(verbose_name="Адрес", max_length=255,
                                      null=True, blank=True, default="")
    sender_phone = models.CharField(verbose_name="Телефон", max_length=25,
                                    default="")

    recipient = models.ForeignKey(
        Contractor, on_delete=models.PROTECT,
        verbose_name="Получатель", related_name="recipient",
        null=True, blank=True)
    recipient_name = models.CharField(
        verbose_name="Наименование получателя", max_length=150, default="")
    recipient_address = models.CharField(
        verbose_name="Адрес", max_length=255, default="")
    recipient_phone = models.CharField(
        verbose_name="Телефон", max_length=25, default="")

    def save(self, *args, **kwargs) -> None:
        if not self.number:
            self.number = ganerate_new_number(model=Order)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Заказ №{self.number} от {format(self.date, 'd F Y')}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-number"]
