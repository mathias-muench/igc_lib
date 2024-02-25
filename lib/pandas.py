import pandas as pd


def flight_to_df(flight):
    df = pd.DataFrame(
        data=[
            [
                flight.IGC,
                pd.to_datetime(fix.timestamp, unit="s"),
                fix.lat,
                fix.lon,
                fix.bearing,
                fix.bearing_change_rate,
                fix.gsp,
                fix.alt,
                fix.flying,
                fix.circling,
                False,
                None
            ]
            for fix in flight.fixes
        ],
        columns=[
            "IGC",
            "timestamp",
            "lat",
            "lon",
            "bearing",
            "bearing_change_rate",
            "gsp",
            "alt",
            "flying",
            "circling",
            "thermalling",
            "phase"
        ],
    )
    for i in flight.thermals:
        df.iloc[
            i.enter_fix.index : i.exit_fix.index, df.columns.get_loc("thermalling")
        ] = True
    df["phase"] = df.thermalling.diff() | df.flying.diff()
    ph = None
    for (i, r) in df.iterrows():
        if not ph or r.phase:
            ph = r.timestamp
        df.loc[i, "phase"] = ph

    return df
