bmwlog
======

.. image:: https://travis-ci.org/bmwant/bmwlog.svg?branch=master
    :target: https://travis-ci.org/bmwant/bmwlog

This is simple blog engine written with `bottle <https://bottlepy.org/docs/dev/>`_
(now only Python 3 comatible).

BmwLOG - some controversial thoughts from `bmwant <https://twitter.com/bmwant>`_.

Try visiting `the web-site <http://bmwlog.pp.ua/>`_ to see some boring articles.


Run local Ansible provisioning manually for your guest VM
(if using `Vagrant <https://www.vagrantup.com/>`_):

``ansible-playbook deploy/ansible/setup.yml -u vagrant -vv -i local/ansible/hosts -l vagrant --ask-pass``


Development
-----------

Install MySQL database first (`Ubuntu tutorial <https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04>`_)

.. code-block:: bash

    npm install
    pip install -r requirements.txt
    make tests
    make style-check
    export PYTHONPATH=`pwd`
    python run.py

Database migrations. Edit ``app/migrations/__main__.py`` and execute

.. code-block:: bash

    export PYTHONPATH=`pwd`
    python -m app.migrations


Deployment
----------

.. code-block:: bash

    make setup
    make update


License
-------

    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.

    In jurisdictions that recognize copyright laws, the author or authors
    of this software dedicate any and all copyright interest in the
    software to the public domain. We make this dedication for the benefit
    of the public at large and to the detriment of our heirs and
    successors. We intend this dedication to be an overt act of
    relinquishment in perpetuity of all present and future rights to this
    software under copyright law.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    For more information, please refer to `unlicense.org <http://unlicense.org>`_
