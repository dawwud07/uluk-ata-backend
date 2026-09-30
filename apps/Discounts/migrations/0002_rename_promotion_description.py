from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ckidki', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promotion',
            old_name='ob_akcii',
            new_name='description',
        ),
        migrations.AlterModelOptions(
            name='promotion',
            options={'verbose_name': 'Promotion', 'verbose_name_plural': 'Promotions'},
        ),
        migrations.AlterModelOptions(
            name='promotioncondition',
            options={'verbose_name': 'Promotion condition', 'verbose_name_plural': 'Promotion conditions'},
        ),
    ]