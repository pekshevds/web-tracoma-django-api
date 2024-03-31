# Generated by Django 3.2.23 on 2024-01-20 11:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0002_auto_20240120_1352'),
        ('warehouse_app', '0006_auto_20240120_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cargo', to='order_app.order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='incomingitem',
            name='incoming',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='warehouse_app.incoming'),
        ),
        migrations.CreateModel(
            name='CargoRegistry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('period', models.DateTimeField(verbose_name='Период')),
                ('register', models.UUIDField()),
                ('quant', models.DecimalField(decimal_places=3, max_digits=15)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse_app.cargo')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse_app.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]