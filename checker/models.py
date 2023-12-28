from django.db import models


class CodeSample(models.Model):
    uid = models.CharField(max_length=20)
    code = models.TextField()
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField()


class Comment(models.Model):
    code_sample = models.ForeignKey(CodeSample, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField()
