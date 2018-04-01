#!/usr/bin/python
# Collects the same metrics as `node_exporter --collector.supervisord`
# (see https://github.com/prometheus/node_exporter/blob/master
#  /collector/supervisord.go) but via unix socket instead of HTTP.
import os
import supervisor.xmlrpc
import time
import xmlrpclib

OUTPUT = '/srv/prometheus/node/supervisord.prom'
METRIC_TYPES = {'up': 'gauge', 'state': 'gauge', 'exit_status': 'gauge',
                'uptime': 'counter'}
RUNNING_STATES = ['STARTING', 'RUNNING', 'STOPPING']


def write(out, now, labels, name, value):
    labels = ','.join('%s="%s"' % (key, value)
                      for key, value in labels.items())
    out.write('supervisord_{name} {{{labels}}} {value} {ts}\n'.format(
        name=name, value=value, ts=now, labels=labels))


# https://stackoverflow.com/a/11746051
api = xmlrpclib.ServerProxy(
    'http://127.0.0.1', transport=supervisor.xmlrpc.SupervisorTransport(
        None, None, serverurl='unix:///var/run/supervisor.sock'))
info = api.supervisor.getAllProcessInfo()

now = int(time.time() * 1000)
with open(OUTPUT + '.tmp', 'w') as out:
    for name, typ in METRIC_TYPES.items():
        out.write('# TYPE supervisord_%s %s\n' % (name, typ))
    for program in info:
        labels = {'name': program['name'], 'group': program['group']}
        is_running = 1 if program['statename'] in RUNNING_STATES else 0
        write(out, now, labels, 'up', is_running)
        write(out, now, labels, 'state', program['state'])
        write(out, now, labels, 'exit_status', program['exitstatus'])
        uptime = program['now'] - program['start']
        if not is_running:
            uptime = 0
        write(out, now, labels, 'uptime', uptime)
os.rename(OUTPUT + '.tmp', OUTPUT)
