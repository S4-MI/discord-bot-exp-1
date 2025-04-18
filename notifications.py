import discord
import datetime
from config import NOTIFICATION_TIMES, SITE_ICONS, DEFAULT_SITE_ICON


class NotificationManager:
    def __init__(self, bot):
        self.bot = bot
        self.contest_data = {}

    def add_contest(self, contest):
        contest_id = contest.id
        if contest_id not in self.contest_data:
            # Ensure start_time is timezone-aware
            start_time = datetime.datetime.fromisoformat(contest.start)
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=datetime.timezone.utc)

            notifications = {minutes: False for minutes in NOTIFICATION_TIMES}

            self.contest_data[contest_id] = {
                'name': contest.contest_title,
                'url': contest.href,
                'start_time': start_time,
                'duration': contest.duration,
                'resource': contest.host,
                'notifications': notifications
            }

    def remove_old_contests(self):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        to_remove = [contest_id for contest_id, contest in self.contest_data.items()
                     if contest['start_time'] < current_time]

        for contest_id in to_remove:
            del self.contest_data[contest_id]

    def _get_site_icon(self, site):
        return SITE_ICONS.get(site, DEFAULT_SITE_ICON)

    def _format_duration(self, duration):
        hours, remainder = divmod(duration, 3600)
        minutes, _ = divmod(remainder, 60)
        if minutes:
            return f"{int(hours)}h {int(minutes)}m"
        return f"{int(hours)}h"

    def _format_time_until(self, start_time):
        time_until = start_time - datetime.datetime.now(datetime.timezone.utc)
        days, remainder = divmod(time_until.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        if days > 0:
            return f"{int(days)}d {int(hours)}h {int(minutes)}m"
        return f"{int(hours)}h {int(minutes)}m"

    async def send_notification(self, channel, contest, minutes):
        time_str = f"{minutes // 60} hour{'s' if minutes > 60 else ''}" if minutes >= 60 else f"{minutes} minutes"
        site_icon = self._get_site_icon(contest['resource'])
        local_time = contest['start_time'].astimezone()
        time_format = local_time.strftime("%Y-%m-%d %H:%M:%S %Z (%A)")
        time_until = self._format_time_until(contest['start_time'])
        duration_str = self._format_duration(contest['duration'])

        embed = discord.Embed(
            title=f"🎯 {contest['name']}",
            description=(
                f"**⏰ Starts in {time_str}!**\n\n"
                f"**Platform:** {contest['resource']}\n"
                f"**Duration:** {duration_str}\n"
                f"**Start Time:** {time_format}\n"
                f"**Time Until:** {time_until}"
            ),
            color=discord.Color.from_rgb(54, 57, 63),
            url=contest['url']
        )

        embed.set_thumbnail(url=site_icon)
        embed.set_footer(
            text="Click the contest name to join!",
            icon_url="https://cdn.discordapp.com/emojis/1064444110334861312.png"
        )

        await channel.send(embed=embed)
        print(f"Sent {time_str} notification for {contest['name']}")

    def get_upcoming_contests(self, count=5):
        if not self.contest_data:
            return []

        sorted_contests = sorted(self.contest_data.values(), key=lambda x: x['start_time'])
        return sorted_contests[:min(count, len(sorted_contests))]
