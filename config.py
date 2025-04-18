import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CLIST_USERNAME = os.getenv('CLIST_USERNAME')
CLIST_API_KEY = os.getenv('CLIST_API_KEY')
NOTIFICATION_CHANNEL_ID = int(os.getenv('NOTIFICATION_CHANNEL_ID'))

# Contest sites to monitor (comma-separated list from .env)
ALLOWED_CONTEST_SITES = [site.strip() for site in os.getenv('ALLOWED_CONTEST_SITES', '').split(',') if site.strip()]

# Contest site icons
SITE_ICONS = {
    'codeforces.com': 'https://codeforces.org/s/0/favicon-32x32.png',
    'codechef.com': 'https://cdn.codechef.com/images/cc-logo.svg',
    'atcoder.jp': 'https://img.atcoder.jp/assets/atcoder.png',
    'leetcode.com': 'https://leetcode.com/favicon.ico',
    'hackerrank.com': 'https://cdn.prod.website-files.com/66b6d7fd4d3e9cef94717176/6765dc51a13e31531996cef3_logo-dark.svg',
    'topcoder.com': 'https://www.topcoder.com/assets/topcoder-mobile-logo.svg',
    'codingcompetitions.withgoogle.com': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/1200px-Google_%22G%22_logo.svg.png',
    'facebook.com/hackercup': 'https://upload.wikimedia.org/wikipedia/commons/6/6c/Facebook_Logo_2023.png',
}

# Default icon for unknown sites
DEFAULT_SITE_ICON = 'https://clist.by/favicon.ico'

# Notification settings
NOTIFICATION_TIMES = [24 * 60, 12 * 60, 60, 10]  # 24 hours, 12 hours, 1 hour, 10 minutes
CHECK_INTERVAL = 30  # minutes
NOTIFICATION_CHECK_INTERVAL = 1  # minutes
