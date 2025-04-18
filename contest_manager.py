from datetime import datetime


class Contest:
    def __init__(
        self, id: int, host: str, href: str, duration: int,
        start: datetime, end: datetime, contest_title: str
    ):
        self.id = id
        self.host = host
        self.href = href
        self.duration = duration
        self.start = start
        self.end = end
        self.contest_title = contest_title


class ContestManager:
    @staticmethod
    def parse_contest(contest: dict):
        return Contest(
            id=contest['id'],
            host=contest['host'],
            href=contest['href'],
            duration=contest['duration'],
            start=contest['start'],
            end=contest['end'],
            contest_title=contest['event']
        )

    @staticmethod
    def get_contests_from_json(json: dict):
        return [ContestManager.parse_contest(contest) for contest in json['objects']]
