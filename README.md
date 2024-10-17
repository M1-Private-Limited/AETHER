
![Aether Logo](https://github.com/ONGQ0019/filedumps/blob/main/Aether6.png?raw=true)

![GitHub release (latest by date)](https://img.shields.io/badge/release-v1.0-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/M1-Private-Limited/AETHER)
![GitHub](https://img.shields.io/github/license/M1-Private-Limited/AETHER)
![GitHub contributors](https://img.shields.io/github/contributors/M1-Private-Limited/AETHER)
![GitHub stars](https://img.shields.io/github/stars/M1-Private-Limited/AETHER?style=social)

In ancient Greek mythology, Aether was the divine substance that illuminated the heavens, revealing hidden truths. Today, Aether is your guiding light in the data world, transforming data into clear, actionable insights and elevating your data insights to celestial heights.

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

[![Demo Video](https://github.com/ONGQ0019/filedumps/blob/main/aether_demo.png?raw=true)](https://youtu.be/JDvVK0nckaA)
### Q&A About Our Demo

#### What industry and topic did you choose?
**Industry:** Telecommunications  
**Topic:** Data Platform

#### Why did you choose this topic?
Telecommunications industry generates vast amounts of data daily. Analyzing this huge and complex data efficiently can be very challenging and time consuming. However, this data do provide significant insights into customer behavior, marketing effectiveness and data trends. Hence, Aether aims to streamline this process by leveraging GENAI technology to simplify data ideation, segmentation, and visualization to allow users like marketer/business analyst to fully leverage our data to achieve our business goals.

#### What dataset and model did you use?
**Dataset:** Sample Telco dataset from our Databricks' DBFS  
**Model:** GPT4o from Azure Openai

#### How did you solve the problem? Please explain the technical details, such as techniques you use.
Full list of techniques can be found in app.py or under our Technologies used section.

Here are some of the key techniques we used:
1. **Smart Prompt Engineering:** Advanced prompt engineering to manipulate datasets and generate complex charts and segments instantaneously. By crafting specific prompts, we guided the AI to produce structured outputs, such as detailed data dictionaries and segmentations in Python format.

2. **Visualization with Nivo Charts:** Utilized Nivo charts to create beautiful, animated visualizations, enhancing the user experience and making data insights more accessible and engaging.

3. **Integration with Tableau, Azure Blob Storage, Databricks APIs:** Connection to various data sources and datasets using Tableau, Azure and Databricks APIs, allowing for seamless data ingestion and integration.



## 🌟 Aether: Your All-in-One Solution for Ideation, Segmentation, and Visualization

### Benefits at a Glance
- **Intuitive Interface**: Aether’s user-centric design, built with Shadcn, ensures seamless navigation and effortless data analysis.
- **Multi-Source Integration**: Connect effortlessly to Tableau, local storage, Azure Blob Storage, and Databricks' DBFS, providing flexible and robust data management.
- **One-Click Go**: Generate data profiles, segmentations and visualizations, consolidated reports with just a single click, allowing you to focus on what matters most.
- **Enhanced Insights**: Gain deeper and more actionable insights quickly with AI Chat, driving better business decisions.
- **Empowerment Through Creativity**: Find innovative ideas, unique segments and exciting versatile visualizations to suit your unique data storytelling needs—all without requiring technical expertise.

Aether is designed to make data analysis easy, insightful, and efficient for everyone. Whether you’re brainstorming new marketing strategies, segmenting your audience, or visualizing complex data, Aether provides the tools you need—all in a single, user-friendly platform.

Here is a quick comparison of Without Aether vs With Aether:
#### Without Aether
<img src="https://github.com/ONGQ0019/filedumps/blob/main/without_aether.png?raw=true" alt="Without Aether" width="800"/>

#### With Aether
<img src="https://github.com/ONGQ0019/filedumps/blob/main/with_aether.png?raw=true" alt="With Aether" width="800"/>


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

- **Datasource Tab**: Connect to various data sources like Tableau, Azure blobstorage, or Databricks. Upload your CSV files or select pre-defined datasources.
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
- [Azure Blob Storage Client Library for Python](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python) - Connection to Azure Blob Storage
- [streamlit-lottie](https://github.com/andfanilo/streamlit-lottie) - Loading animations

## 📜 License

This project is licensed under the [MIT License](LICENSE).


---

