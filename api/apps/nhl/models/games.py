import datetime

from django.db import models
from apps.nhl.utilities import download_url, haversine_distance
from apps.nhl.constants import BASE_API_URL
from apps.nhl.models.teams import Team, Franchise, Conference, Division, Venue

class Freq(models.Model):
    game = models.OneToOneField('nbaway_games.Game', to_field='game_id', related_name='freq')
    away_days_rest = models.IntegerField()
    away_pst_2_mst_b2b = models.BooleanField(db_column='amstb2b', default=False)
    away_first_of_2 = models.BooleanField(db_column='a1of2', default=False)
    away_first_of_3 = models.BooleanField(db_column='a1of3', default=False)
    away_2_of_3 = models.BooleanField(db_column='a2of3', default=False)
    away_b2b = models.BooleanField(default=False, db_column='ab2b')
    away_b2b2b = models.BooleanField(default=False, db_column='ab2b2b')
    # 2n3
    away_two_in_three = models.BooleanField(db_column='a2n3', default=False)
    # 3n4
    away_three_in_four = models.BooleanField(db_column='a3n4', default=False)
    # 4n5
    away_four_in_five = models.BooleanField(db_column='a4n5', default=False)
    # 4n6
    away_four_in_six = models.BooleanField(db_column='a4n6', default=False)
    # 5n6
    away_five_in_six = models.BooleanField(db_column='a5n6', default=False)
    # 5n7
    away_five_in_seven = models.BooleanField(db_column='a5n7', default=False)
    # 6n8
    away_six_in_eight = models.BooleanField(db_column='a6n8', default=False)
    # 6n9
    away_six_in_nine = models.BooleanField(db_column='a6n9', default=False)
    # 7n9
    away_seven_in_nine = models.BooleanField(db_column='a7n9', default=False)
    # 7n10
    away_seven_in_ten = models.BooleanField(db_column='a7n10', default=False)
    # 7n11
    away_seven_in_eleven = models.BooleanField(db_column='a7n11', default=False)
    # 8n11
    away_eight_in_eleven = models.BooleanField(db_column='a8n11', default=False)
    # 9n12
    away_nine_in_twelve = models.BooleanField(db_column='a9n12', default=False)

    home_days_rest = models.IntegerField()
    home_pst_2_mst_b2b = models.BooleanField(db_column='hmstb2b', default=False)
    home_first_of_2 = models.BooleanField(db_column='h1of2', default=False)
    home_first_of_3 = models.BooleanField(db_column='h1of3', default=False)
    home_2_of_3 = models.BooleanField(db_column='h2of3', default=False)
    home_b2b = models.BooleanField(default=False, db_column='hb2b')
    home_b2b2b = models.BooleanField(default=False, db_column='hb2b2b')
    # 2n3
    home_two_in_three = models.BooleanField(db_column='h2n3', default=False)
    # 3n4
    home_three_in_four = models.BooleanField(db_column='h3n4', default=False)
    # 4n5
    home_four_in_five = models.BooleanField(db_column='h4n5', default=False)
    # 4n6
    home_four_in_six = models.BooleanField(db_column='h4n6', default=False)
    # 5n6
    home_five_in_six = models.BooleanField(db_column='h5n6', default=False)
    # 5n7
    home_five_in_seven = models.BooleanField(db_column='h5n7', default=False)
    # 6n8
    home_six_in_eight = models.BooleanField(db_column='h6n8', default=False)
    # 6n9
    home_six_in_nine = models.BooleanField(db_column='h6n9', default=False)
    # 7n9
    home_seven_in_nine = models.BooleanField(db_column='h7n9', default=False)
    # 7n10
    home_seven_in_ten = models.BooleanField(db_column='h7n10', default=False)
    # 7n11
    home_seven_in_eleven = models.BooleanField(db_column='h7n11', default=False)
    # 8n11
    home_eight_in_eleven = models.BooleanField(db_column='h8n11', default=False)
    # 9n12
    home_nine_in_twelve = models.BooleanField(db_column='h9n12', default=False)

    def __str__(self):
        return f"Freq {self.game.game_id} - {self.game.game_date}"

class Game(models.Model):
    game_id = models.IntegerField(unique=True)
    link = models.URLField()
    game_type = models.CharField(max_length=1)
    season = models.ForeignKey('Season', on_delete=models.CASCADE)
    game_date = models.DateTimeField()
    home_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_team')
    previous_home_game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='previous_home_game', null=True)
    away_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='away_team')
    previous_away_game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='previous_away_game', null=True)
    away_distance_travelled = models.FloatField(null=True)
    home_distance_travelled = models.FloatField(null=True)
    away_altitude_difference = models.FloatField(null=True)
    home_altitude_difference = models.FloatField(null=True)
    away_days_rest = models.IntegerField(null=True)
    home_days_rest = models.IntegerField(null=True) 
    freq = models.OneToOneField('Freq', on_delete=models.CASCADE, null=True)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    live = models.BooleanField(default=False)
    class Meta:
        ordering = ['-game_date']

    def __str__(self):
        return f"{self.game_id} - {self.game_date} - {self.home_team} vs {self.away_team}"
    
    def save(self, *args, **kwargs):
        self.away_distance_travelled = haversine_distance(self.previous_away_game.venue.latitude, self.previous_away_game.venue.longitude, self.venue.latitude, self.venue.longitude)
        self.home_distance_travelled = haversine_distance(self.previous_home_game.venue.latitude, self.previous_home_game.venue.longitude, self.venue.latitude, self.venue.longitude)
        self.away_altitude_difference = self.previous_away_game.venue.altitude - self.venue.altitude
        self.home_altitude_difference = self.previous_home_game.venue.altitude - self.venue.altitude
        self.away_days_rest = (self.game_date - self.previous_away_game.game_date).days
        self.home_days_rest = (self.game_date - self.previous_home_game.game_date).days
        super().save(*args, **kwargs)
    
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
                name=venue['name'],
                kwargs={
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
        previous_game = {}
        for dt in dates:
            game_date = datetime.strptime(dt, '%Y-%m-%d')
            for game in dt['games']:
                venue = Venue.objects.get(id=game['venue']['id'])
                home_team = Team.objects.get(id=game['teams']['home']['team']['id'])
                away_team = Team.objects.get(id=game['teams']['away']['team']['id'])
                Game.objects.get_or_create(
                    game_id=game['gamePk'],
                    kwargs={
                        'link': game['link'],
                        'game_type': game['gameType'],
                        'season': self,
                        'game_date': game_date,
                        'home_team': home_team,
                        'previous_home_game': previous_game.get(home_team.id),
                        'away_team': away_team,
                        'previous_away_game': previous_game.get(away_team.id),
                        'completed': game['status']['detailedState'] == 'Final',
                        'venue': venue,
                    }
                )
                previous_game[home_team.id] = game
                previous_game[away_team.id] = game

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.download_teams()
        self.download_games()
