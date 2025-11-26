# Generated manually to add ManyToMany relationship

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relecloud', '0002_auto_20210330_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='cruise',
            name='destinations',
            field=models.ManyToManyField(related_name='cruises', to='relecloud.destination'),
        ),
    ]
