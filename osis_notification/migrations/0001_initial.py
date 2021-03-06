# Generated by Django 2.2.13 on 2021-06-03 11:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('type', models.CharField(choices=[('EMAIL_TYPE', 'Email notification'), ('WEB_TYPE', 'Web notification')], max_length=25, verbose_name='Type')),
                ('payload', models.TextField(verbose_name='Payload')),
                ('state', models.CharField(choices=[('PENDING_STATE', 'Pending'), ('SENT_STATE', 'Sent'), ('READ_STATE', 'Read')], default='PENDING_STATE', max_length=25, verbose_name='State')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('sent_at', models.DateTimeField(editable=False, null=True, verbose_name='Sent at')),
                ('read_at', models.DateTimeField(editable=False, null=True, verbose_name='Read at')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='base.Person')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
            ],
            options={
                'verbose_name': 'Email notification',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('osis_notification.notification',),
        ),
        migrations.CreateModel(
            name='WebNotification',
            fields=[
            ],
            options={
                'verbose_name': 'Web notification',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('osis_notification.notification',),
        ),
    ]
