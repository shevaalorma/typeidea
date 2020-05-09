from django.db.models import F, Q
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
    # 指定获取的模型列表数据保存的变量名，这个变量会被传递给模板
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
        return queryset.filter(owner_id=author_id)


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

    # 通用视图在处理用户请求时，URL的变量和参数都会存放在通用视图的属性kwargs中
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        # 多对多查询
        return queryset.filter(tag__id=tag_id)


from datetime import date
from django.core.cache import cache


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid

        pv_key = 'pv:{}:{}'.format(uid, self.request.path)
        uv_key = 'uv:{}:{}:{}'.format(uid, str(date.today()), self.request.path)
        # pv_key = 'pv:%s:%s' % (uid,self.request.path)
        # uv_key = 'uv:%s:%s:%s' % (uid,str(date.today()),self.request.path)


        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24* 60 * 24)

        if increase_uv and increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)

