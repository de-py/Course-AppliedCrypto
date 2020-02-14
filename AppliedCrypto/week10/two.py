#!/usr/bin/env python
import rypto
import sha1
import os


if __name__ == "__main__":

    keys = os.urandom(16)
    message = 'Well this is a message'

    pre_mac = keys + message

    mac = sha1.sha1(pre_mac)

    print 'Keyed mac = ' + mac
