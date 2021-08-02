#!/bin/sh

ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post1.json" -T application/json http://localhost:5000/purchase 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post2.json" -T application/json http://localhost:5000/purchase 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post3.json" -T application/json http://localhost:5000/guild 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post4.json" -T application/json http://localhost:5000/guild 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post5.json" -T application/json http://localhost:5000/guild 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post6.json" -T application/json http://localhost:5000/guild 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post7.json" -T application/json http://localhost:5000/guild 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post8.json" -T application/json http://localhost:5000/purchase 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post9.json" -T application/json http://localhost:5000/purchase 
ab -n 10 -H "Host: user1.comcast.com" -p "/w205/proj-3-george-reece-julian-francisco/baseline/postfiles/post10.json" -T application/json http://localhost:5000/purchase 
