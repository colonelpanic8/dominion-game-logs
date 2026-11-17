import collections
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

os.umask(0o077)
state_path = Path('/home/imalison/.local/state/dominion/series/sol-rating-20261116/status.json')
source_root = Path('/home/imalison/.local/state/dominion/agents/archives')
dest = Path('/home/imalison/Backups/dominion/sol-rating-20261116')
dest.mkdir(parents=True, exist_ok=False, mode=0o700)
state = json.loads(state_path.read_text())
assert state['phase'] == 'complete' and len(state['completed']) == 15
ids = {x['game_id'] for x in state['completed']}
assert len(ids) == 15
sessions = collections.defaultdict(list)
times = []

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def check_secrets(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in {'token', 'authorization', 'access_token', 'password', 'api_key', 'session_id', 'sessionid', 'cookie'}:
                assert item in ('[redacted]', None, ''), 'Unredacted credential field'
            check_secrets(item)
    elif isinstance(value, list):
        for item in value:
            check_secrets(item)

for path in sorted(source_root.glob('*/interactions.jsonl')):
    with path.open() as f:
        first = json.loads(next(f))
    gid = first.get('data', {}).get('job', {}).get('gameId')
    if gid not in ids:
        continue
    records = [json.loads(line) for line in path.open()]
    for record in records:
        check_secrets(record)
    target = dest / 'games' / gid.split(':')[1] / 'traces' / path.parent.name
    shutil.copytree(path.parent, target)
    for copied in target.rglob('*'):
        copied.chmod(0o700 if copied.is_dir() else 0o600)
        if copied.is_file():
            original = path.parent / copied.relative_to(target)
            assert digest(original) == digest(copied), 'Copy checksum mismatch'
    times.extend(r['time'] for r in records)
    sessions[gid].append((path, records))

assert set(sessions) == ids, 'Missing a game trace'
games = []
for number, result in enumerate(state['completed'], 1):
    gid = result['game_id']
    root = dest / 'games' / gid.split(':')[1]
    write_json(root / 'authoritative-result.json', result)
    latest = {}
    history = []
    last_seen = {}
    final_views = []
    summaries = []
    for path, records in sessions[gid]:
        kinds = collections.Counter(r['kind'] for r in records)
        agent = records[0]['data']['agent']
        assert agent['name'] == 'Sol High' and agent['model'] == 'gpt-6.1-sol' and agent['effort'] == 'high'
        summaries.append({'archive': path.parent.name, 'source': str(path.parent),
            'events': len(records), 'event_kinds': dict(kinds),
            'first_time_ms': records[0]['time'], 'last_time_ms': records[-1]['time'],
            'model': agent['model'], 'effort': agent['effort'],
            'recorded_final_view': bool(kinds['result'])})
        for record in records:
            data = record['data']
            view = None
            if record['kind'] == 'response':
                reply = data.get('reply', {}).get('json')
                if isinstance(reply, dict):
                    view = reply.get('view', reply)
                    entries = view.get('sinceLastDecision', reply.get('log', []))
                else:
                    entries = []
            elif record['kind'] == 'result':
                view = data.get('view', data)
                entries = view.get('sinceLastDecision', [])
            else:
                entries = []
            if isinstance(view, dict) and view.get('game', {}).get('running') is False:
                final_views.append({'time': record['time'], 'archive': path.parent.name, 'view': view})
            for entry in entries:
                if not isinstance(entry, dict) or not isinstance(entry.get('seq'), int):
                    continue
                seq = entry['seq']
                if entry != last_seen.get(seq):
                    history.append({'observed_at_ms': record['time'], 'archive': path.parent.name, 'entry': entry})
                    last_seen[seq] = entry
                latest[seq] = entry
    entries = [latest[i] for i in sorted(latest)]
    missing = sorted(set(range(max(latest) + 1)) - set(latest)) if latest else []
    write_json(root / 'observed-game-log.json', entries)
    (root / 'observed-game-log.txt').write_text(''.join(f"{e['seq']:05d} {e.get('text', json.dumps(e, ensure_ascii=False))}\n" for e in entries))
    (root / 'game-log-observations.jsonl').write_text(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in history))
    if final_views:
        write_json(root / 'recorded-final-views.json', final_views)
    game = {'number': number, 'game_id': gid, 'result': result['result'], 'sessions': summaries,
        'observed_log_entries': len(entries), 'log_seq_range': [min(latest), max(latest)] if latest else None,
        'missing_observed_sequence_numbers': missing, 'has_recorded_final_view': bool(final_views),
        'log_note': 'Observed entries and revisions only; authoritative result saved separately. An unobserved final notification is not reconstructed.'}
    write_json(root / 'coverage.json', game)
    games.append(game)

series = dest / 'series'
series.mkdir()
for source, name in [(state_path, 'status.json'),
    (Path('/home/imalison/.config/dominion/series/sol-rating-20261116.toml'), 'config.toml'),
    (Path('/home/imalison/.local/share/dominion/automation/rated_series.py'), 'rated_series.py')]:
    shutil.copy2(source, series / name)
shutil.copy2(Path(__file__), series / 'preserve-series.py')
start = dt.datetime.fromtimestamp(min(times)/1000, dt.timezone.utc) - dt.timedelta(minutes=5)
end = dt.datetime.fromtimestamp(max(times)/1000, dt.timezone.utc) + dt.timedelta(minutes=5)
journals = dest / 'journals'
journals.mkdir()
for service, user in [('dominion-sol-rated-15-20261116.service', True), ('dominion-agents.service', False), ('dominion.service', False)]:
    command = (['journalctl', '--user'] if user else ['/run/wrappers/bin/sudo', '-n', 'journalctl'])
    command += ['-u', service, '--since', start.strftime('%Y-%m-%d %H:%M:%S UTC'), '--until', end.strftime('%Y-%m-%d %H:%M:%S UTC'), '--no-pager', '-o', 'short-iso-precise']
    data = subprocess.check_output(command)
    (journals / (service + '.log')).write_bytes(data)

manifest = {'series': 'sol-rating-20261116', 'account': 'SolDominion', 'agent': 'Sol High',
    'created_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'completed_games': len(games),
    'agent_sessions': sum(len(g['sessions']) for g in games), 'games': games,
    'preservation': 'Byte-for-byte copies of all matching local agent archive directories; original files untouched. No official login or game reload performed.',
    'limitations': ['Only data actually recorded can be preserved. No raw official WebSocket capture was enabled.',
        'Some agent sessions stopped before the final server notification. Saved authoritative results cover all 15 games.',
        'Agent archives contain recorded tool requests/replies, legal views, usage and reasoning summaries; unrecorded provider internals are unavailable.',
        'Local disk archive and compressed copy; no off-machine backup is asserted.']}
write_json(dest / 'manifest.json', manifest)
lines = ['# SolDominion: 15 rated games, 2026-11-16', '',
    '12 wins, 3 losses. Sol High: gpt-6.1-sol, high reasoning effort.',
    'Officially verified final level 48.52, mu 0.68, phi 0.438; rank 1811.', '',
    '## Contents', '',
    '- `manifest.json`: per-game results, source trace locations, coverage and session counts.',
    '- `games/<id>/traces/`: unchanged original agent archives, including retries.',
    '- `games/<id>/observed-game-log.{json,txt}`: readable game entries extracted from recorded tool replies.',
    '- `games/<id>/game-log-observations.jsonl`: changes to previously observed log entries, with source and timestamp.',
    '- `games/<id>/authoritative-result.json`: result recorded by the coordinator or operator.',
    '- `series/`: final state, rating verification, flat config, coordinator and preservation script.',
    '- `journals/`: server, runner and coordinator journals during the series.',
    '- `SHA256SUMS`: checksums for every file other than this checksum file.', '',
    '## Coverage and limits', '',
    'All 15 games have agent traces. All recorded JSONL events parse cleanly.',
    'All copies were checked against their source with SHA-256.',
    'Eight games have a recorded finished-game view; the other seven have saved authoritative results but their traces end before that notification.',
    'Observed log sequences are checked for holes; see each coverage.json. Absence of holes does not prove that an unobserved final tail exists in the archive.',
    'Full raw responses and all observed log revisions are retained; the readable log is a convenience, not an independent official replay.',
    'No raw WebSocket capture or unrecorded provider internals can be recovered from these traces.',
    'No credentials, session files or password-store contents were copied. Existing token fields in agent archives are redacted.',
    'This is a local archive with a compressed copy, not an off-machine backup.', '',
    '## Verify', '', 'Run `sha256sum -c SHA256SUMS` from this directory.', '']
count_final = sum(g['has_recorded_final_view'] for g in games)
lines = [line.replace('Eight games have a recorded finished-game view; the other seven', f'{count_final} games have a recorded finished-game view; the other {15-count_final}') for line in lines]
(dest / 'README.md').write_text('\n'.join(lines))
for p in dest.rglob('*'):
    p.chmod(0o700 if p.is_dir() else 0o600)
files = sorted(p for p in dest.rglob('*') if p.is_file())
(dest / 'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.relative_to(dest)}\n' for p in files))
print(json.dumps({'archive':str(dest), 'games':len(games), 'sessions':manifest['agent_sessions'],
    'files':len(files)+1, 'bytes':sum(p.stat().st_size for p in dest.rglob('*') if p.is_file()),
    'recorded_final_views':count_final, 'log_sequence_gaps':{g['game_id']:g['missing_observed_sequence_numbers'] for g in games if g['missing_observed_sequence_numbers']}}))
