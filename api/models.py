# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.db.models.signals import post_save
# from django.utils.text import slugify
# from shortuuid.django_fields import ShortUUIDField
# import shortuuid

# class user(AbstractUser):
#     username = models.CharField(unique=True, max_length=100)
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=100, null=True, blank=True)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
    
#     def __str__(self):
#         return self.username
    
#     def save(self, *args, **kwargs):
#         email_username, mobile = self.email.split('@')
#         if self.full_name == '' or self.full_name == None:
#             self.full_name = email_username
#         if self.username == '' or self.username == None:
#             self.username = email_username 
            
#         super(user, self).save(*args, **kwargs)      

# class Profile(models.Model):
#     user = models.OneToOneField(user, on_delete=models.CASCADE)
#     image = models.FileField(upload_to='image', default='default/default-user.jpg', null=True, blank=True)
#     full_name = models.CharField(max_length=100, null=True, blank=True)
#     bio = models.CharField(max_length=100, null=True, blank=True)
#     about = models.CharField(max_length=100, null=True, blank=True)
#     author = models.CharField(max_length=100, blank=True, null=True)
#     country = models.CharField(max_length=100, null=True, blank=True)
#     facebook = models.CharField(max_length=100, null=True, blank=True)
#     twitter = models.CharField(max_length=100, null=True, blank=True)
#     date = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
#         return self.user.username
    
#     def save(self, *args, **kwargs):
#         if self.full_name == '' or self.full_name == None:
#             self.full_name = self.user.full_name
              
#         super(Profile, self).save(*args, **kwargs)  
        
# def create_user_profile(sender, instance, created,**kwargs): 
#     if created:
#         Profile.objects.create(user=instance)
        
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
    
# post_save.connect(create_user_profile, sender=user) 
# post_save.connect(save_user_profile, sender=user)

# class Category(models.Model):
#     title  = models.CharField()
#     image = models.FileField(upload_to= 'image', null=True, blank=True)
#     slug = models.SlugField(unique=True, null=True, blank=True)
    
#     def __str__(self):
#         return self.title
    
#     # class Meta:
#     #     ordering = ['date']
#     #     verbose_name_plural = 'Category'
        
#     def save(self, *args, **kwargs):
#         if self.slug -- '' or self.slug -- None:
#             self.slug = slugify(self.title)
            
#         super(Category, self).save( *args, **kwargs)  
        
# class Post(models.Model):
    
#     STATUS = (
#         ('Active', 'Active'),
#         ('Draft', 'Draft'),
#         ('Disabled', 'Disabled'),
#     )
#     user = models.ForeignKey(user, on_delete=models.CASCADE)
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
#     title = models.CharField(max_length=100)
#     description = models.TextField(null=True, blank=True)
#     image = models.FileField(upload_to='image', null=True, blank=True)
#     status = models.CharField(choices=STATUS, max_length=100, default='Active')
#     view = models.IntegerField(default=0)
#     likes = models.ManyToManyField(user, blank=True, related_name='likes_user')
#     slug = models.SlugField(unique=True, null=True, blank=True) 
#     date = models.DateTimeField(auto_now_add=True)
    
    
#     def __str__(self):
#         return self.user.title
    
#     class Meta:
#         ordering = ['date']
#         verbose_name_plural = 'Post'
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#           self.slug = slugify(self.title) + '-' + shortuuid.uuid()[:2]
#         super().save(*args, **kwargs)


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
import shortuuid


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        email_username = self.email.split('@')[0]
        if not self.full_name:
            self.full_name = email_username
        if not self.username:
            self.username = email_username
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='image', default='default/default-user.jpg', blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=100, blank=True)
    about = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='image', blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def post_count(self):
        return Post.objects.filter(category=self).count()    

class Post(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('Draft', 'Draft'),
        ('Disabled', 'Disabled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='image', blank=True)
    status = models.CharField(choices=STATUS, max_length=20, default='Active')
    view = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    slug = models.SlugField(unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Post'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + shortuuid.uuid()[:6]
        super().save(*args, **kwargs)
 
                              
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    commet = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.post.title
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Comment'
        
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.post.title
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Bookmark'          
                                  
class Notification(models.Model):
    NOTI_TYPE = (
        ('I like', 'I like'),
        ('Comment', 'Comment'),
        ('Bookmark', 'Bookmark'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(choices=NOTI_TYPE, max_length=100)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)   
    
    def __str__(self):
        if self.post:
         return f'{self.post.title}'-'{self.type}'
        else:
            return 'Notification'
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Notification'  
                                   