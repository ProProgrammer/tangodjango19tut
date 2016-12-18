# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_category__page_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='_page_count',
        ),
    ]
