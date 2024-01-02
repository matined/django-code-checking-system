from django.db import models
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter


class CodeSample(models.Model):
    code = models.CharField(max_length=200)
    language = models.ForeignKey(
        "checker.Language", on_delete=models.PROTECT, null=True
    )
    result_ai = models.CharField(max_length=200, null=True)
    result_static = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField()

    @property
    def code_colored(self) -> str:
        return highlight(
            self.code,
            guess_lexer(self.code),
            HtmlFormatter(noclasses=True, style="xcode"),
        )


class Note(models.Model):
    code_sample = models.ForeignKey("checker.CodeSample", on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    pub_date = models.DateTimeField()


class Language(models.Model):
    name = models.CharField(max_length=30)
    abbr = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.name
