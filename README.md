
![Aether Logo](https://github.com/ONGQ0019/filedumps/blob/main/Aether6.png?raw=true)
![GitHub release (latest by date)](https://img.shields.io/badge/release-v1.0-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/M1-Private-Limited/AETHER)
![GitHub](https://img.shields.io/github/license/M1-Private-Limited/AETHER)
![GitHub contributors](https://img.shields.io/github/contributors/M1-Private-Limited/AETHER)
![GitHub stars](https://img.shields.io/github/stars/M1-Private-Limited/AETHER?style=social)

Aether is a powerful Streamlit application designed to elevate your data insights to celestial heights. 


## 🚀 Features

- **AI-Powered Insights**: Leverage Azure OpenAI to generate marketing ideas, intelligent data segments and complex visualizations instantly.
- **Multi-Source Integration**: Connect seamlessly to Tableau, local storage, Azure Blob Storage, and Databricks' DBFS for flexible data management.
- **Dynamic Dashboards**: Create and view real-time, customizable dashboards built with Streamlit Elements and Nivo charts to effortlessly track trends.
- **In-platform Filtering**: Apply categorical, numerical, and date filters to refine datasets for targeted analysis.
- **Data Profiling**: Instantly generate detailed profiles with key statistics for quick decision-making.
- **AI-Driven Segmentation**: Automatically create valuable data segments based on intelligent groupings and breakpoints.
- **AI Chart Generation**: Produce diverse visualizations, from simple bar charts to complex animated race charts, with a single click.
- **Easy Report Generation**: Export your analysis and charts into a downloadable PDF with a single click.
- **User-Friendly UI**: Intuitive design for seamless navigation and analysis built with Shadcn.
- **AI Chat**: Interact with AI agents to gain insights from your data or external web in real time.

## 🎥 Promo Video

https://github.com/user-attachments/assets/36a4b863-7245-4183-9aa5-bb05dcb025f5


## ▶️ Demo

[![Demo Video](https://github.com/ONGQ0019/filedumps/blob/main/aether_demo.png?raw=true)](https://www.youtube.com/watch?v=cVjDr3Uhmhc)

## Aether: Your All-in-One Solution for Ideation, Segmentation, and Visualization

Here’s why Aether stands out:

### 1. Comprehensive Ideation
- **AI-Powered Insights**: Harness the capabilities of Azure OpenAI to generate innovative marketing ideas, intelligent data segments, and complex visualizations instantly.
- **AI Chat**: Interact with AI agents to gain real-time insights from your data and external web sources, fueling your creative and strategic thinking.

### 2. Advanced Segmentation
- **AI-Driven Segmentation**: Automatically create valuable data segments through intelligent groupings and breakpoints, enabling targeted analysis and personalized strategies.
- **In-Platform Filtering**: Easily apply categorical, numerical, and date filters to refine datasets, ensuring precise and relevant data exploration.

### 3. Dynamic Visualization
- **Easy Chart Generation**: Produce a wide range of visualizations, from simple bar charts to intricate animated race charts, with just a single click—no technical knowledge required.
- **Customizable Dashboards**: Build and view real-time dashboards using Streamlit Elements and Nivo charts, allowing you to effortlessly track trends and monitor key metrics.

### User-Friendly Experience
- **Intuitive Interface**: Aether’s user-centric design, built with Shadcn, ensures seamless navigation and effortless data analysis.
- **Multi-Source Integration**: Connect effortlessly to Tableau, local storage, Azure Blob Storage, and Databricks' DBFS, providing flexible and robust data management.
- **Data Profiling**: Instantly generate detailed data profiles with key statistics and dictionaries, facilitating quick and informed decision-making.

### Efficiency and Productivity
- **Consolidated Activities**: Track and consolidate all your activities on the platform, making it easy to manage your workflow.
- **Easy Report Generation**: Export your analyses and visualizations into downloadable PDFs with a single click, streamlining your reporting process.

### Benefits at a Glance
- **Time-Saving**: Streamline your data analysis and visualization processes, allowing you to focus on what matters most.
- **Enhanced Insights**: Gain deeper and more actionable insights quickly, driving better business decisions.
- **Creative Freedom**: Generate new ideas and conduct comprehensive data analyses without needing technical expertise.
- **Versatile Visualizations**: Create a variety of visual representations to suit your unique data storytelling needs.

Aether is designed to make data analysis accessible, insightful, and efficient for everyone. Whether you’re brainstorming new marketing strategies, segmenting your audience, or visualizing complex data, Aether provides the tools you need—all in a single, user-friendly platform.



## 🛠 Installation

### Prerequisites

- Python 3.9 or higher
- Azure OpenAI account
- Serpapi (Optional)

### Clone the Repository

```bash
git clone https://github.com/M1-Private-Limited/AETHER.git
cd aether
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔧 Configuration

### Set Up Environment Variables

Create a `.env` file in the root directory and add your Azure OpenAI credentials:

```env
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-azure-openai-endpoint/
```


### Update Environment Variables in Code

Ensure that your application reads from the `.env` file. You can use the `dotenv` package for this purpose.

```python
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
```

## 🏃‍♂️ Usage

### Run the Streamlit App

```bash
streamlit run app.py
```

### Application Overview

- **Datasource Tab**: Connect to various data sources like Tableau, Snowflake, or Databricks. Upload your CSV files or select pre-defined datasources.
- **Dashboard Tab**: View and interact with your data through custom dashboards, dictionaries, analytics, segments, and charts.
- **Chat Tab**: Engage with the AI to ask questions and get insights based on your data.

## 📂 Project Structure

```
aether/
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── app.py
├── fdf.py
├── ploty.py
├── requirements.txt
├── style.css
├── assets/
│ ├── DINRoundPro-Black.woff2
│ ├── loading.json
│ ├── m1logo.png
│ ├── m1plan.txt
│ ├── particles.html
│ ├── promo_video.mp4
│ ├── singapore_districts.geojson
│ └── testingcsv.csv


```

## 🔍 Technologies Used

- [Streamlit](https://streamlit.io/) - The app framework
- [Azure OpenAI](https://azure.microsoft.com/en-us/services/openai-service/) - GPT-4o LLM of Choice
- [Plotly](https://plotly.com/python/) - Interactive visualizations
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [Tableau Server Client](https://tableau.github.io/server-client-python/docs/) - Tableau API integration
- [Streamlit Elements](https://github.com/okld/streamlit-elements) - Enable Nivo animated charts in Streamlit
- [ShadCN UI](https://github.com/shadcn/ui) - TypeScript UI components for Streamlit
- [Pygwalker](https://github.com/KamandPrompt/pygwalker) - Advanced data visualization
- [SerpApi](https://serpapi.com/) - Providing web search capability
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html) - Connection to DBFS
- [Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html) - Connection to Snowflake
- [streamlit-lottie](https://github.com/andfanilo/streamlit-lottie) - Loading animations

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Inspired by the need for advanced AI-driven data analytics tools.
- Thanks to the open-source community for providing the tools and libraries that make Aether possible.

---

> **Disclaimer:** Ensure that you handle sensitive information like API keys securely. Do not expose them in your codebase or public repositories.
