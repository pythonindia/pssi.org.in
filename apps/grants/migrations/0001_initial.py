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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event_details', models.TextField()),
                ('event_address', models.TextField()),
                ('event_url', models.URLField(blank=True, null=True)),
                ('event_date_to', models.DateField()),
                ('event_date_from', models.DateField()),
                ('talk_url', models.TextField(blank=True, null=True)),
                ('amount', models.FloatField()),
                ('granted_amount', models.FloatField(default=0)),
                ('support_from_other', models.TextField(blank=True, null=True)),
                ('previous_talk_info', models.TextField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=100)),
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
