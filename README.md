# waveguide-screening

碩論衍生的 Python 小專案。把原本的 MATLAB 篩選腳本重構成模組化 pipeline，使用 synthetic demo data 展示 physics-guided screening 的分析流程。

## What it does

依三個物理條件篩選 (波長, 寬度) 候選參數，再依傳輸效率排序：

- **C1**：中心軸 (r=0) 的 Er 能量排名前 5%（峰值夠高）
- **C2**：Er / Ephi 重疊積分 η ≥ 0.95（場分布對稱）
- **C3**：半擴散角 < 1.5°（光束發散夠低）

最後計算傳輸效率 = 偵測平面總能量 / 光源平面總能量，取 Top-10。

## Pipeline

![波導篩選管線：從 8,200 組候選到最優 Top 10](pipeline.png)

完整流程文字說明見 [PIPELINE.md](PIPELINE.md)。

## Why demo data

原始模擬資料來自專用光學 / 電磁模擬工具，未納入公開版本。本專案以 synthetic data 展示分析方法與篩選邏輯，**不重現論文結果**。

## How to run

```bash
pip install -r requirements.txt
python main.py
```

輸出：
- terminal 印出 Top-10 候選排行
- `outputs/screening_and.png`、`outputs/top10_scatter.png`

## Project structure

```
config.py              # 網格、閾值、隨機種子
generate_demo_data.py  # 物理啟發式合成資料
metrics.py             # 物理指標純函數
screening.py           # 篩選條件 + 排序
visualization.py       # 散點圖
main.py                # pipeline
```
