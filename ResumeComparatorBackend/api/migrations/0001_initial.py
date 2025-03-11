# Generated by Django 5.2b1 on 2025-03-10 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_resume', models.FileField(upload_to='resumes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
