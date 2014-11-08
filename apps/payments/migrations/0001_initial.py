# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='Payment ID')),
                ('amount', models.FloatField(default=0.0)),
                ('status', models.CharField(max_length=1, verbose_name='Status', choices=[('p', 'Pending'), ('r', 'Received'), ('c', 'Cancelled'), ('f', 'Refunded')])),
                ('status_pg', models.CharField(max_length=50, verbose_name='Status from Payment Gateway')),
                ('raw_details', django_pgjson.fields.JsonField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('api_key', models.CharField(max_length=100, verbose_name='API Key')),
                ('auth_token', models.CharField(max_length=100, verbose_name='Auth Token')),
                ('webhook_salt', models.CharField(blank=True, max_length=100, null=True, verbose_name='Salt for Webhook')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='payment',
            name='gateway',
            field=models.ForeignKey(to='payments.PaymentGateway'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='payment',
            name='ptype',
            field=models.ForeignKey(to='payments.PaymentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
