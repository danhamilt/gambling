import datetime

from django.db import models
from apps.nhl.utilities import download_url
from apps.nhl.constants import BASE_API_URL
from apps.nhl.models import Team, Venue, Division, Conference, Franchise

class Game(models.Model):
    game_id = models.IntegerField(unique=True)
    link = models.URLField()
    game_type = models.CharField(max_length=1)
    season = models.ForeignKey('Season', on_delete=models.CASCADE)
    game_date = models.DateTimeField()
    home_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='away_team')
    class Meta:
        ordering = ['-game_date']

    def __str__(self):
        return f"{self.game_id} - {self.game_date} - {self.home_team} vs {self.away_team}"
    
class Season(models.Model):
    season = models.IntegerField(unique=True)
    current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-season']

    def __str__(self):
        return f"{self.season}"
    
    def get_nhl_season(self):
        return f'{self.season-1}{self.season}'
    
    def download_teams(self):
        url = f'{BASE_API_URL}/teams?expand=team.roster&season={self.get_nhl_season()}'
        return_json = download_url(url)
        for team in return_json['teams']:
            venue = team['venue']
            venue_object = Venue.objects.get_or_create(
                id=venue['id'],
                kwargs={
                    'name': venue['name'],
                    'link': venue['link'],
                    'city': venue['city'],
                    'timezone_id': venue['timeZone']['id'],
                    'timezone_offset': venue['timeZone']['offset'],
                    'timezone_tz': venue['timeZone']['tz']
                }
            )
            division = team['division']
            division_object = Division.objects.get_or_create(
                id=division['id'],
                kwargs={
                    'name': division['name'],
                    'link': division['link']
                }
            )
            conference = team['conference']
            conference_object = Conference.objects.get_or_create(
                id=conference['id'],
                kwargs={
                    'name': conference['name'],
                    'link': conference['link']
                }
            )   
            franchise = team['franchise']
            franchise_object = Franchise.objects.get_or_create(
                franchise_id=franchise['franchiseId'],
                kwargs={
                    'team_name': franchise['teamName'],
                    'link': franchise['link']
                }
            )   
            Team.objects.get_or_create(
                season=self,
                id=team['id'],
                kwargs={
                    'name': team['name'],
                    'link': team['link'],
                    'abbreviation': team['abbreviation'],
                    'team_name': team['teamName'],
                    'location_name': team['locationName'],
                    'first_year_of_play': team['firstYearOfPlay'],
                    'roster': team['roster'],
                    'short_name': team['shortName'],
                    'official_site_url': team['officialSiteUrl'],
                    'active': team['active'],
                    'franchise': franchise_object,
                    'division': division_object,
                    'conference': conference_object,
                    'venue': venue_object
                }
            )

    def download_games(self):
        url = f'{BASE_API_URL}teams?expand=team.roster&season={self.get_nhl_season()}'
        return_json = download_url(url)
        for dt in dates:
               game_date = datetime.strptime(dt, '%Y-%m-%d')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.download_teams()
        self.download_games()
