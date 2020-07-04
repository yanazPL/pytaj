from django import template

register = template.Library()

@register.simple_tag
def votes_up_exists(votable, user_id):
    user_votes_up = votable.votes.user_ids(0)
    check = {'user_id': user_id}
     #Lists all votes with action 0 - upvoting
    return check in user_votes_up.values('user_id')


@register.simple_tag
def votes_down_exists(votable, user_id):
    user_votes_down = votable.votes.user_ids(1)
    #Lists all votes with action 1 - downvoting
    check = {'user_id': user_id}

    return check in user_votes_down.values('user_id')