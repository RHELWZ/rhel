#!/bin/bash
/root/bin/redis-trib.rb  create --replicas  1  192.168.1.31:6379  192.168.1.32:6379 192.168.1.33:6379  192.168.1.34:6379 192.168.1.35:6379  192.168.1.36:6379 <<EOF
yes
EOF