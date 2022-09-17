# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`server_info`
=============

Code for maintaining the server information and status

* Author: Alec Delaney
"""

from datetime import datetime, timedelta
from typing import Optional, Sequence

class ServerInfo:

    def __init__(self, is_testing: bool = False, simulated_time: Optional[datetime] = None, candle_lighting_times: Sequence[datetime] = (), burnout: bool = False):
        self.is_testing = is_testing
        self._simulated_time = simulated_time if simulated_time else datetime.now()
        self._set_time = datetime.now()
        self.candle_lighting_times = candle_lighting_times
        self.burnout = burnout
        self._test_day_index = 0
        self.return_turnoff_time = False

    @property
    def simulated_time(self) -> datetime:
        return self._simulated_time + self.time_since_set

    @simulated_time.setter
    def simulated_time(self, new_time: datetime) -> None:
        self._simulated_time = new_time
        self._set_time = datetime.now()

    @property
    def time_since_set(self) -> timedelta:
        return datetime.now() - self._set_time

    @property
    def test_day(self) -> int:
        return self._test_day_index + 1

    @test_day.setter
    def test_day(self, new_day: int) -> None:
        self._test_day_index = new_day - 1

    @property
    def current_lighting_time(self) -> datetime:
        return self.candle_lighting_times[self._test_day_index]

    @property
    def target_time(self) -> datetime:
        if self.burnout and self.return_turnoff_time:
            return self.current_lighting_time + timedelta(hours=12)
        return self.current_lighting_time
