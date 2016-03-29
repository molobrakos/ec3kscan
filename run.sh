nice ./ec3k-listen | grep is_on --line-buffered | tee >(./ha-feeder) | cronolog ec3k.%Y-%m-%d.log.ndjson

