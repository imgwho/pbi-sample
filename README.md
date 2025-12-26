# Tableau to Power BI Conversion Showcase

## Introduction

This repository serves as a practical guide and a collection of examples for migrating dashboards from Tableau to Power BI. It focuses on a developer-oriented approach, leveraging the modern Power BI Project (PBIP) format, which facilitates version control, collaboration, and programmatic manipulation.

This project is designed for developers and data analysts looking for a comprehensive reference on migrating from Tableau to Power BI, complete with technical details and best practices.

## Core Case Studies

This project features two main conversion examples:

### 1. Superstore Sales Dashboard

-   **Source**: `Superstore.twb` (Tableau Workbook)
-   **Result**: `superstore dashboard.pbip` (Power BI Project)
-   **Description**: A classic sales analytics dashboard covering common visualization types like KPIs, trend analysis, and geographical maps.

### 2. Fitcheck Application Overview

-   **Source**: `Fitcheck OVERVIEW.twb` (Tableau Workbook)
-   **Result**: `pbi fitcheck ver2.0.pbip` (Power BI Project)
-   **Description**: A business application monitoring dashboard that demonstrates the migration of business metrics from Tableau to Power BI.
-   **Alternative Version**: The repository also includes a Python-based web dashboard of the same subject built with Streamlit (`fitcheck_streamlit_dashboard`), providing a comparison across different technology stacks.

## Repository Structure

```
/
├── *.twb                            # Original Tableau Workbooks
├── *.pbip                           # Converted Power BI Project files
├── *.Report/                        # Power BI report definition folder (source-controllable)
│   └── definition.pbir
├── *.SemanticModel/                 # Power BI semantic model folder (source-controllable)
│   └── definition.pbism
├── docs/                            # Technical documentation (PBIP, TMDL)
├── comparison_analysis.md           # Comparative analysis between Tableau and Power BI
├── Tableau_to_PowerBI_Conversion_Guide.md # Official conversion guide
└── ppt/                             # Presentation slides for technical sharing (Slidev)
```

-   **`*.pbip`**: The Power BI Project file. This is central to modern Power BI development, as it decouples the report and data model into separate, human-readable folders (`.Report` and `.SemanticModel`), making it ideal for version control systems like Git.
-   **`.Report` & `.SemanticModel` Folders**: These directories contain the "source code" of the PBIP project. The report layout and visuals are defined in `report.json`, while the data model is described using the Tabular Model Definition Language (TMDL). Editing these text-based files allows for managing Power BI reports as code (Infrastructure as Code).
-   **`docs/`**: Contains official technical documentation on PBIP and TMDL, which are essential references for understanding and implementing code-based Power BI development.
-   **Markdown Guides**: The `comparison_analysis.md` and other guides document the challenges, feature differences, and best practices encountered during the migration process.

## How to Use

1.  **Prerequisites**:
    -   Install the latest version of **Power BI Desktop**.
    -   In Power BI Desktop, go to `File > Options and settings > Options > Preview features` and ensure that **"Power BI Project (.pbip) save option"** is enabled.

2.  **Explore the Reports**:
    -   Open the `.pbip` files (e.g., `superstore dashboard.pbip`) directly with Power BI Desktop to view and interact with the converted reports.

3.  **Inspect the Project Source**:
    -   Open the repository in a code editor like VS Code.
    -   Examine the contents of the `*.Report/definition.pbir` file and the `.tmdl` files within the `*.SemanticModel` folder. These are the "source code" for the Power BI report and its data model.

4.  **Learn from the Migration Experience**:
    -   Read `comparison_analysis.md` and `Tableau_to_PowerBI_Conversion_Guide.md` to gain insights into the key decisions and technical details of the migration process.

---

## 中文版

# Tableau 到 Power BI 转换实践项目

## 简介

本项目是一个关于如何将 Tableau 看板（Dashboard）迁移到 Power BI 的实践指南和示例集合。它专注于面向开发人员的方法，利用现代的 Power BI 项目（PBIP）格式，该格式极大地便利了版本控制、团队协作和代码化操作。

本项目旨在为希望从 Tableau 迁移到 Power BI 的开发者和数据分析师提供一套完整的参考资料，包含技术细节与最佳实践。

## 核心案例

本项目包含两个核心的转换案例：

### 1. Superstore 销售仪表板

-   **原始文件**: `Superstore.twb` (Tableau 工作簿)
-   **转换后**: `superstore dashboard.pbip` (Power BI 项目)
-   **简要说明**: 这是一个经典的销售分析案例，涵盖了 KPI、趋势分析、地理分布图等多种常见的可视化类型。

### 2. Fitcheck 应用概览

-   **原始文件**: `Fitcheck OVERVIEW.twb` (Tableau 工作簿)
-   **转换后**: `pbi fitcheck ver2.0.pbip` (Power BI 项目)
-   **简要说明**: 这是一个业务应用监控仪表板，展示了如何将业务指标从 Tableau 迁移到 Power BI。
-   **其他版本**: 项目中还包含一个用 Python Streamlit 构建的相同主题的 Web 仪表板 (`fitcheck_streamlit_dashboard`)，可用于对比不同技术栈的实现。

## 仓库结构

```
/
├── *.twb                            # 原始 Tableau 工作簿
├── *.pbip                           # 转换后的 Power BI 项目文件
├── *.Report/                        # Power BI 报表定义文件夹 (可进行版本控制)
│   └── definition.pbir
├── *.SemanticModel/                 # Power BI 数据模型文件夹 (可进行版本控制)
│   └── definition.pbism
├── docs/                            # Power BI 技术文档 (PBIP, TMDL)
├── comparison_analysis.md           # Tableau 与 Power BI 对比分析
├── Tableau_to_PowerBI_Conversion_Guide.md # 官方转换指南
└── ppt/                             # 用于技术分享的演示文稿 (Slidev)
```

-   **`*.pbip`**: Power BI 项目文件。这是现代 Power BI 开发的核心，它将报表和数据模型分解为单独的、人类可读的文件夹（`.Report` 和 `.SemanticModel`），极大地便利了 Git 等版本控制系统。
-   **`.Report` 和 `.SemanticModel` 文件夹**: 这些是 `.pbip` 项目的“源代码”。其中，报表的布局、视觉对象等被定义在 `report.json` 中，而数据模型则使用表格模型定义语言 (TMDL) 进行描述。通过直接编辑这些文本文件，可以实现对 Power BI 报表的代码化管理 (Infrastructure as Code)。
-   **`docs/`**: 包含了关于 PBIP 和 TMDL 的官方技术文档，是理解和实践代码化 Power BI 开发的重要参考。
-   **Markdown 指南**: `comparison_analysis.md` 等文件记录了在转换过程中遇到的挑战、两种工具的功能差异以及迁移的最佳实践。

## 如何使用

1.  **环境准备**:
    -   安装最新版本的 **Power BI Desktop**。
    -   在 Power BI Desktop 的 `文件 > 选项和设置 > 选项 > 预览功能` 中，确保 **"Power BI Project (.pbip) 保存选项"** 已被勾选。

2.  **浏览报表**:
    -   直接使用 Power BI Desktop 打开根目录下的 `.pbip` 文件（如 `superstore dashboard.pbip`）即可查看和交互转换后的报表。

3.  **研究项目源码**:
    -   使用 VS Code 等代码编辑器打开项目文件夹。
    -   重点关注 `*.Report/definition.pbir` 文件和 `*.SemanticModel` 文件夹内的 `.tmdl` 文件。这些是 Power BI 报表和数据模型的“源代码”。

4.  **学习迁移经验**:
    -   阅读根目录下的 `comparison_analysis.md` 和 `Tableau_to_PowerBI_Conversion_Guide.md`，以深入了解迁移过程中的关键决策和技术细节。

