#!/bin/bash

cd /root/BOT || exit
git add .
git commit -m "Auto-push desde VPS: $(date '+%Y-%m-%d %H:%M:%S')" || exit
git push origin main
