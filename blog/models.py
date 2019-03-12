from django import forms
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

# Add a validation to the Article form so that if the article has draft
# set to True, the published_date must be in the future.
# If draft is set to False, published_date must be in the past.
def draft_date(value):
    today = date.today()
    if Article.draft == True and value < today:
        raise ValidationError('Date must be in the future.')
    elif Article.draft == False and value > today:
        raise ValidationError('Date cannot be in the future')

def no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('Article date cannot be in the future.')

class Article(models.Model):
    title = models.CharField(max_length = 255)
    body = models.TextField(validators=[MinLengthValidator(2)])
    draft = models.BooleanField()
    published_date = models.DateField(help_text = "mm/dd/yyyy") #validators=[draft_date])
    author = models.CharField(max_length = 255)
    user = models.ForeignKey(User, default = 1, on_delete = models.CASCADE, related_name = 'articles')

    def __str__(self):
        return self.title + " by " + self.author

class Topic(models.Model):
    name = models.CharField(max_length = 255, default = 'topic')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='topic')

    def __str__(self):
        return self.name

class Comment(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete = models.CASCADE, related_name = 'comments')

    def __str__(self):
        return self.name

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message', 'article']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'draft', 'published_date', 'author']
