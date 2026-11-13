from pathlib import Path
import json,pandas as pd,collections
O=Path(__file__).resolve().parents[1];d=pd.read_csv(O/'source/ibtracs.WP.list.v04r01.csv',skiprows=[1],low_memory=False,na_values=[' ']);d=d[d.SEASON.between(1980,2024)&d.TRACK_TYPE.str.lower().eq('main')&d.IFLAG.str[1].eq('O')];d['ts']=pd.to_datetime(d.ISO_TIME,utc=True).astype('int64')//10**6
lookup={(r.SID,int(r.ts)):r for r in d.itertuples()};D=json.loads((O/'data/tracks.json').read_text());audit=collections.Counter()
for s in D['storms']:
 for p in s['points']:
  r=lookup.get((s['id'],p[0]));winds=[]
  for k in [30,50]:
   if r is None:vals=[None]*3
   else:vals=[getattr(r,f'TOKYO_R{k}_{c}') for c in ['DIR','LONG','SHORT']]
   direction,lo,sh=vals
   valid=all(x is not None and pd.notna(x) for x in vals) and direction in range(1,10) and lo>=sh>0 and (direction!=9 or lo==sh)
   winds.append([int(direction),float(lo),float(sh)] if valid else None);audit[f'r{k}_valid' if valid else f'r{k}_missing_or_invalid']+=1
  p[5:]=winds
D['wind_audit']=dict(audit);(O/'data/tracks.json').write_text(json.dumps(D,separators=(',',':')));(O/'evidence/wind-audit.json').write_text(json.dumps(dict(audit),indent=2));print(audit)
