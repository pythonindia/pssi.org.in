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
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_id', models.CharField(verbose_name='Payment ID', max_length=50, null=True, blank=True)),
                ('amount', models.FloatField(default=0.0)),
                ('status', models.CharField(verbose_name='Status', max_length=1, choices=[('p', 'Pending'), ('r', 'Received'), ('c', 'Cancelled'), ('f', 'Refunded')])),
                ('status_pg', models.CharField(verbose_name='Status from Payment Gateway', max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('api_key', models.CharField(verbose_name='API Key', max_length=100)),
                ('auth_token', models.CharField(verbose_name='Auth Token', max_length=100)),
                ('webhook_salt', models.CharField(verbose_name='Salt for Webhook', max_length=100, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
