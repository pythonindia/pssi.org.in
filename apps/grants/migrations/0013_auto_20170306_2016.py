# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0012_auto_20170305_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localconfteammember',
            name='local_conf',
        ),
        migrations.RemoveField(
            model_name='localconfteammember',
            name='team_member',
        ),
        migrations.DeleteModel(
            name='LocalConfTeamMember',
        ),
        migrations.AlterField(
            model_name='localconfrequest',
            name='description',
            field=django_markdown.models.MarkdownField(verbose_name='Say us about the conference', help_text='\nGive us more information about the conference. These details are target audience,\nevent structure, sponsors, partners, local community, previous events details, WiFi, Transport, accomodation etc ...\n\nTake your time and fill the application. The markdown format is supported\n'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localconfrequest',
            name='location_url',
            field=models.URLField(default='http://pssi.org.in', help_text='Your event location URL.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='localconfrequest',
            name='website',
            field=models.URLField(default='http://pssi.org.in', help_text='Your event website.'),
            preserve_default=False,
        ),
    ]
