**表格模型定义语言 （TMDL）**

*🔗 原文链接：* [*https://learn.microsoft.com/zh-cn/a...*](https://learn.microsoft.com/zh-cn/analysis-services/tmdl/tmdl-overview?view=sql-analysis-services-2025#tmdl-folder-structure)

*⏰ 剪存时间：2025-11-09 23:19:57 (UTC+8)*

*✂️ 本文档由* [*飞书剪存*](https://www.feishu.cn/hc/zh-CN/articles/606278856233?from=in_ccm_clip_doc) *一键生成*

**适用于：**

![](data:image/png;base64...)

SQL Server 2016 及更高版本 Analysis Services

![](data:image/png;base64...)

Azure Analysis Services

![](data:image/png;base64...)

Fabric/Power BI Premium

表格模型定义语言（TMDL）是兼容级别为 1200 或更高版本的表格数据模型的对象模型定义语法。

TMDL 的关键元素包括：

* 与整个 [表格对象模型（TOM）](https://learn.microsoft.com/zh-cn/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=sql-analysis-services-2025) 完全兼容。 每个 TMDL 对象都公开与 TOM 相同的属性。
* 基于文本并针对人工交互和可读性进行优化。 TMDL 使用类似于 YAML 的语法语法。 每个 TMDL 对象以文本表示，使用最小分隔符，并使用缩进来标记父子关系。
* 更好的编辑体验，尤其是具有来自不同内容类型的嵌入表达式（如数据分析表达式（DAX）和 M 的属性。
* 更适合协作，因为它的文件夹表示形式，其中每个模型对象都有单独的文件表示形式，使其更便于源代码管理。

TMDL 的一个重要方面是使用空格缩进来表示 TOM 对象结构。 以下示例演示如何在使用 TMDL 时表示表格模型是多么容易：

|  |
| --- |
| Plaintext database Sales  compatibilityLevel: 1567  model Model   culture: en-US   table Sales    partition 'Sales-Partition' = m  mode: import  source =   let  Source = Sql.Database(Server, Database)  …    measure 'Sales Amount' = SUMX('Sales', 'Sales'[Quantity] \* 'Sales'[Net Price])  formatString: $ #,##0    column 'Product Key'  dataType: int64  isHidden  sourceColumn: ProductKey  summarizeBy: None    column Quantity  dataType: int64  isHidden  sourceColumn: Quantity  summarizeBy: None   column 'Net Price'  dataType: int64  isHidden  sourceColumn: "Net Price"  summarizeBy: none  table Product    partition 'Product-Partition' = m  mode: import  source =   let  Source = Sql.Database(Server, Database),  …   column 'Product Key'  dataType: int64  isKey  sourceColumn: ProductKey  summarizeBy: none  relationship cdb6e6a9-c9d1-42b9-b9e0-484a1bc7e123  fromColumn: Sales.'Product Key'  toColumn: Product.'Product Key'  role Role\_Store1  modelPermission: read   tablePermission Store = 'Store'[Store Code] IN {1,10,20,30}  expression Server = "localhost" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]  expression Database = "Contoso" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true] |

**TMDL 文件夹结构**

与 TMSL 不同，TMDL 使用文件夹结构。 默认文件夹结构只有一个级别的 *子文件夹* ，所有子文件夹中都有 .tmdl 文件。

* 文化
* 观点
* 角色
* 表

*根文件* 的用途是：

* 数据库
* 模型
* 关系
* 表达 式
* 数据源
* 函数 （ [DAX 用户定义的函数）](https://learn.microsoft.com/zh-cn/dax/best-practices/dax-user-defined-functions)

下面是 TMDL 文件夹的示例：

|  |
| --- |
| Plaintext TMDL/ ├── cultures/ │ ├── en-US.tmdl │ └── pt-PT.tmdl ├── perspectives/ │ └── perspective1.tmdl ├── roles/ │ ├── role1.tmdl │ └── role2.tmdl ├── tables/ │ ├── About.tmdl │ ├── Calendar.tmdl │ ├── Customer.tmdl │ ├── Product.tmdl │ ├── Sales.tmdl │ └── Store.tmdl ├── relationships.tmdl ├── functions.tmdl ├── expressions.tmdl ├── dataSources.tmdl ├── model.tmdl └── database.tmdl |

定义包括：

* 一个文件用于数据库定义。
* 模型定义的一个文件。
* 模型中 *所有* 数据源的一个文件。
* 模型中 *所有* 表达式的一个文件。
* 一个文件用于 *所有* 函数（模型中的 [DAX 用户定义的函数](https://learn.microsoft.com/zh-cn/dax/best-practices/dax-user-defined-functions) ）。
* 模型中 *所有* 关系的一个文件。
* *每个* 文化语言架构的一个文件。
* *每个* 视图一个文件。
* 为每个角色生成一个文件。
* *每个表一个文件* 。
* 表（列、层次结构、分区,...）元数据的所有内部元数据属性都位于父表 TMDL 文件中。

**TMDL API**

与 [表格模型脚本语言（TMSL）](https://learn.microsoft.com/zh-cn/analysis-services/tmsl/tabular-model-scripting-language-tmsl-reference?view=sql-analysis-services-2025) 类似，有一个类来处理 TMDL 序列化。 对于 TMDL，类是 [**tmdlSerializer**](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.analysisservices.tmdlserializer) ，位于 [**Microsoft.AnalysisServices.Tabular**](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.analysisservices.tabular) 命名空间下。

TmdlSerializer 类公开了序列化和反序列化 TMDL 文档的方法：

**文件夹序列化**

public static void SerializeDatabaseToFolder (Database database, string path)

* 接收 TOM 数据库对象和 TMDL 输出路径。
* 将 TOM 数据库序列化为 TMDL 文件夹表示形式。

详细了解 [如何将数据序列化到文件夹中](https://learn.microsoft.com/zh-cn/analysis-services/tmdl/tmdl-how-to?view=sql-analysis-services-2025#get-a-tmdl-model-representation) 。

public static Database DeserializeDatabaseFromFolder (string path)

* 接收 TMDL 文件夹的完整路径。
* 返回 TMDL 文件夹的 TOM 数据库对象表示形式。

详细了解 [如何从文件夹反序列化](https://learn.microsoft.com/zh-cn/analysis-services/tmdl/tmdl-how-to?view=sql-analysis-services-2025#deploy-a-tmdl-model-representation) 。

**字符串序列化**

public static string SerializeObject (MetadataObject object, bool qualifyObject = true)

* 接收 TOM 对象并返回其 TMDL 文本表示形式。

详细了解 [如何将对象序列化为字符串](https://learn.microsoft.com/zh-cn/analysis-services/tmdl/tmdl-how-to?view=sql-analysis-services-2025#object-text-serialization) 。

**流序列化**

可以将 TMDL 序列化/反序列化为流，以便将 TOM 对象转换为字节流，以实现跨平台的存储、传输和互操作性。 流 API 还允许你控制加载哪些 TMDL 文档以及输出了哪些 TMDL 文档。

TMDL 流序列化由 [**MetadataSerializationContext**](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.analysisservices.tabular.serialization.metadataserializationcontext) 类处理。

详细了解 [如何使用流进行 TMDL 的序列化和反序列化](https://learn.microsoft.com/zh-cn/analysis-services/tmdl/tmdl-how-to?view=sql-analysis-services-2025#stream-serialization) 。

**TMDL 语言**

**对象声明**

除了 Server 对象，TMDL 在 *Microsoft.AnalysisServices.Tabular 命名空间* 中公开整个 TOM [数据库](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.analysisservices) 对象树。

通过指定 TOM 对象类型后跟其名称来声明 TMDL 对象。 在下面的代码示例中，每个对象类型 model 、 table 、 column 后面跟着一个对象名称。

|  |
| --- |
| Plaintext model Model   culture: en-US   table Sales    measure Sales = SUM(…)  formatString: $ #,##0   column 'Customer Key'  datatype: int64  sourceColumn: CustomerKey |

对象（例如 partition 或 measure ）具有 默认属性 ，这些属性可以在对象声明的同一行的等号（ **=** ）分隔符之后或在多行 表达式 的以下行中分配。

|  |
| --- |
| Plaintext table Sales   partition Sales-Part1 = m  mode: import  ...     measure Sales = SUM(…)  formatString: $ #,##0   measure 'Sales (ly)' =   var ly = ...  return ly  formatString: $ #,##0 |

如果 TMDL 对象名称包含以下任何字符，则必须用单引号（ **'** ）括起来：

* 点 （ **.** ）
* 等于 （ **=** ）
* 冒号 （ **：** ）
* 单引号 （ **'** ）
* 空格 （ ）

如果对象名称包含单引号（ **'** ），请使用两个单引号对其进行转义。

**对象属性**

对象属性在对象声明或对象默认属性多行表达式之后指定。 对象属性值在冒号 （ **：** ） 分隔符下指定。 例如：

|  |
| --- |
| Plaintext table Sales  lineageTag: e9374b9a-faee-4f9e-b2e7-d9aafb9d6a91    column Quantity  dataType: int64  isHidden  isAvailableInMdx: false  sourceColumn: Quantity   measure 'Sales Amount' =   var result = SUMX(...)  return result  formatString: $ #,##0  displayFolder: " My ""Amazing"" Measures" |

以下规则适用于属性值：

* 值必须位于冒号之后的同一行中，并且不能具有多行。
* 文本属性值
* 前导和尾随双引号是可选的，在序列化期间自动去除。
* 如果文本包含尾随空格或前导空格，则必须用双引号（ **“** ）括起来。
* 当用双引号括起来时，如果值包含双引号，请使用两个双引号来转义它们（请参阅上面的代码示例中的 displayFolder 属性）。
* 可以使用标准键/值对语法来设置 **布尔属性** ，如 'isAvailableInMdx' 上一示例中的属性。 还可以通过使用仅声明属性名称且 true 隐含的快捷语法来设置它们。 例如，请参阅上一示例中的“isHidden”属性。

**命名对象引用**

某些对象属性保存对其他模型对象的引用，例如：

* 层次结构级别的列引用。
* 每个表列中的 sortByColumn 引用。
* 透视中的表/列/度量值引用。

在 TMDL 中，引用时使用对象名称，并遵循与对象声明相同的转义和用单引号 ( **'** ) 括起来的要求。 在下面的代码示例中，可以看到保存对另一个对象的引用的对象属性： column.sortByColumn ， level.column perspectiveMeasure.measure 以及 perspectiveTable.table 。

|  |
| --- |
| Plaintext  table Product   column Category  sortByColumn: 'Category Order'    hierarchy 'Product Hierarchy'   level Category   column: Category     perspective Product   perspectiveTable Product   perspectiveMeasure '# Products' |

如果需要引用完全限定的名称，TMDL 使用 *点* 表示法引用对象，例如： 'Table 1'.'Column 1'

**子对象**

TOM 对象树包含多个位置及不同级别的子对象。 例如：

* 模型对象包含表、角色和表达式对象。
* 表对象包含列、度量值和层次结构对象。

TMDL 不会显式声明子集合。 相反，其各自父级范围内的所有适用子元素都隐式构成相应集合的元素。 例如，特定表范围内的所有列元素都将成为 TOM 中该表的列集合的元素，如下所示：

|  |
| --- |
| Plaintext table Sales   measure 'Sales Amount' = SUMX('Sales', [Quantity] \* [Net Price])   measure 'Total Quantity' = SUM('Sales'[Quantity])   measure 'Sales Amount YTD' = TOTALYTD([Sales Amount], 'Calendar'[Date]) |

子对象不必连续。 例如，可以按任意顺序声明列和度量值并相互关联。

**默认属性**

某些对象类型具有默认属性，大多数时间都被视为 表达式 。 默认属性特定于对象类型。 如果适用，则在节声明之后，属性值或表达式通过等号（ **=** ）分隔符指定。

支持的语法：

* 该值在节标头所在的同一行上指定。
* 该值指定为节标头后面的多行表达式。

在以下代码示例中，度量 Sales Amount 值和分区 Sales-Partition1 是单行，度量 Quantity 值是多行：

|  |
| --- |
| Plaintext table Sales   measure 'Sales Amount' = SUM(...)  formatString: $ #,##0   measure Quantity =   var result = SUMX (...)  return result  formatString: #,##0   partition Sales-Partition1 = m  mode: import  source =  let  ...  in  finalStep |

**表达 式**

在 TOM 中作为文本属性时，有一些对象属性在 TMDL 中获取特殊分析。 整个文本都是逐字读取的，因为它可以在 M 或 DAX 表达式中包含特殊字符，如引号或方括号。 表达式可以是多行或单行。 如果多行，则它们必须紧跟在属性或对象声明之后的行中。

在 TMDL 中，表达式的值是通过等号（ **=** ）分隔符指定的，如以下示例所示：

|  |
| --- |
| Plaintext table Table1   partition 'partition 1' = m  mode: import  source =  let  ...  in  finalStep    measure Measure1 = SUM(...)   measure Measure2 =  var result = SUMX (   ...  )  return result  formatString: $ #,##0 |

以下特殊规则适用于表达式：

* 多行表达式必须更深入地缩进到父对象属性的一个级别，并且整个表达式必须位于该缩进级别内。
* 所有外部缩进空格被剥离到父对象的缩进级别之外。
* 允许垂直空格（没有空格的空白行），并被视为表达式的一部分。
* 删除尾随空白行和空格。
* 若要强制实施不同的缩进或者保留行尾空行或空格，请使用三个反引号（ **```** ）括住。
* 默认情况下，如果表达式值包含任何可能导致往返修改的任何内容（例如尾随空格、带空格的空白行），TMDL 序列化程序将用反引号括起来。

用三个反引号（ **```** ）括起来的表达式是逐字读取的，包括缩进、空白行和空格。 分隔符应紧跟在等号（ **=** ）后面，紧跟表达式后面的行，并且之后不能包含任何内容，如以下示例所示：

|  |
| --- |
| Plaintext table Table1   partition partition1 = m  mode: import  source = ```  let  ...  in  finalStep   ```   measure Measure1 = ```  var myVar = Today()  …  return result  ``` |

使用三个反引号（ **```** ）作为分隔符是可选的，并且仅在特殊情况下才是必需的。 在大多数情况下，使用正确的缩进和对象声明可确保正确分析添加到属性的任何表达式。

当表达式包含在反杆内时，将应用以下规则：

* 三个反引号（ **```** ）之间的所有内容被视为多块表达式的一部分，因此不适用 TMDL 缩进规则。 结束分隔符确定表达式中的缩进。
* 将保留表达式中的相对缩进。 结束分隔符 （ **```** ） 确定表达式左边界（请参阅上一示例中的“Measure1”。

以下属性被视为表达式：

|  |  |  |
| --- | --- | --- |
| 对象类型 | 财产 | 表达式语言 |
| 量 | 表达 | DAX |
| 功能 | 表达 | DAX |
| MPartitionSource | 表达 | M |
| CalculatedPartitionSource | 表达 | DAX |
| QueryPartitionSource | 查询 | NativeQuery |
| CalculationItem | 表达 | DAX |
| BasicRefreshPolicy | SourceExpression、PollingExpression | M |
| KPI | StatusExpression、TargetExpression、TrendExpression | DAX |
| LinguisticMetadata | 内容 | XML 或 Json |
| JsonExtendedProperty | 价值 | Json |
| FormatStringDefintion | 表达 | DAX |
| DataCoverageDefinition | 表达 | DAX |
| CalculationGroupExpression | 表达 | DAX |
| NamedExpression | 表达 | DAX |
| DetailRowsDefinition | 表达 | DAX |
| TablePermission | FilterExpression | DAX |
| CalculatedColumn | 表达 | DAX |

**按对象类型排序的默认属性**

下表按对象类型显示默认属性和表达式语言：

|  |  |  |
| --- | --- | --- |
| 对象类型 | 默认属性 | 表达式语言 |
| 量 | 表达 | DAX |
| 功能 | 表达 | DAX |
| CalculatedColumn | 表达 | DAX |
| CalculationItem | 表达 | DAX |
| FormatStringDefinition | 表达 | DAX |
| DetailRowsDefinition | 表达 | DAX |
| CalculationExpression | 表达 | DAX |
| DataCoverageDefinition | 表达 | DAX |
| TablePermission | FilterExpression | DAX |
| ColumnPermission | MetadataPermission | [MetadataPermission 枚举](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.analysisservices.tabular.metadatapermission) |
| NamedExpression | 表达 | M |
| MPartitionSource | 表达 | M |
| CalculatedPartitionSource | 表达 | DAX |
| JsonExtendedProperty | 价值 | Json |
| 注解 | 价值 | 文本 |
| StringExtendedProperty | 价值 | 文本 |
| DataSource | 类型 | [DataSourceType 枚举](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.analysisservices.tabular.datasourcetype) |
| 分区 | SourceType | [PartitionSourceType 枚举类型](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.analysisservices.tabular.partitionsourcetype) |
| ChangedProperty | 财产 | [属性文本](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.analysisservices.tabular.changedproperty.property#microsoft-analysisservices-tabular-changedproperty-property) |
| ExternalModelRoleMember | MemberType | [RoleMemberType 枚举](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.analysisservices.tabular.rolemembertype) |
| 任何自定义 JSON 属性（例如 DataAccessOptions） | JSON 文档 | Json |
| LinguisticMetadata | 内容 | Json |

**描述**

TMDL 为说明提供一流的支持。 出于模型文档的目的，最佳做法是为每个 TOM 对象提供说明。 TMDL 将说明视为具有显式语法支持的特殊属性。 按照许多其他语言的示例，使用三斜杠（ **///** ）语法在每个对象声明的基础上指定说明。

说明块末尾和对象类型标记之间不允许有空格。

可以跨多行拆分说明。 TMDL 序列化程序将对象描述分解为多行，以将发出的文档行保持在最大长度之下。 默认的最大长度为 80 个字符。

|  |
| --- |
| Plaintext /// Table Description table Sales   /// This is the Measure Description  /// One more line  measure 'Sales Amount'' = SUM(...)  formatString: #,##0 |

**分部声明**

TMDL 不会强制同一文档中的对象声明。 但是，它类似于 [C# 分部类](https://learn.microsoft.com/zh-cn/dotnet/csharp/programming-guide/classes-and-structs/partial-classes-and-methods) ，可以在多个文件之间拆分对象定义。 例如，可以在 [table].tmdl 文件中声明表定义，然后让单个 [measures].tmdl 文件中定义的所有表的所有度量值，如下所示：

|  |
| --- |
| Plaintext table Sales   measure 'Sales Amount' = SUM(…)  formatString: $ #,##0  table Product   measure CountOfProduct = COUNTROWS(…) |

为了避免分析错误，无法声明同一属性两次。 例如，在两个不同的 TMDL 文档中为同一表声明具有相同名称的两个度量值会导致错误。

**对象引用**

可以使用 **ref** 关键字引用另一个 TMDL 对象，后跟对象类型和名称。

例如，如果使用字符串序列化 API 序列化 Column 对象，结果将为：

|  |
| --- |
| Plaintext ref table Table1  column Column1  datatype: int64  sourceColumn: Column1 |

**确定性集合排序**

**ref** 关键字还用于定义和保留 TOM <> TMDL 往返的集合顺序。 在 TMDL 对象上避免源代码管理差异尤其重要，这些对象可序列化为单个文件：表、角色、区域性和透视。 **ref** 关键字用于父对象 TMDL 文件，以声明 TOM 中的项排序：

|  |
| --- |
| Plaintext  model Model  ref table Calendar ref table Sales ref table Product ref table Customer ref table About  ref culture en-US ref culture pt-PT  ref role 'Stores Cluster 1' ref role 'Stores Cluster 2' |

应用以下规则：

* 在 TMDL 反序列化期间：
* 在 TMDL 中引用但缺少 TMDL 文件的对象将被忽略。
* 未引用但具有现有 TMDL 文件的对象将追加到集合的末尾。
* 在 TMDL 序列化期间：
* TOM 中的所有集合对象都使用 **ref** 关键字进行引用。
* 只有一个项目的集合不会发出 ref。
* 如果对象类型相同，则不在同一对象类型之间发出空行。

**属性值分隔符**

只有两个分隔符/符号可用于分配属性值：

* 等于 （ **=** ）
* 用于对象声明和 默认属性 （多行和单行）
* 在每个 表达式属性 （例如 partition.expression）上使用
* 冒号 （ **：** ）
* 用于每个非表达式 属性值 。 包括保存模型引用的属性。

**凹痕**

TMDL 使用严格的空格缩进规则来表示 TOM 层次结构的结构。 TMDL 文档使用默认单 **制表符** 缩进规则。

每个对象可以有三个级别的缩进：

* 级别 1 - 对象声明
* 级别 2 - 对象属性
* 级别 3 - 对象属性多行表达式

在 TMDL 文档中，在以下情况下应用缩进：

* 在对象部分标头和对象的属性（表 -> 属性）之间。

|  |
| --- |
| Plaintext table Sales  isHidden  lineageTag: 9a48bea0-e5fb-40fa-9e81-f61288e31a02 |

* 对象及其子对象（表 -> 度量值）之间。

|  |
| --- |
| Plaintext table Sales   measure 'Sales Amount' = SUMX(...)   measure 'Total Quantity' = SUM(...) |

* 对象与其多行表达式（表 -> 度量值 -> 表达式）之间。

|  |
| --- |
| Plaintext table Sales   measure 'Sales Amount' =   var result = SUMX(...)  return result  formatString: $ #,##0 |

* 多行表达式必须缩进一个比对象属性更深的级别，并且整个表达式必须位于该缩进级别（请参阅 表达式 ）。

模型的数据库和直接子对象不需要缩进，因为它们是隐式假定嵌套在根模型或数据库下：

* 模型
* 表
* 共享表达式
* 角色
* 文化
* 观点
* 关系
* 数据源
* 查询组
* 模型级批注
* 模型级扩展属性

不遵循这些缩进规则将生成分析错误。

**空白**

默认情况下，TMDL 将以下规则应用于属性和表达式值中的空格（如果未包含在反引号（ **```** ）或双引号内（ **“** ）：

* 在属性值上，将剪裁前导空格和尾随空格。
* 在表达式上，删除表达式末尾的空格行。
* 空格行被剪裁为空行（无空格/制表符）。

**套管**

默认情况下，TMDL API 在序列化/写入时使用 **camelCase** ，适用于：

* 对象类型
* 关键字
* 枚举值

在反序列化/读取时，TMDL API 不区分大小写。

**相关内容**

了解 TMDL 后，请务必了解 [TMDL](https://learn.microsoft.com/zh-cn/analysis-services/tmdl/tmdl-how-to?view=sql-analysis-services-2025) 入门，了解如何获取和部署 Power BI 语义模型的 TMDL 模型表示形式。