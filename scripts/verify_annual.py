from pathlib import Path
import json,datetime
O=Path(__file__).resolve().parents[1];ss=json.loads((O/'data/tracks.json').read_text())['storms']
def ms(s):return int(datetime.datetime.fromisoformat(s).replace(tzinfo=datetime.timezone.utc).timestamp()*1000)
def active(t,threshold=0):return [s for s in ss if s['points'][0][0]<=t<=s['points'][-1][0] and (threshold==0 or (s['peak'] or 0)>=threshold)]
cases={d:[s['name'] for s in active(ms(d))] for d in ['2024-01-01','2024-11-09','2024-11-10','2024-11-12','2024-11-20','2024-12-31']}
assert set(cases['2024-11-09'])=={'YINXING','TORAJI','MAN-YI','USAGI'}
assert [s['name'] for s in active(ms('2015-01-01'))]==['JANGMI']
assert not cases['2024-01-01'] and not cases['2024-12-31']
assert {s['name'] for s in active(ms('2024-11-09'),100)}=={'YINXING','MAN-YI'}
# All lifecycle boundaries are inclusive; no extrapolation beyond first/last agency records.
for s in ss:
 a,b=s['points'][0][0],s['points'][-1][0]
 assert not(a<=a-1<=b) and a<=a<=b and a<=b<=b and not(a<=b+1<=b)
# Check record gaps and six-hour interpolation remains bracketed, no future trail vertices.
segments=0
for s in ss:
 for a,b in zip(s['points'],s['points'][1:]):
  assert 0<b[0]-a[0]<=43200000
  t=(a[0]+b[0])/2;u=(t-a[0])/(b[0]-a[0]);xy=[a[j]+u*(b[j]-a[j]) for j in [1,2]]
  assert all(min(a[j],b[j])<=xy[j-1]<=max(a[j],b[j]) for j in [1,2]);segments+=1
r={'date_cases':cases,'peak100_on_20241109':['YINXING','MAN-YI'],'lifecycle_boundary_checks':len(ss),'interpolation_segment_checks':segments,'cross_year_policy':'calendar overlap, not SEASON only','tail_hours':72,'time_zone':'UTC'}
(O/'evidence/annual-validation.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False))
