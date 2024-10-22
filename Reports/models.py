from django.db import models

# Create your models here.
from app.models import (
    student_master, student_fee
)


class transport(student_master):
  class Meta:
      proxy = True  # Use this model as a proxy for the original model
     
class tuition_fees_defaulter(student_fee):
  class Meta:
      proxy = True  # Use this model as a proxy for the original model
      verbose_name = 'Tuition Fees Defaulters'
      verbose_name_plural = 'Tuition Fees Defaulters'
     
class admission_report(student_master):
  class Meta:
      proxy = True
      verbose_name = 'Admission Report'
      verbose_name_plural = 'Admission Reports'

class collection_report(student_fee):
  class Meta:
      proxy = True
      verbose_name = 'Collection'
      verbose_name_plural = 'Collection'

class activity_fees_defaulter(student_fee):
  class Meta:
      proxy = True
      verbose_name = 'Activity Fees Defaulters'
      verbose_name_plural = 'Activity Fees Defaulters'