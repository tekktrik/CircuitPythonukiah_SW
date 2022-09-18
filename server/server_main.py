# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`server_main`
=============

Main code for running the validation test code on the server

* Author: Alec Delaney
"""

from datetime import datetime, timedelta
from typing import Optional, Literal
from fastapi import FastAPI, Response, status
from server_info import ServerInfo

app = FastAPI()

server_info = ServerInfo()


@app.post("/setup/", status_code=status.HTTP_201_CREATED)
def setup() -> None:
    """Setup API for the server"""
    server_info.is_testing = True
    server_info.candle_lighting_times = []
    server_info.burnout = False


@app.patch("/setup/time/{candle_lighting}")
def setup_time(candle_lighting: str) -> None:
    """Load times into server

    :param str candle_lighting: The candle lighting time, as an ISO
        formatted string
    """
    if not isinstance(server_info.candle_lighting_times, list):
        server_info.candle_lighting_times = list(server_info.candle_lighting_times)
    new_lighting_time = datetime.fromisoformat(candle_lighting)
    server_info.candle_lighting_times.append(new_lighting_time)


@app.patch("/setup/burnout/{setting}")
def setup_burnout(setting: Literal[0, 1]) -> None:
    """Load burnout setting into server

    :param int setting: The settings for burnout
    """
    server_info.burnout = bool(setting)


@app.patch("/setup/finalize")
def finalize_setup() -> None:
    """Finalize the setup process"""
    server_info.simulated_time = server_info.candle_lighting_times[0] - timedelta(
        seconds=10
    )
    server_info.test_day = 1


@app.get("/time", status_code=200)
def get_time(response: Response) -> Optional[str]:
    """Time API for the server"""
    if not server_info.is_testing:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return None
    sim_time = server_info.simulated_time
    if sim_time > server_info.target_time:
        if server_info.test_day != 9:  # If not last day...
            if server_info.return_turnoff_time:  # And not returning a turn off time...
                server_info.test_day = server_info.test_day + 1
            server_info.return_turnoff_time = not server_info.return_turnoff_time
            new_target_time = server_info.target_time
            server_info.simulated_time = new_target_time - timedelta(seconds=10)
        else:
            server_info.is_testing = False
            server_info.candle_lighting_times = []
            server_info.burnout = False
            server_info.simulated_time = datetime.now()
            server_info.test_day = 0
    return str(sim_time)
