Prometheus ZPOOL Exporter
===


Requirements
---

1. Python (tested with 3.5)
2. Python [prometheus_client](https://github.com/prometheus/client_python) module
4. `zpool` command (tested with FreeNAS 11.1/FreeBSD 11.1)



Run the zpool exporter as a command
---

```
export ZPOOLS=jails,bacup
python zpool_exporter.py
```

Access http://localhost:8000/metrics

You should get something like this:

```
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="6",patchlevel="3",version="3.6.3"} 1.0
# HELP request_processing_seconds Time spent processing request
# TYPE request_processing_seconds summary
request_processing_seconds_count 1.0
request_processing_seconds_sum 5.110865458846092e-06
# HELP zfs_health_status ZPool Health Status
# TYPE zfs_health_status gauge
zfs_health_status{name="backup",status="ONLINE",zpool="backup"} 1.0
zfs_health_status{name="raidz2-0",status="ONLINE",zpool="backup"} 1.0
zfs_health_status{name="gptid/90cd818f-5bd0-11e7-bea1-ac1f6b14d936",status="ONLINE",zpool="backup"} 1.0
zfs_health_status{name="jails",status="ONLINE",zpool="jails"} 1.0
zfs_health_status{name="mirror-0",status="ONLINE",zpool="jails"} 1.0
zfs_health_status{name="gptid/f2c6a679-5b4c-11e7-bb2a-ac1f6b14d936",status="ONLINE",zpool="jails"} 1.0
zfs_health_status{name="gptid/f2eedce1-5b4c-11e7-bb2a-ac1f6b14d936",status="ONLINE",zpool="jails"} 1.0
# HELP zfs_read_errors ZPool Read Errors
# TYPE zfs_read_errors gauge
zfs_read_errors{name="backup",zpool="backup"} 0.0
zfs_read_errors{name="raidz2-0",zpool="backup"} 0.0
zfs_read_errors{name="gptid/99cd818f-712g-89as-bea1-bc1f6b14d936",zpool="backup"} 0.0
zfs_read_errors{name="jails",zpool="jails"} 0.0
zfs_read_errors{name="mirror-0",zpool="jails"} 0.0
zfs_read_errors{name="gptid/f2c6a679-5b4c-11e7-bb2a-ac1f6b14d936",zpool="jails"} 0.0
zfs_read_errors{name="gptid/f2eedce1-5b4c-11e7-bb2a-ac1f6b14d936",zpool="jails"} 0.0
# HELP zfs_write_errors ZPool Write Errors
# TYPE zfs_write_errors gauge
zfs_write_errors{name="backup",zpool="backup"} 0.0
zfs_write_errors{name="raidz2-0",zpool="backup"} 0.0
zfs_write_errors{name="gptid/99cd818f-712g-89as-bea1-bc1f6b14d936",zpool="backup"} 0.0

zfs_write_errors{name="jails",zpool="jails"} 0.0
zfs_write_errors{name="mirror-0",zpool="jails"} 0.0
zfs_write_errors{name="gptid/f2c6a679-5b4c-11e7-bb2a-ac1f6b14d936",zpool="jails"} 0.0
zfs_write_errors{name="gptid/f2eedce1-5b4c-11e7-bb2a-ac1f6b14d936",zpool="jails"} 0.0
# HELP zfs_chksum_errors ZPool Checksum Errors
# TYPE zfs_chksum_errors gauge
zfs_chksum_errors{name="backup",zpool="backup"} 0.0
zfs_chksum_errors{name="raidz2-0",zpool="backup"} 0.0
zfs_chksum_errors{name="gptid/90cd818f-5bd0-11e7-bea1-ac1f6b14d936",zpool="backup"} 0.0
zfs_chksum_errors{name="gptid/916e53f8-5bd0-11e7-bea1-ac1f6b14d936",zpool="backup"} 0.0
zfs_chksum_errors{name="gptid/91edc509-5bd0-11e7-bea1-ac1f6b14d936",zpool="backup"} 0.0
zfs_chksum_errors{name="gptid/927287f1-5bd0-11e7-bea1-ac1f6b14d936",zpool="backup"} 0.0
zfs_chksum_errors{name="jails",zpool="jails"} 0.0
zfs_chksum_errors{name="mirror-0",zpool="jails"} 0.0
zfs_chksum_errors{name="gptid/f2c6a679-5b4c-11e7-bb2a-ac1f6b14d936",zpool="jails"} 0.0
zfs_chksum_errors{name="gptid/f2eedce1-5b4c-11e7-bb2a-ac1f6b14d936",zpool="jails"} 0.0
# HELP zfs_avail_space Zpool Available Space
# TYPE zfs_avail_space gauge
zfs_avail_space{zpool="backup"} 9698825433088.0
zfs_avail_space{zpool="jails"} 171691900928.0
# HELP zfs_used_space Zpool Used Space
# TYPE zfs_used_space gauge
zfs_used_space{zpool="backup"} 6244093169664.0
zfs_used_space{zpool="jails"} 75268718592.0
# HELP zfs_space_total Zpool Total Space
# TYPE zfs_space_total gauge
zfs_space_total{zpool="backup"} 15942918602752.0
zfs_space_total{zpool="jails"} 246960619520.0
# HELP zfs_scrub_repaired ZPool Scrub Repaired Bytes
# TYPE zfs_scrub_repaired gauge
zfs_scrub_repaired{zpool="backup"} 0.0
zfs_scrub_repaired{zpool="jails"} 0.0
# HELP zfs_scrub_errors ZPool Scrub Errors
# TYPE zfs_scrub_errors gauge
zfs_scrub_errors{zpool="backup"} 0.0
zfs_scrub_errors{zpool="jails"} 0.0
# HELP zfs_last_scrub ZPool Last Scrub Run
# TYPE zfs_last_scrub gauge
zfs_last_scrub{zpool="backup"} 1522564754.0
zfs_last_scrub{zpool="jails"} 1522555440.0
```
