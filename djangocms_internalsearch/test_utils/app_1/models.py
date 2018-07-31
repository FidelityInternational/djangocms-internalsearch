from django.db import models


class TestModel3(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)


class TestModel4(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)


class TestModel5(models.Model):
    pass
