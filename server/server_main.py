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
from typing import List, Optional
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from server_info import ServerInfo

app = FastAPI()

server_info = ServerInfo()

class SetupInfo(BaseModel):
    candle_lighting_times: List[datetime]
    burnout: bool

@app.post("/setup", status_code=status.HTTP_201_CREATED)
def setup(setup_info: SetupInfo) -> None:
    """Setup API for the server"""
    server_info.is_testing = True
    server_info.candle_lighting_times = setup_info.candle_lighting_times
    server_info.burnout = setup_info.burnout
    server_info.simulated_time = setup_info.candle_lighting_times[0] - timedelta(seconds=60)
    server_info.test_day = 1

@app.get("/time", status_code=200)
def get_time(response: Response) -> Optional[datetime]:
    """Time API for the server"""
    if not server_info.is_testing:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return
    sim_time = server_info.simulated_time
    if sim_time > server_info.target_time:
        if server_info.test_day != 8:  # If not last day...
            if server_info.burnout:  # Flip return type in burnout
                server_info.return_turnoff_time = not server_info.return_turnoff_time
            if not server_info.return_turnoff_time:  # And not returning a turn off time...
                server_info.test_day = server_info.test_day + 1
                new_target_time = server_info.target_time
                server_info.simulated_time = new_target_time - timedelta(seconds=60)
        else:
            server_info.is_testing = False
            server_info.candle_lighting_times = ()
            server_info.burnout = False
            server_info.simulated_time = datetime.now()
            server_info.test_day = 0
    return sim_time
