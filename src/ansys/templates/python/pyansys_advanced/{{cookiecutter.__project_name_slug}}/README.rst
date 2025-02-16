Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }}
{{ '=' * (cookiecutter.__project_name_slug | length) }}
|pyansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/{{cookiecutter.__project_name_slug}}?logo=pypi
   :target: https://pypi.org/project/{{cookiecutter.__project_name_slug}}/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/{{cookiecutter.__project_name_slug}}.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/{{cookiecutter.__project_name_slug}}
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/pyansys/{{cookiecutter.__project_name_slug}}/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/pyansys/{{cookiecutter.__project_name_slug}}
   :alt: Codecov

.. |GH-CI| image:: https://github.com/pyansys/{{cookiecutter.__project_name_slug}}/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/pyansys/{{cookiecutter.__project_name_slug}}/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black


{{ cookiecutter.short_description }}


How to install
--------------

At least two installation modes are provided: user and developer.

For users
^^^^^^^^^

In order to install Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }}, make sure you
have the latest version of `pip`_. To do so, run:

.. code:: bash

    python -m pip install -U pip

Then, you can simply execute:

{% if cookiecutter.build_system in ["flit", "setuptools"] -%}

.. code:: bash

    python -m pip install {{ cookiecutter.__pkg_name }}

{% elif cookiecutter.build_system == "poetry" -%}

.. code:: bash

    poetry run python -m pip install {{ cookiecutter.__pkg_name }}

{% endif -%}


For developers
^^^^^^^^^^^^^^

Installing Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }} in developer mode allows
you to modify the source and enhance it.

Before contributing to the project, please refer to the `PyAnsys Developer's guide`_. You will
need to follow these steps:

#. Start by cloning this repository:

   .. code:: bash

      git clone {{ cookiecutter.repository_url }}

#. Create a fresh-clean Python environment and activate it:

   .. code:: bash

      # Create a virtual environment
      python -m venv .venv

      # Activate it in a POSIX system
      source .venv/bin/activate

      # Activate it in Windows CMD environment
      .venv\Scripts\activate.bat

      # Activate it in Windows Powershell
      .venv\Scripts\Activate.ps1

#. Make sure you have the latest required build system and doc, testing, and CI tools:

   .. code:: bash

      python -m pip install -U pip {{ cookiecutter.build_system }} tox
      python -m pip install -r requirements/requirements_build.txt
      python -m pip install -r requirements/requirements_doc.txt
      python -m pip install -r requirements/requirements_tests.txt


#. Install the project in editable mode:

    {% if cookiecutter.build_system in ["flit", "setuptools"] -%}

   .. code:: bash

      python -m pip install --editable {{ cookiecutter.__pkg_name }}

    {% elif cookiecutter.build_system == "poetry" -%}

   .. code:: bash

      poetry run python -m pip install {{ cookiecutter.__pkg_name }}

    {% endif -%}

#. Finally, verify your development installation by running:

   .. code:: bash

      tox


How to testing
--------------

This project takes advantage of `tox`_. This tool allows to automate common
development tasks (similar to Makefile) but it is oriented towards Python
development.

Using tox
^^^^^^^^^

As Makefile has rules, `tox`_ has environments. In fact, the tool creates its
own virtual environment so anything being tested is isolated from the project in
order to guarantee project's integrity. The following environments commands are provided:

- **tox -e style**: will check for coding style quality.
- **tox -e py**: checks for unit tests.
- **tox -e py-coverage**: checks for unit testing and code coverage.
- **tox -e doc**: checs for documentation building process.


Raw testing
^^^^^^^^^^^

If required, you can always call the style commands (`black`_, `isort`_,
`flake8`_...) or unit testing ones (`pytest`_) from the command line. However,
this does not guarantee that your project is being tested in an isolated
environment, which is the reason why tools like `tox`_ exist.


A note on pre-commit
^^^^^^^^^^^^^^^^^^^^

The style checks take advantage of `pre-commit`_. Developers are not forced but
encouraged to install this tool via:

.. code:: bash

    python -m pip install pre-commit && pre-commit install


Documentation
-------------

For building documentation, you can either run the usual rules provided in the
`Sphinx`_ Makefile, such us:

.. code:: bash

    make -C doc/ html && your_browser_name doc/html/index.html

However, the recommended way of checking documentation integrity is using:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/index.html


Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements and then executing the build module:

.. code:: bash

    python -m pip install -r requirements/requirements_build.txt
    python -m build
    python -m twine check dist/*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
