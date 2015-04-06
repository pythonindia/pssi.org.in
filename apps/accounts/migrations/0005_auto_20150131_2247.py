# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20141130_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershipapplication',
            name='status',
            field=models.CharField(max_length=1, verbose_name='Membership Application Status', default='u', choices=[('u', 'Under Review'), ('a', 'Approved'), ('r', 'Rejected')]),
            preserve_default=True,
        ),
    ]
