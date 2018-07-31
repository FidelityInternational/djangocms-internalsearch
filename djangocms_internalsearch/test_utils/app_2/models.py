from django.db import models


class TestModel1(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)


class TestModel2(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)
