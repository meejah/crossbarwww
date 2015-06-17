Native Workers, that is *Routers* and *Containers* can be further configured with `options`.

Both *Routers* and *Containers* share the following `options`:

option | description
---|---
**`title`** | The worker process title (default: **"crossbar-worker [router]"** or **"crossbar-worker [container]"**)
**`python`** | The Python executable to run the Worker with, e.g. `/opt/python27/bin/python` - this **must** be an absolute path (default: **same as controller**)
**`pythonpath`** | A list of paths to prepend to the Python seach path, e.g. `["..", "/home/joe/mystuff"]` (default: **[]**)
**`cpu_affinity`** | The worker CPU affinity to set - a list of CPU IDs (integers), e.g. `[0, 1]` (default: **unset**) - currently only supported on Linux and Windows, [not on FreeBSD](https://github.com/giampaolo/psutil/issues/566)
**`reactor`** | Choose the type of Twisted reactor, instead of the one chosen automatically. See below.
**`env`** | Environment variables to pass to components within the worker. This should be a `dict` with two keys: **inherit** which is a bool or a list of variables to inherit; and **vars** which is a `dict` of (additional) environment variables to set.

Selecting a **Twisted reactor** is platform-based: `reactor` takes a dictionary as an argument, with the platform as the keys and a single reactor per platform as the value.

Platform values which are handled are `bsd` (with possible prefixes), `darwin`, `win32` and `linux`, while reactor values are `select`, `poll`, `epoll`, `kqueue`, and `iocp`.

Additionally, the **process environment** for the worker can be determined using the option `env` - for more information see [[Process Environments]].