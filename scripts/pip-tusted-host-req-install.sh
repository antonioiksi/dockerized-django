#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
	cmd="pip install $line --trusted-host 172.16.9.160"
	eval $cmd
done < "$1"