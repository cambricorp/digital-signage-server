digital-signage-server
======================

The SAPO Digital Signage Server v2.0, [MQTT][mqtt] branch

## Context:

This is an [MQTT][mqtt]-centric version of the server we used to run our digital signage solution during [Codebits 2014][cb].

That version was used to schedule hundreds of assets (including live data and video streams) across roughly 20 wide screen LCDs, wall projectors, etc. during the 3 days of the event, using [a custom built Android client][ac].

In case you're just curious about what it looked like, here's a screenshot we took during the event, with most of the assets loaded:

<img src="https://raw.githubusercontent.com/sapo/digital-signage-server/codebits2014/about/screenshot.jpg">

Managing assets and moving them between playlists is done entirey via drag-and-drop, using a Kanban component [Hugo Lima](https://github.com/hmiguellima) developed for the [Ink][ink] library (we'll be releasing that component as part of a single page application framework we're also working on).

## Next Steps

The intent of this branch is to use [MQTT][mqtt] instead of HTTP polling in an attempt to provide real-time synchronization of multiple displays and integration with other hardware devices (such as lighting and projection controllers based on Arduino).

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
