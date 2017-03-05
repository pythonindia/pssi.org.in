# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0011_auto_20170305_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localconfcomment',
            name='local_conf',
            field=models.ForeignKey(to='grants.LocalConfRequest'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localconfrequest',
            name='location_address',
            field=models.TextField(help_text='Venue address with the venue name'),
            preserve_default=True,
        ),
    ]
