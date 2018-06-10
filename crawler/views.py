
# Create your views here.
from django.views.generic import TemplateView

from crawler.models import ShopeeComment, ShopeeUser, UnexpectedValue, ShopeeProduct, ShopeeStore


class ShopeeView(TemplateView):
    
    template_name = 'shopee/list.html'
    
    def get(self, request, *args, **kwargs):
        
        uc_user = UnexpectedValue.objects.filter(name='confidence_unexpectedness')
        usp_user = UnexpectedValue.objects.filter(name='support_unexpectedness')
        
        
        
        context={
            'usp_user':usp_user.order_by('-value')[:20],
            'uc_user':uc_user.order_by('-value')[:20],
            'c_user':uc_user.order_by('value')[:10],
            'data_percent':ShopeeComment.class_count(),
            'user_count':ShopeeUser.objects.all().count(),
            'product_count':ShopeeProduct.objects.all().count(),
            'store_count':ShopeeStore.objects.all().count(),
        }
        
        
        return self.render_to_response(context=context)
    

shopee_view = ShopeeView.as_view()

