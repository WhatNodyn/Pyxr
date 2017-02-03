# Pyxr
An object-relational mapping-ish wrapper around Xlib ad X's resource manager/xrdb

## How to Use
Pyxr provides only one class: `pyxr.Namespace`.
That takes two optional arguments: The namespace to operate in (`*` by default) and the display address, which Xlib will pick on its own if unspecified.

Then, you access members of the xrdb class name as if they were attributes of the `Namespace` instance. They'll be written, read and deleted as you go.
