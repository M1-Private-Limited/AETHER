
![Aether Logo](https://github.com/ONGQ0019/filedumps/blob/main/Aether6.png?raw=true)

![GitHub release (latest by date)](https://img.shields.io/badge/release-v1.0-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/M1-Private-Limited/AETHER)
![GitHub](https://img.shields.io/github/license/M1-Private-Limited/AETHER)
![GitHub contributors](https://img.shields.io/github/contributors/M1-Private-Limited/AETHER)
![GitHub stars](https://img.shields.io/github/stars/M1-Private-Limited/AETHER?style=social)

Aether is a powerful Streamlit application designed to elevate your data insights to celestial heights. Leveraging the power of Azure OpenAI, Aether enables you to generate sophisticated data segments and charts using AI, providing a seamless and interactive experience for data analysis and visualization.

## 🚀 Features

- **AI-Powered Data Insights**: Utilize Azure OpenAI to generate intelligent data segments and visualizations.
- **Multi-Source Data Integration**: Connect effortlessly to various data sources including Tableau, Snowflake, and Databricks.
- **Interactive Dashboards**: Create and view dynamic dashboards with real-time data updates.
- **Custom Data Filtering**: Apply custom filters to your datasets for refined analysis.
- **Comprehensive Data Profiling**: Generate detailed data profiles to understand your datasets better.
- **Report Generation**: Automatically generate reports with visualizations and key insights.
- **User-Friendly Interface**: Intuitive UI built with Streamlit Elements and ShadCN UI for enhanced user experience.
- **Real-Time Communication**: Stream data and interact with AI in real-time.

## 🎥 Promo Video



https://github.com/user-attachments/assets/36a4b863-7245-4183-9aa5-bb05dcb025f5



## ▶️ Demo

[![Demo Video](https://github.com/ONGQ0019/filedumps/blob/main/thumbnail.png?raw=true)](https://www.youtube.com/watch?v=cVjDr3Uhmhc)



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
