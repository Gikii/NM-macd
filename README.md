# MACD Financial Indicator Analysis

A Python-based financial analysis tool that implements and evaluates the Moving Average Convergence/Divergence (MACD) indicator. Developed for a Numerical Methods course, this project simulates a trading strategy on the EUR/USD currency pair over a 5-year period (April 2020 - March 2025).



## Overview

The MACD is a highly popular momentum and trend-following indicator used in technical analysis. This project calculates the indicator entirely from scratch using historical market data, generates buy and sell signals based on line crossovers, and simulates a trading portfolio starting with an initial capital of 1000 units. 

The core mathematical calculation implemented for the indicator is:
$$MACD = EMA_{12} - EMA_{26}$$
*(Where $EMA$ stands for Exponential Moving Average)*.

## Technologies

* **Language:** Python 3
* **Libraries:** `pandas` for data manipulation, and `matplotlib.pyplot` for rendering financial charts and trading signals.

## Key Features

* **Algorithmic Signal Generation:** Accurately identifies market entry (BUY) and exit (SELL) points when the MACD line crosses the SIGNAL line.
* **Trading Simulation:** Tracks a virtual investment wallet, executing trades strictly based on the generated signals to calculate the final capital.
* **Data Visualization:** Renders detailed charts highlighting the EUR/USD price action alongside clearly marked Buy (green triangles) and Sell (red triangles) markers.
* **Performance Analysis:** Includes a comprehensive evaluation of the strategy's real-world viability. **[Read the full analysis report here (sprawozdanie.pdf)](./sprawozdanie.pdf)**

## Project Conclusions

Based on the 5-year simulation, the pure MACD strategy yielded a win rate of approximately 40%. The analysis concludes that while MACD is a powerful tool for capturing long-term trends, it generates a high volume of false signals during market consolidations in highly volatile environments like the FOREX market. Consequently, the project demonstrates that MACD should not be used as a standalone decision-making tool for long-term currency trading.

## Setup and Execution

1. Ensure you have Python installed along with the required libraries:
   `pip install pandas matplotlib`
2. Clone the repository containing the `MACD.py` script and your historical dataset.
3. Run the analysis script from your terminal:
   `python MACD.py`
