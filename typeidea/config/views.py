from django.views.generic import ListView
from blog.views import CommonViewMixin
from .models import Link

class LinkListView(CommonViewMixin,ListView):
    queryset = Link.objects.filter(status = Link.STATUS_NORMAL)
    context_object_name = 'link_list'
    template_name = 'config/links.html'


# @property
# def content_html(self):
#     """直接渲染模板"""
#     from blog.models import Post
#     from comment.models import Comment
#
#     result = ''
#     if self.display_type == self.DISPLAY_HTML:
#         result = self.content
#     elif self.display_type == self.DISPLAY_LATEST:
#         context = {
#             'posts':Post.latest_posts()
#         }
#         result = render_to_string('config/blocks/sidebar_posts.html',context)
#     elif self.display_type == self.DISPLAY_HOT:
#         context = {
#             'posts':Post.hot_posts()
#         }
#         result = render_to_string('config/blocks/sidebar_posts.html',context)
#     elif self.display_type == self.DISPLAY_COMMENT:
#         context = {
#             'comments':Comment.objects.filter(status = Comment.STATUS_NORMAL)
#         }
#         result = render_to_string('config/blocks/sidebar_comment.html',context)
#
#     return result