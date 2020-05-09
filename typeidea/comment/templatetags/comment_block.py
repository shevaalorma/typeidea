from comment.models import Comment
from comment.forms import CommentForm

from django import template

register = template.Library()

@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target':target,
        'comment_list':Comment.get_by_target(target),
        'comment_form':CommentForm()
    }