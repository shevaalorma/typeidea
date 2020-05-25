import xadmin
from xadmin.filters import RelatedFieldListFilter
from xadmin.filters import manager
from xadmin.layout import Row, Fieldset, Container

from django.urls import reverse
from django.utils.html import format_html

from .adminforms import PostAdminForm
from .models import Post, Category, Tag
from typeidea.base_admin import BaseOwnerAdmin


class PostInline:
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 1  # 控制额外多几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    #显示的字段
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]
    #指定链接变蓝的字段
    list_display_links = []

    #指定过滤能使用的字段，一般为外键
    list_filter = ['category', 'owner']
    #指定可以用来查询的字段
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 用来控制是否在页面顶部展示上述的三个按钮。
    save_on_top = True

    #fields 配置有两个作用，一个是限定要展示的字段，另外一个是配置展示字段的顺序。
    #fieldsets 用来控制页面布局，先用它来替换上述代码的 fields
    #     fieldsets = (
    #     (名称, {内容}),
    #     (名称, {内容}),
    # )
    #在编辑页面隐藏的字段
    exclude = ['owner']
    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )

    #指定了可以编辑该选项
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # def get_media(self):
        # # xadmin基于bootstrap，引入会页面样式冲突，仅供参考, 故注释。
        # media = super().get_media()
        # media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
        # media.add_css({
            # 'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        # })
        # return media
