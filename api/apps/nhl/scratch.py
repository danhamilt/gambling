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



def create_seasons():
    from apps.nhl.constants import CURRENT_SEASON, BEGINNING_SEASON
    from apps.nhl.models.games_models import Season
    seasons = range(BEGINNING_SEASON, CURRENT_SEASON+1)
    for season in seasons:
        Season.objects.create(season=season, current = season == CURRENT_SEASON)
