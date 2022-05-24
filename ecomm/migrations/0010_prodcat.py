# Generated by Django 4.0.3 on 2022-05-24 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0009_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.category')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.product')),
            ],
            options={
                'unique_together': {('cat_id', 'product_id')},
            },
        ),
    ]
