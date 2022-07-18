#!/bin/sh
while true;
do
  NOW=$(date +"%H:%M:%S")
  echo "The current time is: ${NOW}"
  if [ -e "client/check_users.sh" ]; then
    echo "Running check_users.sh script..."
    /client/check_users.sh
  fi
  sleep 5
done
