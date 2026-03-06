# Generated manually for PageBanner (bannière / slider page maintenance)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_assistantquestion"),
    ]

    operations = [
        migrations.CreateModel(
            name="PageBanner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("page", models.CharField(choices=[("maintenance", "Maintenance de site web")], max_length=50, verbose_name="Page")),
                ("image", models.ImageField(upload_to="banners/", verbose_name="Image")),
                ("order", models.IntegerField(default=0, verbose_name="Ordre d'affichage")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Bannière de page",
                "verbose_name_plural": "Bannières de page",
                "ordering": ["page", "order"],
            },
        ),
    ]
