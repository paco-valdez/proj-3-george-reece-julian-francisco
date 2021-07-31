#!/bin/sh

ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/
ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post1.json" -T application/json http://localhost:5000/purchase 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post2.json" -T application/json http://localhost:5000/purchase 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post3.json" -T application/json http://localhost:5000/guild 