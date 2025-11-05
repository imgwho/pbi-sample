# Tableau 到 Power BI 看板转换完整指南

> 本指南详细说明如何系统地将 Tableau 工作簿（.twb）转换为 Power BI 报表（.pbip），适用于任何 AI 助手执行此转换。

---

## 📋 目录

1. [前期准备与分析](#1-前期准备与分析)
2. [数据源映射](#2-数据源映射)
3. [数据模型转换](#3-数据模型转换)
4. [页面和布局创建](#4-页面和布局创建)
5. [可视化组件转换](#5-可视化组件转换)
6. [筛选器和交互配置](#6-筛选器和交互配置)
7. [样式和格式调整](#7-样式和格式调整)
8. [验证和测试](#8-验证和测试)

---

## 1. 前期准备与分析

### 1.1 读取和分析 Tableau 工作簿结构

**必须读取的文件：**
- `*.twb` - Tableau 工作簿 XML 文件
- 数据源文件（如 `Sample - Superstore.xls`）
- Tableau 看板截图（用于视觉参考）

**分析步骤：**

```bash
# 1. 读取 Tableau 工作簿
Read(<tableau_file>.twb)

# 2. 提取关键信息
- 数据源定义（<datasources> 节点）
- 工作表定义（<worksheets> 节点）
- 仪表板定义（<dashboards> 节点）
- 计算字段（<column> 节点中的 <calculation>）
- 参数定义（<column param-domain-type>）
```

**需要识别的 Tableau 元素：**

| Tableau 元素 | XML 路径 | Power BI 对应 |
|-------------|----------|--------------|
| 数据源 | `/workbook/datasources/datasource` | SemanticModel |
| 计算字段 | `/workbook/datasources/datasource/column/calculation` | DAX Measures |
| 工作表 | `/workbook/worksheets/worksheet` | Report Pages |
| 仪表板 | `/workbook/dashboards/dashboard` | Report Pages |
| 可视化 | `/workbook/worksheets/worksheet/table/panes/pane` | Visual Containers |

### 1.2 理解 Power BI 项目结构

**Power BI 项目文件结构：**

```
project.pbip                                    # 项目入口文件
├── project.Report/                             # 报表定义
│   ├── definition/
│   │   ├── report.json                        # 报表配置
│   │   ├── version.json                       # 版本信息
│   │   └── pages/                             # 页面定义
│   │       ├── pages.json                     # 页面列表
│   │       └── <PageName>/                    # 单个页面
│   │           ├── page.json                  # 页面配置
│   │           └── visuals/                   # 可视化组件
│   │               └── <VisualName>/
│   │                   └── visual.json        # 单个可视化定义
│   └── definition.pbir                        # 报表元数据
│
└── project.SemanticModel/                      # 数据模型
    ├── definition/
    │   ├── model.tmdl                         # 模型配置
    │   ├── database.tmdl                      # 数据库配置
    │   └── tables/                            # 表定义
    │       └── <TableName>.tmdl               # 单个表定义（包含 measures）
    └── definition.pbism                        # 模型元数据
```

---

## 2. 数据源映射

### 2.1 识别 Tableau 数据源

从 Tableau TWB 文件中提取数据源信息：

```xml
<datasource caption='Orders+ (Sample - Superstore)' inline='true' name='federated...'>
  <connection class='excel-direct' filename='Sample - Superstore.xls'>
    <relation connection='excel-direct...' name='Orders' table='[Orders$]' type='table'>
      <columns>
        <column datatype='string' name='Order ID' ordinal='1' />
        <column datatype='date' name='Order Date' ordinal='2' />
        <column datatype='real' name='Sales' ordinal='17' />
        <column datatype='real' name='Profit' ordinal='20' />
        ...
      </columns>
    </relation>
  </connection>
</datasource>
```

**提取信息：**
- 数据源名称：`Orders+ (Sample - Superstore)`
- 连接类型：`excel-direct`
- 文件路径：`Sample - Superstore.xls`
- 表名称：`Orders`
- 列定义：名称、数据类型、序号

### 2.2 创建 Power BI 数据模型

**在 SemanticModel 中定义表：**

```tmdl
table Orders
  lineageTag: <generate-unique-tag>

  column 'Order ID'
    dataType: string
    lineageTag: <generate-unique-tag>

  column 'Order Date'
    dataType: dateTime
    formatString: Short Date
    lineageTag: <generate-unique-tag>

  column Sales
    dataType: double
    formatString: \$#,0.00
    lineageTag: <generate-unique-tag>

  column Profit
    dataType: double
    formatString: \$#,0.00
    lineageTag: <generate-unique-tag>
```

**数据类型映射表：**

| Tableau 类型 | Power BI 类型 | 格式示例 |
|-------------|-------------|---------|
| `string` | `string` | - |
| `integer` / `int64` | `int64` | `0` |
| `real` / `double` | `double` | `\$#,0.00` |
| `date` / `datetime` | `dateTime` | `Short Date` |
| `boolean` | `boolean` | `TRUE/FALSE` |

---

## 3. 数据模型转换

### 3.1 识别 Tableau 计算字段

**Tableau 计算字段示例：**

```xml
<column caption='Profit Ratio' datatype='real' name='[Calculation_9921103144103743]' role='measure' type='quantitative'>
  <calculation class='tableau' formula='sum([Profit])/sum([Sales])' />
</column>

<column caption='Order Profitable?' datatype='boolean' name='[Calculation_9060122104947471]' role='dimension' type='nominal'>
  <calculation class='tableau' formula='{fixed [Order ID]:sum([Profit])}&gt;0' />
</column>
```

### 3.2 转换为 Power BI DAX 度量值

**转换规则：**

| Tableau 函数 | Power BI DAX 对应 | 示例 |
|-------------|------------------|------|
| `SUM([field])` | `SUM(Table[field])` | `SUM(Orders[Sales])` |
| `AVG([field])` | `AVERAGE(Table[field])` | `AVERAGE(Orders[Discount])` |
| `COUNTD([field])` | `DISTINCTCOUNT(Table[field])` | `DISTINCTCOUNT(Orders[Customer ID])` |
| `{FIXED [field]: agg()}` | `CALCULATE(agg(), ALLEXCEPT(Table, Table[field]))` | `CALCULATE(SUM(Orders[Profit]), ALLEXCEPT(Orders, Orders[Order ID]))` |
| `IF condition THEN a ELSE b END` | `IF(condition, a, b)` | `IF(OrderProfit > 0, "Profitable", "Unprofitable")` |
| `DATEDIFF('unit', [date1], [date2])` | `DATEDIFF([date1], [date2], DAY)` | `DATEDIFF(Orders[Order Date], Orders[Ship Date], DAY)` |

**完整示例转换：**

```tableau
// Tableau 计算字段
sum([Profit])/sum([Sales])
```

```dax
// Power BI DAX Measure
measure 'Profit Ratio' = DIVIDE(SUM(Orders[Profit]), SUM(Orders[Sales]), 0)
  formatString: 0.0%
  lineageTag: m-profit-ratio-001
```

```tableau
// Tableau LOD 表达式
{fixed [Order ID]:sum([Profit])}>0
```

```dax
// Power BI DAX Measure with CALCULATE
measure 'Order Profitable' =
  VAR OrderProfit = CALCULATE(SUM(Orders[Profit]), ALLEXCEPT(Orders, Orders[Order ID]))
  RETURN IF(OrderProfit > 0, "Profitable", "Unprofitable")
  lineageTag: m-order-profitable-001
```

### 3.3 常用度量值模板

```dax
// 1. 总和度量值
measure 'Total Sales' = SUM(Orders[Sales])
  formatString: \$#,0
  lineageTag: m-total-sales-001

// 2. 平均值度量值
measure 'Average Discount' = AVERAGE(Orders[Discount])
  formatString: 0.0%
  lineageTag: m-avg-discount-001

// 3. 比率度量值
measure 'Profit Ratio' = DIVIDE([Total Profit], [Total Sales], 0)
  formatString: 0.0%
  lineageTag: m-profit-ratio-001

// 4. 每项平均值度量值
measure 'Profit per Order' = DIVIDE([Total Profit], DISTINCTCOUNT(Orders[Order ID]), 0)
  formatString: \$#,0.00
  lineageTag: m-profit-per-order-001

// 5. 条件分类度量值
measure 'Order Profitable' =
  VAR OrderProfit = CALCULATE(SUM(Orders[Profit]), ALLEXCEPT(Orders, Orders[Order ID]))
  RETURN IF(OrderProfit > 0, "Profitable", "Unprofitable")
  lineageTag: m-order-profitable-001
```

### 3.4 创建辅助计算列

对于需要按月聚合的日期字段，创建一个年月列：

```dax
column 'Order Year-Month' = FORMAT(Orders[Order Date], "YYYY-MM")
  dataType: string
  lineageTag: c-order-year-month-001
  summarizeBy: none
  dataCategory: Months

  annotation SummarizationSetBy = User
```

---

## 4. 页面和布局创建

### 4.1 从 Tableau 仪表板提取布局信息

**Tableau 仪表板 XML：**

```xml
<dashboard name='Overview'>
  <size maxheight='1200' maxwidth='1400' minheight='1200' minwidth='1400' sizing-mode='fixed' />
  <zones>
    <zone h='100000' id='2' type-v2='layout-basic' w='100000' x='0' y='0'>
      <zone h='6526' id='38' fixed-size='37' x='571' y='667'>
        <!-- 标题区域 -->
      </zone>
      <zone h='10473' id='29' x='571' y='7193'>
        <!-- KPI 卡片区域 -->
      </zone>
      ...
    </zone>
  </zones>
</dashboard>
```

**提取关键信息：**
- 仪表板尺寸：1400×1200
- 区域位置（x, y, width, height）
- 区域层级关系（嵌套结构）

### 4.2 创建 Power BI 页面

**步骤：**

```bash
# 1. 创建页面目录
mkdir -p "project.Report/definition/pages/ProfitabilityOverview/visuals"

# 2. 创建 page.json
Write(project.Report/definition/pages/ProfitabilityOverview/page.json)
```

**page.json 模板：**

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
  "name": "ProfitabilityOverview",
  "displayName": "Profitability Overview",
  "displayOption": "FitToPage",
  "width": 1280,
  "height": 720,
  "filterConfig": {
    "filters": []
  }
}
```

### 4.3 布局坐标转换

**Tableau 到 Power BI 坐标映射：**

Tableau 使用相对单位（0-100000），Power BI 使用像素（1280×720 标准画布）。

**转换公式：**

```
Power BI X = (Tableau X / 100000) × 1280
Power BI Y = (Tableau Y / 100000) × 720
Power BI Width = (Tableau Width / 100000) × 1280
Power BI Height = (Tableau Height / 100000) × 720
```

**示例布局（基于 Superstore 仪表板）：**

| 组件类型 | X | Y | Width | Height | Z-Index |
|---------|---|---|-------|--------|---------|
| 标题文本 | 10 | 10 | 1070 | 40 | 1000 |
| KPI 卡片 1-7 | 10-940 | 60 | 145×7 | 70 | 1001-1007 |
| 地图 | 10 | 140 | 850 | 240 | 1000 |
| 面积图 1 | 10 | 390 | 415 | 320 | 1009 |
| 面积图 2 | 435 | 390 | 425 | 320 | 1010 |
| 筛选器 1-4 | 870 | 140-410 | 200 | 70-90 | 1011-1014 |

---

## 5. 可视化组件转换

### 5.1 可视化类型映射表

| Tableau 可视化 | Power BI 可视化 | visualType 值 |
|---------------|----------------|--------------|
| Text | Textbox | `textbox` |
| Number (BANs) | Card | `card` |
| Bar Chart | Bar Chart | `barChart` |
| Line Chart | Line Chart | `lineChart` |
| Area Chart | Area Chart | `areaChart` |
| Pie Chart | Pie Chart | `pieChart` |
| Map | Map | `map` |
| Filled Map | Filled Map | `filledMap` |
| Table | Table | `table` |
| Quick Filter | Slicer | `slicer` |

### 5.2 创建可视化组件

**通用步骤：**

```bash
# 1. 为每个可视化创建目录
mkdir -p "project.Report/definition/pages/<PageName>/visuals/<VisualName>"

# 2. 创建 visual.json
Write(project.Report/definition/pages/<PageName>/visuals/<VisualName>/visual.json)
```

### 5.3 Card 可视化（KPI 卡片）

**Tableau 定义：**

```xml
<worksheet name='Total Sales'>
  <table>
    <view>
      <datasource-dependencies datasource='federated...'>
        <column-instance column='[Sales]' derivation='Sum' name='[sum:Sales:qk]' />
      </datasource-dependencies>
    </view>
  </table>
</worksheet>
```

**Power BI visual.json：**

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
  "name": "CardSales",
  "position": {
    "x": 10,
    "y": 60,
    "z": 1001,
    "height": 70,
    "width": 145
  },
  "visual": {
    "visualType": "card",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "Orders"
                    }
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
    "objects": {
      "categoryLabels": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            },
            "fontSize": {
              "expr": {
                "Literal": {
                  "Value": "'10pt'"
                }
              }
            }
          }
        }
      ],
      "labels": [
        {
          "properties": {
            "fontSize": {
              "expr": {
                "Literal": {
                  "Value": "'18pt'"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

### 5.4 Area Chart 可视化（面积图）

**Tableau 定义：**

```xml
<worksheet name='SalesbySegment'>
  <table>
    <view>
      <datasource-dependencies>
        <column-instance column='[Order Date]' derivation='Month-Trunc' name='[tmn:Order Date:qk]' />
        <column-instance column='[Sales]' derivation='Sum' name='[sum:Sales:qk]' />
        <column-instance column='[Segment]' derivation='None' name='[none:Segment:nk]' />
      </datasource-dependencies>
    </view>
    <panes>
      <pane>
        <mark class='Area' />
        <encodings>
          <color column='[Segment]' />
        </encodings>
      </pane>
    </panes>
    <rows>[sum:Sales:qk]</rows>
    <cols>[tmn:Order Date:qk]</cols>
  </table>
</worksheet>
```

**Power BI visual.json：**

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
  "name": "AreaChartSegment",
  "position": {
    "x": 10,
    "y": 390,
    "z": 1009,
    "height": 320,
    "width": 415
  },
  "visual": {
    "visualType": "areaChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "Orders"
                    }
                  },
                  "Property": "Order Year-Month"
                }
              },
              "queryRef": "Orders.Order Year-Month",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "Orders"
                    }
                  },
                  "Property": "Total Sales"
                }
              },
              "queryRef": "Orders.Total Sales",
              "active": true
            }
          ]
        },
        "Series": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "Orders"
                    }
                  },
                  "Property": "Segment"
                }
              },
              "queryRef": "Orders.Segment",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "title": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            },
            "text": {
              "expr": {
                "Literal": {
                  "Value": "'Monthly Sales by Segment'"
                }
              }
            },
            "fontSize": {
              "expr": {
                "Literal": {
                  "Value": "12"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

### 5.5 Map 可视化（地图）

**Power BI visual.json：**

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
  "name": "MapSales",
  "position": {
    "x": 10,
    "y": 140,
    "z": 1000,
    "height": 240,
    "width": 850
  },
  "visual": {
    "visualType": "map",
    "query": {
      "queryState": {
        "Location": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "Orders"
                    }
                  },
                  "Property": "State/Province"
                }
              },
              "queryRef": "Orders.State/Province",
              "active": true
            }
          ]
        },
        "Size": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "Orders"
                    }
                  },
                  "Property": "Total Sales"
                }
              },
              "queryRef": "Orders.Total Sales",
              "active": true
            }
          ]
        },
        "Gradient": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "Orders"
                    }
                  },
                  "Property": "Order Profitable"
                }
              },
              "queryRef": "Orders.Order Profitable",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "bubbles": [
        {
          "properties": {
            "bubbleSize": {
              "expr": {
                "Literal": {
                  "Value": "10D"
                }
              }
            }
          }
        }
      ],
      "title": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "false"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

### 5.6 Slicer 可视化（筛选器）

**日期范围筛选器：**

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
  "name": "SlicerOrderDate",
  "position": {
    "x": 870,
    "y": 140,
    "z": 1011,
    "height": 80,
    "width": 200
  },
  "visual": {
    "visualType": "slicer",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "Orders"
                    }
                  },
                  "Property": "Order Date"
                }
              },
              "queryRef": "Orders.Order Date",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "general": [
        {
          "properties": {
            "orientation": {
              "expr": {
                "Literal": {
                  "Value": "'1'"
                }
              }
            }
          }
        }
      ],
      "header": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            },
            "title": {
              "expr": {
                "Literal": {
                  "Value": "'Order Date'"
                }
              }
            },
            "fontSize": {
              "expr": {
                "Literal": {
                  "Value": "11"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

**多选列表筛选器（State/Province）：**

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
  "name": "SlicerState",
  "position": {
    "x": 870,
    "y": 310,
    "z": 1013,
    "height": 90,
    "width": 200
  },
  "visual": {
    "visualType": "slicer",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "Orders"
                    }
                  },
                  "Property": "State/Province"
                }
              },
              "queryRef": "Orders.State/Province",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "selection": [
        {
          "properties": {
            "selectAllCheckboxEnabled": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            },
            "singleSelect": {
              "expr": {
                "Literal": {
                  "Value": "false"
                }
              }
            }
          }
        }
      ],
      "header": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            },
            "title": {
              "expr": {
                "Literal": {
                  "Value": "'State/Province'"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

---

## 6. 筛选器和交互配置

### 6.1 从 Tableau 提取筛选器配置

**Tableau 筛选器定义：**

```xml
<filter class='quantitative' column='[Order Date]' included-values='in-range'>
  <min>#2023-02-28#</min>
  <max>#2024-12-30#</max>
</filter>

<filter class='categorical' column='[Region]' filter-group='7'>
  <groupfilter function='level-members' level='[none:Region:nk]' />
</filter>
```

### 6.2 在 Power BI 中配置页面级筛选器

**更新 page.json：**

```json
{
  "filterConfig": {
    "filters": [
      {
        "name": "FilterOrderDate",
        "field": {
          "Column": {
            "Expression": {
              "SourceRef": {
                "Entity": "Orders"
              }
            },
            "Property": "Order Date"
          }
        },
        "type": "Advanced",
        "howCreated": "User"
      },
      {
        "name": "FilterRegion",
        "field": {
          "Column": {
            "Expression": {
              "SourceRef": {
                "Entity": "Orders"
              }
            },
            "Property": "Region"
          }
        },
        "type": "Categorical",
        "howCreated": "User"
      }
    ]
  }
}
```

### 6.3 配置可视化交互

Power BI 默认启用交叉筛选和交叉高亮。如果需要禁用特定交互，可以在 visual.json 中添加：

```json
{
  "visual": {
    "interactions": {
      "filter": {
        "mode": "None"
      },
      "highlight": {
        "mode": "None"
      }
    }
  }
}
```

---

## 7. 样式和格式调整

### 7.1 字体和颜色

**从 Tableau 提取样式：**

```xml
<style-theme name='clean' />
<style>
  <style-rule element='mark'>
    <encoding attr='color' field='[Profit Ratio]' palette='tableau-orange-blue' type='interpolated' />
  </style-rule>
</style>
```

**在 Power BI 中应用：**

```json
{
  "objects": {
    "dataColors": [
      {
        "properties": {
          "defaultColor": {
            "solid": {
              "color": "#1F77B4"
            }
          }
        }
      }
    ]
  }
}
```

### 7.2 数字格式

| Tableau 格式 | Power BI formatString |
|-------------|----------------------|
| `$#,##0` | `\$#,0` |
| `$#,##0.00` | `\$#,0.00` |
| `0.0%` | `0.0%` |
| `#,##0` | `#,0` |

---

## 8. 验证和测试

### 8.1 检查清单

```bash
# 1. 验证数据模型
- [ ] 所有表已创建
- [ ] 所有列已定义
- [ ] 所有 DAX 度量值已添加
- [ ] 数据类型正确
- [ ] 格式字符串正确

# 2. 验证报表结构
- [ ] pages.json 已更新
- [ ] page.json 配置正确
- [ ] 所有 visual.json 文件已创建
- [ ] 位置和尺寸正确

# 3. 验证可视化
- [ ] 所有可视化类型正确
- [ ] 数据字段绑定正确
- [ ] 标题和标签显示正确
- [ ] 格式和样式正确

# 4. 验证筛选器
- [ ] 筛选器组件已创建
- [ ] 页面级筛选器已配置
- [ ] 筛选器交互正常
```

### 8.2 在 Power BI Desktop 中测试

```powershell
# 在 Power BI Desktop 中打开项目
Start-Process "C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe" -ArgumentList "<project>.pbip"
```

**测试步骤：**
1. 打开报表，查看所有页面是否正确加载
2. 检查每个可视化组件是否显示数据
3. 测试筛选器是否正常工作
4. 验证交互（点击可视化查看其他组件的响应）
5. 检查数据准确性（对比 Tableau 看板的数值）

---

## 9. 完整转换示例工作流

以下是完整的转换流程代码示例：

```typescript
// 伪代码示例：完整的 Tableau 到 Power BI 转换流程

async function convertTableauToPowerBI(
  tableauFile: string,
  powerBIProject: string
) {
  // 1. 读取 Tableau 工作簿
  const twb = await readTableauWorkbook(tableauFile);

  // 2. 提取数据源和列定义
  const dataSources = extractDataSources(twb);
  const columns = extractColumns(dataSources);

  // 3. 创建 Power BI 数据模型
  for (const table of dataSources) {
    await createPowerBITable(
      `${powerBIProject}.SemanticModel/definition/tables/${table.name}.tmdl`,
      table,
      columns[table.name]
    );
  }

  // 4. 转换计算字段为 DAX 度量值
  const calculations = extractCalculations(twb);
  const daxMeasures = convertCalculationsToDAX(calculations);

  for (const measure of daxMeasures) {
    await addMeasureToTable(
      `${powerBIProject}.SemanticModel/definition/tables/${measure.table}.tmdl`,
      measure
    );
  }

  // 5. 创建辅助计算列（如需要）
  await addCalculatedColumn(
    `${powerBIProject}.SemanticModel/definition/tables/Orders.tmdl`,
    {
      name: "Order Year-Month",
      formula: "FORMAT(Orders[Order Date], \"YYYY-MM\")",
      dataType: "string",
      dataCategory: "Months"
    }
  );

  // 6. 提取仪表板定义
  const dashboards = extractDashboards(twb);

  for (const dashboard of dashboards) {
    // 7. 创建报表页面
    const pageName = dashboard.name;
    await createPowerBIPage(
      `${powerBIProject}.Report/definition/pages/${pageName}/page.json`,
      dashboard
    );

    // 8. 提取和转换可视化组件
    const worksheets = extractWorksheets(twb, dashboard);

    for (const worksheet of worksheets) {
      const visual = convertWorksheetToVisual(worksheet);
      await createVisual(
        `${powerBIProject}.Report/definition/pages/${pageName}/visuals/${visual.name}/visual.json`,
        visual
      );
    }

    // 9. 配置筛选器
    const filters = extractFilters(dashboard);
    await configureFilters(
      `${powerBIProject}.Report/definition/pages/${pageName}/page.json`,
      filters
    );
  }

  // 10. 更新 pages.json
  await updatePagesJson(
    `${powerBIProject}.Report/definition/pages/pages.json`,
    dashboards.map(d => d.name)
  );

  console.log("转换完成！");
}

// 辅助函数示例

function convertCalculationsToDAX(calculations: Calculation[]): DAXMeasure[] {
  return calculations.map(calc => {
    // Tableau 公式 -> DAX 转换逻辑
    let daxFormula = calc.formula;

    // 替换常见函数
    daxFormula = daxFormula.replace(/sum\(\[(\w+)\]\)/gi, "SUM(Orders[$1])");
    daxFormula = daxFormula.replace(/avg\(\[(\w+)\]\)/gi, "AVERAGE(Orders[$1])");
    daxFormula = daxFormula.replace(/countd\(\[(\w+)\]\)/gi, "DISTINCTCOUNT(Orders[$1])");

    // 处理除法
    daxFormula = daxFormula.replace(/(\w+)\/(\w+)/g, "DIVIDE($1, $2, 0)");

    // 处理 LOD 表达式
    if (daxFormula.includes("{fixed")) {
      // {fixed [Order ID]:sum([Profit])}>0
      // -> CALCULATE(SUM(Orders[Profit]), ALLEXCEPT(Orders, Orders[Order ID]))>0
      const lodMatch = daxFormula.match(/\{fixed \[(\w+)\]:(\w+\(\[(\w+)\]\))\}/);
      if (lodMatch) {
        const [, field, aggExpr, column] = lodMatch;
        daxFormula = `CALCULATE(${convertAggExpression(aggExpr)}, ALLEXCEPT(Orders, Orders[${field}]))`;
      }
    }

    return {
      name: calc.caption,
      table: "Orders",
      formula: daxFormula,
      formatString: getFormatString(calc.datatype, calc.format)
    };
  });
}

function convertWorksheetToVisual(worksheet: TableauWorksheet): PowerBIVisual {
  // 识别可视化类型
  const visualType = identifyVisualType(worksheet);

  // 提取数据字段
  const fields = extractFields(worksheet);

  // 提取位置和尺寸
  const position = extractPosition(worksheet);

  // 构建 Power BI visual 定义
  return {
    name: worksheet.name,
    visualType: visualType,
    position: position,
    query: buildQuery(fields),
    objects: buildFormatting(worksheet.style)
  };
}
```

---

## 10. 常见问题和解决方案

### Q1: 如何处理 Tableau 的 LOD 表达式？

**A:** 使用 `CALCULATE` 和 `ALLEXCEPT`：

```dax
// Tableau: {FIXED [Order ID]:SUM([Profit])}
// Power BI:
VAR OrderProfit = CALCULATE(SUM(Orders[Profit]), ALLEXCEPT(Orders, Orders[Order ID]))
```

### Q2: 如何按月聚合日期？

**A:** 创建一个计算列：

```dax
column 'Order Year-Month' = FORMAT(Orders[Order Date], "YYYY-MM")
  dataType: string
  dataCategory: Months
```

然后在可视化中使用这个列而不是直接使用日期列。

### Q3: 为什么 Power BI 不支持 HierarchyLevel？

**A:** Power BI 的 JSON schema 不支持直接引用日期层次结构级别。解决方案是创建独立的月份列或使用标准的 Column 引用。

### Q4: 如何确保数值格式正确？

**A:** 在 TMDL 文件中使用正确的 formatString：

```tmdl
measure 'Total Sales' = SUM(Orders[Sales])
  formatString: \$#,0           # 货币格式，无小数

measure 'Profit Ratio' = DIVIDE([Total Profit], [Total Sales], 0)
  formatString: 0.0%            # 百分比格式，一位小数
```

### Q5: 如何调试 JSON 语法错误？

**A:**

1. 使用 JSON 验证器检查语法
2. 参考官方 schema：`https://developer.microsoft.com/json-schemas/fabric/item/report/...`
3. 对比 Retail Analysis Sample 等示例文件
4. 逐个添加属性，每次添加后验证

---

## 11. 最佳实践

### 11.1 命名约定

```
✅ 推荐：
- 度量值：'Total Sales', 'Profit Ratio'
- 计算列：'Order Year-Month', 'Order Profitable'
- 可视化：'CardSales', 'AreaChartSegment'
- 筛选器：'SlicerOrderDate', 'SlicerRegion'

❌ 避免：
- 使用特殊字符：'Sales$', 'Profit%'
- 空格过多：'Total   Sales'
- 混合大小写不一致：'totalsales', 'TotalSales'
```

### 11.2 lineageTag 管理

每个元素需要唯一的 lineageTag：

```tmdl
table Orders
  lineageTag: f1af49d1-3fe0-4c72-8aee-b7f20d358a5c

  measure 'Total Sales' = SUM(Orders[Sales])
    lineageTag: m-total-sales-001

  column 'Order ID'
    lineageTag: c-order-id-001
```

**命名规则：**
- 表：随机 GUID
- 度量值：`m-<name>-<number>`
- 列：`c-<name>-<number>`
- 计算列：`calc-<name>-<number>`

### 11.3 Z-index 管理

合理分配 z-index 确保层次正确：

```
1000-1099: 背景元素（地图、大型图表）
1100-1199: 中层元素（标准图表）
1200-1299: 前景元素（KPI 卡片、文本）
1300+:     顶层元素（筛选器、工具提示）
```

### 11.4 性能优化

1. **避免过度嵌套的 CALCULATE**
2. **使用变量（VAR）缓存重复计算**
3. **创建计算列而不是在度量值中重复计算**
4. **合理使用 ALLEXCEPT 而不是 ALL + FILTER**

---

## 12. 工具和资源

### 12.1 必备工具

- **Power BI Desktop**: 用于测试和验证报表
- **VS Code**: 编辑 JSON 和 TMDL 文件
- **JSON Validator**: 验证 JSON 语法
- **Git**: 版本控制

### 12.2 官方文档

- [Power BI JSON Schema](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report)
- [DAX Function Reference](https://learn.microsoft.com/en-us/dax/)
- [Tableau to Power BI Migration Guide](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-overview)

### 12.3 示例项目

- Retail Analysis Sample (本项目参考)
- Superstore Dashboard (本项目完成品)

---

## 13. 完整转换检查表

```markdown
## 数据模型转换
- [ ] 读取 Tableau TWB 文件
- [ ] 提取数据源定义
- [ ] 创建 Power BI 表结构（.tmdl）
- [ ] 添加所有基础列
- [ ] 转换计算字段为 DAX 度量值
- [ ] 创建辅助计算列（如 Year-Month）
- [ ] 验证数据类型和格式

## 报表结构创建
- [ ] 创建页面目录结构
- [ ] 创建 page.json
- [ ] 设置页面尺寸和显示选项
- [ ] 更新 pages.json

## 可视化组件转换
- [ ] 创建所有 KPI 卡片
- [ ] 创建面积图/折线图
- [ ] 创建地图可视化
- [ ] 创建筛选器（Slicer）
- [ ] 验证所有组件的位置和尺寸
- [ ] 检查数据字段绑定

## 筛选器和交互
- [ ] 配置页面级筛选器
- [ ] 设置筛选器默认值
- [ ] 验证交叉筛选功能
- [ ] 测试交叉高亮功能

## 样式和格式
- [ ] 应用颜色主题
- [ ] 设置字体和字号
- [ ] 配置数字格式
- [ ] 调整标题和标签

## 最终验证
- [ ] 在 Power BI Desktop 中打开
- [ ] 验证所有可视化正常显示
- [ ] 测试所有筛选器功能
- [ ] 对比 Tableau 看板验证数据准确性
- [ ] 检查性能和加载速度
```

---

## 总结

这个转换指南涵盖了从 Tableau 到 Power BI 的完整转换流程。关键步骤包括：

1. **数据模型转换**：将 Tableau 计算字段转换为 DAX 度量值
2. **布局转换**：将 Tableau 的相对布局转换为 Power BI 的像素坐标
3. **可视化转换**：为每个 Tableau 工作表创建对应的 Power BI visual
4. **筛选器配置**：在 Power BI 中重建 Tableau 的筛选器和交互
5. **样式应用**：匹配 Tableau 的颜色和格式

遵循本指南，任何 AI 助手都应该能够系统地完成 Tableau 到 Power BI 的转换工作。

---

**版本**: 1.0
**最后更新**: 2025-01-27
**作者**: AI Assistant
**基于项目**: Superstore Dashboard 转换实例
