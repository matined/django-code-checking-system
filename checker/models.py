from django.db import models


class CodeSample(models.Model):
    code = models.CharField(max_length=200)
    result_ai = models.CharField(max_length=200)
    result_static = models.CharField(max_length=200)
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField()


class Comment(models.Model):
    code_sample = models.ForeignKey(CodeSample, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField()
