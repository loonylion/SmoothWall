#!/bin/bash

if (! -e /var/smoothwall/speedtest/runonce)
{
	/usr/bin/speedtest --accept-license --accept-gdpr --ca-certificate=/usr/lib/ssl/certs/ca-certificates.crt -f csv
	touch /var/smoothwall/speedtest/runonce
}
/usr/bin/speedtest --ca-certificate=/usr/lib/ssl/certs/ca-certificates.crt -f csv > /tmp/speedtest
