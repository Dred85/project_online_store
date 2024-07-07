from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    preview_image = models.ImageField(upload_to='blog_previews/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'