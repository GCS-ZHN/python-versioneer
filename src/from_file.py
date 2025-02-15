SHORT_VERSION_PY = """
# This file was generated by 'versioneer.py' (@VERSIONEER-VERSION@) from
# revision-control system data, or from the parent directory name of an
# unpacked source archive. Distribution tarballs contain a pre-generated copy
# of this file.

import json

version_json = '''
%s
'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)
"""

import json # --STRIP DURING BUILD
import re # --STRIP DURING BUILD
class NotThisMethod(Exception): pass  # --STRIP DURING BUILD

def versions_from_file(filename):
    """Try to determine the version from _version.py if present."""
    try:
        with open(filename) as f:
            contents = f.read()
    except OSError:
        raise NotThisMethod("unable to read _version.py")
    mo = re.search(r"version_json = '''\n(.*)'''  # END VERSION_JSON",
                   contents, re.M | re.S)
    if not mo:
        mo = re.search(r"version_json = '''\r\n(.*)'''  # END VERSION_JSON",
                       contents, re.M | re.S)
    if not mo:
        raise NotThisMethod("no version_json in _version.py")
    return json.loads(mo.group(1))


def write_to_version_file(filename, versions):
    """Write the given version number to the given _version.py file."""
    contents = json.dumps(versions, sort_keys=True,
                          indent=1, separators=(",", ": "))
    with open(filename, "w") as f:
        f.write(SHORT_VERSION_PY % contents)

    print("set %s to '%s'" % (filename, versions["version"]))

