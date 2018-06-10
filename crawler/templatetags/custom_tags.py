
from django.template import Library

register = Library()

@register.simple_tag(takes_context=True)
def update_url(context,**kwargs):
    request = context['request']
    updated = request.GET.copy()
    for k, v in kwargs.items():  # have to iterate over and not use .update as it's a QueryDict not a dict
        updated[k] = v

    return '?{}'.format(updated.urlencode()) if updated else ''

@register.filter
def jsonify(obj):
    from django.utils.safestring import mark_safe
    import json
    return mark_safe(json.dumps(obj))

@register.simple_tag(takes_context=True)
def full_url(context, url, *args):
    request = context['request']
    from django.urls import reverse
    return request.build_absolute_uri() + reverse(url,args=args)[1:]

@register.filter(name='remove_strail')
def remove_strail(str):
    print(str)
    return str[:-1]


@register.inclusion_tag('components/toast_message.html',takes_context=True)
def show_messages(context):
    request = context['request']
    from django.contrib.messages import get_messages
    return {
        'messages':get_messages(request)
    }

@register.inclusion_tag('payment/cards_column.html',takes_context=True)
def cards_template(context):
    request = context['request']
    return {
        'cards':request.user.customer.card_set.all()
    }

@register.inclusion_tag('payment/plan_package.html',takes_context=True)
def packages_template(context):
    request = context['request']
    user = request.user.customer
    from pinax.stripe.models import Plan
    plans = Plan.objects.all()
    # user_plan = Plan.objects.filter(subscription__in=user.subscription_set.filter(Q(status='active') | Q(status='trial') ))

    return {
        'packages'  : plans,
        'request'   : request
    }

@register.simple_tag(takes_context=True)
def get_active_sub(context, plan):
    request = context['request']
    from django.db.models import Q
    sub = request.user.customer.subscription_set.filter((Q(status='active') | Q(status='trial')) ,plan=plan).order_by('-created_at').first()

    return sub