from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment = True)
    

    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Post_detail", kwargs={"pk": self.pk})



class Comment(models.Model):

    post = models.ForeignKey(Post,related_name='comments', on_delete=models.CASCADE)
    author = models.CharField( max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField( auto_now=True, auto_now_add=False)
    approved_comment = models.BooleanField(default=False)

    def approve_comment(self):
        self.approved_comment = True
        self.save()

    class Meta:
        verbose_name = ("Comment")
        verbose_name_plural = ("Comments")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("Post_list", kwargs={"pk": self.pk})

