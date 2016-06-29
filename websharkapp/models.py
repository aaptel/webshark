#!/usr/bin/env python3

from django.db import models

class Trace(models.Model):
    pub_date = models.DateField(auto_now_add=True)
    path = models.CharField(max_length=512)
    name = models.CharField(max_length=512)
    desc = models.TextField()
    conf = models.TextField() # persistent viewer conf in json

    def __str__(self):
        return self.path

class Comment(models.Model):
    pub_date = models.DateField()
    author = models.CharField(max_length=64)
    content = models.TextField()
    on_packet = models.IntegerField()
    trace = models.ForeignKey(Trace, on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.author, self.content)
