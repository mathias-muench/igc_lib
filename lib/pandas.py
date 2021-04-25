import pandas as pd


def flight_to_df(flight):
    index = pd.MultiIndex.from_product(
        [
            [flight.IGC],
            [pd.to_datetime(fix.timestamp, unit="s") for fix in flight.fixes],
        ]
    )
    df = pd.DataFrame(
        data=[
            [
                pd.to_datetime(fix.timestamp, unit="s"),
                fix.lat,
                fix.lon,
                fix.bearing,
                fix.bearing_change_rate,
                fix.gsp,
                fix.alt,
                fix.flying,
                fix.circling,
            ]
            for fix in flight.fixes
        ],
        index=index,
        columns=[
            "timestamp",
            "lat",
            "lon",
            "bearing",
            "bearing_change_rate",
            "gsp",
            "alt",
            "flying",
            "circling",
        ],
    )
    return df


def thermals_to_df(flight):
    df = pd.DataFrame()
    df["enter"] = [
        pd.to_datetime(i.enter_fix.timestamp, unit="s") for i in flight.thermals
    ]
    df["exit"] = [
        pd.to_datetime(i.exit_fix.timestamp, unit="s") for i in flight.thermals
    ]
    return df
