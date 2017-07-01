bmwlog
======
This is my simple blog written with Python 2.7 (bottle)
BmwLOG - *Most Wanted*'s blog.

Try visiting `the web-site <http://bmwlog.pp.ua/>`_ to see some boring articles.


Run Ansible provisioning manually

``ansible-playbook local/ansible/setup.yml -u vagrant -vv -i local/ansible/hosts -l vagrant --ask-pass``


Development
-----------

.. code-block:: bash

    make install

    make tests
    make style-check


Deployment
----------

.. code-block:: bash

    make setup
    make update
