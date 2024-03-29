# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
`server_info`
=============

Code for maintaining the server information and status

* Author: Alec Delaney
"""

from datetime import datetime, timedelta


# pylint: disable=too-many-instance-attributes
class ServerInfo:
    """Class for holding server information and status"""

    def __init__(self):
        self.is_testing: bool = False
        """Whether the server is actively testing"""
        self._simulated_time = datetime.now()
        self._set_time = datetime.now()
        self.candle_lighting_times: list[datetime] = []
        """The stored candle lighting times"""
        self.burnout: bool = False
        """Whether burnout is set"""
        self.test_type: str = ""
        """The type of testing"""
        self._test_day_index = 0
        self.return_turnoff_time = False

    @property
    def simulated_time(self) -> datetime:
        """The current simulated time"""
        return self._simulated_time + self.time_since_set

    @simulated_time.setter
    def simulated_time(self, new_time: datetime) -> None:
        self._simulated_time = new_time
        self._set_time = datetime.now()

    @property
    def time_since_set(self) -> timedelta:
        """The amount of time since the simulated time was set"""
        return datetime.now() - self._set_time

    @property
    def test_day(self) -> int:
        """The day of the current test (starts from 1)"""
        return self._test_day_index + 1

    @test_day.setter
    def test_day(self, new_day: int) -> None:
        self._test_day_index = new_day - 1

    @property
    def current_lighting_time(self) -> datetime:
        """The current candle lighting time for the active test day"""
        return self.candle_lighting_times[self._test_day_index]

    @property
    def target_time(self) -> datetime:
        """The "taraget" time to use, based off of the current server settigns"""
        if self._test_day_index == len(self.candle_lighting_times):
            return self.candle_lighting_times[-1] + timedelta(hours=24)
        if self.return_turnoff_time:
            return self.current_lighting_time + timedelta(hours=12)
        return self.current_lighting_time
