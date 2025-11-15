**Power BI Desktop 项目报表文件夹 - Power BI**

*🔗 原文链接：* [*https://learn.microsoft.com/zh-cn/p...*](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-report?tabs=v2%2Cdesktop)

*⏰ 剪存时间：2025-11-09 23:17:52 (UTC+8)*

*✂️ 本文档由* [*飞书剪存*](https://www.feishu.cn/hc/zh-CN/articles/606278856233?from=in_ccm_clip_doc) *一键生成*

重要

Power BI Desktop 项目目前为 **预览版** 。

本文介绍 Microsoft Power BI Desktop 项目的“ **报表** ”文件夹中的文件和子文件夹。 这里的文件和子文件夹代表 Power BI 报表。 根据项目不同，报表文件夹可以包括：

* .pbi\
* localSettings.json
* CustomVisuals\
* StaticResources\
* RegisteredResources\
* semanticModelDiagramLayout.json
* definition.pbir 1
* mobileState.json
* report.json 2
* definition\ 文件夹 3
* 平台

1 - 此文件是必需的。
2 - 保存为 PBIR-Legacy 格式时需要此文件。
3 - 保存为 PBIR 格式时需要此文件。

并非每个项目报表文件夹都包含文中介绍的所有文件和子文件夹。

**报表文件**

**.pbi\localSettings.json**

包含仅适用于当前用户和本地计算机的报表设置。 应包含在 gitIgnore 或其他源代码管理排除中。 默认情况下，Git 会忽略此文件。

有关详细信息，请参阅 [localSettings.json 架构文档](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/localSettings) 。

**CustomVisuals\**

该子文件夹包含报表中的自定义视觉对象的元数据。 Power BI 支持三种类型的自定义视觉对象：

* 组织存储视觉对象 - 组织可以批准自定义视觉对象并将其部署到组织的 Power BI。 若要了解详细信息，请参阅 [组织存储](https://learn.microsoft.com/zh-cn/power-bi/developer/visuals/power-bi-custom-visuals#organizational-store) 。
* AppSource Power BI 视觉对象 - 也称为“公共自定义视觉对象”。 这些视觉对象可从 Microsoft AppSource 中获取。 报表开发人员可以直接从 Power BI Desktop 安装这些视觉对象。
* 自定义视觉对象文件 - 也称为“专用自定义视觉对象”。 可以通过上传 pbiviz 包将文件加载到报表中。

只有专用自定义视觉对象才会加载到 CustomVisuals 文件夹中。 AppSource 和组织视觉对象将通过 Power BI Desktop 自动加载。

**RegisteredResources\**

该子文件夹包含特定于报表并由用户加载的资源文件，例如自定义主题、图像和自定义视觉对象（pbiviz 文件）。

开发人员负责管理此处的文件，并且支持更改。 例如，你可以更改文件，当 Power BI Desktop 重启后，新文件将加载到报表中。 此文件夹可以取消阻止一些有用的方案，例如：

* 使用公共架构在 Power BI Desktop 外部创作自定义主题。
* 通过更改多个报表上的资源文件来应用批量更改。 例如，可以切换公司的自定义主题、在浅色和深色主题之间更改，以及更改徽标图像。

每个资源文件都必须在 report.json 文件中有一个对应的条目，在 **预览** 期间，report.json 文件不支持编辑。 只有导致 Power BI Desktop 在 report.json 中注册资源的已加载资源才支持编辑 RegisteredResources 文件。

**semanticModelDiagramLayout.json**

包含数据模型关系图，它描述了与报表关联的语义模型的结构。 **预览** 期间，此文件不支持外部编辑。

**definition.pbir**

包含报表和核心设置的总体定义。 此文件还包含对报表使用的语义模型的引用。 Power BI Desktop 可以直接打开 PBIR 文件，就像从 PBIP 文件打开报表一样。 打开 PBIR 文件时，如果存在相对引用 byPath ，会同时打开语义模型。

示例 definition.pbir：

|  |
| --- |
| Plaintext {   "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",  "version": "4.0",  "datasetReference": {  "byPath": {  "path": "../Sales.Dataset"  }   } } |

定义包括 datasetReference 属性，该属性引用报表中使用的语义模型。 引用可以是：

byPath - 指定目标语义模型文件夹的相对路径。 不支持绝对路径。 使用正斜杠 (/) 作为文件夹分隔符。 使用时，Power BI Desktop 还会在完全编辑模式下打开语义模型。

byConnection - 使用连接字符串指定与 Fabric 工作区中的语义模型的连接。 使用 byConnection 引用时，Power BI Desktop 不会在编辑模式下打开语义模型。

* 第 2 版
* 版本 1

使用 byConnection 引用时，必须指定以下属性：

|  |  |
| --- | --- |
| properties | 说明 |
| connectionString | 引用 Fabric 工作区中的语义模型的连接字符串。 |

使用 byConnection 的示例：

|  |
| --- |
| Plaintext {   "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",  "version": "4.0",  "datasetReference": {  "byConnection": {   "connectionString": "Data Source=\"powerbi://api.powerbi.com/v1.0/myorg/[WorkpaceName]\";initial catalog=[SemanticModelName];access mode=readonly;integrated security=ClaimsToken;semanticmodelid=[SemanticModelId]"  }  } } |

通过 [Fabric REST API](https://learn.microsoft.com/zh-cn/rest/api/fabric/report/items) 部署报表时，只需指定 semanticmodelid 属性。 例如：

|  |
| --- |
| Plaintext {   "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",  "version": "4.0",  "datasetReference": {  "byConnection": {   "connectionString": "semanticmodelid=[SemanticModelId]"  }  } } |

重要

通过 [Fabric REST API](https://learn.microsoft.com/zh-cn/rest/api/fabric/report/items) 部署报表时，必须使用 byConnection 引用。 这不应与语义模型的 [存储模式](https://learn.microsoft.com/zh-cn/power-bi/transform-model/desktop-storage-mode) （如 DirectQuery）混淆。 报表 datasetReference 中仅指定报表连接到的语义模型，它不定义该模型如何存储或访问其数据。

**多个 \*.pbir 文件**

当语义模型和报表共享同一工作区时， [Fabric Git Integration](https://learn.microsoft.com/zh-cn/fabric/cicd/git-integration/intro-to-git-integration) 始终使用 byPath 对语义模型的引用导出定义。 如果需要强制报表在实时连接中打开（例如在使用报表级度量值时），可以设置多个 definition\*.pbir 文件，例如一个文件有 byPath 连接，另一个有 byConnection 连接。 Fabric Git 集成仅处理 *definition.pbir* 文件，并忽略所有其他 \*.pbir 文件。 但是，这些文件可以共存在同一存储库中。

|  |
| --- |
| Plaintext  ├── definition\  ├── StaticResources\  ├── .platform  ├── definition-liveConnect.pbir  └── definition.pbir |

该文件 definition.pbir 还通过“version”属性指定支持的报表定义格式。

|  |  |
| --- | --- |
| 版本 | 支持的格式 |
| 1.0 | 报表定义必须以 PBIR-Legacy 格式存储在 report.json 文件中。 |
| 4.0 或更高版本 | 报表定义可以存储为 PBIR-Legacy（report.json 文件）或 PBIR （\definition 文件夹）。 |

有关详细信息，请参阅 [definition.pbir 架构文档](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definitionProperties) 。

**mobileState.json**

包含在移动设备上呈现时的报表外观和行为设置。 此文件不支持外部编辑。

**report.json**

此文件包含采用 Power BI 报表旧版格式 (PBIR-Legacy) 的报表定义，不支持外部编辑。

**definition\ 文件夹**

仅当 Power BI 项目使用 Power BI 增强型报表格式 (PBIR) 保存时，此文件夹才可用。 它将替换 report.json 文件。

**平台中添加用户。**

Fabric 平台文件，其中包含对于建立和维护 Fabric 项目与 Git 之间的连接至关重要的属性。

若要了解详细信息，请参阅 [Git 集成自动生成的系统文件](https://learn.microsoft.com/zh-cn/fabric/cicd/git-integration/source-code-format#automatically-generated-system-files) 。

**PBIR 格式**

使用 Power BI 增强型报表格式 (PBIR) 保存 Power BI 项目文件 (PBIP) 可通过使用格式正确的 JSON 文件极大地改进更改跟踪和合并冲突解决。

![](data:image/png;base64...)

每个页面、视觉对象、书签等组织到文件夹结构中的单独文件中。 此格式非常适合协同开发中的冲突解决。

![](data:image/png;base64...)

与 PBIR-Legacy (report.json) 不同，PBIR 是一种公开记录的格式，支持非 Power BI 应用程序的修改。 每个文件都有一个公共 JSON 架构，它不仅可以记录文件，还可以让代码编辑器（例如 Visual Studio Code）在编辑时执行语法验证。

目前可以使用 PBIR 的一些应用场景包括：

* 在报表之间复制页面/视觉对象/书签。
* 通过复制和粘贴视觉对象文件，确保所有页面的一组视觉对象的一致性。
* 在多个报表文件中轻松查找和替换。
* 使用脚本对所有视觉对象进行批量编辑（例如，隐藏视觉对象级别筛选器）

**启用 PBIR 格式预览功能**

目前，使用 PBIR 进行 Power BI 报表保存的功能正在预览阶段。 在使用它之前，必须先在 Power BI Desktop 预览功能中启用它：

对于 Power BI 项目（PBIP）文件：

1. 转到 **“文件 > 选项和设置 > 选项 > 预览功能”** 。
2. 选中 **“使用增强的元数据格式（PBIR）存储报表”** 复选框。

对于 PBIX 文件：

1. 转到 **“文件 > 选项和设置 > 选项 > 预览功能”** 。
2. 选中 **存储 PBIR 报表使用增强元数据格式 (PBIR)** 的复选框。

为 PBIX 启用 PBIR 可确保 PBIR 格式也保存在 PBIX 文件中，而不仅仅是在 Power BI 项目 （PBIP） 文件中保存。

**使用 PBIR 另存为项目**

启用 PBIR 预览功能后，保存项目时，报表将保存在 *报表文件夹* 中名为 \definition 的文件夹中 ：

![](data:image/png;base64...)

详细了解 PBIR 文件夹结构 。

**将现有报表转换为 PBIR**

如果已有使用 PBIR-Legacy 格式的 PBIP，则可将其转换为 PBIR，如下所示：

1. 在 Power BI Desktop 中打开 PBIP。
2. 确保已启用该预览功能。
3. 保存该项目。 出现提示，要求你升级到 PBIR。
4. 选择“升级”。

![](data:image/png;base64...)

1. 重要
2. 升级到 PBIR 后，无法从 UI 还原为 PBIR-Legacy。 若要还原为 PBIR-Legacy，请保存 PBIP 文件的副本。
3. 在升级到 PBIR 之前，Power BI Desktop 会自动创建报表的备份。 此备份在以下位置之一中保留 30 天：

* Microsoft应用商店版本： %USERPROFILE%\Microsoft\Power BI Desktop Store App\TempSaves\Backups
* 可执行安装程序版本： %USERPROFILE%\AppData\Local\Microsoft\Power BI Desktop\TempSaves\Backups

现有的 PBIR-Legacy 文件 (report.json) 将替换为包含报表 PBIR 表示形式的 \definition 文件夹 。

如果选择 **“保留当前** 格式”，桌面不会再次提示升级。

**PBIR 文件夹和文件**

报表定义存储在具有以下结构的 definition\ 文件夹中：

|  |
| --- |
| Plaintext ├── bookmarks\ │ ├── [bookmarkName].bookmark.json | └── bookmarks.json ├── pages\ │ ├── [pageName]\ │ | ├── \visuals | │ | ├── [visualName]\ | | │ │ |── mobile.json | | | └ └── visual.json | | └── page.json | └── pages.json ├── version.json ├── reportExtensions.json └── report.json |

|  |  |  |
| --- | --- | --- |
| 文件/文件夹 | 必须 | 说明 |
| 书签\ | 否 | 包含报表的所有书签文件的文件夹。 |
| • [bookmarkName].bookmark.json | 否 | 书签元数据，例如目标视觉对象和筛选器。 有关详细信息，请参阅 [架构](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition/bookmark) 。 |
| bookmarks.json | 否 | 书签元数据，例如书签顺序和组。 有关详细信息，请参阅 [架构](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition/bookmarksMetadata) 。 |
| 页面\ | 是 | 包含报表的所有页面的文件夹。 |
| ── [pageName] | 是 | 每页一个文件夹。 |
| 视觉内容 | 否 | 包含页面的所有视觉对象的文件夹。 |
| ────── [visualName]\ | 否 | 每个视觉对象一个文件夹。 |
| ──────── mobile.json | 否 | 视觉对象移动布局元数据，例如移动位置和格式设置。 有关详细信息，请参阅 [架构](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition/visualContainerMobileState) 。 |
| ─────── visual.json | 是 | 视觉对象元数据，例如位置和格式、查询。 有关详细信息，请参阅 [架构](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition/visualContainer) 。 |
| page.json | 是 | 页面元数据，例如页面级别筛选器和格式设置。 有关详细信息，请参阅 [架构](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition/page) 。 |
| pages.json | 否 | 页面元数据，例如页面顺序和活动页。 有关详细信息，请参阅 [架构](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition/pagesMetadata) 。 |
| version.json | 是 | PBIR 文件版本以及其他因素决定了要加载的必需文件。 有关详细信息，请参阅 [架构](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition/versionMetadata) |
| reportExtensions.json | 否 | 报表扩展，例如报表级别度量值。 有关详细信息，请参阅 [架构](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition/reportExtension) |
| report.json | 是 | 报表元数据，例如报表级别筛选器和格式设置。 有关详细信息，请参阅 [架构](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition/report) |

重要

某些报表元数据文件（如 visual.json 或 bookmarks.json）可以使用语义模型中的数据值进行保存。 例如，如果将筛选器应用于字段“Company”= “Contoso”的视觉对象，则值“Contoso”将保留为元数据的一部分。 这也适用于其他配置，例如切片器选择、矩阵自定义列宽度和特定系列的格式设置。

**PBIR 命名约定**

上表中方括号（[]）中的所有名称都遵循默认命名约定，但可以重命名为更易用的名称。 默认情况下，页面、视觉对象和书签使用其报表对象名称作为其文件或文件夹名称。 这些对象名称最初是一个 20 个字符的唯一标识符，例如“90c2e07d8e84e7d5c026”。

![](data:image/png;base64...)

支持重命名每个 JSON 文件中的“name”属性，但可能会破坏报表内外的外部引用。 对象名称和/或文件/文件夹名称必须包含一个或多个单词字符（字母、数字、下划线）或连字符。

重命名任何 PBIR 文件或文件夹后，必须重启 Power BI Desktop。 重启后，Power BI Desktop 将在保存时保留原始文件或文件夹名称。

**复制报表对象名称**

报表中的每个对象都保存在单独的文件夹或文件中，但文件夹的名称并不总是显而易见的。 为方便起见，可以直接将任何报表对象名称（包括页面、视觉对象、书签和筛选器）的名称从 Power BI 复制到剪贴板。

![](data:image/png;base64...)

* 从桌面
* 从服务中

1. 转到 **“文件>选项”和“设置报表设置>>”报表对象** “， *并在右键单击报表对象设置时启用”复制对象名称* ”。 此操作仅需执行一次。

![](data:image/png;base64...)

1. 右键单击任何报表对象，然后选择 *“复制对象名称* ”。

![](data:image/png;base64...)

将对象名称复制到剪贴板后，可以轻松地将其输入到 Windows 资源管理器或 Visual Studio Code 的搜索栏中，以查找或标识 PBIR 文件夹中的对象名称。

![](data:image/png;base64...)

**PBIR Json 架构**

每个 PBIR JSON 文件都包含文档顶部的 [JSON 架构](https://json-schema.org/) 声明。 此架构 URL 可公开访问，可用于详细了解每个文件的可用属性和对象。 此外，它还在使用 [Visual Studio Code](https://code.visualstudio.com/) 等代码编辑器进行编辑时提供内置的 IntelliSense 和验证。

![](data:image/png;base64...)

架构 URL 还定义了文档的版本，该版本预计会随着报表定义的发展而变化。

所有 JSON 架构均在 [此处](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition) 发布。

**PBIR 批注**

可以将批注作为名称/值对包含在每个 visual 报表定义中， page 以及 report 。 虽然 Power BI Desktop 忽略这些批注，但它们对于外部应用程序（如脚本）非常有用。

例如，可以为文件中的报表 report.json 指定 defaultPage，然后部署脚本就可以利用它。

|  |
| --- |
| Plaintext {  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",  "themeCollection": {  "baseTheme": {  "name": "CY24SU06",  "reportVersionAtImport": "5.55",  "type": "SharedResources"  }  },  ...  "annotations": [  {  "name": "defaultPage",  "value": "c2d9b4b1487b2eb30e98"  }  ] } |

**对 PBIR 文件的外部更改**

可以使用代码编辑器（例如 [Visual Studio Code](https://code.visualstudio.com/) 或外部工具）编辑 PBIR JSON 文件，只要该文件遵循 JSON 架构。 可以直接在 Visual Studio Code 中轻松检测到使用错误的属性名称或类型：

![](data:image/png;base64...)

对 PBIR 内容的外部更改可能会导致在 Power BI Desktop 中重新打开文件时出现错误。 这些错误可以是两种类型：

“阻止错误”阻止 Power BI Desktop 打开报表 。 这些错误有助于识别问题以及重新打开之前必须修复的问题文件：

![](data:image/png;base64...)

无效架构或缺少必需的属性等错误被视为阻止错误。 通过在 Visual Studio Code 中打开文件并检查架构错误，可以轻松识别这些错误。

“非阻止错误”不会阻止 Power BI Desktop 打开报表并自动解决 。

![](data:image/png;base64...)

无效 activePageName 配置等错误是可以自动修复的非阻止错误的示例 。 警告很有必要，可让你有机会避免使用自动修复保存报表，从而防止任何潜在的工作损失。

**常见 PBIR 错误**

**场景：** *重命名视觉对象或页面文件夹名称后，打开报表时不再显示视觉对象或页面。*

解决方案：验证名称是否符合 **命名约定**  。 如果不符合，Power BI Desktop 将忽略文件或文件夹，并将其视为专用用户文件。

**场景：** *新报表对象的名称与其他报表对象不同。例如，大多数页面文件夹都名为“ReportSection0e71dafbc949c0853608”，而少数文件夹名为“1b3c2ab12b603618070b”。*

解决方案：PBIR 为每个对象采用了新的 **命名约定** ，但它仅适用于新对象 。 将现有报表保存为 PBIP 时，必须保留当前名称以防止中断引用。 如果需要保持一致性，则允许使用脚本批量重命名。

**场景：** *我复制了书签文件，保存后，删除了大部分书签配置。*

解决方案：此行为是故意如此，报表书签捕获报表页的状态及其所有视觉对象 。 由于捕获的状态源自具有不同视觉对象的另一个报表页，因此任何无效的视觉对象都会从书签配置中删除。 如果还复制依赖视觉对象和页面，书签将维护其配置。

**场景：** *我从另一个报表复制了一个页面文件夹，并遇到一个错误，指出“'pageBinding.name'属性的值必须是唯一的。*

解决方案：要支持钻取和页面工具提示，必须具有 pageBinding 对象。 由于它们可能由其他页面引用，因此名称在报表中必须是唯一的。 在新复制的页面上，分配一个唯一值来解决错误。 2024 年 6 月之后，这种情况不再是问题，因为 pageBinding 名称将默认是 GUID。

**PBIR 注意事项和限制**

PBIR 当前处于预览状态。 请记住以下几点：

* 包含 500 多个文件的大型报表可能会遇到创作性能问题（报表查看不受影响）。
* 将报表从 PBIR-Legacy 转换为 PBIR 后，无法回滚。 虽然备份是在转换时创建的。
* 使用“另存为”功能将 PBIP 文件转换为 PBIX 文件会将 PBIR 报表嵌入 PBIX 文件中，并将所有 PBIR 限制都传递给 PBIX。
* 只有在编辑报表时筛选器窗格至少展开一次后， [视觉自动筛选器](https://learn.microsoft.com/zh-cn/power-bi/create-reports/power-bi-report-filter-types#automatic-filters) 才会保存到 PBIR visual.json 文件中。

服务强制实施的 PBIR 大小限制：

* 每个报表最多 1,000 页。
* 每个页面的最大视觉对象数为 1000。
* 每个报表最多 1,000 个资源包文件。
* 所有资源包文件的最大大小为 300 mb。
* 所有报表文件的最大大小为 300 mb。

[Fabric Git 集成](https://learn.microsoft.com/zh-cn/fabric/cicd/git-integration/intro-to-git-integration) 和 [Fabric REST API](https://learn.microsoft.com/zh-cn/rest/api/fabric/articles/item-management/item-management-overview) 使用服务中当前应用的格式导出报表。 如果使用 PBIR 格式创建或导入到 Fabric 中的报表，则会以 PBIR 格式导出报表。 同样，如果报表为 PBIR-Legacy，则会以 PBIR-Legacy 格式导出报表。

**相关内容**

* [Power BI Desktop 项目语义模型文件夹](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-dataset)
* [Power BI Desktop 项目](https://learn.microsoft.com/zh-cn/power-bi/developer/projects/projects-overview)