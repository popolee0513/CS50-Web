from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self',blank=True,related_name='user_followers',symmetrical=False)
    following = models.ManyToManyField('self',blank=True,related_name='user_following',symmetrical=False)
    def count_followers(self):
        return self.followers.count()
    
    def count_following(self):
        return User.objects.filter(followers=self).count()

class Post(models.Model):
    content = models.TextField(blank=False)
    author  = models.ForeignKey(
        User,
        related_name='post',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(
        User,
        related_name='post_like',
        blank=True
    )
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "author": self.author,
            "users_like": self.users_like
            
        }
#class comment(models.Model):
 #   user = models.ForeignKey(User_info)
  #  blog = models.ForeignKey(Blog, related_name='comments')
  #  comment = models.CharField(max_length=500)
  #  parent = models.ForeignKey('self', null=True, related_name='replies')
  #  https://stackoverflow.com/questions/17157828/django-how-to-display-comments-and-replies-made-on-that-comment-in-template
    
"""
{% for comment in blog_obj.comments.all %}
    {{ comment.comment }}
    {% for reply in comment.replies.all %}
        {{ reply.comment }}
    {% endfor %}
{% endfor %}
"""

