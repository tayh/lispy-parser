import re
from lark import Lark, InlineTransformer, v_args
from typing import NamedTuple


class Symbol(NamedTuple):
    value: str


grammar = Lark(
    r"""
        ?start : expr+

            ?expr : atom
                | list
                | quote 
            

            list  : "(" expr+ ")"

            quote : "'" expr
            
            ?atom : STRING -> string
                | NUMBER -> num
                | SYMBOL -> symbol
                | BOOLEAN -> bool
                | NAME -> name
                | CHAR -> char

            STRING : /\"[^"\\]*(\\[^\n\t\r\f][^"\\]*)*\"/
            SYMBOL : /[-+=\/*!@$^&~<>?<=]+/
            NUMBER : /\+?\-?\d+(\.\d*)?([eE][+-]?\d+)?/
            BOOLEAN: /\#t|\#f/
            NAME   : /[a-zA-Z][-?\w]*/
            CHAR   : /\#\\[\w]+|\d+/

            %ignore /\s+/
            %ignore /\;([^\n\r]+)/
    """
)


class LispyTransformer(InlineTransformer):
    CHARS = {
        "altmode": "\x1b",
        "backnext": "\x1f",
        "backspace": "\b",
        "call": "SUB",
        "linefeed": "\n",
        "page": "\f",
        "return": "\r",
        "rubout": "\xc7",
        "space": " ",
        "tab": "\t",
    }

    def atom(self, tk):
        return tk
    
    def comment(self, tk):
        return tk

    def number(self, tk):
        return float(tk)

    def true(self):
        return True
    
    def false(self):
        return False
    
    def null(self):
        return None

    def array(self, *args):
        return list(args)

    def object(self, *args):
        raise NotImplementedError


