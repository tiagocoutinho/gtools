# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

import urllib.parse
import xmlrpc.client

from geventhttpclient.httplib import HTTPConnection, HTTPSConnection


class Transport(xmlrpc.client.Transport):

    def make_connection(self, host):
        #return an existing connection if possible.  This allows
        #HTTP/1.1 keep-alive.
        if self._connection and host == self._connection[0]:
            return self._connection[1]
        # create a HTTP connection object from a host descriptor
        chost, self._extra_headers, x509 = self.get_host_info(host)
        self._connection = host, HTTPConnection(chost)
        return self._connection[1]


class SafeTransport(xmlrpc.client.SafeTransport):

    def make_connection(self, host):
        if self._connection and host == self._connection[0]:
            return self._connection[1]
        # create a HTTPS connection object from a host descriptor
        # host may be a string, or a (host, x509-dict) tuple
        chost, self._extra_headers, x509 = self.get_host_info(host)
        self._connection = host, HTTPSConnection(chost,
            None, context=self.context, **(x509 or {}))
        return self._connection[1]


class ServerProxy(xmlrpc.client.ServerProxy):

    def __init__(self, uri, transport=None, encoding=None, verbose=False,
                 allow_none=False, use_datetime=False, use_builtin_types=False,
                 *, headers=(), context=None):
        if transport is None:
            p = urllib.parse.urlsplit(uri)
            if p.scheme not in ("http", "https"):
                raise OSError("unsupported XML-RPC protocol")
            if p.scheme == "https":
                handler = SafeTransport
                extra_kwargs = dict(context=context)
            else:
                handler = Transport
                extra_kwargs = {}
            transport = handler(use_datetime=use_datetime,
                                use_builtin_types=use_builtin_types,
                                headers=headers,
                                **extra_kwargs)
        super().__init__(
            uri, transport=transport, encoding=encoding, verbose=verbose,
            allow_none=allow_none, use_datetime=use_datetime,
            use_builtin_types=use_builtin_types, headers=headers,
            context=context)


Server = ServerProxy
