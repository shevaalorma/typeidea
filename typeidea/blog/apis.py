# from rest_framework import generics
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
#
# from .models import Post
# from .serializers import PostSerializer
#
# @api_view()
# def post_list(request):
#     posts = Post.objects.filter(status = Post.STATUS_NORMAL)
#     post_serializers =PostSerializer(posts,many=True)
#     return Response(post_serializers)
#
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
#     serializer_class = PostSerializer
#
# # from rest_framework import viewsets
# # from rest_framework.permissions import IsAdminUser
#
# # from .models import Post
# # from .serializers import PostSerializer
#
# # class PostViewSet(viewsets.ModelViewSet):
# #     serializer_class = PostSerializer
# #     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
# #     #permission_classes = [IsAdminUser] #写入时校验权限