from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.
class Product(models.Model):

    image = models.CharField(verbose_name='图片地址', max_length=255,null=True,blank=True)
    pid = models.BigIntegerField(verbose_name="商品ID",)
    release_date = models.DateTimeField(verbose_name="发布日期",null=True,blank=True)# 发布日期
    pid_num = models.CharField(verbose_name="产品编号",max_length=200,null=True,blank=True)    

    spec = models.CharField(verbose_name="规格",max_length=200,null=True,blank=True)
    brand_spec = models.CharField(verbose_name='网店规格',max_length=150,null=True,blank=True)
    sku = models.CharField(verbose_name="条形码",max_length=200,null=True,blank=True)#SKU

    shop_price= models.DecimalField(verbose_name="专柜价",max_digits=8, decimal_places=2,null=True,blank=True)
    daily_price= models.DecimalField(verbose_name="日常售价",max_digits=8, decimal_places=2,null=True,blank=True)
    activity_price= models.DecimalField(verbose_name="活动价",max_digits=8, decimal_places=2,null=True,blank=True)
    check_price= models.DecimalField(verbose_name="控价",max_digits=8, decimal_places=2,null=True,blank=True)
    tmall_price= models.DecimalField(verbose_name="双11价",max_digits=8, decimal_places=2,null=True,blank=True)
    tmall_presell= models.DecimalField(verbose_name="双11预售",max_digits=8, decimal_places=2,null=True,blank=True)

    interval = models.IntegerField(verbose_name="区间",null=True,blank=True)
    category_parent=models.CharField(verbose_name='父类目',max_length=150,null=True,blank=True)
    category_second=models.CharField(verbose_name='二级类目',max_length=150,null=True,blank=True)
    category_third=models.CharField(verbose_name='子类目',max_length=150,null=True,blank=True)
    
    prd_name = models.CharField(verbose_name="产品简称",max_length=200,null=True,blank=True)#产品简称
    sell_points =models.CharField(verbose_name='核心卖点',max_length=200,null=True,blank=True)
    sell_describe =models.TextField(verbose_name='核心卖点描述',null=True,blank=True)
    sell_state = models.CharField(verbose_name="在售状态",max_length=150,null=True,blank=True)
    
    goods_name = models.CharField(verbose_name='网店品名',max_length=150,null=True,blank=True)
    repeat =models.IntegerField(verbose_name="单店重复次数",null=True,blank=True)
    goods = models.CharField(verbose_name='品牌',max_length=150,null=True,blank=True)
    weight = models.DecimalField(verbose_name="重量_kg",max_digits=5, decimal_places=3,null=True,blank=True)
    shop = models.CharField(verbose_name="店铺",max_length=150,null=True,blank=True)

    create_date = models.DateTimeField(verbose_name='创建时间', null=True,auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', null=True,auto_now=True)
    class Meta:
        ordering = ['-release_date']
        verbose_name = u"商品信息"
        verbose_name_plural = u"商品信息"
    def __str__(self):
        return str(self.pid)


# class User(AbstractUser):

#     class Meta(AbstractUser.Meta):
#         verbose_name = u"用户信息"
#         verbose_name_plural = u"用户信息"