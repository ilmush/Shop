# Generated by Django 4.2.7 on 2024-02-15 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0004_alter_imageproduct_product_alter_product_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageproduct',
            name='product',
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(related_name='related_image', to='shopApp.imageproduct', verbose_name='Изображение'),
        ),
    ]