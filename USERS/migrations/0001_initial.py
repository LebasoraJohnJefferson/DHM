# Generated by Django 5.1 on 2024-09-01 04:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='owner', max_length=255)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('contact_number', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=200, null=True)),
                ('relationship_to_household', models.CharField(blank=True, choices=[('mother', 'Mother'), ('father', 'Father'), ('son', 'Son'), ('daugter', 'Daughter'), ('others', 'Others')], max_length=255, null=True)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('block_number', models.IntegerField(blank=True, null=True)),
                ('house_number', models.IntegerField(blank=True, null=True)),
                ('total_household_members', models.IntegerField(blank=True, null=True)),
                ('profile_picture', models.ImageField(default='homeOwner.png', upload_to='')),
                ('pending', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('age', models.IntegerField()),
                ('email_address', models.EmailField(max_length=255, unique=True)),
                ('contact_number', models.IntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=200)),
                ('relationship_to_household', models.CharField(choices=[('mother', 'Mother'), ('father', 'Father'), ('son', 'Son'), ('daugter', 'Daughter'), ('others', 'Others')], max_length=255)),
                ('occupation', models.CharField(max_length=255)),
                ('block_number', models.IntegerField(blank=True, null=True)),
                ('lot_number', models.IntegerField(blank=True, null=True)),
                ('household_representative', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]