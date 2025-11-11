# Tableau 到 Power BI 转换模型比较分析

以下表格详细对比了 Tableau (TWB) 和 Power BI (PBIP) 在实现六个核心组件时的不同方式。为了保持表格的简洁性，具体的代码案例已移至表格下方的“详细代码案例”部分。

| 组件 (Component) | Tableau (TWB) 实现 | Power BI (PBIP) 实现 | 代码案例引用 |
| :--- | :--- | :--- | :--- |
| **数据 (Data)** | 在 `Superstore.twb` 中，数据源连接、计算字段（如 `Profit Ratio`）的定义都集中在 `<datasource>` XML 节点内。 | 在 `superstore dashboard.SemanticModel` 文件夹中，数据模型被拆分为多个 `.tmdl` 文件。数据源连接通过 M 语言定义，度量值（如 `Profit Ratio`）通过 DAX 公式定义。 | [数据案例](#数据案例) |
| **布局 (Layout)** | 在 `Superstore.twb` 的仪表板定义中，每个图表或对象的位置由 `<zone>` 的 `x`, `y`, `w`, `h` 属性（0-100k 相对坐标）确定。 | 在 `superstore dashboard.Report` 目录中，每个视觉对象是一个独立的 `visual.json` 文件。其 `position` 对象使用像素绝对坐标来定义位置和大小。 | [布局案例](#布局案例) |
| **可视化 (Visuals)** | 在 `Superstore.twb` 中，一个可视化的类型由 `<worksheet>` 内的 `<mark class='...' />` 标签以及字段在 `<rows>` 和 `<cols>` 中的放置方式共同决定。 | 在 `visual.json` 文件中，`visualType` 明确指定图表类型（如 `areaChart`），并通过 `query` 属性定义图表的数据角色（如 X轴、系列、Y轴）。 | [可视化案例](#可视化案例) |
| **交互 (Interactions)** | 在 `Superstore.twb` 的仪表板区域，筛选器被定义为特殊的 `<zone type-v2='filter'>`，通过 `param` 属性关联到数据字段（如 `[Region]`）。 | 在 `visual.json` 文件中，筛选器是一个独立的 `slicer` 视觉对象，其 `visualType` 明确设为 `slicer`，并通过 `query` 属性指向数据字段。 | [交互案例](#交互案例) |
| **样式 (Styling)** | 在 `Superstore.twb` 中，样式信息（如字体大小 `fontsize`）散布在 `<run>` 标签等多个 XML 节点中，应用于标题或图表元素。 | 在 `visual.json` 文件中，视觉对象的样式（如标题文本、字体大小 `fontSize`）集中定义在 `visualContainerObjects` 或 `objects` 属性内。 | [样式案例](#样式案例) |
| **元数据 (Metadata)** | 在 `Superstore.twb` 中，仪表板的内部名称由 `<dashboard name='...'` 属性定义，显示标题在 `<layout-options>` 中定义。 | 在 `page.json` 文件中，页面的内部名称由 `name` 属性定义，用户可见的显示名称由 `displayName` 属性定义。 | [元数据案例](#元数据案例) |

---

## 详细代码案例

### 数据案例

**Tableau (TWB) - `Superstore.twb` 中的数据源和计算字段定义**
```xml
<!-- File: Superstore.twb -->
<datasource caption='Orders+ (Sample - Superstore)' inline='true' name='federated.1grjkbe1rk3bgn18cone81nvfrpo' version='18.1'>
  <connection class='federated'>
    <named-connections>
      <named-connection caption='Sample - Superstore' name='excel-direct.0tub4sk168y68u10hp9hu0qlkoge'>
        <connection class='excel-direct' cleaning='no' compat='no' dataRefreshTime='' filename='C:/Users/imgwho/Desktop/临时/20251017 twb2pbi/Superstore.twb 个文件/Data/20251017 twb2pbi/Sample - Superstore.xls' interpretationMode='0' password='' server='' validate='no' />
      </named-connection>
    </named-connections>
    <relation connection='excel-direct.0tub4sk168y68u10hp9hu0qlkoge' name='Orders' table='[Orders$]' type='table'>
      <columns gridOrigin='A1:U10195:no:A1:U10195:0' header='yes' outcome='2'>
        <!-- ... 字段定义 ... -->
        <column datatype='real' name='Sales' ordinal='17' />
        <column datatype='real' name='Profit' ordinal='20' />
      </columns>
    </relation>
  </connection>
  <column caption='Profit Ratio' datatype='real' default-format='p0.0%' name='[Calculation_9921103144103743]' role='measure' type='quantitative'>
    <calculation class='tableau' formula='sum([Profit])/sum([Sales])' />
  </column>
  <!-- ... 其他字段和计算 ... -->
</datasource>
```

**Power BI (PBIP) - `Orders.tmdl` 中的数据源和度量值定义**
```tmdl
// File: superstore dashboard.SemanticModel\definition\tables\Orders.tmdl
table Orders
	lineageTag: f1af49d1-3fe0-4c72-8aee-b7f20d358a5c

	measure 'Total Sales' = SUM(Orders[Sales])
		formatString: \$#,0
		lineageTag: m-total-sales-001

	measure 'Total Profit' = SUM(Orders[Profit])
		formatString: \$#,0
		lineageTag: m-total-profit-001

	measure 'Profit Ratio' = DIVIDE([Total Profit], [Total Sales], 0)
		formatString: 0.0%
		lineageTag: m-profit-ratio-001

	// ... 其他度量值和列定义 ...

	partition Orders = m
		mode: import
		source =
				let
				    源 = Excel.Workbook(File.Contents("C:\Users\imgwho\Desktop\临时\20251017 twb2pbi\pbi sample\Sample - Superstore.xls"), null, true),
				    Orders1 = 源{[Name="Orders"]}[Data],
				    提升的标题 = Table.PromoteHeaders(Orders1, [PromoteAllScalars=true]),
				    更改的类型 = Table.TransformColumnTypes(提升的标题,{{"Row ID", Int64.Type}, {"Order ID", type text}, {"Order Date", type date}, {"Ship Date", type date}, {"Ship Mode", type text}, {"Customer ID", type text}, {"Customer Name", type text}, {"Segment", type text}, {"Country/Region", type text}, {"City", type text}, {"State/Province", type text}, {"Postal Code", type text}, {"Region", type text}, {"Product ID", type text}, {"Category", type text}, {"Sub-Category", type text}, {"Product Name", type text}, {"Sales", type number}, {"Quantity", Int64.Type}, {"Discount", type number}, {"Profit", type number}})
				in
				    更改的类型
```

### 布局案例

**Tableau (TWB) - `Superstore.twb` 中的仪表板区域布局**
```xml
<!-- File: Superstore.twb -->
<dashboard name='Overview'>
  <!-- ... 其他仪表板配置 ... -->
  <zones>
    <zone h='100000' id='2' type-v2='layout-basic' w='100000' x='0' y='0'>
      <!-- ... 布局容器 ... -->
      <zone h='81667' id='53' param='vert' type-v2='layout-flow' w='84561' x='571' y='17666'>
        <zone h='58083' id='54' param='horz' type-v2='layout-flow' w='84561' x='571' y='41250'>
          <zone h='58083' id='44' name='SalesbySegment' w='41852' x='571' y='41250'>
            <layout-cache minheight='361' minwidth='226' type-h='scalable' type-w='scalable' />
            <zone-style>
              <format attr='border-color' value='#000000' />
              <format attr='border-style' value='none' />
              <format attr='border-width' value='0' />
              <format attr='margin' value='4' />
              <format attr='margin-bottom' value='0' />
              <format attr='margin-left' value='0' />
            </zone-style>
          </zone>
          <!-- ... 另一个区域图 ... -->
        </zone>
      </zone>
    </zone>
  </zones>
</dashboard>
```

**Power BI (PBIP) - `AreaChartSegment\visual.json` 中的视觉对象位置**
```json
// File: superstore dashboard.Report\definition\pages\ProfitabilityOverview\visuals\AreaChartSegment\visual.json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
  "name": "AreaChartSegment",
  "position": {
    "x": 10,
    "y": 390,
    "z": 8000,
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
              "queryRef": "Orders.Total Sales"
            }
          ]
        }
      }
    },
    "objects": {
      "legend": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            },
            "position": {
              "expr": {
                "Literal": {
                  "Value": "'Bottom'"
                }
              }
            }
          }
        }
      ]
    },
    "visualContainerObjects": {
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
                  "Value": "12D"
                }
              }
            }
          }
        }
      ]
    }
  },
  "filterConfig": {
    "filters": [
      {
        "name": "25b77b2c21dcc3510543",
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
        "type": "Categorical",
        "howCreated": "User"
      }
    ]
  }
}
```

### 可视化案例

**Tableau (TWB) - `Superstore.twb` 中的 `SalesbyProduct` 工作表定义**
```xml
<!-- File: Superstore.twb -->
<worksheet name='SalesbyProduct'>
  <layout-options>
    <title>
      <formatted-text>
        <run>Monthly Sales by Product Category</run>
        <run bold='false'><![CDATA[ - States: <[federated.1grjkbe1rk3bgn18cone81nvfrpo].[none:State/Province:nk]>]]></run>
      </formatted-text>
    </title>
  </layout-options>
  <table>
    <view>
      <datasources>
        <datasource caption='Orders+ (Sample - Superstore)' name='federated.1grjkbe1rk3bgn18cone81nvfrpo' />
      </datasources>
      <datasource-dependencies datasource='federated.1grjkbe1rk3bgn18cone81nvfrpo'>
        <column datatype='string' name='[Category]' role='dimension' type='nominal' />
        <column datatype='date' name='[Order Date]' role='dimension' type='ordinal' />
        <column datatype='real' name='[Sales]' role='measure' type='quantitative' />
        <column-instance column='[Category]' derivation='None' name='[none:Category:nk]' pivot='key' type='nominal' />
        <column-instance column='[Sales]' derivation='Sum' name='[sum:Sales:qk]' pivot='key' type='quantitative' />
        <column-instance column='[Order Date]' derivation='Month-Trunc' name='[tmn:Order Date:qk]' pivot='key' type='quantitative' />
      </datasource-dependencies>
      <!-- ... 筛选器 ... -->
      <aggregation value='true' />
    </view>
    <panes>
      <pane id='4' selection-relaxation-option='selection-relaxation-disallow'>
        <view>
          <breakdown value='auto' />
        </view>
        <mark class='Area' />
        <encodings>
          <color column='[federated.1grjkbe1rk3bgn18cone81nvfrpo].[none:Calculation_9060122104947471:nk]' />
          <tooltip column='[federated.1grjkbe1rk3bgn18cone81nvfrpo].[sum:Profit:qk]' />
        </encodings>
        <!-- ... 自定义工具提示 ... -->
      </pane>
    </panes>
    <rows>([federated.1grjkbe1rk3bgn18cone81nvfrpo].[none:Category:nk] * [federated.1grjkbe1rk3bgn18cone81nvfrpo].[sum:Sales:qk])</rows>
    <cols>[federated.1grjkbe1rk3bgn18cone81nvfrpo].[tmn:Order Date:qk]</cols>
  </table>
</worksheet>
```

**Power BI (PBIP) - `AreaChartCategory\visual.json` 中的视觉对象定义**
```json
// File: superstore dashboard.Report\definition\pages\ProfitabilityOverview\visuals\AreaChartCategory\visual.json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
  "name": "AreaChartCategory",
  "position": {
    "x": 435,
    "y": 390,
    "z": 9000,
    "height": 320,
    "width": 425
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
                  "Property": "Category"
                }
              },
              "queryRef": "Orders.Category",
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
              "queryRef": "Orders.Total Sales"
            }
          ]
        }
      }
    },
    "objects": {
      "legend": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            },
            "position": {
              "expr": {
                "Literal": {
                  "Value": "'Bottom'"
                }
              }
            }
          }
        }
      ]
    },
    "visualContainerObjects": {
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
                  "Value": "'Monthly Sales by Product Category'"
                }
              }
            },
            "fontSize": {
              "expr": {
                "Literal": {
                  "Value": "12D"
                }
              }
            }
          }
        }
      ]
    }
  },
  "filterConfig": {
    "filters": [
      {
        "name": "b15277bbcbb0d0507ca4",
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
        "type": "Categorical",
        "howCreated": "User"
      }
    ]
  }
}
```

### 交互案例

**Tableau (TWB) - `Superstore.twb` 中的区域筛选器**
```xml
<!-- File: Superstore.twb -->
<dashboard name='Overview'>
  <!-- ... 其他仪表板配置 ... -->
  <zones>
    <!-- ... 布局容器 ... -->
    <zone h='81667' id='52' param='horz' type-v2='layout-flow' w='14297' x='85132' y='17666'>
      <zone fixed-size='304' h='81667' id='51' is-fixed='true' param='vert' type-v2='layout-flow' w='14297' x='85132' y='17666'>
        <!-- ... 其他筛选器 ... -->
        <zone h='5500' id='17' mode='dropdown' name='SaleMap' param='[federated.1grjkbe1rk3bgn18cone81nvfrpo].[none:Region:nk]' type-v2='filter' values='relevant' w='13869' x='85489' y='23916'>
          <zone-style>
            <format attr='border-color' value='#000000' />
            <format attr='border-style' value='none' />
            <format attr='border-width' value='0' />
            <format attr='margin' value='4' />
            <format attr='margin-right' value='1' />
            <format attr='margin-left' value='1' />
            <format attr='background-color' value='#f0f0f0' />
          </zone-style>
        </zone>
        <!-- ... 其他筛选器 ... -->
      </zone>
    </zone>
  </zones>
</dashboard>
```

**Power BI (PBIP) - `SlicerRegion\visual.json` 中的切片器定义**
```json
// File: superstore dashboard.Report\definition\pages\ProfitabilityOverview\visuals\SlicerRegion\visual.json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
  "name": "SlicerRegion",
  "position": {
    "x": 870,
    "y": 230,
    "z": 11000,
    "height": 70,
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
                  "Property": "Region"
                }
              },
              "queryRef": "Orders.Region",
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
                  "Value": "1D"
                }
              }
            }
          }
        }
      ],
      "data": [
        {
          "properties": {
            "mode": {
              "expr": {
                "Literal": {
                  "Value": "'Dropdown'"
                }
              }
            }
          }
        }
      ]
    },
    "visualContainerObjects": {
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
                  "Value": "'Region'"
                }
              }
            },
            "fontSize": {
              "expr": {
                "Literal": {
                  "Value": "11D"
                }
              }
            }
          }
        }
      ]
    }
  },
  "filterConfig": {
    "filters": [
      {
        "name": "c9d8120c05da47cc0b5e",
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
        "type": "Categorical"
      }
    ]
  }
}
```

### 样式案例

**Tableau (TWB) - `Superstore.twb` 中的 `SaleMap` 工作表标题样式**
```xml
<!-- File: Superstore.twb -->
<worksheet name='SaleMap'>
  <layout-options>
    <title>
      <formatted-text>
        <run fontsize='13'>Sales by Geography</run>
      </formatted-text>
    </title>
  </layout-options>
  <!-- ... 其他工作表配置 ... -->
</worksheet>
```

**Power BI (PBIP) - `AreaChartCategory\visual.json` 中的视觉对象标题样式**
```json
// File: superstore dashboard.Report\definition\pages\ProfitabilityOverview\visuals\AreaChartCategory\visual.json
{
  "$schema": "...",
  "name": "AreaChartCategory",
  "position": { ... },
  "visual": {
    "visualType": "areaChart",
    "query": { ... },
    "objects": { ... },
    "visualContainerObjects": {
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
                  "Value": "'Monthly Sales by Product Category'"
                }
              }
            },
            "fontSize": {
              "expr": {
                "Literal": {
                  "Value": "12D"
                }
              }
            }
          }
        }
      ]
    }
  },
  "filterConfig": { ... }
}
```

### 元数据案例

**Tableau (TWB) - `Superstore.twb` 中的仪表板名称和显示标题**
```xml
<!-- File: Superstore.twb -->
<dashboard name='Overview'>
  <layout-options export-center-horz='true' export-center-vert='true' export-orientation='landscape'>
    <title>
      <formatted-text>
        <run fontalignment='0'>Profitability Overview</run>
      </formatted-text>
    </title>
  </layout-options>
  <!-- ... 其他仪表板配置 ... -->
</dashboard>
```

**Power BI (PBIP) - `ProfitabilityOverview\page.json` 中的页面名称和显示名称**
```json
// File: superstore dashboard.Report\definition\pages\ProfitabilityOverview\page.json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
  "name": "ProfitabilityOverview",
  "displayName": "Profitability Overview",
  "displayOption": "FitToPage",
  "width": 1280,
  "height": 720
}
```