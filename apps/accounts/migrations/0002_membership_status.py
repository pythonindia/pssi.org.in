# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='status',
            field=models.CharField(max_length=1, choices=[('u', 'Under Review'), ('a', 'Approved')], default='u', verbose_name='Status'),
            preserve_default=True,
        ),
    ]
