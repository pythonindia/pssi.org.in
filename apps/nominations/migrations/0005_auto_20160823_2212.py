# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nominations', '0004_auto_20160729_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVoting',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comments', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(to='nominations.Nomination')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VotingURL',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url_hash', models.CharField(max_length=32, verbose_name='hash', unique=True)),
                ('expiry', models.DateTimeField(verbose_name='Expiry')),
                ('ntype', models.ForeignKey(to='nominations.NominationType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='uservoting',
            name='voting_url',
            field=models.ForeignKey(to='nominations.VotingURL'),
            preserve_default=True,
        ),
    ]
