# vim: set filetype=python tabstop=4 shiftwidth=4 expandtab:

import os

import entry
import secrets
import status

secrets.open_store()

err_handler = None

if __name__ == "__main__":
    status_code = status.START
    handler = status._handlers[status.START]

    while status_code != status.END:
        if handler.defer:
            err_handler = handler.method
        else:
            handler.method()

        pid = os.fork()

        if pid:
            status_code, handler = status.extract_status(os.waitpid(pid, 0)[1])
        else:
            entry.start(err_handler)
