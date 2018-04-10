import subprocess
import itertools
import datetime
import time
import logging
import os
from multiprocessing import Process, Manager
from prometheus_client import start_http_server, Summary
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from subprocess import call


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Set ZPOOLS to scan
if os.environ.get('ZPOOLS') is not None:
    ZPOOLS = os.getenv('ZPOOLS').split(',')
    print("Using these zpools %s.",ZPOOLS)
else:
    print("Collecting all available zpools.")
    result = subprocess.run(["zpool list | tail -n +2 | awk '{print $1}'"], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    ZPOOLS = result.stdout.splitlines()
    print("Found these zpools %s.",ZPOOLS)


class ZpoolStatsCollector(object):
    @REQUEST_TIME.time()
    def collect(self):
        sys_metrics = {
            'health_status': GaugeMetricFamily('zfs_health_status', 'ZPool Health Status', labels=['zpool','status','name']),
            'read_errors': GaugeMetricFamily('zfs_read_errors', 'ZPool Read Errors', labels=['zpool','name']),
            'write_errors': GaugeMetricFamily('zfs_write_errors', 'ZPool Write Errors', labels=['zpool','name']),
            'chksum_errors': GaugeMetricFamily('zfs_chksum_errors', 'ZPool Checksum Errors', labels=['zpool','name']),
            'scrub_process': GaugeMetricFamily('zfs_scrub_process', 'ZPool Scrub is in Process', labels=['zpool','name']),
            'space_available': GaugeMetricFamily('zfs_avail_space', 'Zpool Available Space', labels=['zpool','name']),
            'used_space': GaugeMetricFamily('zfs_used_space', 'Zpool Used Space', labels=['zpool','name']),
            'space_total': GaugeMetricFamily('zfs_space_total', 'Zpool Total Space', labels=['zpool','name']),
            'scrub_repaired': GaugeMetricFamily('zfs_scrub_repaired', 'ZPool Scrub Repaired Bytes', labels=['zpool','name']),
            'scrub_errors': GaugeMetricFamily('zfs_scrub_errors', 'ZPool Scrub Errors', labels=['zpool','name']),
            'last_scrub': GaugeMetricFamily('zfs_last_scrub', 'ZPool Last Scrub Run', labels=['zpool','name'])
        }
        for pool in ZPOOLS:

            # zpool disk size metrics
            logging.info("Collecting zpool disk size stats for %s", pool)
            proc = subprocess.Popen('zpool list -p -H {0}'.format(pool),shell=True, stdout=subprocess.PIPE,universal_newlines=True)
            out = proc.communicate()[0]
            usage = [x.replace('\t', ' ').strip() for x in out.strip().split()]
            sys_metrics['space_available'].add_metric([pool], float(usage[3]))
            sys_metrics['used_space'].add_metric([pool], float(usage[2]))
            sys_metrics['space_total'].add_metric([pool], float(usage[1]))

            # scrub metrics
            logging.info("Collecting zpool scrub stats for %s", pool)
            proc = subprocess.Popen('zpool status {0} | grep "scan"'.format(pool),shell=True, stdout=subprocess.PIPE,universal_newlines=True)
            out = proc.communicate()[0]
            scrub = [x.replace('\t', ' ').strip() for x in out.strip().split()]
            if len(scrub) > 3:
                if scrub[3] in "progress":
                     sys_metrics['scrub_process'].add_metric([pool], float(1))
                     date_text = scrub[9] + "-" + scrub[6] + "-" + scrub[7].zfill(2) + "_" +scrub[8]
                     date = time.mktime(datetime.datetime.strptime(date_text, "%Y-%b-%d_%H:%M:%S").timetuple())
                     sys_metrics['last_scrub'].add_metric([pool], float(date))
                elif scrub[1] in "scrub":
                    sys_metrics['scrub_repaired'].add_metric([pool], float(scrub[3]))
                    sys_metrics['scrub_errors'].add_metric([pool], float(scrub[9]))
                    date_text = scrub[16] + "-" + scrub[13] + "-" + scrub[14].zfill(2) + "_" +scrub[15]
                    date = time.mktime(datetime.datetime.strptime(date_text, "%Y-%b-%d_%H:%M:%S").timetuple())
                    sys_metrics['last_scrub'].add_metric([pool], float(date))
            else:
                x = datetime.datetime.now()
                sys_metrics['scrub_repaired'].add_metric([pool], float(0))
                sys_metrics['scrub_errors'].add_metric([pool], float(0))
                date = x.strftime("%Y-%b-%d_%H:%M:%S")
                sys_metrics['last_scrub'].add_metric([pool], float(0))


            # zpool read write error metrics
            logging.info("Collecting zpool read and write stats for %s", pool)
            proc = subprocess.Popen('zpool status {0} | egrep "(ONLINE|DEGRADED|FAULTED|UNAVAIL|REMOVED)[ \t]+[0-9]+"'.format(pool),shell=True, stdout=subprocess.PIPE)
            out = proc.communicate()[0]
            zpoolErrorMetrics = [x.replace('\t', ' ').strip() for x in out.decode().strip().split()]

            all_metrics = list(itertools.zip_longest(*[iter(zpoolErrorMetrics)] * 5, fillvalue=""))
            for metrics in all_metrics:
                name = metrics[0]
                health = metrics[1]
                if health in "ONLINE":
                    sys_metrics['health_status'].add_metric([pool,health,name], 1)
                else:
                    sys_metrics['health_status'].add_metric([pool,health,name], 0)
                readErrors = metrics[2]
                sys_metrics['read_errors'].add_metric([pool,name], float(readErrors))
                writeErrors = metrics[3]
                sys_metrics['write_errors'].add_metric([pool,name], float(writeErrors))
                chksumErrors = metrics[4]
                sys_metrics['chksum_errors'].add_metric([pool,name], float(chksumErrors))

        for metric in sys_metrics.values():
            yield metric


def main():
    REGISTRY.register(ZpoolStatsCollector())
    start_http_server(8000)
    while True:
        time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(format='ts=%(asctime)s level=%(levelname)s msg=%(message)s', level=logging.DEBUG)
    main()