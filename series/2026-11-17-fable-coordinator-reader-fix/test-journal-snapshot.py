import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, '/home/imalison/.local/share/dominion/automation')
from best_of_series import complete_records

with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp)/'events.jsonl'
    p.write_bytes(b'{"event": 1}\n{"event":')
    assert list(complete_records(p)) == [{'event': 1}]
    with p.open('ab') as f:f.write(b' 2}\n')
    assert list(complete_records(p)) == [{'event': 1}, {'event': 2}]
    class GrowingFile:
        calls = 0
        def read_bytes(self):
            self.calls += 1
            snapshot = p.read_bytes()
            with p.open('ab') as f:f.write(b' 3}\n')
            return snapshot
    p.write_bytes(b'{"event": 1}\n{"event":')
    growing = GrowingFile()
    assert list(complete_records(growing)) == [{'event': 1}]
    assert growing.calls == 1
    assert list(complete_records(p)) == [{'event': 1}, {'event': 3}]
    p.write_bytes(b'{"valid":true}\nnot-json\n')
    try:list(complete_records(p))
    except RuntimeError:pass
    else:raise AssertionError('Complete malformed record was accepted')
    p.write_bytes(b'{"valid":true}\n{"partial":"\xe2\x82')
    assert list(complete_records(p)) == [{'valid': True}]
print('5 completed-record snapshot, concurrent append, malformed record and UTF8-tail checks passed')
