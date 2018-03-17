#!/usr/bin/env bash
set -e

pushd "/data"
  for file in *.sql; do
    mysql -D bmwlogdb_test < "${file}"
  done;
popd
