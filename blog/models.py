from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatar')
    # avatar = models.URLField(default="https://uxwing.com/wp-content/themes/uxwing/download/peoples-avatars/user-profile-icon.png")
    phone = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=25, blank=True)
    city = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Дата публікації")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Автор", blank=True)
    # image = models.URLField(default="http://placehold.it/900x300")
    image = models.ImageField(upload_to='post_images')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')
    content = models.TextField(verbose_name='Коментар')
    post = models.ForeignKey(Post, max_length=30, verbose_name="Заголовок", on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class Subscribe(models.Model):
    email = models.EmailField(unique=True, verbose_name='email')

    def __str__(self):
        return self.email


# class ProfileImage(models.Model):
#     profile_image = models.ImageField(upload_to='photos', verbose_name='Зображення профілю')
#     user = models.OneToOneField(Post, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return 'profile image'
