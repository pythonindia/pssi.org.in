# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20141130_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipApplication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='u', max_length=1, choices=[('u', 'Under Review'), ('a', 'Approved')], verbose_name='Membership Application Status')),
                ('profile', models.OneToOneField(to='accounts.UserProfile')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='application_status',
        ),
    ]
