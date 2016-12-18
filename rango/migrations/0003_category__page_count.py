# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20161218_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='_page_count',
            field=models.IntegerField(default=0, verbose_name='Page Count', db_column='page_count'),
        ),
    ]
