from django.contrib import admin
from .models import auction_listings,bids,comments,watch_list

# Register your models here.


admin.site.register(auction_listings)
admin.site.register(bids)
admin.site.register(comments)
admin.site.register(watch_list)

