from datetime import datetime
from products_crawler.crawlers.base_crawler import BaseCrawler


class TransactionCrawler(BaseCrawler):
    
    API = 'https://feedback.aliexpress.com/display/evaluationProductDetailAjaxService.htm'
    
    def __init__(self,trans_id,page=1,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.trans_id   = trans_id
        self.page       = page
        
        
        
    def _crawl_now(self):
        
        reps = self._get(self.API, params={
            'callback'  :'',
            'productId' :self.trans_id,
            'type'      :'default',
            'page'      :self.page,
        })
        json_data = reps.json()
        
        data = []
        for trans in json_data.get('records',[]):
            try:
                obj = {
                    'buyer_name':trans['name'],
                    # 'buyer_id'  :trans['buyerAccountPointLeval'],
                    'buyer_time':datetime.strptime(trans['date'],'%d %b %Y %H:%M'),
                }

            except:
                print('Error ')
                continue
            print(obj)

            data.append(obj)
        
        return data
    
    