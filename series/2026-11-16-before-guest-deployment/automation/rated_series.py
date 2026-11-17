import argparse
import datetime as dt
import fcntl
import http.cookiejar
import json
from pathlib import Path
import subprocess
import time
import tomllib
import urllib.error
import urllib.request


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


class Series:
    def __init__(self, config):
        self.config = config
        self.directory = Path(config['state_dir'])
        self.directory.mkdir(parents=True, exist_ok=True)
        self.lock = (self.directory / 'lock').open('w')
        fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.path = self.directory / 'status.json'
        self.state = json.loads(self.path.read_text()) if self.path.exists() else {
            'created_at': now(), 'completed': [], 'active_game': None,
            'awaiting_game': False, 'previous_game': None,
        }
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.idle_since = None

    def save(self, phase, **updates):
        self.state.update(updates, phase=phase, updated_at=now(),
                          target=self.config['games'], agent=self.config['agent'],
                          account=self.config['account_name'])
        tmp = self.path.with_suffix('.tmp')
        tmp.write_text(json.dumps(self.state, indent=2) + '\n')
        tmp.replace(self.path)

    def note(self, message):
        print(f'{now()} {message}', flush=True)

    def request(self, suffix, body=None):
        url = self.config['server'] + '/api/online/' + self.config['account_id'] + '/' + suffix
        return self.http(url, body)

    def http(self, url, body=None):
        headers = {'Origin': self.config['server']}
        if body is not None:
            headers['Content-Type'] = 'application/json'
        request = urllib.request.Request(url, headers=headers,
            data=json.dumps(body).encode() if body is not None else None)
        try:
            with self.opener.open(request, timeout=120) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            detail = error.read(4096).decode(errors='replace')
            raise RuntimeError(f'HTTP {error.code}: {detail}') from None

    def login(self):
        password = subprocess.check_output(['pass', 'show', self.config['password_entry']],
                                            text=True).splitlines()[0]
        self.http(self.config['server'] + '/api/auth/login',
                  {'name': self.config['owner'], 'password': password})

    def tick(self):
        status = self.request('manage')
        observation = self.request('view')
        if status['id'] != self.config['account_id'] or status.get('account') != self.config['account_name']:
            raise RuntimeError('Account identity changed')
        if status.get('agent') not in (None, self.config['agent']):
            raise RuntimeError('Another agent is assigned to this account')
        if not status['connected'] or status.get('error') or observation.get('error'):
            active = self.state['active_game']
            recoveries = self.state.setdefault('reconnects', {})
            limit = self.config.get('reconnects_per_game', 1)
            observed = (observation.get('view') or {}).get('game') or {}
            if active and observed.get('id') == active and recoveries.get(active, 0) < limit:
                recoveries[active] = recoveries.get(active, 0) + 1
                self.save('reconnecting')
                self.note(f'Reconnecting existing session for {active}; attempt {recoveries[active]}/{limit}')
                self.request('reconnect', {})
                return False
            raise RuntimeError('Official connection needs inspection: ' + str(status.get('error') or observation.get('error')))
        view = observation.get('view') or {}
        game = view.get('game') or {}
        game_id = game.get('id')
        completed = {entry['game_id'] for entry in self.state['completed']}
        active = self.state['active_game']
        if self.state['awaiting_game'] and game_id and game_id != self.state['previous_game'] and game_id not in completed:
            active = game_id
            self.save('playing', active_game=active, awaiting_game=False)
            self.note(f'Game {len(completed) + 1}/{self.config["games"]} matched: {active}')
        if active:
            if game_id != active:
                raise RuntimeError('Active game disappeared or changed before its result')
            if status['mode'] != 'rated':
                raise RuntimeError('Active game is not rated')
            result = game.get('result')
            if not game.get('running') and result:
                if not any(p['name'] == self.config['account_name'] for p in result['players']):
                    raise RuntimeError('Official result does not contain this account')
                self.state['completed'].append({'game_id': active, 'completed_at': now(), 'result': result})
                self.save('between_games', active_game=None, previous_game=active)
                self.note(f'Completed {len(self.state["completed"])}/{self.config["games"]}: {active} ' +
                          json.dumps(result['players']))
                active = None
                completed.add(game_id)
            elif game.get('running'):
                if status.get('agent') is None:
                    self.request('agent', {'agent': self.config['agent']})
                    self.note('Reattached selected agent to the active game')
                self.save('playing', current_turn=view.get('turn'))
                return False
            else:
                raise RuntimeError('Game stopped without an authoritative result')
        if len(self.state['completed']) >= self.config['games']:
            self.save('complete', finished_at=now())
            self.note(f'Finished all {self.config["games"]} rated games; no more searches will start')
            return True
        if status['running'] and not active:
            raise RuntimeError('An untracked game is running; refusing to take it over')
        if status['searching']:
            if not self.state['awaiting_game']:
                raise RuntimeError('An untracked search already exists')
            self.idle_since = None
            self.save('searching', queue_feedback=status.get('queueFeedback', []))
            return False
        if self.state['awaiting_game']:
            self.idle_since = self.idle_since or time.monotonic()
            if time.monotonic() - self.idle_since > 60:
                raise RuntimeError('Search ended without a new game; refusing to submit another search')
            return False
        if status.get('agent') is not None:
            return False
        if self.config['agent'] not in status['agents']:
            raise RuntimeError('Selected runner agent is unavailable')
        if game_id and game_id not in completed and self.state.get('initial_checked'):
            raise RuntimeError('Unexpected game appeared outside this series')
        self.save('starting_search', awaiting_game=True, previous_game=game_id,
                  initial_checked=True, last_search_at=now())
        body = {'agent': self.config['agent'], 'mode': 'rated', 'matching': {
            'players': self.config['players'], 'minRating': self.config['min_rating'],
            'maxRating': self.config['max_rating'], 'timer': self.config['timer']}}
        self.request('start', body)
        self.save('searching')
        self.note(f'Searching for rated game {len(completed) + 1}/{self.config["games"]}; ' +
                  f'agent={self.config["agent"]}, rating={self.config["min_rating"]}..{self.config["max_rating"]}')
        return False

    def run(self):
        try:
            self.login()
            while not self.tick():
                time.sleep(self.config['poll_seconds'])
        except Exception as error:
            self.save('needs_attention', error=str(error))
            self.note(f'Stopped scheduling new games: {error}')
            raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=Path)
    args = parser.parse_args()
    with args.config.open('rb') as handle:
        Series(tomllib.load(handle)).run()
