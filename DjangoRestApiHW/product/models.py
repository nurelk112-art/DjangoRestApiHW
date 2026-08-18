from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(null=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="products",
    )

    def __str__(self) -> str:
        return self.title

STARS = ((i,'*' * 1)for i in range (1,6) )

class Review(models.Model):
    stars = models.IntegerField(choices=STARS, default=3)
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')

    def __str__(self) -> str:
        return self.text
