#!/bin/bash

# Hypercorn 프로세스를 찾습니다.
PIDS=$(pgrep -f hypercorn)

# 프로세스가 없는 경우 메시지를 출력합니다.
if [ -z "$PIDS" ]; then
    echo "No Hypercorn process found."
    exit 0
fi

# Hypercorn 프로세스를 종료합니다.
echo "Stopping Hypercorn processes..."
for PID in $PIDS; do
    echo "Killing process ID $PID"
    kill $PID
done

# 프로세스가 종료되었는지 확인합니다.
sleep 2
PIDS=$(pgrep -f hypercorn)
if [ -z "$PIDS" ]; then
    echo "All Hypercorn processes stopped successfully."
else
    echo "Some Hypercorn processes could not be stopped. Force killing..."
    for PID in $PIDS; do
        echo "Force killing process ID $PID"
        kill -9 $PID
    done
fi

echo "Hypercorn processes have been stopped."