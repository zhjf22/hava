from django.contrib import admin
from havaApp.models import LogInfo,HavaUserGroup

# Register your models here.

@admin.register(LogInfo)
class LogInfoAdmin(admin.ModelAdmin):

    list_display = ('id', 'log_id','log_context', 'hava_submit_log_name', 'states','step','gmt_create')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    ordering = ('-log_id',)
    search_fields = ('states',)


@admin.register(HavaUserGroup)
class HavaUserGroupAdmin(admin.ModelAdmin):
    list_display = ('id','user_group')
    list_display_links = ('user_group',)
    ordering = ('-id',)
