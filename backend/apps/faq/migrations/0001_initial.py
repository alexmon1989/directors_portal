# Generated by Django 2.2.7 on 2019-12-19 14:32

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('title', models.CharField(max_length=255, verbose_name='Название раздела')),
                ('weight', models.PositiveIntegerField(default=1000, help_text='Чем выше вес, тем выше расположен элемент на странице.', verbose_name='Вес')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Отображать')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('title', models.CharField(max_length=255, verbose_name='Название вопроса')),
                ('answer', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Ответ')),
                ('weight', models.PositiveIntegerField(default=1000, help_text='Чем выше вес, тем выше расположен элемент на странице.', verbose_name='Вес')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Отображать')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faq.Section', verbose_name='Раздел')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
    ]