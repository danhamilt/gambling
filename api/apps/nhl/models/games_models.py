from django.db import models

# Create your models here.
class Season(models.Model):
    season = models.IntegerField(unique=True)
    current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-season']

    def __str__(self):
        return f"{self.season}"
    
    def get_nhl_season(self):
        return f'{self.season-1}{self.season}'