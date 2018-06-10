from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
from django.db.models import Count, Q, FloatField, F
from django.db.models.functions import Cast


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return getattr(self, 'name', super().__str__())
    
    class Meta:
        abstract = True


class ShopeeStore(BaseModel):
    
    store_id    = models.CharField(max_length=500)
    name        = models.CharField(max_length=500)



class ShopeeUser(BaseModel):
    
    user_id     = models.CharField(max_length=500)
    name        = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name


class ShopeeProduct(BaseModel):
    
    product_id  = models.CharField(max_length=500)
    name        = models.CharField(max_length=500)
    rating      = JSONField(default={})


class ShopeeCommentManager(models.Manager):
    def with_class(self):
        return self.all().annotate(
            _class=models.Case(
                models.When(rating__gte=4, then=models.Value('positive')),
                models.When(rating__lt=4, rating__gte=3, then=models.Value('neutral')),
                models.When(rating__lt=3, then=models.Value('negative')),
                output_field=models.CharField(),
            )
        )
    
    def class_count(self):
        return self.all().aggregate(
            positive    = Cast( Count( 'rating', filter = Q(rating__gte=4 )) ,FloatField()),
            neutral     = Cast( Count( 'rating', filter = Q(rating__lt=4  , rating__gte=3 )), FloatField()),
            negative    = Cast( Count( 'rating', filter = Q(rating__lt=3 )), FloatField()),
            total       = Cast( Count( 'id' ),FloatField())
        )
    
class ShopeeComment(BaseModel):
    
    comment_id  = models.CharField(max_length=500)
    user        = models.ForeignKey(ShopeeUser,on_delete=models.CASCADE)
    product     = models.ForeignKey(ShopeeProduct,on_delete=models.CASCADE)
    content     = models.TextField()
    rating      = models.PositiveIntegerField(default=0)
    
    objects     = ShopeeCommentManager()

    @staticmethod
    def all_with_class():
        
        return ShopeeComment.objects.all().annotate(
            _class=models.Case(
                models.When(                rating__gte=4,  then=models.Value('positive')),
                models.When(rating__lt=4,   rating__gte=3,  then=models.Value('neutral')),
                models.When(rating__lt=3,                   then=models.Value('negative')),
                output_field=models.CharField(),
            )
        )
    
    @staticmethod
    def class_count():
        return ShopeeComment.objects.all().aggregate(
            positive    = Cast( Count( 'rating', filter = Q(rating__gte=4 )) ,FloatField()),
            neutral     = Cast( Count( 'rating', filter = Q(rating__lt=4  , rating__gte=3 )), FloatField()),
            negative    = Cast( Count( 'rating', filter = Q(rating__lt=3 )), FloatField()),
            total       = Cast( Count( 'id' ),FloatField())
        )
    
    @staticmethod
    def class_prob():
        
        counts = ShopeeComment.class_count()
        
        return { k : counts[k]/counts['total'] for k in counts.keys() if k is not 'total'}
        
        
class UnexpectedValue(BaseModel):
    
    user        = models.ForeignKey(ShopeeUser,on_delete=models.CASCADE)
    name        = models.CharField(max_length=500)
    class_name  = models.CharField(max_length=500)
    value       = models.FloatField()

