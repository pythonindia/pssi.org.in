# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grants', '0006_granttype_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalConfRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Name of your event', max_length=100)),
                ('start_date', models.DateField(help_text='Enter in following format: YYYY-MM-DD')),
                ('end_date', models.DateField(help_text='Enter in following format: YYYY-MM-DD')),
                ('website', models.URLField(null=True, blank=True, help_text='Your event website.')),
                ('location_url', models.URLField(null=True, blank=True, help_text='Your event location URL.')),
                ('location_address', models.TextField(help_text='Location address with the venue name')),
                ('required_amount', models.FloatField(verbose_name='Requested amount in INR')),
                ('budget', models.FloatField(verbose_name='Conference budget')),
                ('expected_audience', models.IntegerField(verbose_name='Total expected participants')),
                ('description', models.TextField(help_text='\nGive us more information about the conference. These details are target audience, \nevent structure, sponsors, partners, local community, previous events details, WiFi, Transport, accomodation etc ...\n\nTake your time and fill the application.\n')),
                ('is_brand_new', models.BooleanField(help_text='Is the event held for the first time?', default=True)),
                ('note', models.TextField(null=True, blank=True, help_text='Any specific note to the board')),
                ('status', models.CharField(choices=[('p', 'PENDING'), ('a', 'ACCEPTED'), ('r', 'REJECTED'), ('c', 'CANCELLED'), ('t', 'TRANSFERRED')], db_index=True, max_length=1)),
                ('requester', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('team_members', models.ForeignKey(related_name='team_members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
