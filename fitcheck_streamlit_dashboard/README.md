# Fitcheck Marketing Dashboard

这是一个使用Streamlit复刻的Fitcheck Marketing看板应用。

## 功能特性

- **动态过滤**: 支持按日期范围、平台、内容主题和目标受众过滤数据
- **KPI指标**: 展示总ROI、总收入、总转化数和平均转化成本
- **平台表现**: 横向条形图对比各平台ROI
- **转化趋势**: 展示每月转化数量趋势
- **效率分析**: 气泡图展示平台效率（转化数量 vs ROI）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
streamlit run app.py
```

应用将在浏览器中自动打开，默认地址为 http://localhost:8501

## 数据文件

应用使用 `Fitcheck OVERVIEW.csv` 作为数据源，包含以下字段：
- 营销活动信息（Campaign Name, Platform, Content Theme等）
- 性能指标（Conversions, Revenue, Spend, ROI等）
- 参与度数据（Clicks, Impressions, Engagement Rate等）

## 看板组件

1. **顶部过滤器**: 日期范围、平台、内容主题、目标受众
2. **KPI卡片**: 4个关键指标的可视化展示
3. **平台性能对比**: 各平台ROI横向对比，带有基准线
4. **月度转化趋势**: 时间序列折线图
5. **平台效率气泡图**: 多维度分析平台表现
