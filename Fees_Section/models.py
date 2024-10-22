from django.db import models
from django.utils import timezone
from datetime import date
from django.core.validators import RegexValidator

# Validator that allows only digits
numeric_validator = RegexValidator(r'^\d+$', 'Enter a valid mobile number. Only digits are allowed.')

from app.models import (
    student_master
)

class cheque_status(student_master):
  class Meta:
      proxy = True  # Use this model as a proxy for the original model
      # verbose_name = "Model 3"
      # verbose_name_plural = "Model 3 Group"
      # app_label = 'group2'


