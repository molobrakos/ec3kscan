Scan radio spectrum to determine most appropriate frequency to use for the ec3k energy counter.
Uses the ec3k package (https://pypi.python.org/pypi/ec3k/, https://github.com/avian2/ec3k).
Optionally feed data into [Home Assistant](https://home-assistant.io).

![specrum](https://cdn.rawgit.com/molobrakos/ec3kscan/master/spectrum.svg "spectrum")

To feed into Home Assistant (http://home-assistant.io)

```nice ./ec3k-listen | grep is_on --line-buffered | tee >(./ha-feeder) | cronolog ec3k.%Y-%m-%d.log.ndjson```
