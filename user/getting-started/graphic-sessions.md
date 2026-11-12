---
title: About graphic sessions
---

# About X11 and VNC sessions

::::::{tab-set}

:::::{tab-item} X11 SESSIONS
### X11 sessions

If your laptop already runs an X server, you can create an X11 tunnel using
either of openssh's native `-X` or `-Y` options.

#### On faraday

```bash
ssh -Y your_slicename@faraday.inria.fr
firefox &
```

#### On a node

Provided that the node OS has the X clients installed:

```bash
ssh -Y your_slicename@faraday.inria.fr ssh -Y root@fit01
xterm &
```
:::::

:::::{tab-item} VNC SESSIONS
### VNC sessions

If your laptop runs a VNC client, that's the easy way to run interactive tools
on faraday.

#### On faraday

`faraday` runs a vnc server, and here is how to create a VNC tunnel.

**Example** from a Mac:

```bash
ssh -L localhost:5901:vnc-your_slicename:5900 your_slicename@faraday.inria.fr
```

While this is running, you can use e.g. the `VNC Viewer` app on the Mac and
connect to `localhost:1`, in order to get an interactive X11 session on
faraday. Using port e.g. 5902 instead of 5901 means you need to connect to
`localhost:2`.

**Other OSes**:

- this is significantly easier from a linux box:

  ```bash
  vncviewer -shared -via your_slicename@faraday.inria.fr vnc-your_slicename
  ```

- see detailed instructions for other OSes here (on faraday itself):

  ```bash
  less /usr/share/doc/vncserver-sop/README.txt
  ```

  where you replace `SERVER` with `faraday.inria.fr` and `LOGIN` with
  `your_slicename`.
:::::

::::::
