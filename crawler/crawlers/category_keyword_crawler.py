
from products_crawler.crawlers.category_crawler import CategoryCrawler
from products_crawler.models import Category


class CategoryKeywordCrawler(CategoryCrawler):
    
    
    
    def _extract_products(self,tree):
        
        category        = tree.select_one('.current-cate')
        if not category:
            return []
            
        category_name   = category.get_text()
        category_url    = category.get('href')
        
        _category, _ = Category.objects.update_or_create(
            name=category_name,
            defaults={
                'name'      :category_name,
                'url'       :category_url,
            }
        )
        self.category = _category
        return super()._extract_products(tree)
        
    def _refactor_data(self,product):
        product.update({
            'category':self.category
        })
        return product