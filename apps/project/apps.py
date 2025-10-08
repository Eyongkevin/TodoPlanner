from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.project"
    label = "apps_project"
    verbose_name = "Project"
