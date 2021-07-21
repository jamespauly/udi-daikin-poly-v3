# Daikin Mini Split

This is a node server to interface with Daikin Mini-Split HVAC systems and make it available to a Universal Devices ISY994i Polyglot interface with Polyglot V2 running on a Polisy

Currently supports Daikin WiFi modules:
* BRP069Axx/BRP069Bxx/BRP072Axx

#### Installation

1. Backup Your ISY!
2. Go to the Polyglot Store in the UI and install.
3. From the Polyglot dashboard, select the udi-daikin-poly node server and configure (see configuration options below).
3. Restart the Admin Console so that it can properly display the new node server nodes.

#### Requirements

Here is what is required to use this poly:<BR>
[pydaikin](https://pypi.org/project/pydaikin/)
<BR>https://pypi.org/project/pydaikin/

urllib3 - For logging


