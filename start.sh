#!/bin/bash
panel serve app.py --allow-websocket-origin=* --port=8888 --address=0.0.0.0 --allow-websocket-origin=$(hostname).mybinder.org