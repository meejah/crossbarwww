An *Endpoint* describes the network connection over which data is transmitted. *Endpoints* are used as part of *Transport* definitions, e.g.

``` javascript
{
   "type": "websocket",
   "endpoint": {
      "type": "tcp",
      "port": 8080
   }
}
```

defines a *WebSocket Transport*, that will listen on TCP port 8080 for incoming WAMP connections.

*Endpoints* are used in different places for **Crossbar**.io configuration. E.g. a *Router* *Transport* will (usually) specify at least one listening *Endpoint* for clients to connect. A component *Container* must specify the *Router* to connect to, and hence will provide configuration for a connecting *Endpoint*.

## Endpoint Types

**Crossbar**.io currently implements two types of *Endpoints*:

* TCP (and TLS)
* Unix Domain Socket

which each come in two flavors:

* listening
* connecting


### TCP Endpoints

TCP *Endpoints* come in two flavors: listening and connecting *Endpoints*.

A listening TCP *Endpoint* accepts incoming connections over TCP (or TLS) from clients. A connecting TCP *Endpoint* establishes a connection over TCP (or TLS) to a server.

#### TCP Listening Endpoints

Here is an *Endpoint* that is listening on TCP port 8080 (on all network interfaces):

```javascript
"endpoint": {
   "type": "tcp",
   "port": 8080
}
```

TCP listening *Endpoints* can be configured using the following parameters:

Option | Description
-----|------
**`type`** | must be `"tcp"` (*required*)
**`port`** | the TCP port to listen on (*required*)
**`version`** | the IP protocol version to speak - either `4` or `6` (default: **4**)
**`interface`** | optional interface to listen on, e.g. `127.0.0.1` to only listen on IPv4 loopback or `::1` to only listen on IPv6 loopback.
**`backlog`** | optional accept queue depth of listening endpoints (default: **50**)
**`shared`** | flag which controls sharing the socket between multiple workers - this currently only works on Linux >= 3.9 (default: **false**)
**`tls`** | optional endpoint TLS configuration. If present, this is a dict containing keys: `key`: file path; `certificate`: file path; `dhparam`: (optional) file path; `ciphers`: (optional) list of strings. Relative paths are allowed, based from the directory the config file is in.

#### TCP Connecting Endpoints

Here is an *Endpoint* that is connecting over TCP to `localhost` on port 8080:

```javascript
"endpoint": {
   "type": "tcp",
   "host": "localhost",
   "port": 8080
}
```

Here is a listening *Endpoint* that uses TLS (note there's "interface" instead of "host"):

```javascript
"endpoint": {
    "type": "tcp",
    "interface": "127.0.0.1",
    "port": 443,
    "tls": {
        "key": "server.key",
        "certificate": "server.crt"
    }
```
TCP connecting *Endpoints* can be configured using the following parameters:

Option | Description
-----|------
**`type`** | must be `"tcp"` (*required*)
**`host`** | the host IP or hostname to connect to (*required*)
**`port`** | the TCP port to connect to (*required*)
**`version`** | the IP protocol version to speak - either `4` or `6` (default: **4**)
**`timeout`** | optional connection timeout in seconds (default: **10**)
**`tls`** | optional endpoint TLS configuration

### Unix Domain Sockets

Unix domain socket *Endpoints* come in two flavors: listening and connecting *Endpoints*.

A listening Unix domain socket *Endpoint* accepts incoming connections over a Unix domain socket from clients. A connecting Unix domain socket *Endpoint* establishes a connection a Unix domain socket to a server.

#### Unix Domain Socket Listening Endpoints

Here is an *Endpoint* that is listening on Unix domain socket `/tmp/socket1`:

```javascript
"endpoint": {
   "type": "unix",
   "path": "/tmp/socket1"
}
```

Unix domain socket listening *Endpoints* can be configured using the following parameters:

Option | Description
-----|------
**`type`** | must be `"unix"` (*required*)
**`path`** | absolute or relative path (relative to node directory) of Unix domain socket (*required*)
**`backlog`** | optional accept queue depth of listening endpoints (default: **50**)

#### Unix Domain Socket Connecting Endpoints

Here is an *Endpoint* that is connecting over Unix domain socket `/tmp/socket1`:

```javascript
"endpoint": {
   "type": "unix",
   "path": "/tmp/socket1"
}
```

Unix domain socket *Endpoints* can be configured using the following parameters:

Option | Description
-----|------
**`type`** | must be `"unix"` (*required*)
**`path`** | absolute or relative path (relative to node directory) of Unix domain socket (*required*)
**`timeout`** | optional connection timeout in seconds (default: **10**)
