from django.db import models

# ตัวอย่าง model
class Line(models.Model):
    column1 = models.CharField(max_length=100)
    column2 = models.CharField(max_length=100)
    
    def __str__(self):
        return self.column1