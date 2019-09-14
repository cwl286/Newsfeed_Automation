#!/bin/bash
REMOTEHOST=$1
REMOTEPORT=$2
TIMEOUT=1
shift 2
cmd="$@"

wait_time=10s

# keep waiting for the database docker to be running
while ! nc -w $TIMEOUT -z $REMOTEHOST $REMOTEPORT; do
>&2 echo "Connection to ${REMOTEHOST}:${REMOTEPORT} failed. Exit code from Netcat was ($?)."

done

# wait for SQL Server to come up
echo Waiting for database $wait_time...
sleep $wait_time

>&2 echo "${REMOTEHOST}:${REMOTEPORT} is up -executing command"

# run the command
exec $cmd