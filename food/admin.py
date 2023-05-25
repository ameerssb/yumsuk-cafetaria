from django.contrib import admin



from .models import User,Item,Order,OrderDetail,Ticket,TicketDetail,Category,Cart,Status
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','total_payment','total_quantity']


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id','item','order','price','quantity','status']

admin.site.register(Item)
admin.site.register(Ticket)
admin.site.register(TicketDetail)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Status)