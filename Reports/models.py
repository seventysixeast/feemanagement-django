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
     
class admission_report(student_master):
  class Meta:
      proxy = True
      verbose_name = 'Admission Report'
      verbose_name_plural = 'Admission Reports'

class final_fees_report(student_fee):
  class Meta:
      proxy = True  # Use this model as a proxy for the original model
      # fields = ('student_class', 'total_annual_fees')

     
class transport_defaulter(student_fee):
  class Meta:
      proxy = True  # Use this model as a proxy for the original model