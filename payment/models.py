from django.db import models

# Create your models here.

class Payment(models.Model):
    payment_reference = models.CharField(max_length=25,blank=True,default='0')
    class Payment_Status(models.TextChoices):
        unpaid = 'Unpaid'
        paid = 'Paid'
    payment = models.CharField(max_length=25,blank=True,choices=Payment_Status.choices, default="Unpaid")    
    reference_number = models.CharField(max_length=30,)
    reference_url = models.CharField(max_length=255,)    

    def __str__(self):
        return str(self.id)
