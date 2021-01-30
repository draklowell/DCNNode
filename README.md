# DCN Node
#### Node
[github](https://github.com/draklowell/DCNNode) | [dockerhub](https://hub.docker.com/r/draklowell/dcn)
#### Client
[github](https://github.com/draklowell/DCNLibrary/) | [pypi](https://pypi.org/project/dcn/)
## Setup guide
### Using DockerHub
```
docker pull draklowell/dcn
```
### Using github
#### Linux and MacOS
```
git clone https://github.com/draklowell/DCNNode && cd DCNNode && docker build .
```
#### Windows
Download node and in downloaded folder run
```
docker build .
```
### Dependencies
1. requests ( `2.22.0` )
2. ansicolors ( `1.1.8` )
3. pycryptodome ( `3.9.9` )
4. pyopenssl ( `20.0.1` )
## Info
#### Privacy
Connection between two nodes is wrapped by `TLSv1.2` ( without certificate verification ), but packet is opened, and can be read by any user.
#### High-level protocols conflict
To avoid protocol conflicts, we recommend to use `protocol sign`, it is some bytes in begin of packet, that indicate what protocol is using
#### License
[Apache License 2.0](LICENSE)
## Using guide
#### Configuration file
Config file is in JSON format. Default:
```json
{
    "DEBUG": {
        "FILE": "debug.log",
        "TIMEFORMAT": "%Y-%m-%d %H:%M:%S"
    },
    "ADDRESS": "0.0.0.0:300",
    "FRIENDLY_HOSTS": []
}
```
`ADDRESS` - address, where node accepts connections 

`FRIENDLY_HOSTS` - other known nodes in format `address:port` ( example: `1.2.3.4:300` ), also it request official nodes, from official tracker
###### Debug
`FILE` - debug file

`TIMEFORMAT` - debug time format :
|Directive|Meaning|Example|
|-|-|-|
|`%a`|Abbreviated weekday name.|Sun, Mon, ...|
|`%A`|Full weekday name.|Sunday, Monday, ...|
|`%w`|Weekday as a decimal number.|0, 1, ..., 6|
|`%d`|Day of the month as a zero-padded decimal.|01, 02, ..., 31|
|`%-d`|Day of the month as a decimal number.|1, 2, ..., 30|
|`%b`|Abbreviated month name.|Jan, Feb, ..., Dec|
|`%B`|Full month name.|January, February, ...|
|`%m`|Month as a zero-padded decimal number.|01, 02, ..., 12|
|`%-m`|Month as a decimal number.|1, 2, ..., 12|
|`%y`|Year without century as a zero-padded decimal number.|00, 01, ..., 99|
|`%-y`|Year without century as a decimal number.|0, 1, ..., 99|
|`%Y`|Year with century as a decimal number.|2013, 2019 etc.|
|`%H`|Hour (24-hour clock) as a zero-padded decimal number.|00, 01, ..., 23|
|`%-H`|Hour (24-hour clock) as a decimal number.|0, 1, ..., 23|
|`%I`|Hour (12-hour clock) as a zero-padded decimal number.|01, 02, ..., 12|
|`%-I`|Hour (12-hour clock) as a decimal number.|1, 2, ... 12|
|`%p`|Locale’s AM or PM.|AM, PM|
|`%M`|Minute as a zero-padded decimal number.|00, 01, ..., 59|
|`%-M`|Minute as a decimal number.|0, 1, ..., 59|
|`%S`|Second as a zero-padded decimal number.|00, 01, ..., 59|
|`%-S`|Second as a decimal number.|0, 1, ..., 59|
|`%f`|Microsecond as a decimal number, zero-padded on the left.|000000 - 999999|
|`%z`|UTC offset in the form +HHMM or -HHMM.| |
|`%Z`|Time zone name.| |
|`%j`|Day of the year as a zero-padded decimal number.|001, 002, ..., 366|
|`%-j`|Day of the year as a decimal number.|1, 2, ..., 366|
|`%U`|Week number of the year (Sunday as the first day of the week). All days in a new year preceding the first Sunday are considered to be in week 0.|00, 01, ..., 53|
|`%W`|Week number of the year (Monday as the first day of the week). All days in a new year preceding the first Monday are considered to be in week 0.|00, 01, ..., 53|
|`%c`|Locale’s appropriate date and time representation.|Mon Sep 30 07:06:05 2013|
|`%x`|Locale’s appropriate date representation.|09/30/13|
|`%X`|Locale’s appropriate time representation.|07:06:05|
|`%%`|A literal '%' character.|%|
_( table from [programiz.com](https://www.programiz.com/python-programming/datetime/strftime))_