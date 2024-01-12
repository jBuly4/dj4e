from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

from taggit.managers import TaggableManager


class Ad(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, 'Title must be greater than 2 characters!')]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, blank=True,
                                    help_text='The MIMEType of the file')

    comments = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            through='Comment',
            related_name='comments_owned'
    )

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       through='Fav', related_name='favorites_ads')

    tags = TaggableManager(blank=True, help_text='Add a comma-separated list of tags')

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(
            validators=[MinLengthValidator(3, 'Comment must be greater than 3 characters!')]
    )
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15:
            return self.text
        return self.text[:15] + '...'


class Fav(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/4.2/ref/models/options/#unique-together
    class Meta:
        unique_together = ('ad', 'user')

    def __str__(self):
        return f'{self.user.username} likes {self.ad.title[:10]}'
