# Day13 — Interactions · Storms in motion

[互動地圖](https://dongpo.github.io/geomni-30daymap-2026-day13-typhoons/) · [完整操作影片](https://dongpo.github.io/geomni-30daymap-2026-day13-typhoons/video/) · [資料說明](https://dongpo.github.io/geomni-30daymap-2026-day13-typhoons/DATA-NOTES.html)

Geomni #30DayMapChallenge 2026。以 Kepler.gl 原生 Trip layer 呈現西北太平洋同期氣旋、強度與資料支持的 30/50 kt 概化風圈。1980–2024 年，1,142 個氣旋、42,118 筆保留機構紀錄。預設 2024-11-10，時間 UTC。

## 操作

播放全年時間、指定日期、篩選年份與生命史最高風速。點選氣旋或名稱查看該時刻紀錄；選取會暫停，不重設時間。青色圈是 30 kt、橙色圈是 50 kt；中心與尾跡配色表示 JMA 10 分鐘平均最大持續風速。末筆紀錄後中心移除，過去72小時的尾跡逐漸淡去。

## 資料與限制

- NOAA NCEI IBTrACS v04r01 Western Pacific，2026-11-12 UTC 保存的快照；採 JMA/Tokyo 欄位，排除 IBTrACS 補出的時間點。
- 缺值不等於零。風圈由最長／最短半徑及方向作偏心圓概化，不是完整風場、官方精細邊界或災害範圍。
- 位置與完整半徑之間作動畫內插；風速沿用前筆紀錄。這是歷史 best-track 視覺化，不是即時觀測或預報。
- Natural Earth 1:110m land：public domain。前端依賴 CDN，需網路；套件版本與引用見 DATA-NOTES.html、index.html。

## 重現

地圖已附處理後資料，無須先安裝 GIS 工具。從專案根目錄啟動 `python3 -m http.server 8000`，瀏覽 `http://localhost:8000/`。不要直接以 file:// 開啟。

完整處理環境記錄為 requirements-lock.txt。資料處理至少需要 pandas、shapely；建置 HTML 使用已保存的前端模板。驗證另需 Node.js。

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
python3 scripts/unpack_source.py
.venv/bin/python scripts/prepare.py
.venv/bin/python scripts/prepare_wind.py
python3 scripts/build_html.py
node scripts/geometry-test.cjs
python3 scripts/verify_annual.py
```

原始 CSV 以 gzip 無損壓縮保存。解壓 SHA-256：`83bf4b39a266b327a80ad2e6a701afb730f3ed7e47cf07891ce207551950e569`。重新執行 prepare.py 的處理時間會改變；原始保存時間與版本請以本次提交的 DATA-NOTES.html 和 source 快照為準。不要把未更新的說明當成新下載資料的稽核結果。

## 影片與驗證

video/Day13-full-operation.mp4 為約43秒完整分頁操作實錄，原始 WebM 一併保存。1366×1080 原比例，平均28.7fps，未補幀；存在少量短頓，最長293ms。包含時間播放、MAN-YI/USAGI選取、同期風圈及強度演變。證據見 evidence/full-video-QA.json；不以錄影影格率宣稱所有裝置的地圖效能。

幾何驗證：41,471個有效風圈、42,765個缺值判定、40,976對中點。原生 Trip layer 與互動檢查見 evidence。

## 引用與權利

NOAA 公開提供 IBTrACS；資料原供應機構含 JMA。保留資料來源與引用，不以本專案名義改授第三方資料權利。

Gahtan et al. (2024), International Best Track Archive for Climate Stewardship (IBTrACS) Project, Version 4r01. NOAA NCEI. https://doi.org/10.25921/82ty-9e16

Knapp et al. (2010), The International Best Track Archive for Climate Stewardship (IBTrACS): Unifying tropical cyclone best track data. BAMS 91, 363–376. https://doi.org/10.1175/2009BAMS2755.1

Natural Earth: https://www.naturalearthdata.com/about/terms-of-use/

公開閱讀不表示原創程式與影片已另授開源授權；未指定的再利用權利請洽作者。第三方程式依各自授權。
