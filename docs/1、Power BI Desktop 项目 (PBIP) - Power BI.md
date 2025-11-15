**1、Power BI Desktop 项目 (PBIP) - Power BI**

*🔗 原文链接：* [*https://learn.microsoft.com/zh-cn/p...*](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-overview)

*⏰ 剪存时间：2025-11-09 23:17:08 (UTC+8)*

*✂️ 本文档由* [*飞书剪存*](https://www.feishu.cn/hc/zh-CN/articles/606278856233?from=in_ccm_clip_doc) *一键生成*

1. 报表定义（PBIR）相关资料

**必须掌握**

* PBIP项目文件结构与编辑说明
  <https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-overview>

|  |
| --- |
| * *涉及 definition、SemanticModel 两大目录的用途、项目文件引用及版本控制场景。* |

* PBIR报表文件夹细节
  <https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-report>

|  |
| --- |
| * *页面、可视化元素、书签的分文件存储与命名规则；与 schema 的绑定方式；以及新增/删除页面时的自动维护机制。* |

* PBIR所有schema规范
  <https://github.com/microsoft/json-schemas>

|  |
| --- |
| * *重点关注 fabric/item/report/definition/ 目录下的 report.json、page.json、visualContainer.json、bookmark.json 等schema文件，每个schema都要用于自动生成或校验对应模块（页面、报表头、每个图表、每个筛选器等）的json。AI要严格按schema字段生成。* |

* 页面、visual、slicer等类型与交互说明
  <https://learn.microsoft.com/zh-cn/power-bi/visuals/power-bi-visualization-types-for-reports-and-q-and-a>

|  |
| --- |
| * *列举了所有visualType（如卡片/表格/柱状图/切片器/地图等）、各种交互特性（筛选/钻取/工具栏等），用于让AI理解各类图表和交互的配置字段取值范围和常用用法。* |

**推荐补充**

* 官方样板库 <https://learn.microsoft.com/zh-cn/power-bi/create-reports/sample-datasets>

|  |
| --- |
| * *可以下载PBIX转PBIP，获得真实的definition页面和visual.json作为实际AI训练/生成参考。* |

1. 语义模型（TMDL）相关资料

**必须掌握**

* TMDL结构总览与文件夹表示法
  <https://learn.microsoft.com/zh-cn/analysis-services/tmdl/tmdl-overview?view=sql-analysis-services-2025#tmdl-folder-structure>

|  |
| --- |
| * *涉及model、table、column、measure、relationship、datasource、expression等对象的文本/YAML风格定义及各自独立.tmdl文件，有助于AI按需生成和拆分模型元数据。* |

* TMDL条目声明、属性与表达式规范（同一个文档）

|  |
| --- |
| * *涉及每个对象的声明语法、属性赋值、表达式（DAX/M/SQL）、引用、聚合、描述等，涵盖模型完整人工可读/可写元数据的所有细节，让AI能批量生成自动校验无误的标准TMDL。* |

* TMDL与TOM的关系与序列化代码

|  |
| --- |
| * *有代码API说明（TmdlSerializer等），如需使用Python或C#等自动化生成可通过托管对象模型序列化/反序列化的文件夹。* |

**推荐补充**

* 官方示例目录（下载TMDL模型结构文件，看真实结构）：

|  |
| --- |
| * *可以配合PBIP的SemanticModel目录，对照实际文件内容与规范生成方式。* |

重要

Power BI Desktop 项目目前为预览版。

Power BI Desktop 引入了一种创作、协作和保存项目的新方法。 将工作另存为 Power BI 项目 (PBIP) 时，报表和语义模型项定义在简单直观的文件夹结构中另存为单独的纯文本文件  。

将工作另存为项目具有以下优势：

* **文本编辑器支持** - PBIP 文件是包含语义模型和报表元数据的格式文本文件。 这些文件已公开记录，可读。 虽然项目文件支持记事本等简单文本编辑工具，但最好使用 [Visual Studio Code (VS Code)](https://code.visualstudio.com/) 等代码编辑器，从而提供丰富的编辑体验，包括智能感知、验证和 Git 集成。
* **文件夹结构透明度** - 语义模型和报表的单独文件夹，可实现强大的简单任务，例如在项目之间复制语义模型表或重用报表页。 用于创建和重用开发模板的绝佳选择。
* **源代码管理就绪** - 打开文本文件，旨在与 Git 无缝集成，启用版本历史记录和团队协作。 要了解详细信息，请参阅 [Git 中的版本控制](https://learn.microsoft.com/zh-cn/devops/develop/git/what-is-version-control) 。
* **持续集成和持续交付（CI/CD）支持** - 使用 PBIP 文件在现有源代码管理系统上应用 CI/CD 做法，结合质量关卡并自动化部署到生产环境。 若要详细了解 Fabric 中的 CI/CD，请参阅 [Fabric CI/CD 工作流](https://learn.microsoft.com/zh-cn/fabric/cicd/manage-deployment) 。
* 编程生成和编辑项定义 - 可以以编程方式生成和修改项定义文本文件，从而实现批处理操作，例如更新所有报表页视觉对象或向每个表添加一组度量值 。 对于语义模型，可以使用 [表格对象模型 (TOM)](https://learn.microsoft.com/zh-cn/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo) 客户端库来反序列化语义模型元数据，进行编程修改，并将其序列化回文件。

**启用预览功能**

“在 Power BI Desktop 中另存为 Power BI 项目”目前以预览版提供，你须在“预览功能”中启用它 。

转到“文件”>“选项和设置”>“选项”>“预览功能”，并勾选 Power BI 项目 (.pbip) 保存选项旁边的框 。

**另存为项目**

如果你正在处理新项目或打开了现有的 Power BI Desktop 文件（pbix），则可以将工作另存为 Power BI 项目文件（pbip）：

![](data:image/png;base64...)

另存为项目时，Power BI Desktop 会将报表和语义模型项另存为文件夹，每个文件夹都包含定义项目的文本文件：

|  |
| --- |
| Plaintext Project/ ├── AdventureWorks.Report/ ├── AdventureWorks.SemanticModel/ ├── .gitignore └── AdventureWorks.pbip |

让我们仔细看看项目根文件夹中显示的内容：

**<project name（项目名称）>.SemanticModel**

表示 Power BI 语义模型的文件和文件夹的集合。 要详细了解此处的文件和子文件夹，请参阅 [项目语义模型文件夹](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-dataset) 。

**<项目名称>。报告**

表示 Power BI 报表的文件和文件夹的集合。 要详细了解此处的文件、子文件夹和文件，请参阅 [项目报表文件夹](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-report) 。

**.gitIgnore**

为 Power BI 项目文件指定 Git 应该忽略的有意未跟踪文件，例如 cache.abf 和 localSettings.json。

仅当所选的保存文件夹或父 Git 存储库中尚不存在 [.gitignore](https://git-scm.com/docs/gitignore) 文件时，Power BI Desktop 才会创建该文件。

另存为 PBIP 时 .gitignore 的默认内容：

|  |
| --- |
| Plaintext \*\*/.pbi/localSettings.json \*\*/.pbi/cache.abf |

**<项目名称>.pbip**

PBIP 文件包含指向报表文件夹的指针，打开 PBIP 可打开目标报表和模型进行创作。

有关详细信息，请参阅 [pbip 架构文档](https://github.com/microsoft/json-schemas/tree/main/fabric/pbip/pbipProperties) 。

**打开 Power BI 项目**

可以打开报表文件夹中的 **pbip** 文件或 [**pbir**](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-report#definitionpbir) 文件，从而从 Power BI 项目文件夹中打开 Power BI Desktop。 这两个选项都可打开报表进行编辑，如果存在对语义模型的相对引用，请打开该语义模型。

可以将多个报表和语义模型保存到同一个文件夹中。 不需要为每个报表使用单独的 pbip 文件，因为可以直接从报表文件夹中的 **.pbir** 打开每个报表。

|  |
| --- |
| Plaintext project/ ├── AdventureWorks-Sales.Report/ │ └── definition.pbir ├── AdventureWorks-Stocks.Report/ │ └── definition.pbir ├── AdventureWorks.SemanticModel/ │ └── definition.pbism ├── .gitignore └── AdventureWorks.pbip |

**导航到文件**

保存为项目后，可以通过查看标题栏来查看项目的处理时间：

![](data:image/png;base64...)

如果选择标题栏，系统将显示特定于 Power BI 项目的浮出控件。 通过此浮出控件，可找到项目文件及报表和语义模型的显示名称设置。 还可以通过单击路径在文件资源管理器中打开文件夹。

![](data:image/png;base64...)

**Power BI Desktop 外部的更改**

另存为项目后，不必仅在 Power BI Desktop 中更改语义模型和报表定义。 可以使用其他工具，例如 VS Code、开源社区工具（例如表格编辑器），甚至是记事本。 但是，并非每个文件或更改都支持通过外部开源工具进行编辑。

在 Power BI Desktop 外部更改文件或属性可能会导致意外错误，甚至阻止打开 Power BI Desktop。 在这些情况下，必须先解决文件中的问题，然后才能尝试在 Power BI Desktop 中再次打开项目。

如果可能，Power BI Desktop 会指示错误的文件和位置：

![](data:image/png;base64...)

未记录以下文件的架构详细信息。 在 **预览** 期间，不支持在 Power BI Desktop 外部更改这些文件：

* 报表\
* [report.json](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-report#reportjson)
* [mobileState.json](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-report#mobilestatejson)
* [semanticModelDiagramLayout.json](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-report#semanticmodeldiagramlayoutjson)
* SemanticModel\
* [diagramLayout.json](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-dataset#diagramlayoutjson)

**部署到 Fabric 工作区**

使用 Power BI 项目文件时，可以使用以下发布机制将内容部署到 Fabric 工作区：

* 使用 [Fabric Git 集成](https://learn.microsoft.com/zh-cn/fabric/cicd/git-integration/intro-to-git-integration) 。
* 使用 [Fabric API](https://learn.microsoft.com/zh-cn/rest/api/fabric/articles/get-started/deploy-project) 。
* 使用 [Power BI Desktop 发布](https://learn.microsoft.com/zh-cn/power-bi/create-reports/desktop-upload-desktop-files) 选项。

备注

通过“ [Power BI Desktop 发布](https://learn.microsoft.com/zh-cn/power-bi/create-reports/desktop-upload-desktop-files) ”进行发布会使用一个发布到服务的临时 PBIX 文件，类似于保存和发布一个 PBIX 文件。 与其他仅部署元数据的 PBIP 部署选项不同，此发布方法会同时部署元数据和正在编辑的语义模型的 [本地数据缓存](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-dataset#pbicacheabf) 。

可通过两种方式使用外部工具更改语义模型定义：

* 通过使用 [外部工具](https://learn.microsoft.com/zh-cn/power-bi/transform-model/desktop-external-tools#data-modeling-operations) 连接到 Power BI Desktop 的 Analysis Service (AS) 实例。
* 通过使用 VS Code 或其他外部工具编辑文件夹中的 /definition TMDL 元数据。

所有语义模型元数据均可读取。 完全支持写入操作，但请注意，修改 Power BI Desktop 外部的元数据可能会导致意外行为，或者在极少数情况下，导致模型中出现不一致。 通过外部工具进行更改时，请谨慎使用。

请记住：

* 在 Power BI Desktop 外部对打开文件所做的任何更改都需要重启，以便这些更改显示在 Power BI Desktop 中。 Power BI Desktop 不知道其他工具对项目文件所做的更改。
* 不应使用外部工具更改由 Power BI Desktop 创建的自动日期表。
* 如果语义模型已启用 [自动日期/时间](https://learn.microsoft.com/zh-cn/power-bi/transform-model/desktop-auto-date-time) 功能，并且你在 Power BI Desktop 之外创建新的日期/时间列，则不会自动生成本地日期表。
* 语义模型（如 [复合模型](https://learn.microsoft.com/zh-cn/power-bi/transform-model/desktop-composite-models#composite-models-on-power-bi-semantic-models-and-analysis-services) 或 [Direct Lake](https://learn.microsoft.com/zh-cn/fabric/fundamentals/direct-lake-overview) ）可以包含从其他模型或数据源源的对象和属性。 自定义这些属性或删除同步的对象时，Power BI 需要设置 changedProperties 属性和 PBI\_RemovedChildren 批注。 这些指示器将更改标记为用户自定义项，确保在下次与数据源的架构同步期间保留这些更改。 若要了解详细信息，请参阅 [Power BI 语义模型的世系标记](https://learn.microsoft.com/zh-cn/analysis-services/tom/lineage-tags-for-power-bi-semantic-models) 。
* 应用这些更改时，在项目中的 Power BI Desktop 外部的任何表达式编辑 [unappliedChanges.json](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-dataset#pbiunappliedchangesjson) 都将丢失。

**JSON 文件架构**

大多数项目文件都包含 JSON 格式的元数据。 相应的 JSON 架构可用于验证和文档。

使用 JSON 架构，可以：

* 了解可配置属性。
* 使用代码编辑器提供的内联 JSON 验证。
* 通过语法突出显示、工具提示和自动完成改进创作。
* 使用外部工具了解项目元数据中受支持的属性。

使用 VS Code 将 JSON 架构映射到正在创作的文件。 项目文件的 JSON 架构在 [json 架构 Git 存储库](https://github.com/microsoft/json-schemas/tree/main/fabric) 中提供。

**注意事项和限制**

* Power BI Desktop 不知道对其他工具或应用程序所做的更改。 使用外部工具所做的更改要求先重启 Power BI Desktop，然后才能显示这些更改。
* Power BI 项目不支持敏感度标签。
* 在服务中编辑模型时，会忽略关系图视图。
* 保存 PBIP 时，请注意，默认情况下，Windows 上项目文件的最大路径长度限制为 260 个字符。 由于 PBIP 文件存储为子文件夹和文件，因此表名等长对象名称可能会导致总路径长度超过此限制，从而导致保存作期间出错。 若要缓解此风险，请使用短文件夹路径作为 PBIP 的根位置。
* 在 Power BI Desktop 中，无法直接将 PBIP 保存到 OneDrive 和 SharePoint。 可以使用 *“另存为”* 将文件保存到本地同步的 OneDrive 文件夹;但是，这可能会导致文件同步问题，这可能会导致 Power BI Desktop 中的保存作失败。
* 在 Power BI Desktop 外部编辑 PBIP 文件时，应使用 UTF-8 保存这些文件，而不使用 BOM 编码。
* Power BI 项目不支持报表语言架构（报表页同义词）。
* Power BI Desktop 使用 CRLF 作为行尾。 为了避免差异出现问题，请通过启用 [autocrlf](https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings) 将 Git 配置为处理行尾。
* 针对 Power BI 报表服务器优化的 Microsoft Power BI Desktop 版本中当前不支持 Power BI 项目。
* 无法使用 [Fabric REST API](https://learn.microsoft.com/zh-cn/rest/api/fabric/report/items) 获取和设置行级安全角色成员
* 无法使用 [Fabric REST API](https://learn.microsoft.com/zh-cn/power-bi/connect-data/incremental-refresh-overview) 获取和设置 [增量刷新](https://learn.microsoft.com/zh-cn/rest/api/fabric/report/items) 分区。 但是，它确实使用刷新策略中定义的查询导出单个分区。

**常见问题解答**

问：查看语义模型和报表项目文件夹定义时，发现只有少数文件标记为“必需”。如果删除它们会发生什么？

**答：** 另存为项目 (PBIP) 时，Power BI Desktop 会自动创建它们。

**问：** Power BI Desktop 是否知道我从外部工具或应用程序对 Power BI 项目文件所做的更改？

**答：** 否。 对文件所做的任何更改都需要重启 Power BI Desktop以反映这些更改。

**问：** 将 PBIX 转换为 PBIP 后，能否将其转换回 PBIX？

**答：** 是的。 可以将 PBIX 另存为 PBIP，也可以将 PBIP 另存为 PBIX。

**问：** 能否以编程方式将 PBIX 与 PBIP 相互转换？

**答：** 否。 只能使用 Power BI Desktop 的 **文件** > **另存为** 将 PBIX 与 PBIP 互相转换。

**问：** 能否将 Power BI Desktop 项目部署到Azure Analysis Services (AAS) 或 SQL Server Analysis Services (SSAS) ？

**答：** 否。 AAS 和 SSAS 中不支持 Power BI Desktop 项目报表定义。 模型定义使用 Power BI 特有的增强型元数据。 对于 AAS 和 SSAS 项目，请使用 Microsoft Visual Studio 进行模型创作、Git 和 Azure DevOps 集成。

问：当我将 Fabric 工作区连接到 Git 时，为什么没有 \*.pbip 文件？ 我可以如何在 Power BI Desktop 中编辑报表和语义模型？

答：PBIP 文件是可选的，只是用作报表文件夹的快捷方式。 你可以通过打开报表文件夹中的 definition.pbir 文件来打开报表和语义模型，以便在 Power BI Desktop 中编辑。

**相关内容**

* [Power BI Desktop 项目语义模型文件夹](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-dataset)
* [Power BI Desktop 项目报表文件夹](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-report)
* [Power BI Desktop 项目 Git 集成](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-git)
* [Power BI Desktop 项目与 Azure DevOps 的集成](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-git)
* [Power BI Desktop 中的外部工具](https://learn.microsoft.com/zh-cn/power-bi/transform-model/desktop-external-tools)