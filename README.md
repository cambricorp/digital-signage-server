digital-signage-server
======================

The SAPO Digital Signage Server v2.0, Codebits 2014 Edition

## Context:

This is the server we used to run our digital signage solution during [Codebits 2014][cb].

It was used to schedule hundreds of assets (including live data and video streams) across roughly 20 wide screen LCDs, wall projectors, etc. during the 3 days of the event, using [a custom built Android client][ac].

This repository contains (almost) all the source code we used, except for a private API to [MEO Kanal][mk] - nevertheless, you should be able to tweak it to get it running without the missing bits.

In case you can't or are just curious about what it looked like, here's a screenshot we took during the event, with most of the assets loaded:

<img src="https://raw.githubusercontent.com/sapo/digital-signage-server/codebits2014/about/screenshot.jpg">

Managing assets and moving them between playlists is done entirely via drag-and-drop, using a Kanban component [Hugo Lima](https://github.com/hmiguellima) developed for the [Pink][pink] single-page web app framework (this repository includes a deployment snapshot of [Pink][pink]).

## Next Steps

As to future developments, the `mqtt` branch contains a reboot of this solution to use [MQTT][mqtt] instead of HTTP polling in an attempt to provide real-time synchronization of multiple displays and integration with other hardware devices (such as lighting and projection controllers based on Arduino).

## Credits:

* [Rui Carmo](https://github.com/rcarmo) - initial implementation, specs, UX rants and random patching
* [Hugo Lima](https://github.com/hmiguellima) - data models and Kanban-like front-end
* [Bruno René Santos](https://github.com/brunorene) - back-end and playlist generation

# How to run

There is a Vagrantfile, so you can get it more or less up and running in
Vagrant using 'vagrant up'.  Another, more manual way follows.

You should set up a virtualenv to install the required dependencies. And you
need to set up some required config files for the app to start.

    virtualenv env/
    pip install -r requirements.txt

    cp etc/users.json.default etc/users.json
    cp etc/default.json.default etc/default.json

    python manage.py add-user <youruser> <yourpassword>

You also need to install and start redis at this point.  After you've done
that, you can easily get the web service up and running:

    python app.py

You probably also need to start the celery workers, and of course you'd need
the clients for showing.  But this should get you started.


# LICENSING

Everything on this source tree is distributed under the MIT license. Go forth and hack it to your contentment.

[ink]: http://ink.sapo.pt
[cb]: https://codebits.eu
[ac]: https://github.com/sapo/android-signage-client
[cl]: https://github.com/sapo/digital-signage-client
[c]: https://github.com/FedericoCeratto/bottle-cork
[b]: https://github.com/bbangert/beaker
[mqtt]: http://mqtt.org
[mk]: http://kanal.pt
[pink]: http://github.com/sapo/pink
