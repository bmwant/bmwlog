#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$(dirname "${DIR}")

function check_image_exists() {
  # Try to pull image provided as argument
  # Allow command to fail
  # Suppress any output to stdout/stderr
  # Print exit code. Zero exit code means that the image exists
  set +e
  docker pull $1 > /dev/null 2>&1
  local rc=$?
  set -e

  echo ${rc}
}

function get_current_tag() {
  # Assuming current working directory contains lock file
  TAG=$(sha1sum poetry.lock | awk '{ print $1 }')
  echo ${TAG}
}



