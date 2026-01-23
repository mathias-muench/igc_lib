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

def thermals_to_dataframe(flight):
    """Converts a Flight's thermals to a pandas DataFrame.

    Args:
        flight: A Flight object (from igc_lib.py).

    Returns:
        A DataFrame where each row is a Thermal, with columns for:
        - enter_time, exit_time: UTC datetime of entry/exit
        - enter_lat, enter_lon: entry point coordinates
        - exit_lat, exit_lon: exit point coordinates
        - duration: time spent in thermal (as timedelta)
        - alt_change: altitude change (meters)
        - v_vel: average vertical velocity (m/s)
        - enter_alt, exit_alt: entry/exit altitudes (meters)

        The index is set to the UTC datetime of the thermal entry.

    Raises:
        ValueError: If the flight is invalid.
    """
    if not flight.valid:
        raise ValueError("Flight is invalid. Check flight.notes for details.")

    return (
        pd.DataFrame({
            "enter_time": pd.to_datetime(thermal.enter_fix.timestamp, unit="s", utc=True),
            "exit_time": pd.to_datetime(thermal.exit_fix.timestamp, unit="s", utc=True),
            "enter_lat": thermal.enter_fix.lat,
            "enter_lon": thermal.enter_fix.lon,
            "exit_lat": thermal.exit_fix.lat,
            "exit_lon": thermal.exit_fix.lon,
            "duration": pd.to_timedelta(thermal.time_change(), unit="s"),
            "alt_change": thermal.alt_change(),
            "v_vel": thermal.vertical_velocity(),
            "enter_alt": thermal.enter_fix.alt,
            "exit_alt": thermal.exit_fix.alt,
        } for thermal in flight.thermals)
        .set_index(
            pd.to_datetime(
                [thermal.enter_fix.timestamp for thermal in flight.thermals],
                unit="s",
                utc=True
            )
        )
        .rename_axis("enter_time")
    )
