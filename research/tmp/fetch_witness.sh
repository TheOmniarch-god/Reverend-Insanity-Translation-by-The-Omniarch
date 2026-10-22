#!/bin/bash
ch=$1
id=$((5346144 + ch - 906))
curl -s --max-time 30 -o /tmp/witness/ch$ch.html "https://www.hetushu.com/book/7640/$id.html"
