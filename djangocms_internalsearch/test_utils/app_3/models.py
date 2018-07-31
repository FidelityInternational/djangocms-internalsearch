from django.db import models


class TestModel5(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    text = models.TextField()
    status = models.CharField(max_length=100)


class TestModel6(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    text = models.TextField()
