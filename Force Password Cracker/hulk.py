#!/usr/bin/env python3

import functools
import hashlib
import itertools
import multiprocessing
import os
import string
import sys

# Constants

ALPHABET    = string.ascii_lowercase + string.digits
ARGUMENTS   = sys.argv[1:]
CORES       = 1
HASHES      = 'hashes.txt'
LENGTH      = 1
PREFIX      = ''
multi = False

# Functions

def usage(exit_code=0):
    print('''Usage: {} [-a alphabet -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file'''.format(os.path.basename(sys.argv[0])))
    sys.exit(exit_code)

def sha1sum(s):
    ''' Generate sha1 digest for given string.

    >>> sha1sum('abc')
    'a9993e364706816aba3e25717850c26c9cd0d89d'

    >>> sha1sum('wake me up inside')
    '5bfb1100e6ef294554c1e99ff35ad11db6d7b67b'

    >>> sha1sum('baby now we got bad blood')
    '9c6d9c069682759c941a6206f08fb013c55a0a6e'
    '''
    s = s.encode()
    hashObject = hashlib.sha1(s)
    return hashObject.hexdigest()

def permutations(length, alphabet=ALPHABET):
    ''' Recursively yield all permutations of alphabet up to provided length.

    >>> list(permutations(1, 'ab'))
    ['a', 'b']

    >>> list(permutations(2, 'ab'))
    ['aa', 'ab', 'ba', 'bb']

    >>> list(permutations(1))       # doctest: +ELLIPSIS
    ['a', 'b', ..., '9']

    >>> list(permutations(2))       # doctest: +ELLIPSIS
    ['aa', 'ab', ..., '99']

    >>> import inspect; inspect.isgeneratorfunction(permutations)
    True
    '''
    #Base Case
    if length == 1:
        yield from alphabet

    #Recursive Call    
    else:
        for letter in alphabet:
            for s in  permutations(length - 1, alphabet):
                yield letter + s

def smash(hashes, length, alphabet=ALPHABET, prefix=PREFIX):
    ''' Return all password permutations of specified length that are in hashes

    >>> smash([sha1sum('ab')], 2)
    ['ab']

    >>> smash([sha1sum('abc')], 2, prefix='a')
    ['abc']

    >>> smash(map(sha1sum, 'abc'), 1, 'abc')
    ['a', 'b', 'c']
    '''
    candidate = ( prefix + m for m in permutations(length, alphabet) ) #Adds the prefix using a generator
    return [ m for m in candidate if sha1sum(m) in hashes ] #Returns the matches in a list using LC

# Main Execution
if __name__ == '__main__':

    # Parse command line arguments
    while len(ARGUMENTS) and ARGUMENTS[0].startswith('-') and len(ARGUMENTS[0]) > 1:
        arg = ARGUMENTS.pop(0)
        if arg == '-a':
            ALPHABET = ARGUMENTS.pop(0)
        elif arg == '-c':
            CORES = int(ARGUMENTS.pop(0))
        elif arg == '-l':
            LENGTH = int(ARGUMENTS.pop(0))
        elif arg == '-p':
            PREFIX = ARGUMENTS.pop(0)
        elif arg == '-s':
            HASHES = ARGUMENTS.pop(0)
        elif arg == '-h':
            usage(0)
        else:
            usage(1)

    if CORES > 1 and LENGTH > 1:
        multi = True

    # Load hashes set
    hashes = set(hashItem.strip() for hashItem in open(HASHES, "r"))

    # Execute smash function
    if multi:
        pool = multiprocessing.Pool(CORES)
        subsmash = functools.partial(smash, hashes, LENGTH-1, ALPHABET)
        prefixes = ( PREFIX+let for let in ALPHABET  )
        match = itertools.chain.from_iterable(pool.imap(subsmash, prefixes))
    if not multi:
        match = smash(hashes, LENGTH, ALPHABET, PREFIX)

    # Print passwords
    for item in match:
        print(item)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
