import string
from random import choice

from django.db import models

SHORT_LINK_LENGTH = 5  # длина короткой ссылки


def generate_key() -> str:
    chars = string.digits + string.ascii_letters
    return ''.join(choice(chars) for _ in range(SHORT_LINK_LENGTH))


class ShortUrl(models.Model):
    key = models.CharField(
        max_length=SHORT_LINK_LENGTH,
        primary_key=True,
        default=generate_key
    )
    target = models.URLField(
        unique=True
    )
    added = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    ttl = models.IntegerField(
        default=100,
        blank=False
    )

    def __unicode__(self):
        return '%s  %s' % (self.target, self.key)


class Hit(models.Model):
    target = models.ForeignKey(
        ShortUrl,
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    referer = models.URLField(
        blank=True
    )
    ip = models.GenericIPAddressField(
        blank=False
    )
    user_agent = models.CharField(
        blank=True,
        max_length=100
    )
