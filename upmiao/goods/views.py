from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import xlwt
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from io import BytesIO
from django.contrib.auth import authenticate, login,logout 
from django.urls import reverse
from django.contrib.auth.models import Permission

# Create your views here.
def login_site(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('upassword')
        user = authenticate(username=username, password=password)   # 使用 Django 的 authenticate 方法来验证
        if user:
            login(request, user)    # <==
            return HttpResponseRedirect('/')
        else:
            return render(request, 'miao/login.html', {
                'login_err': '请输入正确的账号和密码 !'
            })
    return render(request, 'miao/login.html')

def logout_site(request):
    logout(request)     # <==
    return HttpResponseRedirect('/')



@login_required
def show_list(request, page=1):
    username = request.user.username
    cur_page = int(page)
    # 查询posts表，按play_counts倒序排序
    products = Product.objects.order_by('-release_date')
    paginator = Paginator(products, 20)
    products = paginator.page(cur_page)

    # 分页逻辑
    # 要显示的页码数量
    page_num = 5
    # 一半的页码数量
    half_page_num = page_num // 2
    first_page = 1
    last_page = paginator.num_pages
    # 如果处理当前页之前的页码不足2页
    if cur_page - half_page_num < 1:
        # 则显示的页码从当前页开始
        display_pages = range(cur_page, cur_page + page_num)
    # 如果处理当前页之后的页码不足2页
    elif cur_page + half_page_num > last_page:
        # 则从当前页往前数5页
        display_pages = range(cur_page - page_num, cur_page + 1)
    else:
        # 其他情况下，当前页左右各显示两页
        display_pages = range(cur_page - half_page_num, cur_page + half_page_num + 1)
    display_pages = list(display_pages)
    # 是否显示下一页
    if products.has_next():
        next_page = products.next_page_number()
    # 是否显示上一页
    if products.has_previous():
        previous_page = products.previous_page_number()
    # 如果当前页码范围内不包含第一页，则把第一页添加进去
    if first_page not in display_pages:
        display_pages.insert(0, first_page)
    # 如果当前页码范围内不包含最后一页，则把最后页添加进去
    if last_page not in display_pages:
        display_pages.append(last_page)
    # 把所有的局部变量传给模板
    return render(request, 'miao/bc.html', locals(),{'products': products,'username':username})

#搜索功能
def search(request):
    q = request.GET.get('q')
    w = request.GET.get('w')
    e = request.GET.get('e')
    error_msg = ''
    if w:
        pid_list = Product.objects.filter(pid__icontains=w)
        return render(request, 'miao/pid_search.html', {'error_msg': error_msg,'pid_list': pid_list})
    if e:
        sku_list = Product.objects.filter(sku__icontains=e)
        return render(request, 'miao/sku_search.html', {'error_msg': error_msg,'sku_list': sku_list})

    pid_num_list = Product.objects.filter(pid_num__icontains=q)
    return render(request, 'miao/name_search.html', {'error_msg': error_msg,
                                               'pid_num_list': pid_num_list,})
    # if w:
    #     pid_list = Product.objects.filter(pid__icontains=w)
    #     return render(request, 'miao/search.html', {'error_msg': error_msg,'pid_list': pid_list})
    # if e:
    #     sku_list = Product.objects.filter(sku__icontains=e)
    #     return render(request, 'miao/search.html', {'error_msg': error_msg,'sku_list': sku_list})

    # post_list = Product.objects.filter(name__icontains=q)
    # return render(request, 'miao/search.html', {'error_msg': error_msg,
    #                                            'post_list': post_list,})


#导出数据
def export_excel(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=order.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    #创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')
    style_heading = xlwt.easyxf("""
            font:
                name Microsoft YaHei,
                colour_index black,
                bold on,
                height 200;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour coral;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    data_row = 1
    products = Product.objects.order_by('-release_date')
    if request.user.is_superuser == False:

        sheet.write(0,0,'商品ID',style_heading)
        sheet.write(0,1,'发布日期',style_heading)
        sheet.write(0,2,'产品编号',style_heading)
        sheet.write(0,3,'规格',style_heading)
        sheet.write(0,4,'网店规格',style_heading)
        sheet.write(0,5,'条形码',style_heading)
        sheet.write(0,6,'专柜价',style_heading)
        sheet.write(0,7,'日常售价',style_heading)
        sheet.write(0,8,'区间',style_heading)
        sheet.write(0,9,'父类目',style_heading)
        sheet.write(0,10,'二级类目',style_heading)
        sheet.write(0,11,'子类目',style_heading)
        sheet.write(0,12,'产品简称',style_heading)
        sheet.write(0,13,'核心卖点',style_heading)
        sheet.write(0,14,'核心卖点描述',style_heading)
        sheet.write(0,15,'在售状态',style_heading)
        sheet.write(0,16,'网店品名',style_heading)
        sheet.write(0,17,'单店重复次数',style_heading)
        sheet.write(0,18,'品牌',style_heading)
        sheet.write(0,19,'重量_kg',style_heading)
        sheet.write(0,20,'店铺',style_heading)

        for i in products:
            sheet.write(data_row,0,i.pid)
            if i.release_date != None:
                sheet.write(data_row,1,i.release_date.strftime('%Y-%m-%d %H:%M:%S'))
            else: 
                sheet.write(data_row,1,i.release_date)
            sheet.write(data_row,2,i.pid_num)
            sheet.write(data_row,3,i.spec)
            sheet.write(data_row,4,i.brand_spec)
            sheet.write(data_row,5,i.sku)
            sheet.write(data_row,6,i.shop_price)
            sheet.write(data_row,7,i.daily_price)
            sheet.write(data_row,8,i.interval)
            sheet.write(data_row,9,i.category_parent)
            sheet.write(data_row,10,i.category_second)
            sheet.write(data_row,11,i.category_third)
            sheet.write(data_row,12,i.prd_name)
            sheet.write(data_row,13,i.sell_points)
            sheet.write(data_row,14,i.sell_describe)
            sheet.write(data_row,15,i.sell_state)
            sheet.write(data_row,16,i.goods_name)
            sheet.write(data_row,17,i.repeat)
            sheet.write(data_row,18,i.goods)
            sheet.write(data_row,19,i.weight)
            sheet.write(data_row,20,i.shop)
            data_row = data_row + 1

    #写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
    else:
        sheet.write(0,0,'商品ID',style_heading)
        sheet.write(0,1,'发布日期',style_heading)
        sheet.write(0,2,'产品编号',style_heading)
        sheet.write(0,3,'规格',style_heading)
        sheet.write(0,4,'网店规格',style_heading)
        sheet.write(0,5,'条形码',style_heading)
        sheet.write(0,6,'专柜价',style_heading)
        sheet.write(0,7,'日常售价',style_heading)
        sheet.write(0,8,'活动价',style_heading)
        sheet.write(0,9,'控价',style_heading)
        sheet.write(0,10,'双11价',style_heading)
        sheet.write(0,11,'双11预售',style_heading)
        sheet.write(0,12,'区间',style_heading)
        sheet.write(0,13,'父类目',style_heading)
        sheet.write(0,14,'二级类目',style_heading)
        sheet.write(0,15,'子类目',style_heading)
        sheet.write(0,16,'产品简称',style_heading)
        sheet.write(0,17,'核心卖点',style_heading)
        sheet.write(0,18,'核心卖点描述',style_heading)
        sheet.write(0,19,'在售状态',style_heading)
        sheet.write(0,20,'网店品名',style_heading)
        sheet.write(0,21,'单店重复次数',style_heading)
        sheet.write(0,22,'品牌',style_heading)
        sheet.write(0,23,'重量_kg',style_heading)
        sheet.write(0,24,'店铺',style_heading)
        for i in products:
            # pri_time = i.pri_date.strftime('%Y-%m-%d')
            # oper_time = i.operating_time.strftime('%Y-%m-%d')
            sheet.write(data_row,0,i.pid)
            if i.release_date != None:
                sheet.write(data_row,1,i.release_date.strftime('%Y-%m-%d %H:%M:%S'))
            else: 
                sheet.write(data_row,1,i.release_date)
            sheet.write(data_row,2,i.pid_num)
            sheet.write(data_row,3,i.spec)
            sheet.write(data_row,4,i.brand_spec)
            sheet.write(data_row,5,i.sku)
            sheet.write(data_row,6,i.shop_price)
            sheet.write(data_row,7,i.daily_price)
            sheet.write(data_row,8,i.activity_price)
            sheet.write(data_row,9,i.check_price)
            sheet.write(data_row,10,i.tmall_price)
            sheet.write(data_row,11,i.tmall_presell)
            sheet.write(data_row,12,i.interval)
            sheet.write(data_row,13,i.category_parent)
            sheet.write(data_row,14,i.category_second)
            sheet.write(data_row,15,i.category_third)
            sheet.write(data_row,16,i.prd_name)
            sheet.write(data_row,17,i.sell_points)
            sheet.write(data_row,18,i.sell_describe)
            sheet.write(data_row,19,i.sell_state)
            sheet.write(data_row,20,i.goods_name)
            sheet.write(data_row,21,i.repeat)
            sheet.write(data_row,22,i.goods)
            sheet.write(data_row,23,i.weight)
            sheet.write(data_row,24,i.shop)
            data_row = data_row + 1

        #写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
    return response


