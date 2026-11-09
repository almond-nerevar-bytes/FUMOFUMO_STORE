from django.db import migrations


IMAGE_BY_NAME = {
    "reimu": "FUMO/Hakurei Reimu.jpg",
    "marisa": "FUMO/Kirisame Marisa.jpg",
    "special week": "FUMO/Special Week.jpg",
    "tokai teio": "FUMO/Tokai Teiou.jpg",
}


def assign_fumo_images(apps, schema_editor):
    PelucheFumo = apps.get_model("catalogo", "PelucheFumo")
    database = schema_editor.connection.alias

    for fumo in PelucheFumo.objects.using(database).all():
        name = fumo.nombre.casefold()
        for product, image_path in IMAGE_BY_NAME.items():
            if product in name:
                fumo.imagen = image_path
                fumo.save(update_fields=["imagen"], using=database)
                break


def clear_fumo_images(apps, schema_editor):
    PelucheFumo = apps.get_model("catalogo", "PelucheFumo")
    database = schema_editor.connection.alias

    for image_path in IMAGE_BY_NAME.values():
        PelucheFumo.objects.using(database).filter(imagen=image_path).update(imagen="")


class Migration(migrations.Migration):

    dependencies = [
        ("catalogo", "0002_rename_figura_peluchefumo_alter_peluchefumo_options"),
    ]

    operations = [
        migrations.RunPython(assign_fumo_images, clear_fumo_images),
    ]
