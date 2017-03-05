# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0008_auto_20170305_1419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='localconfrequest',
            old_name='transfered_amount',
            new_name='transferred_amount',
        ),
    ]
