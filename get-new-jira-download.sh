#!/bin/bash

function log () {
  echo "$(date +"%b %e %T") $@"
  logger -- $(basename $0)" - $@"
}

function check_last_command () {
  if [[ $? == 0 ]] ; then
    log "$1 was successful"
  else
    log "$1 was unsuccessful"
    exit 1
  fi
}

function download_jira () {
  if [[ -s "$1/$2" ]] ; then
    log "The version of Jira has already been downloaded to $1/$2"
    exit 0
  else
    wget -O "$1/$2" "https://www.atlassian.com/software/jira/downloads/binary/$2.gz"
    check_last_command "DOWNLOAD_JIRA"
  fi
}

function upload_to_s3 () {
  aws s3 cp "$1/$2" "s3://$3/$2"
  check_last_command "Upload to S3"
}

version="8.2.1"
download_dir="/tmp"
bucket_loc="com.leadx.puppet/jira"
filename="atlassian-jira-software-$version.tar"

download_jira "$download_dir" "$filename"
upload_to_s3 "$download_dir" "$filename" "$bucket_loc"
