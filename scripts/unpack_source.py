from pathlib import Path
import gzip,hashlib
p=Path(__file__).resolve().parents[1]/'source/ibtracs.WP.list.v04r01.csv'
b=gzip.decompress(p.with_suffix('.csv.gz').read_bytes())
assert hashlib.sha256(b).hexdigest()=='83bf4b39a266b327a80ad2e6a701afb730f3ed7e47cf07891ce207551950e569'
p.write_bytes(b)
print('Source checksum verified:',p.name)
