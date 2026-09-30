from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('background_image', models.ImageField(upload_to='estatic/images/')),
                ('tag', models.CharField(max_length=100)),
                ('valid_until', models.CharField(blank=True, max_length=100, null=True)),
                ('ob_akcii', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции  и скидки',
            },
        ),
        migrations.CreateModel(
            name='PromotionCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_text', models.TextField()),
                ('promotion', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='conditions', to='Ckidki.promotion')),
            ],
            options={
                'verbose_name': 'Условие акции',
                'verbose_name_plural': 'Условия акций',
            },
        ),
    ]