from django.db import models

class Myproduct(models.Model):
    prod_name=models.CharField(max_length=200,db_index=True,default='Name not found')
    prod_quantity = models.CharField(max_length=100, blank=False, null=False)
    prod_price = models.CharField(max_length=100, blank=False, null=False)

def __str__(self):
    return self.prod_name