from django.contrib import admin

from .models import Training, TrainingType

admin.site.register([TrainingType, Training])
