# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
`setup_helper`
==============

Simple module for holding the connectin status

* Author(s): Alec Delaney

"""


# pylint: disable=too-few-public-methods
class ConnectionStatus:
    """The connection status"""

    def __init__(self) -> None:
        self.is_connected = False
