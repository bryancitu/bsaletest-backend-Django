from django.db import models

# Create your models here.
class Category(models.Model):
    """Model definition for category."""

    name    = models.CharField('name', max_length=200)

    class Meta:
        """Meta definition for category."""

        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        """Unicode representation of category."""
        return self.name

class Product(models.Model):
    """Model definition for product."""

    name        = models.CharField('name', max_length=200)
    url_image   = models.CharField('url_image', max_length=1000)
    price       = models.FloatField()
    discount    = models.IntegerField()
    category    = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        """Meta definition for product."""

        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        """Unicode representation of product."""
        return self.name


