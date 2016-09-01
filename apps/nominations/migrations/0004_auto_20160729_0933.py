# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominations', '0003_nominationtype_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nominationtype',
            name='description',
            field=models.TextField(verbose_name='Description about nomination', default=''),
        ),
    ]
