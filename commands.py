import discord
from discord.ext import commands
import datetime
from config import SITE_ICONS, DEFAULT_SITE_ICON


class CommandManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(name="upcoming")
    async def upcoming(self, ctx, count: int = 5):
        """Show upcoming contests"""
        contests = self.bot.notification_manager.get_upcoming_contests(count)

        if not contests:
            embed = discord.Embed(
                title="📅 No Contests Found",
                description="There are no upcoming contests at the moment.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Send header message
        header = discord.Embed(
            title="📅 Upcoming Contests",
            description=f"Found {min(count, len(contests))} upcoming contests",
            color=discord.Color.from_rgb(54, 57, 63)
        )
        await ctx.send(embed=header)

        # Send each contest as a separate message
        for contest in contests:
            site_icon = self._get_site_icon(contest['resource'])
            local_time = contest['start_time'].astimezone()
            time_format = local_time.strftime("%Y-%m-%d %H:%M:%S %Z (%A)")
            time_until = self._format_time_until(contest['start_time'])
            duration_str = self._format_duration(contest['duration'])

            embed = discord.Embed(
                title=f"🎯 {contest['name']}",
                description=(
                    f"**Platform:** {contest['resource']}\n"
                    f"**Duration:** {duration_str}\n"
                    f"**Start Time:** {time_format}\n"
                    f"**Time Until:** {time_until}\n"
                    f"[Join Contest]({contest['url']})"
                ),
                color=discord.Color.from_rgb(54, 57, 63),
                url=contest['url']
            )

            embed.set_thumbnail(url=site_icon)
            embed.set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None
            )

            await ctx.send(embed=embed)

    @commands.command(name="setnotificationchannel")
    @commands.has_permissions(administrator=True)
    async def set_notification_channel(self, ctx):
        """Set the current channel as the notification channel"""
        self.bot.notification_channel_id = ctx.channel.id

        embed = discord.Embed(
            title="✅ Channel Set",
            description=f"Contest notifications will now be sent to {ctx.channel.mention}",
            color=discord.Color.green()
        )

        embed.set_footer(
            text=f"Set by {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )

        await ctx.send(embed=embed)
