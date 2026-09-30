from django.db import models


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    background_image = models.ImageField(upload_to='estatic/images/')
    tag = models.CharField(max_length=100)
    valid_until = models.CharField(max_length=100 , null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
        

class PromotionCondition(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='conditions')
    condition_text = models.TextField()
    
    class Meta:
        verbose_name = 'Promotion condition'
        verbose_name_plural = 'Promotion conditions'
        


