#!/bin/sh

ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/
ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword
