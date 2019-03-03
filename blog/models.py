from django.db import models

class Article(models.Model):
    title = models.CharField(max_length = 255)
    body = models.TextField()
    draft = models.BooleanField()
    published_date = models.DateField()
    author = models.CharField(max_length = 255)

    def __str__(self):
        return self.title + " by " + self.author

class Topic(models.Model):
    name = models.CharField(max_length = 255, default = 'topic')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='topic')

    def __str__(self):
        return self.name
