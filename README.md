# 📱 Smartphone Recommendation Engine

An intelligent agentic AI application that analyzes smartphone data and provides personalized recommendations with natural language intelligence.

## ✨ Features

- **Data-Driven Analysis**: Upload your smartphone dataset and get instant insights about device specifications and features
- **Intelligent Recommendations**: AI-powered agent that understands user preferences and suggests the best smartphones
- **Question Answering**: Ask natural language questions about phones and get accurate, detailed answers
- **Multi-Source Data Support**: Process information from various data formats
- **Real-Time Intelligence**: Leverages advanced AI models for context-aware responses

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or conda package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Devikrishna545/Smartphone-recommendation-engine.git
   cd Smartphone-recommendation-engine
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (if needed)
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 📖 Usage

### Basic Usage

```python
from smartphone_engine import SmartphoneRecommender

# Initialize the engine
recommender = SmartphoneRecommender()

# Upload data
recommender.load_data('path/to/smartphones.csv')

# Get recommendations
recommendations = recommender.recommend(
    budget=500,
    preferences={'camera': 'high', 'battery_life': 'long'}
)

# Ask questions
answer = recommender.query("What are the best phones under $500?")
```

### Using the CLI

```bash
python app.py --data path/to/data.csv --mode interactive
```

### API Endpoints

If using as a web service, the following endpoints are available:

- `POST /upload` - Upload smartphone data
- `GET /recommend` - Get smartphone recommendations
- `POST /query` - Ask natural language questions

## 📁 Project Structure

```
Smartphone-recommendation-engine/
├── README.md
├── requirements.txt
├── .env.example
├── app.py                 # Main application entry point
├── config.py             # Configuration settings
├── data/                 # Sample datasets
│   └── smartphones.csv
├── src/
│   ├── __init__.py
│   ├── engine.py         # Core recommendation logic
│   ├── agent.py          # AI agent implementation
│   ├── utils.py          # Utility functions
│   └── models/           # Data models
├── tests/                # Test suite
│   ├── test_engine.py
│   └── test_agent.py
└── notebooks/            # Jupyter notebooks for exploration
```

## 🧠 How It Works

### 1. Data Processing
- Accepts various data formats (CSV, JSON, Excel, etc.)
- Cleans and normalizes smartphone specifications
- Creates a knowledge base for the AI agent

### 2. Intelligent Agent
- Uses large language models to understand user queries
- Analyzes smartphone data against user preferences
- Provides contextual recommendations with explanations

### 3. Recommendation Engine
- Scores phones based on multiple criteria
- Considers budget, features, brand preferences, and more
- Ranks results by relevance and user preferences

## 🔧 Configuration

Edit `config.py` to customize:

```python
MODEL_NAME = "gpt-4"  # LLM model to use
MAX_RECOMMENDATIONS = 5
DATA_PATH = "data/"
API_PORT = 5000
```

## 📊 Dataset Format

Your smartphone data should include columns like:

| phone_name | brand | price | screen | battery | camera | processor |
|-----------|-------|-------|--------|---------|--------|-----------|
| iPhone 14 | Apple | 799 | 6.1" | 3200 | 48MP | A16 |

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=src tests/
```

## 📦 Dependencies

- `langchain` - For LLM integration and agents
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `Flask` - Web framework (if using API)
- `python-dotenv` - Environment variable management
- See `requirements.txt` for complete list

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Devikrishna545**

- GitHub: [@Devikrishna545](https://github.com/Devikrishna545)

## 🙏 Acknowledgments

- Thanks to the open-source AI community
- LangChain for agent framework
- All contributors and testers

## 📧 Support

For support, email or open an issue on the [GitHub Issues](https://github.com/Devikrishna545/Smartphone-recommendation-engine/issues) page.

## 🗺️ Roadmap

- [ ] Add multi-language support
- [ ] Implement user preference learning
- [ ] Create web UI dashboard
- [ ] Add price trend analysis
- [ ] Support for more smartphone data sources
- [ ] Mobile app integration

---

**Made with ❤️ for smartphone enthusiasts and tech lovers**
