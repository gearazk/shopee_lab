from math import log



def cal_confidence_unexpectedness():
    
    item_per_time = 100
    items_loaded = 0
    from crawler.models import ShopeeUser, ShopeeComment, UnexpectedValue
    total = ShopeeUser.objects.all()
    value_name = 'confidence_unexpectedness'
    probs = ShopeeComment.class_prob()
    li = total.count()
    
    while items_loaded <= li:
        print('%s / %s items'% (items_loaded,li))
        
        for user in total[ items_loaded : items_loaded + item_per_time ]:
            
            co = user.shopeecomment_set.class_count()
            for c in ['positive', 'neutral', 'negative']:
                if co[c] and co[c] >= 3:
                    value = abs( float(co[c] / co['total']) - probs[c]) / probs[c]
                    UnexpectedValue.objects.update_or_create(
                        user=user,
                        name=value_name,
                        class_name=c,
                        defaults={
                            'value': value
                        }
                    )
        items_loaded += item_per_time

def cal_support_unexpectedness():
    from crawler.models import ShopeeUser, ShopeeComment, UnexpectedValue

    item_per_time = 100
    items_loaded = 0
    total = ShopeeUser.objects.all()
    value_name = 'support_unexpectedness'
    probs = ShopeeComment.class_prob()
    li = total.count()

    while items_loaded <= li:
        print('%s / %s items' % (items_loaded, li))
    
        for user in total[items_loaded: items_loaded + item_per_time]:
        
            co = user.shopeecomment_set.class_count()
            for c in ['positive', 'neutral', 'negative']:
                if co[c] >= 3:
                    expect = probs[c]/co['total']
                    
                    value = abs( ( (co[c] / co['total'] ) * probs[c] ) - expect ) / expect
                    UnexpectedValue.objects.update_or_create(
                        user=user,
                        name=value_name,
                        class_name=c,
                        defaults={
                            'value': value
                        }
                    )
        items_loaded += item_per_time


def cal_attr_unexpectedness():
    from crawler.models import ShopeeUser, ShopeeComment, UnexpectedValue

    item_per_time = 500
    items_loaded = 0
    total = ShopeeUser.objects.all()
    value_name = 'attribute_unexpectedness'
    probs = ShopeeComment.class_prob()
    li = total.count()
    
    entrophy_D = - sum([probs[c]*log(probs[c]) for c in ['positive', 'neutral', 'negative'] ])
    
    while items_loaded <= li:
        print('%s / %s items' % (items_loaded, li))
        
        for user in total[items_loaded: items_loaded + item_per_time]:
    
            co = user.shopeecomment_set.class_count()
            if not co['total']: continue
            prob_co = { k : co[k]/co['total'] for k in co.keys() if k is not 'total' }
            entrophy_Dk = - sum([ prob_co[c] * log( prob_co[c] ) for c in ['positive', 'neutral', 'negative'] if prob_co[c] ])
            entrophy_Dk = entrophy_Dk * (co['total']/li)
            
            value = entrophy_Dk - entrophy_D

            UnexpectedValue.objects.update_or_create(
                user=user,
                name=value_name,
                class_name='',
                defaults={
                    'value': value
                }
            )

        items_loaded += item_per_time

print('Start counting "confidence_unexpectedness"')
cal_confidence_unexpectedness()
print('Done counting "confidence_unexpectedness"')
print('\n')
print('Start counting "support unexpectedness"')
cal_support_unexpectedness()
print('Done counting "support unexpectedness"')
print('open localhost:8080 or 127.0.0.1:8080 "')
