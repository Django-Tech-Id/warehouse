# Generated by Django 2.2.10 on 2021-11-24 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20211124_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='warehousestatuses', to='app.Warehouse'),
        ),
        migrations.AlterField(
            model_name='status',
            name='status',
            field=models.CharField(blank=True, choices=[('Created', 'Created'), ('Registered', 'Registered'), ('Delivered', 'Delivered'), ('Received', 'Received'), ('Pending', 'Pending'), ('Accepted', 'Accepted')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(blank=True, choices=[('Created', 'Created'), ('Registered', 'Registered'), ('Delivered', 'Delivered'), ('Received', 'Received'), ('Pending', 'Pending'), ('Accepted', 'Accepted')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='app.Transaction'),
        ),
    ]
