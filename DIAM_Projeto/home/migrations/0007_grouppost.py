# Generated by Django 4.2.1 on 2023-05-13 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.group')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.post')),
            ],
        ),
    ]