from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('core', 'Category')
    categories = [
        ('CORE1', 'MD', 'Mobile Devices'),
        ('CORE1', 'NW', 'Networking'),
        ('CORE1', 'HW', 'Hardware'),
        ('CORE1', 'VC', 'Virtualization and Cloud Computing'),
        ('CORE1', 'HNT', 'Hardware and Network Troubleshooting'),
        ('CORE2', 'OS', 'Operating Systems'),
        ('CORE2', 'SEC', 'Security'),
        ('CORE2', 'ST', 'Software Troubleshooting'),
        ('CORE2', 'OP', 'Operational Procedures'),
    ]
    for core, domain, name in categories:
        Category.objects.get_or_create(core=core, domain=domain, name=name)

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0014_category_name'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]