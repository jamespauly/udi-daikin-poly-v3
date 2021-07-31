# Daikin Mini Split

This is a node server to interface with Daikin Mini-Split HVAC systems and make it available to a Universal Devices ISY994i Polyglot interface with Polyglot V2 running on a Polisy

Currently supports Daikin WiFi modules:
* BRP069Axx/BRP069Bxx/BRP072Axx

#### Installation

1. Backup Your ISY!
2. Go to the Polyglot Store in the UI and install.
3. From the Polyglot dashboard, select the Daikin node server.
3. Restart the Admin Console to properly display the new node server nodes.

#### Configuration
1. No configuration needed.  Currently the nodeserver must run on the same network as your Daikin network modules, it will autodetect and set them up automatically.  I will be releasing a version soon that will allow you to set them up manually via static IP's or through Daikin's cloud service.

#### Requirements

Here is what is required to use this poly:<BR>
[pydaikin](https://pypi.org/project/pydaikin/)
<BR>https://pypi.org/project/pydaikin/

