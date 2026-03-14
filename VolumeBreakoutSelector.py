from typing import Dict, List
import pandas as pd


class VolumeBreakoutSelector:
    """
    放量突破选股器
    
    选股条件：
    1. 当天的成交量比前一天高N倍（可配置）
    2. 当天的收盘价高于开盘价，但是涨幅小于10%
    3. 当天收盘价高于近M天（可配置）的最高价
    """

    def __init__(self,
                 volume_ratio_threshold: float = 3.0,
                 high_day_window: int = 20):
        """
        初始化放量突破选股器
        
        Parameters
        ----------
        volume_ratio_threshold : float, default 3.0
            成交量比前一天高的倍数阈值
        high_day_window : int, default 20
            创新高的时间窗口（交易日）
        """
        self.volume_ratio_threshold = volume_ratio_threshold
        self.high_day_window = high_day_window
        # 涨幅上限设为10%
        self.max_pct_change = 10.0

    def _passes_filters(self, hist: pd.DataFrame) -> bool:
        """
        检查单支股票是否通过所有选股条件
        
        Parameters
        ----------
        hist : pd.DataFrame
            股票历史行情数据
            
        Returns
        -------
        bool
            是否通过所有条件
        """
        if len(hist) < self.high_day_window + 1:
            # 数据不足，无法计算条件
            return False

        # 获取最近一天的数据（当天）
        today = hist.iloc[-1]
        # 获取前一天的数据
        yesterday = hist.iloc[-2]
        
        # 条件1：当天的成交量比前一天高N倍
        if yesterday['volume'] <= 0 or today['volume'] / yesterday['volume'] < self.volume_ratio_threshold:
            return False
        
        # 条件2：当天的收盘价高于开盘价，但是涨幅小于10%
        if today['close'] <= today['open']:
            return False
        
        # 计算涨幅
        pct_change = (today['close'] - today['open']) / today['open'] * 100
        if pct_change >= self.max_pct_change:
            return False
        
        # 条件3：当天收盘价高于近M天的最高价
        recent_highs = hist.iloc[-(self.high_day_window + 1):-1]['high']
        if today['close'] <= recent_highs.max():
            return False
        
        return True

    def select(self, date: pd.Timestamp, data: Dict[str, pd.DataFrame]) -> List[str]:
        """
        批量选股
        
        Parameters
        ----------
        date : pd.Timestamp
            选股日期
        data : Dict[str, pd.DataFrame]
            股票代码到历史行情数据的映射
            
        Returns
        -------
        List[str]
            通过所有条件的股票代码列表
        """
        picks = []
        
        for code, df in data.items():
            # 筛选出日期小于等于指定日期的数据
            hist = df[df['date'] <= date]
            
            # 检查数据是否充足
            if len(hist) < self.high_day_window + 1:
                continue
            
            # 检查是否通过所有条件
            if self._passes_filters(hist):
                picks.append(code)
        
        return picks