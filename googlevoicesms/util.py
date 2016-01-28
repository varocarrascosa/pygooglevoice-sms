import re
import sys
from xml.parsers.expat import ParserCreate
from time import gmtime
from datetime import datetime
from pprint import pprint
from urllib.request import build_opener, install_opener, HTTPCookieProcessor, Request, urlopen
from urllib.parse import urlencode, quote
from http.cookiejar import LWPCookieJar as CookieJar
from json import loads

sha1_re = re.compile(r'^[a-fA-F0-9]{40}$')

def print_(*values, **kwargs):
    """
    Implementation of Python3's print function
    
    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    
    file: a file-like object (stream); defaults to the current sys.stdout.
    sep:  string inserted between values, default a space.
    end:  string appended after the last value, default a newline.
    """
    fo = kwargs.pop('file', stdout)
    fo.write(kwargs.pop('sep', ' ').join(map(str, values)))
    fo.write(kwargs.pop('end', '\n'))
    fo.flush()

def is_sha1(s):
    """
    Returns ``True`` if the string is a SHA1 hash
    """
    return bool(sha1_re.match(s))

def validate_response(response):
    """
    Validates that the JSON response is A-OK
    """
    try:
        assert 'ok' in response and response['ok']
    except AssertionError:
        sys.stdout.write("Error, but login was successful. Did you setup a GV number?\n")
        sys.exit(0)

def load_and_validate(response):
    """
    Loads JSON data from http response then validates
    """
    validate_response(loads(response.read().decode('utf-8')))

class ValidationError(Exception):
    """
    Bombs when response code back from Voice 500s
    """

class LoginError(Exception):
    """
    Occurs when login credentials are incorrect
    """
    
class ParsingError(Exception):
    """
    Happens when XML feed parsing fails
    """
    
class JSONError(Exception):
    """
    Failed JSON deserialization
    """
    
    
class AttrDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]


class XMLParser(object):
    """
    XML Parser helper that can dig json and html out of the feeds. 
    The parser takes a ``Voice`` instance, page name, and function to grab data from. 
    Calling the parser calls the data function once, sets up the ``json`` and ``html``
    attributes and returns a ``Folder`` instance for the given page::
    
        >>> o = XMLParser(voice, 'voicemail', lambda: 'some xml payload')
        >>> o()
        ... <Folder ...>
        >>> o.json
        ... 'some json payload'
        >>> o.data
        ... 'loaded json payload'
        >>> o.html
        ... 'some html payload'
        
    """
    attr = None
        
    def start_element(self, name, attrs):
        if name in ('json','html'):
            self.attr = name
    def end_element(self, name): self.attr = None
    def char_data(self, data):
        if self.attr and data:
            setattr(self, self.attr, getattr(self, self.attr) + data)

    def __init__(self, voice, name, datafunc):
        self.json, self.html = '',''
        self.datafunc = datafunc
        self.voice = voice
        self.name = name
        
    def __call__(self):
        self.json, self.html = '',''
        parser = ParserCreate()
        parser.StartElementHandler = self.start_element
        parser.EndElementHandler = self.end_element
        parser.CharacterDataHandler = self.char_data
        try:
            data = self.datafunc()
            parser.Parse(data, 1)
        except:
            raise ParsingError
        return self.folder

    def folder(self):
        """
        Returns associated ``Folder`` instance for given page (``self.name``)
        """
        return Folder(self.voice, self.name, self.data)        
    folder = property(folder)
    
    def data(self):
        """
        Returns the parsed json information after calling the XMLParser
        """
        try:
            return loads(self.json)
        except:
            raise JSONError
    data = property(data)
    
