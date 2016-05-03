from django.db import models

# Create your models here.
class Node_Data(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    group = models.IntegerField()
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    # timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __unicode__(self):
        return self.name


class Node_Relations(models.Model):
    source = models.IntegerField()
    target = models.IntegerField()
    value = models.IntegerField(default=1)