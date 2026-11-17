import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, '/home/imalison/.local/share/dominion/automation')
from fixed_series import FixedSeries as BestOfSeries

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    cfg = {'state_dir': str(root/'state'), 'archives_dir': str(root/'archives'), 'agents': ['Fable High', 'Astra High'], 'required_models': {'Fable High': 'claude-fable-5-2', 'Astra High': 'gpt-6-astra'}, 'best_of': 5, 'max_total_games': 15}
    s = BestOfSeries(cfg)
    assert not s.model_check('g1')['finished']
    for name, program, model in [('Fable High', 'claude', 'claude-fable-5-2'), ('Astra High', 'openai', 'gpt-6-astra')]:
        p = root/'archives'/name;p.mkdir(parents=True)
        events = [{'kind': 'seat', 'data': {'agent': {'name': name, 'program': program, 'model': model}, 'job': {'gameId': 'g1'}}}]
        if program == 'openai':events.append({'kind': 'direct_request', 'data': {'model': model}})
        events.append({'kind': 'seat_finished', 'data': {'result': {'Ok': None}}})
        (p/'interactions.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events))
        if program == 'claude':(p/'response-000001.stdout.jsonl').write_text(json.dumps({'type': 'assistant', 'message': {'model': model}})+'\n')
    report = s.model_check('g1');assert report['eligible'] and report['finished']
    stdout = root/'archives/Fable High/response-000001.stdout.jsonl'
    with stdout.open('a') as f:f.write(json.dumps({'type': 'assistant', 'message': {'model': 'claude-opus-5'}})+'\n')
    report = s.model_check('g1');assert not report['eligible'] and report['finished'];assert (s.directory/'deployment-hold.json').exists()
    s.state['completed'] = [{'game_id': 'g1', 'winner': 'Astra High', 'eligible_for_score': False}, {'game_id': 'g2', 'winner': 'Fable High', 'eligible_for_score': True}]
    assert s.score() == {'Fable High': 1, 'Astra High': 0}
    stdout.write_text(json.dumps({'type': 'assistant', 'message': {'model': 'claude-fable-5-2'}})+'\n'+json.dumps({'type': 'result', 'is_error': True, 'stop_reason': 'refusal'})+'\n')
    assert not s.model_check('g1')['eligible']
    stdout.write_text(json.dumps({'type': 'assistant', 'message': {'model': 'claude-fable-5-2'}})+'\n'+ '{"type":')
    assert s.model_check('g1')['eligible']
    journal=root/'archives/Fable High/interactions.jsonl';lines=journal.read_text().splitlines(True);journal.write_text(lines[0])
    assert not s.model_check('g1')['finished']
    direct = root/'archives/Astra High/interactions.jsonl'
    with direct.open('a') as f:
        f.write(json.dumps({'kind': 'seat_finished', 'data': {'result': {'Err': 'provider unavailable'}}})+'\n')
    assert not s.model_check('g1')['eligible']
    unexpected = root/'archives/unexpected'
    unexpected.mkdir()
    (unexpected/'interactions.jsonl').write_text(json.dumps({'kind':'seat','data':{'agent':{'name':'Unexpected'},'job':{'gameId':'g1'}}})+'\n')
    assert any('Unexpected agent' in p for p in s.model_check('g1')['problems'])
print('9 model guard checks passed, including direct-provider errors and unexpected agents')
