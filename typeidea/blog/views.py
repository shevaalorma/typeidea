from django.shortcuts import render
from .models import Post, Tag, Category
from config.models import SideBar
from django.views.generic import DetailView


def post_list(request, category_id=None, tag_id=None):
    # get 返回 一个对象object filter返回queryset
    category = None
    tag = None

    # if tag_id:
    #     try:
    #         tag = Tag.objects.get(id=tag_id)
    #     except Tag.DoesNotExist:
    #         post_list = []
    #     else:
    #         post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    # else:
    #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
    #     if category_id:
    #         try:
    #             category = Category.objects.get(id=category_id)
    #         except Category.DoesNotExist:
    #             category = None
    #         else:
    #             post_list = post_list.filter(category_id=category_id)
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars':SideBar.get_all() #返回未隐藏侧边栏
    }
    context.update(Category.get_navs())  #return navs categories
    return render(request, 'blog/list.html', context=context)


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
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
