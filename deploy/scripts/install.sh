#!/usr/bin/env bash

if [[ -z $(vagrant box list | grep freebsd)  ]]; then
    echo "Adding FreeBSD vagrant box"
    vagrant box add freebsd http://iris.hosting.lv/freebsd-10.1-i386.box
fi

vagrant up
