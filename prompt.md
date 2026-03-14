# 提示词
在conda的stock虚拟环境下下载最近行情数据（stock环境中已包含所有依赖），要求使用Mootdx数据源

在conda的stock（已经包含所有依赖）下下载从20260101到现在的行情数据，要求使用mootdx数据源

在conda的stock（已经包含所有依赖）下执行选股

# 下载最近一个交易日的行情数据
conda activate stock && python fetch_kline.py --datasource mootdx --start 20260101 --end today --frequency 4 --out ./data  --workers 10 --exclude-gem true

说明：
如果使用mootdx数据源下载行情数据非常慢，可以先执行这个命令： python -m mootdx bestip -vv

# 执行选股
conda activate stock && python select_stock.py --data-dir ./data --config ./configs.json