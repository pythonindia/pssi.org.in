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
            name='Nomination',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fullname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=100)),
                ('gender', models.CharField(
                    db_index=True, max_length=1, choices=[('M', 'MALE'), ('F', 'FEMALE')])),
                ('self_nomiation', models.BooleanField(
                    default=False, verbose_name='Self Nomination ')),
                ('contact_number', models.CharField(max_length=10)),
                ('postal_address', models.TextField(
                    default='Your Full address')),
                ('profession', models.CharField(
                    default='I work/study at ...', max_length=300)),
                ('contribution_info', models.TextField(
                    default=' Explain in detail about the candidate contribution')),
                ('references', models.TextField(
                    default='The references themselves must be people who are known by\n        either their work in the Python community')),
                ('reason_to_join_board', models.TextField(
                    default='Reason to join PSSI board ', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NominationType',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, max_length=100, choices=[
                 ('Board Member', 'Board Member'), ('Kenneth Gonsalves', 'Kenneth Gonsalves')])),
                ('slug', models.CharField(unique=True, max_length=10)),
                ('active', models.BooleanField(
                    default=True, verbose_name='Whether this  type should be available to public')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nomination',
            name='ntype',
            field=models.ForeignKey(to='nominations.NominationType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nomination',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
