# from django.contrib import admin
# from rango.models import Category, Page
# # Register your models here.
from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile
# 定制管理界面，访问 Page 模型时显示网页的分类、名称和 URL，就像图 5-5 那样。你
# 要做完前一题才知道怎么解答这一题
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# 要编辑 rango/admin.py 文件，定义 PageAdmin
# 类，继承自 admin.ModelAdmin。 • 在新增的 PageAdmin 类中添加 list_display = ('title', 'category', 'url')。
# • 然后注册 PageAdmin 类。要修改 Rango 应用的 admin.py 文件，把
# admin.site.register(Page) 改成 admin.site.register(Page, PageAdmin)。
admin.site.register(Category,CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
# admin.site.register(PageAdmin)

