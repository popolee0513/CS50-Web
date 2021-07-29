from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auction_listings(models.Model):
        title = models.CharField(max_length=70)
        description=models.TextField()
        category=models.CharField(max_length=20)
        created_at = models.DateTimeField(auto_now_add=True)  #auto_now_add=True -- 物件新增的時間
        image = models.URLField(blank=True)
        people = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction")
        
class bids(models.Model):
        item=models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="bids")
        price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
        created_at = models.DateTimeField(auto_now_add=True)
        is_closed = models.BooleanField(default=False)
        people = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder" ,blank=True)
        
class comments(models.Model):
        
        item = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="comments")
        created_at = models.DateTimeField(auto_now_add=True)
        comment=models.TextField()
        
class watch_list(models.Model):
        people = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_list")
        item   = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="favorite_item")
        created_at = models.DateTimeField(auto_now_add=True)  #auto_now_add=True -- 物件新增的時間
        class Meta:
                unique_together = ('people', 'item',)
        
        
        
        
        