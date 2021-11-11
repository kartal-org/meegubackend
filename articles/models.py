from django.db import models

# Create your models here.
def upload_to(instance, filename):
    return "posts/{filename}".format(filename=filename)


class Article(models.Model):
    title = models.TextField(max_length=300)
    file = models.FileField(upload_to=upload_to)
    abstract = models.TextField()
    author = models.TextField()
    publisher = models.TextField()
    publishedDate = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["title", "author"]

    def __str__(self):
        return self.title
