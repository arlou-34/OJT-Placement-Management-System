# Generated by Django 5.2.1 on 2025-06-10 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0008_report_link_alter_report_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=20)),
                ('full_name', models.CharField(max_length=150)),
                ('file', models.FileField(blank=True, null=True, upload_to='archived_reports/')),
                ('link', models.URLField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField()),
                ('archived_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
