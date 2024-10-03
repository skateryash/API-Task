from django.db import models

class Job(models.Model):
    STATUS = [
        ('Success', 'Success'),
        ('Failure', 'Failure')
    ]
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS, default='Failure')


class FEmployee(models.Model):
    STATUS = [
        ('Created', 'Created'),
        ('Updated', 'Updated')
    ]
    
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Created')
    job = models.CharField(max_length=200, default='')


class SEmployee(models.Model):
    STATUS = [
        ('Created', 'Created'),
        ('Updated', 'Updated')
    ]
    
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    salary = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, choices=STATUS, default='Created')
    job = models.CharField(max_length=200, default='')
