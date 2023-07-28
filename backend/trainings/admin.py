from django.contrib import admin

from .models import TrainingType, Training


admin.site.register([TrainingType, Training])
