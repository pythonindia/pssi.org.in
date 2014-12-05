# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0002_auto_20141022_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grantrequest',
            name='amount',
            field=models.FloatField(verbose_name='Requested amount'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grantrequest',
            name='comments',
            field=models.TextField(blank=True, null=True, help_text='If you have anything else to mention, please do it here.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grantrequest',
            name='event_date_from',
            field=models.DateField(help_text='Enter in following format: YYYY-MM-DD'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grantrequest',
            name='event_date_to',
            field=models.DateField(help_text='Enter in following format: YYYY-MM-DD'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grantrequest',
            name='support_from_other',
            field=models.TextField(verbose_name='Support from others (if any)', blank=True, null=True, help_text="If you've received any financial help from any other             organization, please mention."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grantrequest',
            name='talk_url',
            field=models.URLField(blank=True, null=True, help_text='Your talk/session should be accepted already for the grant         request to be processed.'),
            preserve_default=True,
        ),
    ]
