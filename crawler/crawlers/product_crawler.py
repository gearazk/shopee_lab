import random
import re

from crawler.crawlers.base_crawler import BaseCrawler
from crawler.models import ShopeeProduct, ShopeeUser, ShopeeStore, ShopeeComment


class CategoryCrawler(BaseCrawler):
    
    product_url = 'https://shopee.vn/api/v2/search_items/?by=relevancy&limit={limit}&match_id={cate_id}&newest={item_loaded}&order=desc&page_type=search'
    
    comment_url = 'https://shopee.vn/api/v1/comment_list/?item_id={item_id}&shop_id={shop_id}&offset={item_loaded}&limit={limit}&flag=1&filter=0'
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    def _comment_url(self,page,item_id,shop_id,limit=50):
        url = self.comment_url.format(**{
            'item_id'    : str(item_id),
            'shop_id'    : str(shop_id),
            'item_loaded': str(page * limit),
            'limit'      : str(limit),
        })
        return url

        
    def _product_url(self,page,cate_id,limit=100):
        url = self.product_url.format(**{
            'cate_id'       :str(cate_id),
            'item_loaded'   :str(page*limit),
            'limit'         :str(limit),
        })
        return url
    
    def _crawl_now(self):
        
        cate_id = 87
        pages = 1000
        for page in range(pages):
            print('Product page %s \n' % page)
            resp = self._get(self._product_url(page,cate_id))
            items = resp.json().get('items',[])
            if len(items) == 0:
                break
            print('Got %s product items \n' % len(items))

            product = self._extract_products(items)
        return []
    
    def _craw_comment(self, product, store, ):
        print('craw comment')
    
        product_id = product.product_id
        store_id = store.store_id
        pages = 100
      

        for page in range(pages):
            resp = self._get(self._comment_url(page, product_id, store_id))

            comments = resp.json().get('comments',[])
            
            if len(comments) == 0:
                break
            print('Got %s comments items \n' % len(comments))
            
            for comment in comments:
                if not comment['authorid']:
                    continue
                user, _ = ShopeeUser.objects.get_or_create(
                    user_id = comment['authorid'],
                    defaults= {
                        'user_id'   :comment['authorid'],
                        'name'      :comment['author_name'],
                    }
                )
                
                _comment, _ = ShopeeComment.objects.get_or_create(
                    
                    comment_id  = comment['cmtid'],
                    defaults    = {
                        'user'      :user,
                        'product'   :product,
                        'comment_id':comment['cmtid'],
                        'content'   :comment['comment'],
                        'rating'    :comment['rating_star'],
                    }
                )

    
        return []
    
    
    def _get_store_model(self,shop_id):
        
        print('Get shop id: %s ' % shop_id)
        store, _ = ShopeeStore.objects.get_or_create(
            store_id = shop_id,
            defaults = {
                'store_id'  : shop_id,
                'name'      : shop_id,
            }
        )
        return store
    
    def _extract_products(self,json_data):
        
        print('Got %s product items \n' % len(json_data))
        list_product = []
        for data in json_data:
            product_data = {
                'product_id'    : data['itemid'],
                'name'          : data['name'],
                'rating'        : data['item_rating'],
            }
            
            product, created = ShopeeProduct.objects.get_or_create(
                product_id  = product_data['product_id'],
                defaults    = product_data
            )
            if not created:
                continue
            
            print('crawler detail')
            store = self._get_store_model(data['shopid'])
            
            self._craw_comment(product, store)
        return list_product
    
