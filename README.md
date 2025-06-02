# IMC_strategy_prep
Repo for statistical analysis for IMC trading competition 2025. We are going to work on 2025 data and backtest it with dedicated backtester. We are focusing just on statistical and patern analysis and treat algoirthm implementation as optional.

Group of Corine Gatete, Anlan Chen, Sanan Mursalli, Michał Brzeziński and Antek Smolski

Link to competition: https://prosperity.imc.com/
Link to Prosperity wiki: https://imc-prosperity.notion.site/Prosperity-3-Wiki-19ee8453a09380529731c4e6fb697ea4


General Remarks:

- Notebooks Round_1, Round_2, Round_3, Round_4 and Round_5 can be run in the way they are prepared, meaning you only need to install the libraries (if you miss some)/
- Algorithm_round_1 needs to be run with prosperity2bt, as "Algorithm_round_1.py 1 2 --print" in the terminal to get the results. The reults are saved in "Backtest" for further analysis. The algorithm is optimized for AMETHYST, without taking STARFRUIT into consideration. It is implemented based on the risk limits, and trades around constant midprice, which is a VWAP mid.