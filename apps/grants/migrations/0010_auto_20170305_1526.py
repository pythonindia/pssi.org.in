# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0009_auto_20170305_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localconfrequest',
            name='description',
            field=django_markdown.models.MarkdownField(verbose_name='Say us about the conference', help_text='\nGive us more information about the conference. These details are target audience, \nevent structure, sponsors, partners, local community, previous events details, WiFi, Transport, accomodation etc ...\n\nTake your time and fill the application. The markdown format is supported\n'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localconfrequest',
            name='team_members',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='team_members', null=True),
            preserve_default=True,
        ),
    ]
