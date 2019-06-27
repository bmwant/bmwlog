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
  # Assuming current working directory contains
  # poetry.lock package-lock.json files
  TAG=$(set -o pipefail && cat poetry.lock package-lock.json | sha1sum | awk '{ print $1 }')
  local rc=$?
  if [[ ${rc} -ne 0 ]]; then
    exit ${rc}
  fi
  echo ${TAG}
}
