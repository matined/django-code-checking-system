from django.db import models


class CodeSample(models.Model):
    uid = models.CharField(max_length=20)
    code = models.TextField()
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.uid


class Comment(models.Model):
    code_sample = models.ForeignKey(CodeSample, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField()
