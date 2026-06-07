# Stock Analysis & Forecasting Dashboard
An interactive stock market web application built using **Streamlit**, which provides stock analysis, visualization, and future price prediction using Machine Learning models like **LSTM** and **ARIMA**. The app helps users explore financial data, understand market trends, and make data-driven investment decisions.

## Live Features

### Stock Information & Analysis
- Historical stock price visualization
- Moving averages and trend detection
- Technical indicators for better insights
- Interactive charts for data exploration

### Stock Price Prediction
- Forecast future stock prices upto the next 30 days
- Machine Learning models used:
  - **LSTM (Long Short-Term Memory)**
  - **ARIMA (AutoRegressive Integrated Moving Average)**
- Compare predictions from both models
- Visualize predicted trends

## Machine Learning Models

### LSTM Model
A deep learning model designed for time-series forecasting that captures long-term dependencies in stock price data.

### ARIMA Model
A statistical model used for analyzing and forecasting time series data based on past values and error terms.

## Tech Stack

- Python 
- Streamlit 
- Pandas & NumPy 
- Scikit-learn 
- TensorFlow / Keras 
- Matplotlib & Plotly 
- Statsmodels 

## Project Structure
stock-analysis-and-pred-app/
│
├── pages/
│    ├── utils/
│       ├── data_processing.py
│       ├── model_utils.py
│   ├── stock_analysis.py
│   ├── stock_prediction.py
│
├── Images/
│    ├── image.jpg
│   
├── trading_app.py
├── requirements.txt
├── SOURCES.txt
└── README.md

## Installation & Setup

1. Clone the repository
```bash
git clone https://github.com/your-username/stock-analysis-app.git
cd stock-analysis-app

2. Create virtual environment(Recommended)
```bash
python -m venv venv

3. Install dependencies
pip install -r requirements.txt

4. Run the application
streamlit run trading_app.py


=## Future Improvements
- Add real-time stock data API integration
- Improve prediction accuracy using Transformer models
- Add news sentiment analysis
- Deploy on Streamlit Cloud / AWS