# Generated by Django 4.0.3 on 2022-05-24 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0008_alter_order_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cat_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('cat_name', models.CharField(max_length=50)),
            ],
        ),
    ]