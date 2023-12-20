#!/bin/bash
echo starting;
touch /tmp/healthy;
echo about to sleep; 
sleep 3600; 
rm -f /tmp/healthy; 
echo removed file;
sleep 10