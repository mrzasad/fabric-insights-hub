# 🚀 Fabric Insights Hub

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Azure](https://img.shields.io/badge/Azure-Integrated-blue.svg)
![Fabric](https://img.shields.io/badge/MS_Fabric-Compatible-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**Advanced analytics portal for Microsoft Fabric - Semantic model exploration, anomaly detection, and operational monitoring powered by Streamlit**

[Features](#-features) • [Quick Start](#-quick-start) • [Examples](#-examples) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

Fabric Insights Hub is a Streamlit-powered analytics portal that bridges the gap between Microsoft Fabric's powerful backend and user-friendly data exploration. It provides an intuitive interface for:



## ✨ Features

### 🔍 **Workspace Explorer**
- Automatically discover all accessible Fabric workspaces
- Browse semantic models and their underlying tables
- View metadata including configuration details and refresh history

### 📊 **Interactive Analytics**
- Execute DAX queries against semantic models
- Real-time data visualization with Plotly
- Customizable dashboards with filtering capabilities
- Export results to CSV for further analysis

### 🧠 **Anomaly Detection**
- Statistical outlier detection using IQR method
- Anomaly scoring and visualization
- Anomalous records log with detailed insights
- Configurable sensitivity thresholds

### ⚡ **Operational Management**
- Trigger semantic model refreshes
- Monitor refresh history and status
- Track processing performance metrics
- Automated health checks

### 👥 **Customer Analytics**
- Customer segmentation analysis
- Lifetime value distribution
- Regional performance metrics
- Segment comparison tools

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Microsoft Fabric workspace (for live connection)
- Azure Service Principal (for live connection)
- Git (for cloning)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fabric-insights-hub.git
cd fabric-insights-hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

- **Data Teams** to discover and explore semantic models
- **Analysts** to run advanced statistical analysis
- **Operations** to monitor and manage data refreshes
- **Business Users** to visualize insights without writing code

### Architecture
