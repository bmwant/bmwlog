bmwlog
======
This is my simple blog written with Python 2.7 (bottle)
BmwLOG - *Most Wanted*'s blog.

Try visiting `the web-site <http://bmwlog.pp.ua/>`_ to see some boring articles.


Run Ansible provisioning manually

``ansible-playbook deploy/ansible/setup.yml -u vagrant -vv -i local/ansible/hosts -l vagrant --ask-pass``


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
