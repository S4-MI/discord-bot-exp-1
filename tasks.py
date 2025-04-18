import discord
from discord.ext import tasks
import datetime
import requests
import json
from contest_manager import ContestManager
from config import CLIST_USERNAME, CLIST_API_KEY, CHECK_INTERVAL, NOTIFICATION_CHECK_INTERVAL, NOTIFICATION_TIMES, ALLOWED_CONTEST_SITES


class TaskManager:
    def __init__(self, bot, notification_manager):
        self.bot = bot
        self.notification_manager = notification_manager
        self.check_contests.start()
        self.send_notifications.start()

    async def fetch_contests(self) -> list:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        end_time = current_time + datetime.timedelta(days=7)

        url = "https://clist.by/api/v2/contest/"
        params = {
            'username': CLIST_USERNAME,
            'api_key': CLIST_API_KEY,
            'start__gte': current_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end__lte': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'order_by': 'start',
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            contests = ContestManager.get_contests_from_json(response.json())

            # Filter contests by allowed sites if specified
            if ALLOWED_CONTEST_SITES:
                contests = [contest for contest in contests if contest.host in ALLOWED_CONTEST_SITES]

            return contests
        except requests.exceptions.RequestException as e:
            print(f"Error fetching contests: {e}")
            return []

    @tasks.loop(minutes=CHECK_INTERVAL)
    async def check_contests(self):
        print("Checking for new contests...")
        contests = await self.fetch_contests()

        for contest in contests:
            self.notification_manager.add_contest(contest)

        self.notification_manager.remove_old_contests()
        print(f"Tracking {len(self.notification_manager.contest_data)} upcoming contests")

    @tasks.loop(minutes=NOTIFICATION_CHECK_INTERVAL)
    async def send_notifications(self):
        if not self.notification_manager.contest_data:
            return

        current_time = datetime.datetime.now(datetime.timezone.utc)
        channel = self.bot.get_channel(self.bot.notification_channel_id)

        if not channel:
            print(f"Error: Could not find channel with ID {self.bot.notification_channel_id}")
            return

        for contest_id, contest in self.notification_manager.contest_data.items():
            for minutes in NOTIFICATION_TIMES:
                notification_time = contest['start_time'] - datetime.timedelta(minutes=minutes)

                if (current_time <= notification_time <= current_time + datetime.timedelta(minutes=1) and
                        not contest['notifications'][minutes]):
                    contest['notifications'][minutes] = True
                    await self.notification_manager.send_notification(channel, contest, minutes)

    @check_contests.before_loop
    @send_notifications.before_loop
    async def before_tasks(self):
        await self.bot.wait_until_ready()
