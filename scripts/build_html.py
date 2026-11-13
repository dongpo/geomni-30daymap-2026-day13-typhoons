from pathlib import Path
O=Path(__file__).resolve().parents[1]
head=(O/'source/bootstrap-template.html').read_text().split('<body>')[0].replace('kepler.gl embedded map','Day13｜西北太平洋颱風路徑')
(O/'index.html').write_text(head+'<body style="background:#0b1722;color:white"><div id="app">載入IBTrACS 颱風資料與 Kepler.gl…</div><script type="text/kepler-bootstrap">'+(O/'scripts/app.js').read_text()+'</script></body></html>',encoding='utf-8')
