from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class VariableMaster(models.Model):
    """Master table to creating tracking varibales - specific to the user"""
    NUMERIC = 'NM'
    CATEGORICAL = 'CT'
    BINARY = 'BN'
    SCALE = 'SC'

    VARIABLE_TYPE_CHOICES = [
        (NUMERIC, 'Numeric'),
        (CATEGORICAL, 'Categorical'),
        (BINARY, 'Binary'),
        (SCALE, 'Scale'),

    ]

    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    variable_name = models.CharField(max_length=100)
    variable_type = models.CharField(max_length=2, choices=VARIABLE_TYPE_CHOICES, default=NUMERIC)

    def __str__(self):
        return self.variable_name


class VariableResults(models.Model):
    """store the results of the variables """
    variable = models.ForeignKey(VariableMaster, on_delete=models.CASCADE)
    result_date = models.DateField(null=True,blank=True)
    result_numeric = models.FloatField(null=True, blank=True)
    result_binary = models.BooleanField(default=False, blank=True)
    result_categorical = models.CharField(max_length=200, null=True, blank=True)
    result_scale = models.PositiveSmallIntegerField(null=True, blank=True,
        validators=[MinValueValidator(limit_value=1), MaxValueValidator(limit_value=10)])

    @property
    def result_value(self):
        if self.variable.variable_type == VariableMaster.NUMERIC:
            return self.result_numeric
        elif self.variable.variable_type == VariableMaster.BINARY:
            return self.result_binary
        elif self.variable.variable_type == VariableMaster.CATEGORICAL:
            return self.result_categorical
        else:
            return self.result_scale

    class Meta:
        ordering = ['-result_date']

    def __str__(self):
        return self.variable.variable_name
