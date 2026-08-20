from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_alter_galleryalbum_options_document_school_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesettings',
            name='price_list_file',
        ),
    ]
