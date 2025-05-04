import pandas as pd # type: ignore
import json

def wrangle_backtest(content_input):
    ts_start = [content_input.index(x) for x in content_input if 'Trade History' in x][0]
    sandbox_log = [content_input.index(x) for x in content_input if 'Sandbox logs' in x][0]
    al_history = [content_input.index(x) for x in content_input if 'Activities log' in x][0]
    
    sandbox = content_input[sandbox_log+1:al_history-3]
    sandbox = [x.strip() for x in sandbox]
    json_string = "[" + "".join(sandbox).replace("}{", "},{") + "]"
    sandbox_logs = pd.DataFrame(json.loads(json_string))

    activity_logs = content_input[al_history+1:ts_start-4]
    df = pd.DataFrame(activity_logs)[0].str.strip().str.split(';', expand=True)
    df.columns = df.loc[0]
    activity_logs_df = df.iloc[1:]

    trades = content_input[ts_start+1:]
    json_str = "".join(trades)
    json_str = json_str.replace(",\n  }", "\n  }")  # Remove trailing commas
    json_str = json_str.replace(",\n]", "\n]")  # Remove trailing comma 
    data = json.loads(json_str)
    trades_df = pd.DataFrame(data)

    return trades_df, activity_logs_df, sandbox_logs

def calculate_VWAP(df):
    df['bid_weighted_price'] = (df['bid_price_1'] * df['bid_volume_1']).fillna(0) \
                            + (df['bid_price_2'] * df['bid_volume_2']).fillna(0) \
                            + (df['bid_price_3'] * df['bid_volume_3']).fillna(0)

    df['total_bid_volume'] = df[['bid_volume_1', 'bid_volume_2', 'bid_volume_3']].fillna(0).sum(axis=1)

    df['ask_weighted_price'] = (df['ask_price_1'] * df['ask_volume_1']).fillna(0) \
                            + (df['ask_price_2'] * df['ask_volume_2']).fillna(0) \
                            + (df['ask_price_3'] * df['ask_volume_3']).fillna(0)

    df['total_ask_volume'] = df[['ask_volume_1', 'ask_volume_2', 'ask_volume_3']].fillna(0).sum(axis=1)

    df['total_weighted_price'] = df['bid_weighted_price'] + df['ask_weighted_price']
    df['total_volume'] = df['total_bid_volume'] + df['total_ask_volume']

    df['VWAP'] = df['total_weighted_price'] / df['total_volume']
    return df