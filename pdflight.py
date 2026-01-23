"""Utilities for converting Flight objects to pandas DataFrames."""

import pandas as pd

def flight_to_dataframe(flight):
    """Converts a Flight object to a pandas DataFrame.

    Args:
        flight: A Flight object (from igc_lib.py).

    Returns:
        A DataFrame where each row is a GNSSFix, with columns for:
        - lat, lon
        - derived attributes: gsp, bearing, flying, circling
        - alt (chosen altitude, PRESS or GNSS)

        The index is set to the UTC datetime of the fix.

    Raises:
        ValueError: If the flight is invalid.
    """
    if not flight.valid:
        raise ValueError("Flight is invalid. Check flight.notes for details.")

    return (
        pd.DataFrame({
            "lat": fix.lat,
            "lon": fix.lon,
            "alt": fix.alt,
            "gsp": fix.gsp,
            "bearing": fix.bearing,
            "bearing_change_rate": fix.bearing_change_rate,
            "flying": fix.flying,
            "circling": fix.circling,
        } for fix in flight.fixes)
        .set_index(
            pd.to_datetime(
                [fix.timestamp for fix in flight.fixes],
                unit="s",
                utc=True
            )
        )
        .rename_axis("datetime")
    )
