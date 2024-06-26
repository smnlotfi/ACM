# Generated by Django 4.2.7 on 2024-01-22 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_soft_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('permission_type', models.CharField(choices=[('endpoint', 'endpoint'), ('model', 'model'), ('action', 'action'), ('page', 'page')], max_length=24)),
                ('permission_key', models.CharField(max_length=255, unique=True)),
                ('extra_fields', models.JSONField(default=dict)),
                ('created_by', models.ForeignKey(blank=True, help_text='Automatically set who was created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_soft_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, help_text='Automatically set who was created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('permissions', models.ManyToManyField(blank=True, null=True, to='acm.grouppermissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
