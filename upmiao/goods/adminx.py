
import xadmin
from .models import Product
from xadmin import views

class ProductAdmin(object):
    list_display =['pid','release_date','pid_num','spec','brand_spec','sku','shop_price','daily_price','activity_price','check_price','tmall_price','tmall_presell','image',]
    # list_filter = [ 'created']
    # list_editable = ['price', 'stock', 'available']

    ordering = ('-release_date',)
    search_fields = ('pid','pid_num','sku',)
    list_editable = ['pid','image','release_date','pid_num','spec','brand_spec','sku','shop_price','daily_price','activity_price','check_price','tmall_price','tmall_presell']


class GlobalSetting(object):
    site_title = "商品后台管理系统"


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(Product, ProductAdmin)


# def save(self, *args, **kwargs):
#     if not self.slug:
#         self.slug = slugify(self.name)
#     super(Product, self).save(*args, **kwargs)

xadmin.site.site_header = '商品管理系统'
# admin.site.site_title = '我在浏览器标签后面'
# admin.site.index_title = '我在浏览器标签前面'

#主题修改
# Register your models here.
# class BaseSetting(object):
#     enable_themes = True
#     use_bootswatch = True
#
#
# xadmin.site.register(views.BaseAdminView, BaseSetting)