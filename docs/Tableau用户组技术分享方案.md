# Tableau 到 Power BI 转换技术分享方案

> 面向 Tableau 用户组的技术分享完整指南

---

## 📋 分享基本信息

**主题**: Tableau 到 Power BI：无缝迁移的技术实践与案例分享

**时长建议**: 45-60 分钟（30分钟演讲 + 15-30分钟演示 + Q&A）

**目标听众**: Tableau 用户、数据分析师、BI 开发人员

**分享目标**:
1. 介绍 Tableau 到 Power BI 的转换技术
2. 展示实际转换案例（Superstore Dashboard）
3. 分享转换过程中的最佳实践和避坑指南
4. 现场演示转换流程
5. 回答听众疑问

---

## 🎯 分享大纲（推荐结构）

### 第一部分：开场和背景（5分钟）

#### 1.1 自我介绍和分享背景
```markdown
- 简单自我介绍
- 为什么要做这个项目？
  * 企业数字化转型需求
  * 多平台并存的现状
  * 客户/业务需求的多样性
- 今天分享的内容概览
```

#### 1.2 快速展示转换效果
```markdown
- 左右对比：Tableau vs Power BI
- 相同数据源
- 相同的可视化效果
- 相同的交互功能
```

**演示素材**:
- `tableau screenshot.jpg`
- `powerbi screenshot.jpg`
- 并排展示，突出相似度

---

### 第二部分：技术架构和方法论（10分钟）

#### 2.1 Tableau 和 Power BI 架构对比

**PPT 内容建议**:

| 维度 | Tableau | Power BI | 转换策略 |
|------|---------|----------|---------|
| **文件格式** | .twb (XML) | .pbip (JSON + TMDL) | 解析 XML → 生成 JSON |
| **数据模型** | 数据源 + 计算字段 | SemanticModel + DAX | 转换计算公式 |
| **可视化** | Worksheet + Dashboard | Report Pages + Visuals | 映射可视化类型 |
| **布局系统** | 相对单位（0-100000） | 像素坐标（1280×720） | 坐标转换 |
| **计算引擎** | Tableau Calculation | DAX | 函数映射 |

#### 2.2 转换技术栈

```
输入                    处理                    输出
┌─────────┐          ┌──────────┐          ┌─────────┐
│ .twb    │────────▶│  解析器   │────────▶│ .tmdl   │
│ (XML)   │          │  ·分析   │          │ (模型)  │
│         │          │  ·映射   │          │         │
│ .xls    │────────▶│  ·转换   │────────▶│ .json   │
│ (数据)  │          │  ·生成   │          │ (报表)  │
└─────────┘          └──────────┘          └─────────┘
    ↓                     ↓                     ↓
  Tableau            转换引擎              Power BI
```

#### 2.3 核心转换步骤概览

```markdown
1️⃣ 数据源映射
   - 识别 Tableau 数据源
   - 创建 Power BI 表结构
   - 映射字段类型和格式

2️⃣ 计算字段转换
   - Tableau 公式 → DAX
   - LOD 表达式 → CALCULATE
   - 参数 → 参数表

3️⃣ 可视化重建
   - 工作表 → 页面
   - 标记 → 可视化类型
   - 布局 → 坐标位置

4️⃣ 交互配置
   - 筛选器 → Slicer
   - 动作 → 交叉筛选
   - 参数控件 → 参数

5️⃣ 样式匹配
   - 颜色方案
   - 字体格式
   - 工具提示
```

---

### 第三部分：实战案例深度解析（15分钟）

#### 3.1 案例介绍：Superstore Dashboard

**展示内容**:
```markdown
📊 原始 Tableau 看板特点：
- 1个仪表板："Profitability Overview"
- 7个 KPI 指标卡片
- 1个地理分布地图
- 2个月度趋势面积图（按细分市场和产品类别）
- 4个交互式筛选器

📈 数据规模：
- 数据源：Sample - Superstore.xls
- 表：Orders（10,194 行）
- 字段：21 列
- 计算字段：7 个
```

#### 3.2 转换难点和解决方案

**难点 1: Tableau 计算字段转换**

```markdown
🔴 Tableau 公式（简单聚合）:
sum([Profit])/sum([Sales])

✅ Power BI DAX:
measure 'Profit Ratio' =
    DIVIDE(SUM(Orders[Profit]), SUM(Orders[Sales]), 0)
    formatString: 0.0%
```

**难点 2: LOD 表达式转换**

```markdown
🔴 Tableau LOD:
{FIXED [Order ID]:SUM([Profit])}>0

✅ Power BI DAX:
measure 'Order Profitable' =
    VAR OrderProfit = CALCULATE(
        SUM(Orders[Profit]),
        ALLEXCEPT(Orders, Orders[Order ID])
    )
    RETURN IF(OrderProfit > 0, "Profitable", "Unprofitable")
```

**难点 3: 按月分组聚合**

```markdown
🔴 问题：
Power BI 不支持直接使用日期层次结构的月份级别

✅ 解决方案：
创建计算列：
column 'Order Year-Month' = FORMAT(Orders[Order Date], "YYYY-MM")
    dataType: string
    dataCategory: Months

然后在可视化中使用这个列进行分组
```

**难点 4: 布局坐标转换**

```markdown
🔴 Tableau 坐标（相对单位）:
x: 571 (相对于 100000)
y: 667
width: 98858
height: 6526

✅ Power BI 坐标（像素）:
转换公式：
Power BI X = (Tableau X / 100000) × 1280 ≈ 7
Power BI Y = (Tableau Y / 100000) × 720 ≈ 5
...

简化后实际使用：
x: 10, y: 10, width: 1070, height: 40
```

#### 3.3 转换效果对比

**展示并排对比图**:

```markdown
指标对比：
┌─────────────────┬───────────┬────────────┬────────┐
│ 指标            │ Tableau   │ Power BI   │ 差异   │
├─────────────────┼───────────┼────────────┼────────┤
│ Total Sales     │ $1,317,840│ $1,317,840 │ ✅ 0%  │
│ Total Profit    │ $170,698  │ $170,698   │ ✅ 0%  │
│ Profit Ratio    │ 13.0%     │ 13.0%      │ ✅ 0%  │
│ Avg Discount    │ 15.7%     │ 15.7%      │ ✅ 0%  │
│ Total Quantity  │ 22,080    │ 22,080     │ ✅ 0%  │
└─────────────────┴───────────┴────────────┴────────┘

功能对比：
✅ 7个 KPI 卡片 - 完全一致
✅ 地图可视化 - 支持相同的气泡地图
✅ 面积图 - 支持堆叠和按月分组
✅ 筛选器 - 支持日期范围、下拉列表、多选
✅ 交互 - 支持交叉筛选和高亮
```

---

### 第四部分：技术深度揭秘（10分钟）

#### 4.1 Power BI 项目文件结构

```markdown
superstore dashboard.pbip/
│
├── 📄 项目入口
│   └── superstore dashboard.pbip
│
├── 📊 数据模型（SemanticModel）
│   ├── definition.pbism
│   └── definition/
│       ├── model.tmdl              # 模型配置
│       ├── database.tmdl           # 数据库设置
│       └── tables/
│           └── Orders.tmdl         # 表定义 + DAX 度量值
│
└── 📈 报表（Report）
    ├── definition.pbir
    └── definition/
        ├── report.json             # 报表配置
        └── pages/
            ├── pages.json          # 页面列表
            └── ProfitabilityOverview/
                ├── page.json       # 页面设置
                └── visuals/        # 可视化组件
                    ├── CardSales/
                    │   └── visual.json
                    ├── AreaChartSegment/
                    │   └── visual.json
                    └── ...
```

**讲解重点**:
- TMDL：Tabular Model Definition Language（文本格式，易于版本控制）
- JSON：可视化组件的完整定义
- 分离的架构：数据模型和报表独立管理

#### 4.2 DAX 度量值深度解析

**示例 1：简单聚合**

```dax
measure 'Total Sales' = SUM(Orders[Sales])
    formatString: \$#,0
    lineageTag: m-total-sales-001
```

**讲解点**:
- `SUM()` 函数：表级聚合
- `formatString`: 货币格式，千位分隔符
- `lineageTag`: 唯一标识符（用于追踪数据血缘）

**示例 2：除法运算**

```dax
measure 'Profit Ratio' = DIVIDE([Total Profit], [Total Sales], 0)
    formatString: 0.0%
```

**讲解点**:
- `DIVIDE()` 优于 `/`：自动处理除零错误
- 第三个参数 `0`：除零时返回的默认值
- 百分比格式：自动乘以 100 并添加 %

**示例 3：上下文转换（LOD）**

```dax
measure 'Order Profitable' =
    VAR OrderProfit = CALCULATE(
        SUM(Orders[Profit]),
        ALLEXCEPT(Orders, Orders[Order ID])
    )
    RETURN IF(OrderProfit > 0, "Profitable", "Unprofitable")
```

**讲解点**:
- `VAR`: 定义变量（提高性能，增加可读性）
- `CALCULATE()`: 修改筛选上下文
- `ALLEXCEPT()`: 保留指定列的筛选，移除其他筛选
- 等价于 Tableau 的 `{FIXED [Order ID]:SUM([Profit])}`

#### 4.3 可视化组件配置详解

**Card 可视化的 visual.json 结构**:

```json
{
  "$schema": "...",
  "name": "CardSales",
  "position": {                    // 位置和尺寸
    "x": 10, "y": 60,
    "z": 1001,                     // z-index 层级
    "height": 70, "width": 145
  },
  "visual": {
    "visualType": "card",          // 可视化类型
    "query": {                     // 数据查询
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {       // 引用度量值
                  "Expression": {
                    "SourceRef": {"Entity": "Orders"}
                  },
                  "Property": "Total Sales"
                }
              },
              "queryRef": "Orders.Total Sales",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {                   // 格式设置
      "categoryLabels": [{
        "properties": {
          "fontSize": {"expr": {"Literal": {"Value": "'10pt'"}}}
        }
      }],
      "labels": [{
        "properties": {
          "fontSize": {"expr": {"Literal": {"Value": "'18pt'"}}}
        }
      }]
    }
  }
}
```

**关键概念讲解**:
- `position`: 绝对像素坐标
- `queryState`: 数据查询定义（支持多个字段）
- `projections`: 字段投影（从数据模型到可视化）
- `objects`: 格式化属性（字体、颜色、样式等）
- `expr.Literal.Value`: 表达式字面值（支持动态值）

---

### 第五部分：现场演示（15分钟）

#### 演示流程

**演示 1: 打开并对比两个看板（3分钟）**

```markdown
1. 打开 Tableau Desktop，加载 Superstore.twb
   - 展示数据连接
   - 展示计算字段
   - 展示 Overview 仪表板

2. 打开 Power BI Desktop，加载 superstore dashboard.pbip
   - 展示数据模型（关系视图）
   - 展示度量值列表
   - 展示 Profitability Overview 页面

3. 并排对比
   - 使用双屏或分屏
   - 同时调整筛选器
   - 观察数值和图表的一致性
```

**演示 2: 查看代码和配置（5分钟）**

```markdown
1. 在 VS Code 中打开项目

2. 展示 Orders.tmdl
   - 滚动到 measure 定义部分
   - 讲解一个简单的度量值
   - 讲解一个复杂的 LOD 度量值

3. 展示 page.json
   - 解释页面配置
   - 展示筛选器配置

4. 展示 visual.json (CardSales)
   - 解释 position 属性
   - 解释 query 属性
   - 解释 objects 属性
```

**演示 3: 快速创建一个新的 KPI 卡片（7分钟）**

```markdown
💡 这是最吸引人的部分！现场编码！

步骤：
1. 在 Orders.tmdl 中添加一个新度量值
   measure 'Average Sales per Order' =
       DIVIDE([Total Sales], DISTINCTCOUNT(Orders[Order ID]), 0)
       formatString: \$#,0.00

2. 复制 CardSales 文件夹，重命名为 CardAvgSalesPerOrder

3. 编辑 visual.json
   - 修改 name: "CardAvgSalesPerOrder"
   - 修改 position.x: 1095 (放在最右边)
   - 修改 Property: "Average Sales per Order"

4. 保存文件

5. 在 Power BI Desktop 中刷新
   - 关闭并重新打开 pbip 文件
   - 查看新的 KPI 卡片是否出现
   - 验证数值是否正确

6. 如果时间允许，调整格式：
   - 修改字体大小
   - 修改卡片颜色
```

**演示注意事项**:
- ⚠️ 提前演练，确保流畅
- ⚠️ 准备备用方案（如果现场出问题）
- ⚠️ 录屏作为 Plan B（以防网络或软件问题）
- ⚠️ 准备好 Git 版本，可以快速回滚

---

### 第六部分：最佳实践和避坑指南（5分钟）

#### 6.1 转换最佳实践

```markdown
✅ DO - 推荐做法：

1. 分阶段转换
   - 先转数据模型（验证数据正确性）
   - 再转可视化（一个个页面转）
   - 最后调样式和交互

2. 使用版本控制
   - Git 管理所有代码文件
   - 每完成一个组件就提交
   - 方便回滚和团队协作

3. 保持命名一致性
   - Tableau 字段名 = Power BI 列名
   - 便于维护和理解

4. 创建转换映射表
   - 记录每个计算字段的转换
   - 文档化复杂的 LOD 表达式

5. 自动化测试
   - 对比关键指标的数值
   - 确保转换后数据一致
```

```markdown
❌ DON'T - 避免的做法：

1. 不要手动在 Power BI Desktop 中创建
   - 无法版本控制
   - 难以批量修改
   - 不便于自动化

2. 不要忽略数据类型
   - Tableau string ≠ Power BI text 总是对应
   - 日期格式需要特别注意

3. 不要直接复制公式
   - Tableau 公式语法 ≠ DAX
   - 需要理解逻辑后重写

4. 不要过度优化
   - 先确保功能正确
   - 再考虑性能优化

5. 不要跳过验证
   - 每个组件都要测试
   - 关键数据点要对比验证
```

#### 6.2 常见错误和解决方案

**错误 1: Schema 验证失败**

```json
// ❌ 错误：
"HierarchyLevel": {
  "Hierarchy": "Order Date",
  "HierarchyLevel": "月份"
}

// ✅ 正确：使用计算列
column 'Order Year-Month' = FORMAT(Orders[Order Date], "YYYY-MM")
```

**错误 2: 除零错误**

```dax
// ❌ 错误：
measure 'Profit Ratio' = [Total Profit] / [Total Sales]

// ✅ 正确：
measure 'Profit Ratio' = DIVIDE([Total Profit], [Total Sales], 0)
```

**错误 3: lineageTag 重复**

```tmdl
// ❌ 错误：缩进不正确导致 lineageTag 重复
measure 'Total Sales' = SUM(Orders[Sales])
  lineageTag: m-total-sales-001
lineageTag: duplicate-tag

// ✅ 正确：
measure 'Total Sales' = SUM(Orders[Sales])
  lineageTag: m-total-sales-001

column 'Order ID'
  lineageTag: c-order-id-001
```

---

### 第七部分：价值和应用场景（5分钟）

#### 7.1 为什么要做这个转换？

```markdown
🎯 业务价值：

1. 降低许可成本
   - Power BI 价格通常低于 Tableau
   - 企业 Microsoft 365 许可可能已包含

2. 技术整合
   - 与 Microsoft 生态系统无缝集成
   - Azure、Power Platform、Office 365

3. 技能复用
   - 保留现有 Tableau 看板的投资
   - 培训团队掌握 Power BI
   - 双平台能力提升竞争力

4. 客户需求
   - 不同客户偏好不同平台
   - 提供多平台交付能力

5. 灾备和迁移
   - 平台替代方案
   - 降低厂商锁定风险
```

#### 7.2 适用场景

```markdown
✅ 适合转换的场景：

1. 标准仪表板
   - KPI 看板
   - 销售/财务报表
   - 运营监控面板

2. 中等复杂度的分析
   - 多个数据源（<5个）
   - 常见可视化类型
   - 基础交互和筛选

3. 定期更新的报表
   - 月度/季度报告
   - 固定格式的看板

⚠️ 需要评估的场景：

1. 高级分析功能
   - 复杂的统计分析
   - 自定义可视化插件
   - R/Python 集成

2. 特殊数据源
   - Tableau 专有连接器
   - 实时数据流

3. 大规模数据
   - 数千万行以上数据
   - 需要性能评估
```

#### 7.3 ROI 分析

```markdown
投入：
- 开发时间：根据看板复杂度，通常 1-5 天/个
- 学习成本：掌握 Power BI 和 DAX 基础
- 测试验证：确保数据一致性

产出：
- 双平台能力：可同时交付 Tableau 和 Power BI
- 代码资产：转换脚本可复用
- 技术文档：建立转换知识库
- 团队能力：提升团队技能广度

典型案例：
- 10个中等复杂度看板
- 投入：2周开发 + 3天测试
- 节省：每年节省 $X 许可费用
- 增值：获得 Y 个新客户项目机会
```

---

### 第八部分：Q&A 准备（15-30分钟）

#### 预期问题清单

**技术类问题**:

Q1: **转换的准确率有多高？**
```markdown
A:
- 标准可视化：95%+ 准确率
- 简单计算字段：90%+ 准确率
- 复杂 LOD 表达式：需要逐个验证，通常 85%+
- 在 Superstore 案例中，所有数值完全一致（100%）

建议：转换后务必进行数据验证测试
```

Q2: **哪些 Tableau 功能无法转换？**
```markdown
A:
目前已知限制：
1. Tableau 特有的可视化类型（如 Sankey 图）
   - 解决方案：使用 Power BI 自定义可视化
2. 复杂的表计算（Table Calculations）
   - 解决方案：用 DAX 迭代函数重写
3. Tableau 动作（Actions）的部分高级功能
   - 解决方案：使用 Power BI 的书签和钻取
4. Tableau Story（故事点）
   - 解决方案：使用 Power BI 的导航按钮

大部分功能都有等价实现方式
```

Q3: **性能表现如何对比？**
```markdown
A:
- 小型数据集（<10万行）：性能相当
- 中型数据集（10-100万行）：Power BI 略优（得益于 VertiPaq 引擎）
- 大型数据集（>100万行）：需要具体测试
  * Tableau：Hyper 引擎表现优秀
  * Power BI：DirectQuery 模式可处理大数据

建议：
- 使用 Import 模式（内存模型）获得最佳性能
- 对大数据集进行聚合或筛选
- 使用增量刷新策略
```

Q4: **转换需要多长时间？**
```markdown
A:
根据看板复杂度：

简单看板（3-5个可视化）：
- 手动：4-8 小时
- 半自动：2-4 小时

中等看板（10-15个可视化）：
- 手动：1-2 天
- 半自动：4-8 小时

复杂看板（20+个可视化）：
- 手动：3-5 天
- 半自动：1-2 天

Superstore 案例（13个组件）：
- 实际用时：约 6 小时（包含调试）
- 如果有完整转换指南：预计 3-4 小时
```

Q5: **是否可以自动化转换？**
```markdown
A:
可以部分自动化：

✅ 可自动化的部分（80%）：
1. XML 解析和数据提取
2. 表结构生成
3. 简单计算字段转换
4. 可视化类型映射
5. 布局坐标转换
6. 文件目录创建

⚠️ 需要人工介入的部分（20%）：
1. 复杂 LOD 表达式验证
2. 自定义可视化处理
3. 样式细节调整
4. 数据验证测试

我已经创建了转换指南，可以作为自动化脚本的基础
```

**业务类问题**:

Q6: **什么情况下建议做这个转换？**
```markdown
A:
建议转换的场景：
1. 企业正在评估 Power BI
2. 客户明确要求 Power BI 交付
3. 需要与 Microsoft 生态集成
4. 希望降低 BI 平台成本
5. 建立多平台交付能力

不建议转换的场景：
1. Tableau 运行良好且无切换计划
2. 使用大量 Tableau 专有功能
3. 团队对 Tableau 非常熟悉但对 Power BI 陌生
4. 数据源兼容性问题
```

Q7: **转换后需要维护两套代码吗？**
```markdown
A:
推荐策略：

方案 1：单一源头（Tableau 优先）
- Tableau 作为主开发平台
- 定期转换到 Power BI
- 适合：Tableau 团队为主的组织

方案 2：单一源头（Power BI 优先）
- Power BI 作为主开发平台
- 适合：Microsoft 生态为主的组织

方案 3：双轨并行
- 根据项目需求选择平台
- 共享数据模型和业务逻辑
- 适合：咨询公司或有双平台需求的企业

方案 4：抽象层（高级）
- 使用元数据驱动的生成器
- 从抽象定义生成两个平台的代码
- 适合：大量看板需要维护的场景
```

Q8: **学习曲线如何？**
```markdown
A:
对于 Tableau 用户学习 Power BI：

基础概念（相似）：✅ 易于理解
- 数据连接、表关系、可视化类型

计算语言（不同）：⚠️ 需要学习
- Tableau Calculation vs DAX
- 相似度约 60%
- 建议学习时间：1-2 周掌握基础，1-2 月精通

开发模式（不同）：⚠️ 需要适应
- Tableau Desktop（GUI） vs Power BI Desktop + 代码
- 我们的方法更偏向代码化
- 对开发者友好，对非技术人员有挑战

建议学习路径：
1. Power BI Desktop 基础（1周）
2. DAX 基础（1周）
3. 参考转换指南实践（1周）
4. 完成1-2个完整项目（2-4周）
```

**工具类问题**:

Q9: **有没有现成的转换工具？**
```markdown
A:
目前状态：

官方工具：❌ 无
- Tableau 和 Microsoft 都没有提供官方转换工具

第三方工具：⚠️ 有限
- 一些商业工具声称支持，但效果参差不齐
- 通常只支持简单场景

我们的方案：✅ 开源指南
- 详细的转换指南文档（36KB）
- 完整的示例代码
- 可以作为自动化脚本的基础
- GitHub: [待发布]

下一步计划：
- 将转换逻辑封装为 Python 脚本
- 提供 CLI 工具
- 建立测试框架
```

Q10: **如何验证转换的正确性？**
```markdown
A:
多层验证策略：

1. 数据层验证
   - 对比关键指标的数值
   - 检查行数、列数
   - 验证数据类型

2. 计算层验证
   - 逐个测试度量值
   - 对比复杂计算结果
   - 边界条件测试

3. 可视化层验证
   - 并排对比图表
   - 检查筛选器效果
   - 测试交互功能

4. 端到端验证
   - 用户接受测试（UAT）
   - 真实场景测试
   - 性能基准测试

示例测试脚本：
```python
# 伪代码
def validate_conversion(tableau_data, powerbi_data):
    assert tableau_data['Total Sales'] == powerbi_data['Total Sales']
    assert tableau_data['Profit Ratio'] == powerbi_data['Profit Ratio']
    # ... 更多断言
```
```

---

## 📊 演示文稿设计建议

### 幻灯片结构（约 30 张）

```markdown
1. 封面
   - 标题：Tableau 到 Power BI：无缝迁移的技术实践
   - 副标题：基于 Superstore Dashboard 的完整案例分享
   - 您的名字和日期

2-3. 开场
   - 自我介绍
   - 为什么要做这个项目
   - 今天的议程

4-5. 效果展示
   - 左右对比：Tableau vs Power BI
   - 关键指标对比表

6-8. 技术架构
   - 双平台架构对比图
   - 转换技术栈流程图
   - 核心转换步骤

9-15. 案例深度解析
   - Superstore Dashboard 介绍
   - 4个转换难点及解决方案（每个难点1张）
   - 转换效果对比

16-20. 技术深度
   - Power BI 文件结构图
   - DAX 度量值示例（3个层次）
   - visual.json 结构解析

21-22. 演示准备
   - 演示内容预告
   - 环境说明

23-25. 最佳实践
   - DO & DON'T 清单
   - 常见错误和解决方案

26-27. 价值分析
   - 业务价值
   - ROI 分析

28. Q&A
   - 常见问题列表

29. 资源和联系方式
   - GitHub 链接
   - 文档下载
   - 联系方式

30. 谢谢
   - 感谢 + 问题环节
```

### 视觉设计建议

```markdown
配色方案：
- 主色：Tableau 蓝 (#1F77B4) + Power BI 黄 (#FFC83D)
- 辅色：深灰 (#2C3E50)，浅灰 (#ECF0F1)
- 强调：绿色（✅）、红色（❌）、橙色（⚠️）

字体：
- 标题：Microsoft YaHei Bold, 32-36pt
- 正文：Microsoft YaHei, 18-24pt
- 代码：Consolas, 14-16pt

布局原则：
- 每页 1-2 个核心观点
- 多用图表少用文字
- 代码示例使用对比格式（Before/After）
- 关键信息使用高亮或边框
```

---

## 🎬 现场演示脚本（详细版）

### 演示准备检查清单

```markdown
硬件准备：
□ 笔记本电脑（已测试，性能良好）
□ 投影适配器（HDMI/USB-C）
□ 鼠标（建议有线，避免连接问题）
□ 电源适配器
□ 备用笔记本（如果可能）

软件准备：
□ Tableau Desktop（已安装，已激活）
□ Power BI Desktop（已安装，最新版本）
□ VS Code（已安装，安装了 JSON/TMDL 插件）
□ 浏览器（用于展示文档）
□ 屏幕录制软件（备用）

文件准备：
□ Superstore.twb（已打开并测试）
□ superstore dashboard.pbip（已打开并测试）
□ Sample - Superstore.xls（确认数据正常）
□ 转换指南 PDF（用于分享）
□ 演示文稿（已上传到云端备份）

网络准备：
□ 下载所有需要的文件到本地
□ 关闭自动更新
□ 准备热点（以防 WiFi 问题）
□ 测试投影效果

时间管理：
□ 设置倒计时工具
□ 准备各部分的时间节点提醒
□ 预留 5 分钟 buffer
```

### 演示脚本（逐步）

#### Part 1: 打开 Tableau（2分钟）

```markdown
【屏幕：Tableau Desktop】

脚本：
"首先，让我们看一下原始的 Tableau 看板。"

操作：
1. 打开 Tableau Desktop
2. 打开 Superstore.twb

讲解：
"这是一个经典的 Superstore 销售分析看板，包含：
- 顶部：7个 KPI 指标
- 中间：美国销售地图
- 底部：两个月度趋势图
- 右侧：4个交互筛选器"

操作：
3. 点击地图上的某个州
4. 观察其他图表的变化

讲解：
"注意看，当我点击地图时，下面的图表会自动筛选，这就是 Tableau 的交互功能。"

操作：
5. 调整日期筛选器
6. 观察所有数值的变化

讲解：
"现在所有的 KPI 数值都更新了，这些都是动态计算的。"

【保持 Tableau 打开，准备对比】
```

#### Part 2: 打开 Power BI（2分钟）

```markdown
【屏幕：Power BI Desktop】

脚本：
"现在，让我们看一下转换后的 Power BI 版本。"

操作：
1. 打开 Power BI Desktop
2. 打开 superstore dashboard.pbip
3. 等待数据加载完成

讲解：
"这是完全基于 Tableau 看板转换过来的 Power BI 版本。
布局、数据、可视化都尽可能保持一致。"

【切换到分屏模式：左边 Tableau，右边 Power BI】

脚本：
"让我们并排对比一下。"

操作：
1. 同时展示两个看板
2. 对比顶部的 KPI 数值

讲解：
"大家可以看到：
- Total Sales: 两边都是 $1,317,840
- Profit Ratio: 都是 13.0%
- 所有数值完全一致"

操作：
3. 在两边同时调整筛选器
4. 观察数值同步变化

讲解：
"当我在两边都选择同样的筛选条件时，
结果是完全一样的，这证明了转换的准确性。"
```

#### Part 3: 查看代码（5分钟）

```markdown
【屏幕：VS Code】

脚本：
"接下来我们深入看一下，这个转换背后的代码是什么样的。"

操作：
1. 打开 VS Code
2. 打开项目文件夹

讲解：
"Power BI 项目实际上是由一系列文本文件组成的：
- SemanticModel：数据模型
- Report：报表定义"

操作：
3. 打开 Orders.tmdl

讲解：
"这是数据模型文件，使用 TMDL 语言编写。
让我们看一个简单的度量值。"

【滚动到 measure 'Total Sales'】

朗读代码：
```
measure 'Total Sales' = SUM(Orders[Sales])
    formatString: \$#,0
    lineageTag: m-total-sales-001
```

讲解：
"这个度量值很简单：
- 对 Sales 列求和
- 格式化为美元货币
- lineageTag 是唯一标识符"

操作：
4. 滚动到 measure 'Order Profitable'

朗读代码：
```
measure 'Order Profitable' =
    VAR OrderProfit = CALCULATE(
        SUM(Orders[Profit]),
        ALLEXCEPT(Orders, Orders[Order ID])
    )
    RETURN IF(OrderProfit > 0, "Profitable", "Unprofitable")
```

讲解：
"这个就复杂一些了，它等价于 Tableau 的 LOD 表达式：
```
{FIXED [Order ID]:SUM([Profit])}>0
```

在 DAX 中我们使用：
- CALCULATE：修改筛选上下文
- ALLEXCEPT：保留 Order ID 的筛选
- VAR：定义变量提高性能"

操作：
5. 打开 visual.json (CardSales)

讲解：
"这是 KPI 卡片的配置文件，JSON 格式。"

【高亮 position 部分】

讲解：
```json
"position": {
    "x": 10,      // 距离左边 10 像素
    "y": 60,      // 距离顶部 60 像素
    "z": 1001,    // 层级
    "height": 70,
    "width": 145
}
```

【高亮 query 部分】

讲解：
"这里定义了数据查询，引用我们刚才看到的度量值：
```json
"Property": "Total Sales"
```

就是这样把数据和可视化连接起来的。"
```

#### Part 4: 现场创建新 KPI（7分钟）

```markdown
【最激动人心的部分！】

脚本：
"理论讲了很多，现在让我们实际操作一下。
我要现场创建一个新的 KPI 卡片：Average Sales per Order（每订单平均销售额）"

【屏幕：VS Code - Orders.tmdl】

操作 1：添加度量值
1. 滚动到 measures 区域
2. 输入：

```dax
measure 'Average Sales per Order' =
    DIVIDE([Total Sales], DISTINCTCOUNT(Orders[Order ID]), 0)
    formatString: \$#,0.00
    lineageTag: m-avg-sales-per-order-001
```

讲解边输入：
"我们创建一个新度量值：
- 总销售额除以订单数量
- 使用 DIVIDE 函数避免除零错误
- 格式化为两位小数的货币"

操作 2：复制 visual 文件
1. 在文件管理器中复制 CardSales 文件夹
2. 重命名为 CardAvgSalesPerOrder

讲解：
"我们复制一个现有的卡片作为模板，
然后修改它的配置。"

操作 3：编辑 visual.json
1. 打开 CardAvgSalesPerOrder/visual.json
2. 修改 name：
```json
"name": "CardAvgSalesPerOrder",
```

3. 修改 position（放在最右边）：
```json
"position": {
    "x": 1095,
    "y": 60,
    "z": 1008,
    "height": 70,
    "width": 145
}
```

4. 修改 Property：
```json
"Property": "Average Sales per Order"
```

5. 修改标题文字（如果有）

讲解边修改：
"我们需要修改三个地方：
1. 名称 - 标识这个组件
2. 位置 - 放在最右边，x 坐标改为 1095
3. 数据字段 - 引用新的度量值"

操作 4：保存所有文件
1. Ctrl+S 保存所有
2. 关闭 VS Code

讲解：
"现在代码都写好了，让我们看看效果。"

【屏幕：Power BI Desktop】

操作 5：刷新 Power BI
1. 关闭 Power BI Desktop
2. 重新打开 superstore dashboard.pbip
3. 等待加载...

讲解：
"因为我们修改了底层文件，
需要重新加载项目才能看到变化。"

【期待的时刻】

操作 6：查看结果
1. 看板加载完成
2. 找到新的 KPI 卡片

脚本：
"太好了！新的 KPI 卡片出现了！
让我们看看数值：$xxx.xx
这就是每个订单的平均销售额。"

操作 7：测试交互（如果时间允许）
1. 调整筛选器
2. 观察新 KPI 的数值变化

讲解：
"新的 KPI 也支持交互，
当我们筛选数据时，它会自动更新。"

【如果出现错误】

备选方案：
"看来出了点小问题（微笑）。
这就是为什么我们需要详细的测试和验证。
我之前录制了一个成功的版本，让我们看看录屏..."

【播放预先录制的成功演示】
```

---

## 📚 会后资料准备

### 分享材料清单

```markdown
1. 演示文稿 PDF
   □ 包含所有幻灯片
   □ 添加备注和详细说明
   □ 文件名：Tableau_to_PowerBI_技术分享_<日期>.pdf

2. 转换指南文档
   □ Tableau_to_PowerBI_Conversion_Guide.md
   □ 转换为 PDF 以便阅读
   □ 36KB，13个章节

3. 示例项目
   □ Superstore.twb
   □ superstore dashboard.pbip
   □ Sample - Superstore.xls
   □ 打包为 ZIP 文件

4. 代码片段集合
   □ 常用 DAX 度量值模板
   □ visual.json 模板
   □ 转换对照表（Excel）

5. 参考资源列表
   □ Power BI 官方文档链接
   □ DAX 学习资源
   □ GitHub 仓库（如果开源）
   □ 博客文章和教程

6. 联系方式
   □ 您的邮箱
   □ 技术交流群（微信/Discord）
   □ GitHub Issue 提交方式
```

### 分享渠道建议

```markdown
1. 现场分享
   - USB 闪存驱动器
   - 二维码扫描下载链接

2. 线上分享
   - GitHub 仓库
   - 云盘链接（百度网盘/OneDrive）
   - 公司内部 Wiki/Confluence

3. 后续跟进
   - 录制视频上传 B站/YouTube
   - 发布技术博客文章
   - 建立技术交流群
   - 定期答疑会议
```

---

## 🎤 演讲技巧建议

### 准备阶段

```markdown
1. 熟悉内容
   □ 至少完整演练 3 遍
   □ 计时每个部分
   □ 调整节奏和内容

2. 准备应急方案
   □ 网络问题：提前下载所有资源
   □ 软件崩溃：准备录屏作为备份
   □ 时间超时：标记可跳过的内容
   □ 设备故障：准备备用笔记本

3. 设置提醒
   □ 5 分钟倒计时提醒（每部分）
   □ 总时长倒计时
   □ 关键时间点标记
```

### 现场技巧

```markdown
1. 开场（重要！）
   - 微笑，眼神交流
   - 简短有力的开场白
   - 快速抓住注意力（展示对比图）
   - 说明今天的价值点

2. 内容讲解
   - 控制语速（不要过快）
   - 适当停顿，给听众消化时间
   - 多用 "大家可以看到..."，"注意这里..."
   - 结合手势，指向屏幕关键部分

3. 现场演示
   - 放慢操作速度
   - 大声说出每个步骤
   - 解释为什么这么做
   - 遇到错误保持冷静，微笑应对

4. 互动
   - 适时询问 "大家有问题吗？"
   - 观察听众反应
   - 调整讲解深度
   - 鼓励提问

5. 结束
   - 总结关键要点
   - 强调价值和应用
   - 感谢听众
   - 引导到 Q&A
```

### 语言表达

```markdown
✅ 好的表达：
- "让我们看一下..."（引导注意）
- "这里有个有趣的点..."（制造期待）
- "可能有人会问..."（主动解答疑问）
- "实际项目中我们发现..."（实战经验）
- "这个技巧帮我们节省了..."（量化价值）

❌ 避免的表达：
- "这个很简单..."（可能对听众不简单）
- "大家都知道..."（不一定都知道）
- "呃...嗯...这个..."（显得不专业）
- 过多的技术黑话（适度使用，及时解释）
```

---

## ✅ 最终检查清单

### T-7天

```markdown
□ 完成演示文稿
□ 完成转换指南文档
□ 测试演示项目
□ 录制备用视频
□ 确认活动时间、地点、设备
```

### T-3天

```markdown
□ 完整演练 3 遍
□ 调整内容和时间
□ 准备 Q&A 答案
□ 打包分享资料
□ 测试所有链接和文件
```

### T-1天

```markdown
□ 再次完整演练
□ 检查笔记本电脑状态
□ 充电所有设备
□ 下载所有在线资源到本地
□ 打印备用笔记
```

### 当天（演讲前）

```markdown
□ 提前 30 分钟到场
□ 测试投影设备
□ 测试声音
□ 打开所有需要的软件
□ 关闭通知和自动更新
□ 测试网络
□ 深呼吸，放松 😊
```

---

## 🌟 成功的关键因素

1. **准备充分**: 演练至少 3 遍，掌握每个细节
2. **实战为主**: 多展示实际效果，少讲理论
3. **保持自信**: 即使出错也要镇定，展现专业性
4. **与听众互动**: 观察反应，调整节奏
5. **提供价值**: 分享实用的技巧和经验，而不只是炫技

---

## 📞 后续跟进建议

```markdown
分享后 24 小时内：
□ 发送感谢邮件
□ 分享演示文稿和资料链接
□ 收集反馈

分享后 1 周内：
□ 整理 Q&A 记录
□ 发布技术博客文章
□ 上传录制视频

分享后 1 个月内：
□ 组织线上答疑会
□ 建立技术交流社群
□ 根据反馈优化转换指南
```

---

## 🎉 祝您分享成功！

记住：听众来这里是为了学习新知识，而您准备得非常充分。
放松、自信地分享您的专业知识和经验！

有任何问题随时联系！Good luck! 🚀
