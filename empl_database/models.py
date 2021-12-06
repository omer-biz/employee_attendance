from django.db import models

class Employee(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    full_name = models.CharField('Full Name', max_length=70)
    occupation = models.CharField('Occupation', max_length=256)
    sex = models.CharField('Sex', choices=GENDER, max_length=10)
    id_number = models.IntegerField('ID Number')
    image = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.full_name

    def show_desc(self):
        return self.occupation
