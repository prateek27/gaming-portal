# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSubmission',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Games',
            new_name='GameDetail',
        ),
        migrations.RemoveField(
            model_name='gamesplayed',
            name='game',
        ),
        migrations.RemoveField(
            model_name='gamesplayed',
            name='user',
        ),
        migrations.DeleteModel(
            name='GamesPlayed',
        ),
        migrations.AddField(
            model_name='gamesubmission',
            name='game',
            field=models.ForeignKey(to='games.GameDetail'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gamesubmission',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
