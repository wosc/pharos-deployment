#!/bin/bash
# https://gist.github.com/cherti/61ec48deaaab7d288c9fcf17e700853a
# https://github.com/prometheus/alertmanager/issues/437

name=$RANDOM
url='http://localhost:9093/api/v1/alerts'

echo "Firing up alert $name"
curl -XPOST $url -d "[{
    \"status\": \"firing\",
    \"labels\": {
        \"alertname\": \"$name\",
        \"service\": \"my-service\",
        \"severity\":\"warning\",
        \"instance\": \"$name.example.net\"
    },
    \"annotations\": {
        \"summary\": \"High latency is high!\"
    },
    \"generatorURL\": \"http://prometheus.example.net/<expression>\"
}]"
echo ""

echo "Press enter to resolve alert"
read

echo "Sending resolve"
curl -XPOST $url -d "[{
    \"status\": \"resolved\",
    \"labels\": {
        \"alertname\": \"$name\",
        \"service\": \"my-service\",
        \"severity\":\"warning\",
        \"instance\": \"$name.example.net\"
    },
    \"annotations\": {
        \"summary\": \"High latency is high!\"
    },
    \"generatorURL\": \"http://prometheus.example.net/<expression>\"
}]"
echo ""
