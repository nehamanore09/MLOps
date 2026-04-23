import yaml
import pandas as pd
import numpy as np
import time
import json
import logging
import argparse

# starting timer (to calculate latency later)
start_time = time.time()

# taking inputs from command line
parser = argparse.ArgumentParser()

parser.add_argument("--input", default="data.csv")
parser.add_argument("--config", default="config.yaml")
parser.add_argument("--output", default="metrics.json")
parser.add_argument("--log-file", default="run.log")

args = parser.parse_args()

# setup logging
logging.basicConfig(
    filename=args.log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Job started... lets see how it goes")

try:

    with open(args.config, "r") as file:
        config = yaml.safe_load(file)

    seed = config.get("seed")
    window = config.get("window")
    version = config.get("version")

    if seed is None or window is None or version is None:
        raise ValueError("Config file seems incomplete")

    logging.info(f"Config loaded -> seed={seed}, window={window}, version={version}")

    # setting seed (just to keep things consistent)
    np.random.seed(seed)


    # reading csv (had some issue earlier so keeping it simple)
    df = pd.read_csv(args.input)

    # splitting manually (yeah not the prettiest but works)
    df = df[0].str.split(",", expand=True)

    df.columns = ['timestamp','open','high','low','close','volume_btc','volume_usd']

    if df.empty:
        raise ValueError("Data file is empty")

    if "close" not in df.columns:
        raise ValueError("Close column missing")

    logging.info(f"Loaded {len(df)} rows")

    # PROCESSING
    logging.info("Calculating rolling mean")

    # converting close to number (just in case)
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    df["rolling_mean"] = df["close"].rolling(window=window).mean()

    # dropping NaN rows (first few rows mostly)
    df = df.dropna()

    logging.info("Generating signals")

    # simple logic
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

    # metrics
    rows_processed = len(df)
    signal_rate = df["signal"].mean()

    latency_ms = int((time.time() - start_time) * 1000)

    logging.info(f"Rows: {rows_processed}, Signal rate: {signal_rate}")

    metrics = {
        "version": version,
        "rows_processed": rows_processed,
        "metric": "signal_rate",
        "value": round(float(signal_rate), 4),
        "latency_ms": latency_ms,
        "seed": seed,
        "status": "success"
    }

    logging.info("Job done successfully")

except Exception as e:
    logging.error(f"Something went wrong: {str(e)}")

    metrics = {
        "version": "v1",
        "status": "error",
        "error_message": str(e)
    }


with open(args.output, "w") as f:
    json.dump(metrics, f, indent=4)

# printing final output (needed for docker)
print(metrics)