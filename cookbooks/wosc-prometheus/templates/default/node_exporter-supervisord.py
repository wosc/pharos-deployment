#!/usr/bin/python
# Collects the same metrics as `node_exporter --collector.supervisord`
# (see https://github.com/prometheus/node_exporter/blob/master
#  /collector/supervisord.go) but via unix socket instead of HTTP.
import os
import supervisor.xmlrpc
import xmlrpclib

OUTPUT = '/srv/prometheus/node/supervisord.prom'
METRIC_TYPES = {'up': 'gauge', 'state': 'gauge', 'exit_status': 'gauge',
                'uptime': 'counter'}
RUNNING_STATES = ['STARTING', 'RUNNING', 'STOPPING']


def write(out, labels, name, value):
    labels = ','.join('%s="%s"' % (key, value)
                      for key, value in labels.items())
    out.write('supervisord_{name} {{{labels}}} {value}\n'.format(
        name=name, value=value, labels=labels))


# https://stackoverflow.com/a/11746051
api = xmlrpclib.ServerProxy(
    'http://127.0.0.1', transport=supervisor.xmlrpc.SupervisorTransport(
        None, None, serverurl='unix:///var/run/supervisor.sock'))
info = api.supervisor.getAllProcessInfo()

with open(OUTPUT + '.tmp', 'w') as out:
    for name, typ in METRIC_TYPES.items():
        out.write('# TYPE supervisord_%s %s\n' % (name, typ))
    for program in info:
        labels = {'name': program['name'], 'group': program['group']}
        is_running = 1 if program['statename'] in RUNNING_STATES else 0
        write(out, labels, 'up', is_running)
        write(out, labels, 'state', program['state'])
        write(out, labels, 'exit_status', program['exitstatus'])
        uptime = program['now'] - program['start']
        if not is_running:
            uptime = 0
        write(out, labels, 'uptime', uptime)
os.rename(OUTPUT + '.tmp', OUTPUT)
