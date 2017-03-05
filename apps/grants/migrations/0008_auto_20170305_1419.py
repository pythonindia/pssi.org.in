# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0007_localconfrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='localconfrequest',
            name='transfered_amount',
            field=models.FloatField(verbose_name='Transferred amount in INR', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localconfrequest',
            name='description',
            field=django_markdown.models.MarkdownField(help_text='\nGive us more information about the conference. These details are target audience, \nevent structure, sponsors, partners, local community, previous events details, WiFi, Transport, accomodation etc ...\n\nTake your time and fill the application.\n'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localconfrequest',
            name='note',
            field=django_markdown.models.MarkdownField(blank=True, null=True, help_text='Any specific note to the board'),
            preserve_default=True,
        ),
    ]
