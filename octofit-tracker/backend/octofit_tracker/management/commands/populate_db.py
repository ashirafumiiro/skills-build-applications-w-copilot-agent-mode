from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import models as app_models

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        app_models.Team.objects.all().delete()
        app_models.Activity.objects.all().delete()
        app_models.Leaderboard.objects.all().delete()
        app_models.Workout.objects.all().delete()

        # Create teams
        marvel = app_models.Team.objects.create(name='Team Marvel')
        dc = app_models.Team.objects.create(name='Team DC')

        # Create users (super heroes)
        ironman = User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password', team=marvel)
        captain = User.objects.create_user(username='captain', email='captain@marvel.com', password='password', team=marvel)
        batman = User.objects.create_user(username='batman', email='batman@dc.com', password='password', team=dc)
        superman = User.objects.create_user(username='superman', email='superman@dc.com', password='password', team=dc)

        # Create activities
        app_models.Activity.objects.create(user=ironman, type='run', duration=30, points=50)
        app_models.Activity.objects.create(user=captain, type='walk', duration=60, points=30)
        app_models.Activity.objects.create(user=batman, type='strength', duration=45, points=40)
        app_models.Activity.objects.create(user=superman, type='run', duration=50, points=60)

        # Create workouts
        app_models.Workout.objects.create(user=ironman, description='Morning run', calories=300)
        app_models.Workout.objects.create(user=batman, description='Night training', calories=400)

        # Create leaderboard
        app_models.Leaderboard.objects.create(team=marvel, points=80)
        app_models.Leaderboard.objects.create(team=dc, points=100)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
