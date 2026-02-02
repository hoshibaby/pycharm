from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    username = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=100, default='')


    class Meta:
        db_table = 'posts'
        verbose_name = '게시글'
        verbose_name_plural = "게시글 목록"

    def __str__(self):
        return self.title