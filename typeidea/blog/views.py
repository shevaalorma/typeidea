from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Post, Tag, Category
from config.models import SideBar

from django.views.generic import DetailView, ListView


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())  # 返回 navs categories
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    #指定获取的模型列表数据保存的变量名，这个变量会被传递给模板
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'keyword': self.request.GET.get('keyword', '')}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        else:
            return queryset.filter((Q(title__icontains=keyword)) | (Q(desc__icontains=keyword)))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id = author_id)

class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag
        })
        return context

#通用视图在处理用户请求时，URL的变量和参数都会存放在通用视图的属性kwargs中
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        #多对多查询
        return queryset.filter(tag__id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

# def post_list(request, category_id=None, tag_id=None):
#     # get 返回 一个对象object filter返回queryset
#     category = None
#     tag = None
#
#     # if tag_id:
#     #     try:
#     #         tag = Tag.objects.get(id=tag_id)
#     #     except Tag.DoesNotExist:
#     #         post_list = []
#     #     else:
#     #         post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
#     # else:
#     #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#     #     if category_id:
#     #         try:
#     #             category = Category.objects.get(id=category_id)
#     #         except Category.DoesNotExist:
#     #             category = None
#     #         else:
#     #             post_list = post_list.filter(category_id=category_id)
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'sidebars':SideBar.get_all() #返回未隐藏侧边栏
#     }
#     context.update(Category.get_navs())  #return navs categories
#     return render(request, 'blog/list.html', context=context)


# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoseNotExist:
#         post = None
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all()
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)
