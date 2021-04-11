import pandas as pd


def flight_to_df(flight):
    index = pd.MultiIndex.from_product(
        [[flight.IGC], [fix.timestamp for fix in flight.fixes]]
    )
    df = pd.DataFrame(
        data=[
            [
                fix.timestamp,
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
    df["enter"] = [i.enter_fix.index for i in flight.thermals]
    df["exit"] = [i.exit_fix.index for i in flight.thermals]
    return df
