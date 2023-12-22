# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from asgiref.sync import sync_to_async
#import mysql.connector as mysql
from django.db.models import F
from mbb.models import School, Season, Team, Player, PlayerSeason
from stats.models import MbbGameEspn, MbbStatlineEspn, MbbGameSref, MbbStatlineSref


class MbbLiveStatsPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        game = MbbGameEspn.objects.get(id=item[1]['game_id'])
        if item[1]['minutes'] != None:
            game.is_final = True
            game.save()
            game_status = f"Game {game.id} @ {School.objects.get(espn_id=game.home_id).short_name} Is Now Final"
        else:
            game_status = f"Game {game.id} @ {School.objects.get(espn_id=game.home_id).short_name} Not Yet Final"
        for line in item.values():
            MbbStatlineEspn.objects.update_or_create(
                player_id = line['player'],
                game_code_id = MbbGameEspn.objects.get(id=line['game_id']).id,
                defaults = {
                    'started_game': line['start'],
                    'field_goals': line['field_goals'],
                    'shot_attempts': line['shot_attempts'],
                    'three_pointers': line['three_pointers'],
                    'three_pt_att': line['three_pt_att'],
                    'free_throw_makes': line['free_throw_makes'],
                    'free_throw_att': line['free_throw_att'],
                    'points': line['points'],
                    'rebounds': line['rebounds'],
                    'off_reb': line['oreb'],
                    'def_reb': line['dreb'],
                    'assists': line['assists'],
                    'steals': line['steals'],
                    'blocks': line['blocks'],
                    'turnovers': line['turnovers'],
                    'fouls': line['fouls'],
                    'minutes': line['minutes'],
                },
            )
        statline_status = 'Statlines Updated in Table'
        return f"{game_status} - {statline_status}"


class MbbSchoolsEspnPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        School.objects.create(
            name = item['team'],
            espn_id = item['espn_id'],
        )
        return item

class MbbSchoolsSrefPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        lookup = School.objects.get(sref_id=item['sref_id'])
        lookup.city = item['city']
        lookup.state = item['state']
        lookup.save()
        return item
    
############
class MbbGamesAmEspnPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        if not isinstance(item['away_team_id'], int):
                #School.objects.get_or_create(name=item['away_team_id'])
                item['away_team_id'] = None
        MbbGameEspn.objects.update_or_create(
            id = item['id'],
            defaults = {
                'season': Season.objects.get(end_date=None),
                'date': item['date'],
                'home_id': item['home_team_id'],
                'away_id': item['away_team_id'],
                'time': item['time'],
                'location': item['location'],
                'arena': item['arena'],
                'spread': item['spread'],
                'total': item['total'],
                'favorite': item['favorite'],
            }
        )
        return f"Game ({item['id']}) Updated in Game Table Successfully."

class MbbGameDataEspnPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        if not isinstance(item['away_team_id'], int):
            try:
                school_id = Team.objects.get(season=Season.objects.get(end_date=None), short_name=item['away_team_id']).school
                espn = School.objects.get(id=school_id).espn_id
                item['away_team_id'] = espn
            except:
                item['away_team_id'] = None
        MbbGameEspn.objects.update_or_create(
            id = item['id'],
            defaults = {
                'date': item['date'],
                'time': item['time'],
                'location': item['location'],
                'arena': item['arena'],
            }
        )
        return f"Game ({item['id']}) Updated in Game Table Successfully."
    
class MbbPlayersSrefPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        school = School.objects.get(sref_id=item['team'][0])
        team = Team.objects.get(school_id=school.id, season_id=item['team'][1])
        if team.coach == None:
            team.coach = item['coach']
            team.save()
        for person in item['roster'].values():
            try:
                player_season = PlayerSeason.objects.get(number=person['number'], team_id=team.id, season_id=item['team'][1])
                if player_season.height == None or player_season.weight == None or player_season.academic_year == None or player_season.position == None:
                    if player_season.height == None:
                        player_season.height = person['height']
                    if player_season.weight == None:
                        player_season.weight == person['weight']
                    if player_season.position == None:
                        player_season.position == person['position']
                    if player_season.academic_year == None:
                        player_season.academic_year = person['class']
                    player_season.save()
                player = Player.objects.get(id=player_season.player_id)
                if player.sref_id == None:
                    player.sref_id = person['sref_id']
                    player.high_school = person['high_school']
                    player.top_100 = person['top100']
                    player.save()
            except:
                print(f"Exception present at {item['team'][0]}")
        return f"Team {item['team'][0]} page processed."
            

class MbbPlayersPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        try:
            Player.objects.get(espn_id=item['espn_id'])
            print('Player Already Exists in Table')
        except:
            Player.objects.create(
                name = item['name'],
                hometown = item['birthplace'],
                espn_id = item['espn_id']
            )
            print('Player Successfully Added to Database')
        try:
            new_player = Player.objects.get(espn_id=item['espn_id'])
            PlayerSeason.objects.get(player_id=new_player.id, season_id=Season.objects.get(year=2024).year)
            return 'PlayerSeason Already Exists'
        except:
            if item['height'] == '--':
                item['height'] = None
            else:
                item['height'] = float(float(item['height'].split("\' ")[0]) + (float(item['height'].split("\' ")[-1].strip('"')) / 12))
            if item['weight'] == '--':
                item['weight'] = None
            else:
                item['weight'] = int(item['weight'].split(' ')[0])
            if item['position'] == 'ATH':
                item['position'] = None
            PlayerSeason.objects.create(
                number = item['number'],
                position = item['position'],
                height = item['height'],
                weight = item['weight'],
                academic_year = item['class'],
                player_id = new_player.id,
                season_id = Season.objects.get(year=2024).year,
                team_id = Team.objects.get(season_id=Season.objects.get(year=2024).year, school_id=School.objects.get(espn_id=item['school_espn'])).id
            )
            return 'Player and PlayerSeason Successfully Added'

        
class MbbGameDataSrefPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        MbbGameSref.objects.update_or_create(
            id = item['game_id'],
            defaults = {
                'date': item['date'],
                'team_one_id': item['team_one'],
                'score_one': item['score_one'],
                'team_two_id': item['team_two'],
                'score_two': item['score_two'],
                'season_id': Season.objects.get(year=2024).year
            }
        )
        for line in item['stats'].values():
            MbbStatlineSref.objects.update_or_create(
                player_id = line['id'],
                game_code_id = MbbGameSref.objects.get(id=item['game_id']).id,
                defaults = {
                    'minutes': line['minutes'],
                    'field_goals': line['fg'],
                    'field_goal_att': line['fga'],
                    'two_pts': line['2p'],
                    'two_pt_att': line['2pa'],
                    'three_pts': line['3p'],
                    'three_pt_att': line['3pa'],
                    'free_throws': line['ft'],
                    'free_throw_att': line['fta'],
                    'reb_o': line['orb'],
                    'reb_d': line['drb'],
                    'rebounds': line['reb'],
                    'assists': line['ast'],
                    'steals': line['stl'],
                    'blocks': line['blk'],
                    'turnovers': line['tov'],
                    'fouls': line['fls'],
                    'points': line['pts'],
                }
            )
        return f"Game data for {item['team_one']} @ {item['team_two']} updated successfully."


class ScraperPipeline:
    def process_item(self, item, spider):
        return item
  