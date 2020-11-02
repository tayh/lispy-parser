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
                | BOOLEAN -> bool
                | NAME -> name
                | CHAR -> char

            NAME   : /[a-zA-Z][-?\w]*/ | /[-+=\/*<><=]+/
            STRING : /\"[^"\\]*(\\[^\n\t\r\f][^"\\]*)*\"/
            NUMBER : /\+?\-?\d+(\.\d*)?([eE][+-]?\d+)?/
            BOOLEAN: /\#t|\#f/
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

   
    def name(self, tk):
        return Symbol(tk)

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

exemplos = [
    "(max 1 2)"

    r"""
       ;; Fatorial
       (define fat (lambda (n) 
           (if (<= n 1)
               1
               (* n (fat (- n 1))))))
       (print (fat 5))
    """
]
for exemplo in exemplos:
    transformer = LispyTransformer()
    tree = grammar.parse(exemplo)
    print(tree.pretty())
    lispy = transformer.transform(tree)
    print(lispy)
    print('-' * 50)
