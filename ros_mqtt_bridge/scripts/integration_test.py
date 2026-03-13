#!/usr/bin/env python3
"""Simple integration test: subscribe to MQTT topics and assert messages arrive.

Usage: python3 integration_test.py --host localhost --port 1883 --prefix marinor --timeout 10

It waits for messages on:
  <prefix>/gps/location
  <prefix>/gps/heading
  <prefix>/system/battery
  <prefix>/system/autonomous

Exits 0 if all messages received within timeout, else 1.
"""
import time
import argparse
import json
import sys
from threading import Event
import paho.mqtt.client as mqtt

EXPECTED_TOPICS = [
    'gps/location',
    'gps/heading',
    'system/battery',
    'system/autonomous',
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--host', default='localhost')
    p.add_argument('--port', type=int, default=1883)
    p.add_argument('--prefix', default='marinor')
    p.add_argument('--timeout', type=int, default=10)
    args = p.parse_args()

    received = set()
    done = Event()

    def on_connect(client, userdata, flags, rc):
        for t in EXPECTED_TOPICS:
            client.subscribe(f"{args.prefix}/{t}")

    def on_message(client, userdata, msg):
        topic = msg.topic
        # strip prefix
        if topic.startswith(args.prefix + '/'):
            suffix = topic[len(args.prefix) + 1 :]
        else:
            suffix = topic
        if suffix in EXPECTED_TOPICS:
            received.add(suffix)
            print(f"Received {suffix}: {msg.payload.decode()}")
        if len(received) == len(EXPECTED_TOPICS):
            done.set()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(args.host, args.port)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        sys.exit(2)
    client.loop_start()

    success = done.wait(args.timeout)
    client.loop_stop()
    client.disconnect()

    missing = set(EXPECTED_TOPICS) - received
    if success:
        print('Integration test succeeded: all topics received')
        sys.exit(0)
    else:
        print('Integration test failed: missing topics:', ', '.join(sorted(missing)))
        sys.exit(1)


if __name__ == '__main__':
    main()
