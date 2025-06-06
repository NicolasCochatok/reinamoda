# Generated by Django 3.2.20 on 2025-05-13 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20250511_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='SizeOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria_aplicable', models.CharField(choices=[('anillo', 'Anillo'), ('pulsera', 'Pulsera'), ('collar', 'Collar'), ('aro', 'Aro'), ('dije', 'Dije')], max_length=20)),
                ('valor', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('color', 'Color'), ('talla', 'Talla')], max_length=100),
        ),
    ]
