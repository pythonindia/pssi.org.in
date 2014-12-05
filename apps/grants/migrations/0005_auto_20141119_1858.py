# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0004_granttype_terms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='granttype',
            name='terms',
            field=models.TextField(null=True, verbose_name='Terms & Conditions', blank=True),
            preserve_default=True,
        ),
    ]
