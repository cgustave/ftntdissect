# ftntdissect

## Disclaimer

This is not a Fortinet official product. It is provided as-is without official support.
I have made this tool for my own use. It can be used at your own risk.

## Author :

Cedric GUSTAVE

## Install

Python package is provided via Pypi, install with pip:

~~~
(venv) /tmp$ python3 -m pip install ftntdissect
Collecting ftntdissect
  Downloading ftntdissect-1.1-py3-none-any.whl (7.9 kB)
Installing collected packages: ftntdissect
Successfully installed ftntdissect-1.1
(venv) /tmp$ 
~~~

## Usage

Provides a library to search within a FortiGate configuration file. 
Searches a made in the global or vdom sections by providing consecutive config scoping criteria reducing the range of line to search.
Once in the expected config and or edit block, keys can be matched and values from the config statement can be extracted. 

To start, create an instance of ftntdissect objects provind a configuration file.  
Call parse() to initialize. 
Once done, query the config by refining the configuration scopesets and search for configuaration keys,  
Use feedback method to return information

Use insert or delete methods to update the configuration file. 

## Examples

For examples, check the test file at ftntdissect/tests/test_ftntdissect.py

