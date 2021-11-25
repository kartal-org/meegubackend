from django.db import models
from django.conf import settings
from workspaces.models import Workspace, WorkspaceUploadedFile
from institutions.models import Institution
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

# Create your models here.
def upload_to(instance, filename):
    return "posts/{filename}".format(filename=filename)


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    options = (("public", "Public"), ("private", "Private"))
    is_featured = models.BooleanField(default=False)
    title = models.TextField(max_length=250, unique=True)
    abstract = models.TextField()
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    publishedDate = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, blank=True)
    privacy = models.CharField(choices=options, default="public", max_length=10)
    # author = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Article(Post):
    file = models.ForeignKey(WorkspaceUploadedFile, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def users(self):
        return self.file.folder.workspace.id


class Archive(Post):
    file = models.FileField(upload_to=upload_to)
    authors = models.TextField()


@receiver(pre_save, sender=Article)
@receiver(pre_save, sender=Archive)
def slug_pre_save(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = slugify(instance.title)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    dateAdded = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-dateAdded",)

    def __str__(self):
        return "%s - %s (%s)" % (self.user.username, self.article.title, self.dateAdded)


class Rating(models.Model):
    options = ((1, "Very Bad"), (2, "Bad"), (3, "Average"), (4, "Good"), (5, "Very Good"))
    rate = models.IntegerField(choices=options)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ["user", "article", "archive"]

    def __str__(self):
        return "%s - %s (%d)" % (self.user.username, self.article.title, self.rate)
