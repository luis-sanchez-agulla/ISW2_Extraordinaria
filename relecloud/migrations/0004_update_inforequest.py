# Generated manually to update InfoRequest model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relecloud', '0003_cruise_destinations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inforequest',
            name='description',
        ),
        migrations.AddField(
            model_name='inforequest',
            name='email',
            field=models.EmailField(default='temp@example.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inforequest',
            name='notes',
            field=models.TextField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inforequest',
            name='cruise',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='relecloud.cruise'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cruise',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='inforequest',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
