from django.db import models


class MockModel(models.Model):
    foo = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.foo

    def hello(self):
        return "world"
