from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class NormalUser(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_normal_user(sender, instance, created, **kwargs):
    if created:
        NormalUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_normal_user(sender, instance, **kwargs):
    instance.normaluser.save()


class LibrarianUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username},{self.user.id}"


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class BookRequest(models.Model):
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    renewal_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.id} - {self.book.title} Request"
