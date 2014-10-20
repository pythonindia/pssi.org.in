# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GrantRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event_details', models.TextField()),
                ('event_date_to', models.DateTimeField()),
                ('event_date_from', models.DateTimeField()),
                ('talk_url', models.TextField(null=True, blank=True)),
                ('amount', models.FloatField()),
                ('accepted_amount', models.FloatField(default=0)),
                ('support_from_other', models.TextField(null=True, blank=True)),
                ('previous_talk_info', models.TextField(null=True, blank=True)),
                ('granted_support_before', models.BooleanField(default=False)),
                ('granted_support_info', models.TextField(null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=1, db_index=True, choices=[('p', 'PENDING'), ('a', 'ACCEPTED'), ('r', 'REJECTED'), ('c', 'CANCELLED')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrantType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='grantrequest',
            name='gtype',
            field=models.ForeignKey(to='grants.GrantType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grantrequest',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
