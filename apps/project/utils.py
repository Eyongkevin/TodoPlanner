from django.db import models

START_DATE_END_DATE_CHECK = (
    models.Q(end_date__isnull=False, start_date__isnull=False)
    | models.Q(start_date__isnull=False, end_date__isnull=True)
    | models.Q(start_date__isnull=True, end_date__isnull=True)
)

END_DATE_gte_START_DATE_CHECK = models.Q(end_date__gte=models.F("start_date"))
