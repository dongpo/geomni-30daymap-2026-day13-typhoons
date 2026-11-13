from pathlib import Path
import pandas as pd,json,hashlib,datetime
O=Path(__file__).resolve().parents[1]
p=O/'source/ibtracs.WP.list.v04r01.csv'
d=pd.read_csv(p,skiprows=[1],low_memory=False,na_values=[' '])
a={'source_rows':len(d),'source_years':[int(d.SEASON.min()),int(d.SEASON.max())]}
s=d[d.SEASON.between(1980,2025)].copy();a['period_rows']=len(s)
s=s[s.TRACK_TYPE.str.lower().eq('main')];a['main_rows']=len(s)
s=s[s.IFLAG.str[1].isin(['O','V'])];a['original_tokyo_rows']=len(s)
s=s.dropna(subset=['TOKYO_LAT','TOKYO_LON']);s['ts']=pd.to_datetime(s.ISO_TIME,utc=True).astype('int64')//10**6
assert not s.duplicated(['SID','ts']).any()
assert s.TOKYO_LAT.between(-90,90).all()
s['lon']=s.TOKYO_LON%360
storms=[];gaps=0
for sid,g in s.groupby('SID'):
 g=g.sort_values('ts');points=[]
 for _,r in g.iterrows():
  w=None if pd.isna(r.TOKYO_WIND) else float(r.TOKYO_WIND)
  points.append([int(r.ts),round(r.lon,3),round(r.TOKYO_LAT,3),w,None if pd.isna(r.TOKYO_GRADE) else int(r.TOKYO_GRADE)])
 if len(points)<2:continue
 gaps+=sum(b[0]-a[0]>12*3600000 for a,b in zip(points,points[1:]))
 winds=[p[3] for p in points if p[3] is not None]
 storms.append(dict(id=sid,name=str(g.NAME.iloc[0]).strip(),year=int(g.SEASON.iloc[0]),peak=max(winds) if winds else None,points=points))
a.update(storms=len(storms),points=sum(len(x['points']) for x in storms),missing_wind=sum(p[3] is None for x in storms for p in x['points']),gaps_over_12h=gaps,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),download_recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),years={str(y):sum(x['year']==y for x in storms) for y in range(1980,2026)})
(O/'data/tracks.json').write_text(json.dumps({'storms':storms,'audit':a},separators=(',',':')),encoding='utf-8')
(O/'evidence/data-audit.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
# Clip only the land backdrop to the eastern-hemisphere map extent, avoiding world-spanning polygons.
from shapely.geometry import shape,mapping,box
land=json.loads((O/'source/ne_110m_land.geojson').read_text());features=[]
for f in land['features']:
 g=shape(f['geometry']).intersection(box(90,-10,180,70))
 if not g.is_empty:features.append({'type':'Feature','properties':{},'geometry':mapping(g)})
(O/'data/land.json').write_text(json.dumps({'type':'FeatureCollection','features':features}))
print(json.dumps(a,indent=2))
