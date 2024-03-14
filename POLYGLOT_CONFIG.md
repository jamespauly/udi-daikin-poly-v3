# Daikin Node Server Custom Parameters

* <b>devices (Optional)</b> - Manually input your devices if they are on a different subnet. Ex. 
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