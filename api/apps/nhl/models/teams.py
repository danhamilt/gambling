from django.db import models

    
# Create DivisionSeason model
class Team(models.Model):
    """
        Every season there will be a new team instance for each team in the NHL.
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    team_name = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100)
    first_year_of_play = models.CharField(max_length=4)
    roster = models.JSONField()
    short_name = models.CharField(max_length=100)
    official_site_url = models.URLField()
    active = models.BooleanField()
    franchise = models.ForeignKey('Franchise', on_delete=models.CASCADE)
    division = models.ForeignKey('Division', on_delete=models.CASCADE)
    conference = models.ForeignKey('Conference', on_delete=models.CASCADE)
    season = models.ForeignKey('Season', on_delete=models.CASCADE)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('id', 'season')
        
class Franchise(models.Model):
    franchise_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name
    
class Conference(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Division(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Venue(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    timezone_id = models.CharField(max_length=100)
    timezone_offset = models.IntegerField()
    timezone_tz = models.CharField(max_length=100)

    def __str__(self):
        return self.name