from django.contrib import admin
from .models import Task, Day, QuarantineTask, QuarantineDay, Quarantine

admin.site.register(Task)
admin.site.register(Day)

admin.site.register(QuarantineTask)
admin.site.register(QuarantineDay)
admin.site.register(Quarantine)
