# Generated by Django 5.0.2 on 2024-02-16 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_check_order_alter_check_pdf_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='pdf_file',
            field=models.FileField(blank=True, help_text='ссылка на созданный PDF-файл', null=True, upload_to='pdf'),
        ),
    ]
