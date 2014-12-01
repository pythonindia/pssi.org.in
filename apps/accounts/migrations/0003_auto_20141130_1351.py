# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_membership_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='status',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='application_status',
            field=models.CharField(verbose_name='Membership Application Status', default='u', max_length=1, choices=[('u', 'Under Review'), ('a', 'Approved')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='learned_about_pssi',
            field=models.TextField(verbose_name='How did you come to know about PSSI?', default='I came to know about PSSI from ...'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profession',
            field=models.CharField(max_length=200, default='I work/study at ...', help_text='What do you do?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(default='I like ...', help_text='Few lines about yourself'),
            preserve_default=True,
        ),
    ]
