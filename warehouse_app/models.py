from django.db import models
from django.utils.dateformat import format
from main_app.base import Directory, Document, Registry
from order_app.models import Order
from main_app.services import ganerate_new_number


class TypeOfWarehouse(models.TextChoices):
    CA = "CA", "Контрагент (юридическое лицо, сторонний контрагент, подрядчик)"
    WH = "WH", "Склад (адрес, помещение)"
    EM = "EM", "Сотрудник (курьер, экспедитор)"


class Warehouse(Directory):
    type = models.CharField(verbose_name="Тип", max_length=2,
                            choices=TypeOfWarehouse.choices,
                            default=TypeOfWarehouse.WH)

    @property
    def type_to_show(self):
        return TypeOfWarehouse(self.type).label

    class Meta:
        verbose_name = "Место хранения"
        verbose_name_plural = "Места хранения"


class Cargo(Directory):
    order = models.ForeignKey(
        Order, related_name="cargo", on_delete=models.PROTECT,
        verbose_name="Заказ")
    width = models.DecimalField(
        verbose_name="Ширина, см", max_digits=15, decimal_places=3)
    height = models.DecimalField(
        verbose_name="Высота, см", max_digits=15, decimal_places=3)
    length = models.DecimalField(
        verbose_name="Длина, см", max_digits=15, decimal_places=3)
    weight = models.DecimalField(
        verbose_name="Вес, кг", max_digits=15, decimal_places=3)
    volume = models.DecimalField(
        verbose_name="Объем, м3", max_digits=15, decimal_places=5)
    description = models.CharField(verbose_name="Описание", max_length=150)

    class Meta:
        verbose_name = "Груз"
        verbose_name_plural = "Грузы"


class Incoming(Document):
    recipient = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, verbose_name="Получатель",
        null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.number:
            self.number = ganerate_new_number(model=Incoming)
        super().save(*args, **kwargs)

    def post(self, *args, **kwargs) -> None:
        self.save(*args, **kwargs)

        CargoRegistry.objects.filter(register=self.id).delete()
        for item in self.items.all():
            CargoRegistry.objects.create(
                period=self.date,
                register=self.id,
                cargo=item.cargo,
                warehouse=self.recipient,
                quant=1)

    def __str__(self) -> str:
        return f"Приходный ордер №{self.number} от {format(self.date, 'd F Y')}"

    class Meta:
        verbose_name = "Приходный ордер"
        verbose_name_plural = "Приходные ордера"
        ordering = ["-number"]


class IncomingItem(models.Model):
    incoming = models.ForeignKey(
        Incoming, on_delete=models.PROTECT, related_name="items"
    )
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)


class Outgoing(Document):

    sender = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, verbose_name="Отправитель",
        null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.number:
            self.number = ganerate_new_number(model=Outgoing)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Расходный ордер №{self.number} от {format(self.date, 'd F Y')}"

    class Meta:
        verbose_name = "Расходный ордер"
        verbose_name_plural = "Расходные ордера"
        ordering = ["-number"]


class OutgoingItem(models.Model):
    outgoing = models.ForeignKey(Outgoing, on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)


class Moving(Document):

    sender = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT,
        verbose_name="Отправитель", related_name="sender",
        null=True, blank=True)
    recipient = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT,
        verbose_name="Получатель", related_name="recipient",
        null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.number:
            self.number = ganerate_new_number(model=Moving)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Перемещение №{self.number} от {format(self.date, 'd F Y')}"

    class Meta:
        verbose_name = "Перемещение"
        verbose_name_plural = "Перемещения"
        ordering = ["-number"]


class MovingItem(models.Model):
    moving = models.ForeignKey(Moving, on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)


class CargoRegistry(Registry):
    register = models.UUIDField()
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    quant = models.DecimalField(max_digits=15, decimal_places=3)

    class Meta:
        verbose_name = "Движение груза"
        verbose_name_plural = "Движения грузов"
