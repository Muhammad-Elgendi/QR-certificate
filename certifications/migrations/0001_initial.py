# Generated by Django 4.0.6 on 2022-09-05 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issuer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ar', models.CharField(max_length=100, verbose_name='Issuer Name In Arabic')),
                ('name_en', models.CharField(max_length=100, verbose_name='Issuer Name In English')),
                ('url', models.CharField(max_length=2000, verbose_name='Verify URL')),
                ('signature', models.ImageField(blank=True, upload_to='signatures')),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ar', models.CharField(max_length=100, verbose_name='Name In Arabic')),
                ('name_en', models.CharField(max_length=100, verbose_name='Name In English')),
                ('national_id', models.IntegerField(blank=True, null=True, verbose_name='National Identification Number')),
                ('image', models.ImageField(blank=True, upload_to='images')),
                ('specialization', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_no', models.IntegerField(blank=True, null=True, verbose_name='Phone Number')),
                ('receipt_no', models.IntegerField(blank=True, null=True, verbose_name='Receipt Number')),
                ('receipt_date', models.DateTimeField(blank=True, null=True, verbose_name='Receipt Issued Time')),
                ('cert_no', models.CharField(max_length=40, unique=True, verbose_name='Certification Number')),
                ('course_ar', models.CharField(max_length=100, verbose_name='Course In Arabic')),
                ('course_en', models.CharField(max_length=100, verbose_name='Course In English')),
                ('course_type_en', models.CharField(max_length=100, verbose_name='Course Type In English')),
                ('course_type_ar', models.CharField(max_length=100, verbose_name='Course Type In Arabic')),
                ('course_start', models.DateTimeField(blank=True, null=True, verbose_name='Course Started Time')),
                ('course_end', models.DateTimeField(verbose_name='Course Ended Time')),
                ('issue_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Certification Issued Time')),
                ('issuer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certifications.issuer')),
            ],
        ),
    ]
