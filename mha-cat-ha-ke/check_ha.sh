while true
do
 if [ `ps -C haproxy --no-header | wc -l` -eq 0 ]; then
  systemctl stop keepalived
 else
  systemctl start keepalived
 else
 fi
sleep 5
done
