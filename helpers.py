import pandas as pd # type: ignore
import json

def wrangle_backtest(content):
    ts_start = [content.index(x) for x in content if 'Trade History' in x][0]
    sandbox_log = [content.index(x) for x in content if 'Sandbox logs' in x][0]
    al_history = [content.index(x) for x in content if 'Activities log' in x][0]
    
    sandbox = content[sandbox_log+1:al_history-3]
    sandbox = [x.strip() for x in sandbox]
    json_string = "[" + "".join(sandbox).replace("}{", "},{") + "]"
    sandbox_logs = pd.DataFrame(json.loads(json_string))

    activity_logs = content[al_history+1:ts_start-4]
    df = pd.DataFrame(activity_logs)[0].str.strip().str.split(';', expand=True)
    df.columns = df.loc[0]
    activity_logs_df = df.iloc[1:]

    trades = content[ts_start+1:]
    json_str = "".join(trades)
    json_str = json_str.replace(",\n  }", "\n  }")  # Remove trailing commas
    json_str = json_str.replace(",\n]", "\n]")  # Remove trailing comma 
    data = json.loads(json_str)
    trades_df = pd.DataFrame(data)

    return trades_df, activity_logs_df, sandbox_logs