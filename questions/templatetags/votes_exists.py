from django import template
from questions import common
register = template.Library()


@register.simple_tag
def votes_up_exists(votable, user_id):
    return common.votes_up_exists(votable, user_id)


@register.simple_tag
def votes_down_exists(votable, user_id):
    return common.votes_down_exists(votable, user_id)
