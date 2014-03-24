stratulat-barbulescu
====================

Python Server dependency list:

* [python-setuptools](https://pypi.python.org/pypi/setuptools) - you can install it in Ubuntu/Fedora using apt/yum. 
* [pytz](http://pytz.sourceforge.net/) - can be installed using setuptools:


```sh
sudo easy_install pytz
```

* [web.py](http://webpy.org) - can be also installed using setuptools

```sh
sudo easy_install web.py
```

* [python-mysqldb](http://mysql-python.sourceforge.net/) - can be installed in Ubuntu/Fedora using apt/yum. 

Running the server
---------

You can run the server easily by starting `main.py` from the `pyserver` folder

```sh
python main.py
```

By default it will start on port `8080`, so if `8080` is busy, you can start it on different port:

```sh
python main.py 8000
```
