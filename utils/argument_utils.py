import argparse
from argparse import Namespace

class ArgumentUtils:
    def __init__(self):
        self.__parser = argparse.ArgumentParser()
    
    def get_argument_token(self) -> str | None:
        '''Check if the user provided a token argument.
        
        Return the token if given, otherwise return None'''
        
        self.__parser.add_argument("-t", "--token", help="Token value given by the user", type=str)
        args = self.__parser.parse_args()
        if args.token:
            return args.token
        else:
            return None