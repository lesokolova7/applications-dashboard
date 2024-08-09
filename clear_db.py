import os
import sys

import django
from django.apps import apps

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AcctSystem.settings")
django.setup()


def clear_database():
    for model in apps.get_models():
        model.objects.all().delete()


if __name__ == "__main__":
    clear_database()
