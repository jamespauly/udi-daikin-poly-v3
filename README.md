# Daikin Mini Split

This is a node server to interface with Daikin Mini-Split HVAC systems and make it available to a Universal Devices ISY994i Polyglot interface with Polyglot V3 running on a Polisy

Currently supports Daikin WiFi modules:
* BRP069Axx/BRP069Bxx/BRP072Axx

#### Installation

1. Backup Your ISY!
2. Go to the Polyglot Store in the UI and install.
3. From the Polyglot dashboard, select the Daikin node server.
3. Restart the Admin Console to properly display the new node server nodes.

#### Configuration
1. No configuration needed.  Tt will autodetect and set them up automatically if they are on the same network as the Daikin
2. If they are not on the same network then you can add a custom config with a key called <i><b>devices</b></i>.  Ex.
```json
[
    {
        "name": "Room1",
        "mac": "20:c5:f6:63:04:f6",
        "ip": "10.99.99.1"
    },
    {
        "name": "Room2",
        "mac": "20:c5:f6:63:04:f7",
        "ip": "10.99.99.2"
    },
    {
        "name": "Room3",
        "mac": "20:c5:f6:63:04:f8",
        "ip": "10.99.99.3"
    }
]
```

#### Requirements

Here is what is required to use this poly:<BR>
[pydaikin](https://pypi.org/project/pydaikin/)
<BR>https://pypi.org/project/pydaikin/
