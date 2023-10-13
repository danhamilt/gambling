def download_season():
    import requests
    import json
    url = 'https://statsapi.web.nhl.com/api/v1/schedule'
    params = {
        'season': '20202021',
        'expand': 'schedule.teams,schedule.linescore,schedule.broadcasts.all',
    }

    response = requests.get(url, params=params)
    data = response.json()
    with open('/Users/danham/gambling/api/apps/nhl/fixtures/season_example.json', 'w') as f:
        json.dump(data, f)

def download_teams():
    import requests
    import json
    url = f'https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster&season={20202021}'

    response = requests.get(url)
    data = response.json()
    with open('/Users/danham/gambling/api/apps/nhl/fixtures/teams_example.json', 'w') as f:
        json.dump(data, f)

def download_rosters():
    import requests
    import json
    url = "https://statsapi.web.nhl.com/api/v1/teams/1/roster"
    response = requests.get(url)
    data = response.json()
    with open('/Users/danham/gambling/api/apps/nhl/fixtures/rosters_example.json', 'w') as f:
        json.dump(data, f)
'

def create_seasons():
    from apps.nhl.constants import CURRENT_SEASON, BEGINNING_SEASON
    from apps.nhl.models.games import Season
    seasons = range(BEGINNING_SEASON, CURRENT_SEASON+1)
    for season in seasons:
        season = Season.objects.create(season=season, current = season == CURRENT_SEASON)
        season.download_teams()


