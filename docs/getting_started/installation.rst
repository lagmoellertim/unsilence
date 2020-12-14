************
Installation
************

To install unsilence as a command line tool, you can use `pipx <https://pipxproject.github.io/pipx/>`_.

.. code-block:: bash

   # Installing pipx
   $ pip install pipx

   # Installing Unsilence as Command Line Software
   $ pipx install unsilence

   # If pipx asks you to, you also need to execute the following line
   # as well as close and reopen your terminal window
   $ pipx ensurepath

If you just want to use it as a python library, you could install it using pip.

.. code-block:: bash

   # Installing Unsilence as Command Line Software
   $ pip install unsilence

To install the command line tool directly from the GitHub source, you can use this:

.. code-block:: bash

   # Clone the repository (stable branch)
   $ git clone -b master https://github.com/lagmoellertim/unsilence.git unsilence

   # Change Directory
   $ cd unsilence

   # Install pip packages
   $ pip install -r requirements.txt
   $ pip install pipx

   # If pipx asks you to, you also need to execute the following line
   # as well as close and reopen your terminal window
   $ pipx ensurepath

   # Install unsilence package
   $ pipx install .


To install the library from the GitHub source, you can use this:

.. code-block:: bash

   # Clone the repository (stable branch)
   $ git clone -b master https://github.com/lagmoellertim/unsilence.git unsilence

   #Change Directory
   $ cd unsilence

   # Install pip packages
   $ pip install -r requirements.txt

   # Install unsilence package
   $ python3 setup.py install