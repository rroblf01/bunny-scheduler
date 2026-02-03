from django import template

register = template.Library()


@register.filter
def get_user_proposal(proposals, user):
    return proposals.filter(proponent=user).first()
