digital-signage-server
======================

The SAPO Digital Signage Server v2.0

# Status

In a similar fashion to the [client][cl], the server code is being refactored piecemeal to take into account a number of fixes and enhancements done over the past few months.

In effect, this will be the next production version - but the code isn't done yet.

# Requirements

Nothing, really. It depends on what you want to do with it - I recommend setting up a Postgres database for the back-end, even though this has been in production using SQLite for ages.

# LICENSING

Everything on this source tree _except_ [Cork][c] (which regretfully is GPLv3) and [Beaker][b] (which has its own LICENSE file) is distributed under the MIT license.

[cl]: https://github.com/sapo/digital-signage-client
[c]: https://github.com/FedericoCeratto/bottle-cork
[b]: https://github.com/bbangert/beaker