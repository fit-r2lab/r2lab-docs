---
title: Shell tools in the gateway
---

# Shell tools in the gateway

::::::{tab-set}

:::::{tab-item} LOG IN
:label: tab-shell-tools-log-in
### Logging in the gateway

Once you have [obtained a slice account on R2lab](registration.md), you can
reach the R2lab gateway using ssh

```bash
ssh your_slicename@faraday.inria.fr
```

*If by any chance your public key is not at its standard location, add the
`-i` option to the command line, with the path to it.*

### Listing commands

From your bash account on the gateway, you have a few very simple but handy
tools at your disposal for the early steps of your experiment, like seeing the
nodes status, turning them on or off, and loading images.

```bash
help
```

### Addressing

From the gateway, you can use the following hostnames to refer to nodes:

`fit08`
: refers to the `control` wired interface on node 8; the control interface is
  configured in all our images to start up automatically at boot-time so the
  nodes can be reached;

`data08`
: refers to the `data` wired interface; this one is not automatically turned
  on, it is up to you to use it or not, you can use DHCP for that purpose;

`reboot08`
: refers to the ethernet interface of the CMC device on the node, that allows
  for remote management of the motherboard (i.e. turning nodes on and off).

Here's an example of how these names resolve. Beware that the IP address of the
reboot interface might occasionally not be directly bound to the node index.

```console
your_slicename@faraday:~$ host fit08
fit08 has address 192.168.3.8
your_slicename@faraday:~$ host data08
data08 has address 192.168.2.8
your_slicename@faraday:~$ host reboot08
reboot08 has address 192.168.1.8
```

### Checking leases

In case you're unsure about the current status of reservation, you can list
reserved timeslots - known as leases - with

```bash
rleases
```

or check that you currently hold a reservation with

```bash
rleases --check
```

This is a poor man's tool, as of course [the scheduler](https://r2lab.inria.fr/book.md)
will give you that same information in a much nicer way.

Note also that this is in fact equivalent to

```bash
rhubarbe leases
```

`rhubarbe` ([see it on github](https://github.com/fit-r2lab/rhubarbe)) being
the set of tools that help us run the testbed. Indeed many of the convenience
functions starting with `r` are in fact aliases to a `rhubarbe` subcommand.

### Switch off the testbed when you're done

One very frequently used command, that requires that you have a valid lease -
or at least that no lease is currently active - is the one that turns off the
nodes when you are done:

```bash
all-off
```

which is an alias for either

```bash
rhubarbe bye
```

or simply

```bash
rbye
```

Please try to make sure to use it, especially when you have many nodes running.

In [the next tab, **SELECT NODES**](#tab-shell-tools-select-nodes), we will see how we can focus on a specific
set of nodes, and easily control them.
:::::

:::::{tab-item} SELECT NODES
:label: tab-shell-tools-select-nodes
### Monitor what you're doing

Be aware that you can have a global and live view of the testbed status
[right in the r2lab website](https://r2lab.inria.fr/status.md). This link works
for all visitors, and if you are logged in you can
[also see this page](https://r2lab.inria.fr/run.md) that will also show you the
state of the reservation system.

### Selecting nodes

Most of the time, you will want to manage a selected subset of nodes. There's a
simple mechanism in place so you don't need to specify your nodes for each and
every command, by defining the environment variable `NODES`. For this the
`nodes` command is your friend.

To **select nodes**, use the `nodes` command. To select nodes 1 2 4 5 33 and 37
you could do this (`~` stands for negation)

```bash
nodes 1-5 33,37 ~3
```

To select **all nodes**, you could do

```bash
all-nodes
```

To **remove** all nodes between 3 and 35 from your selection; same with
`nodes-add` for **adding nodes**

```bash
nodes-sub 3-35
```

To see your selection, just run

```bash
nodes
```

Finally the commands `nodes-save` and `nodes-restore` let you name selections,
and then reinstate them

```bash
nodes-save run1
# ...
nodes-restore run1
```

### Are these nodes on or off

```bash
st
```

By default - i.e. **with no argument** - this command and most of the ones we
show here operate on **your nodes selection**, but you can always **specify
another set of nodes** to operate on, regardless of the overall selection.

So this will give you the status of nodes 1 2 and 3, no matter what you have
selected

```bash
st 1-3
```

### Managing nodes (turning them on or off, or rebooting)

To turn on your selected nodes just do

```bash
on
```

Or again, if you want to turn on node 3 only, just do

```bash
on 3
```

Turning them off is of course just

```bash
off
```

You can trigger a reset (reboot) on a node - provided it is already on - with

```bash
reset
```

To see the list of nodes that are ON

```bash
show-nodes-on
```

You can select all the nodes currently ON with

```bash
focus-nodes-on -a
```

To see the linux version running in the nodes (this is less sophisticated than
what the [livetable](https://r2lab.inria.fr/status.md#livetable) would provide)

```bash
releases
```
:::::

:::::{tab-item} IMAGES
:label: tab-shell-tools-images
### Loading images

The tool for loading images is called `rload`. It is in fact a shortcut for
`rhubarbe load`, like most commands described here

```bash
rhubarbe --help
```

See [the source code for `rhubarbe` for more details](https://github.com/fit-r2lab/rhubarbe).

Back to image loading, you will first want to know which images are available:

```bash
rimages
```

Assuming you want to load the latest fedora image, you would just do

```bash
rload -i fedora
```

that would act on all your selected nodes (or as always, add a list of nodes
to the command)

```bash
rload -i fedora 1-10
```

Image loading has a fancier mode that can come in handy for troubleshooting:
the `--curses` mode - `-c` in short - gives you a live progress bar for each
node. Note however that the curses mode is not suitable for scripting, as it
will wait for a keystroke before exiting.

### Waiting for nodes

You can wait for all the selected nodes to be ssh-ready by running

```bash
rwait
```

This command, like all the `rhubarbe`-related commands, has a default timeout,
that you can change with (`-t` is the shortcut)

```bash
rwait --timeout 30
```

### `ssh`-ing into nodes

Once you have loaded an image, you can enter all nodes by just doing

```bash
ssh root@fit25
```

or just, if you're really lazy

```bash
s1 25
```

:::{note}
This shortcut used to be called `ss`, but `ss` is also the name of a standard
linux tool for inspecting sockets; the name `s1` stands for **s**sh into the
**1**st selected node.
:::

You can run a command on all selected nodes with

```bash
map ip addr show
```

this time of course, you cannot specify another set of nodes than the
selection.

### Saving images

You have the ability to save the image - this now of course applies only to
**one node** at a time. To save node 25

```bash
rsave 25 -o my-image-name
```

Your slice can then later on re-use this image using e.g. a simple

```bash
rload -i my-image-name 12-15
```

The image file ends up in your slice's home directory, under a temporary name
starting in `saving__`; if you need to publish these into the common repository
`/var/lib/rhubarbe-images`, get in touch with the admins, who can grant you the
right to use `rhubarbe-share` (not documented here).
:::::

:::::{tab-item} PHONES
:label: tab-shell-tools-phones
### Phones

For now we have two commercial phones available right in the room; each phone
can be controlled through a dedicated MAC box, called `macphone1` and
`macphone2`.

As far as shell commands are concerned, since that is the focus of this
tutorial, be aware that you can reach e.g. the second `macphone` from faraday
by doing just

```bash
macphone2
```

and from then, as usual

```bash
help
```

to get a reminder.

Please refer to [the 5G offering page](../offering-5g.md) ([PHONES tab](../offering-5g.md#tab-offering-5g-phones)) for more details on this offering, and how
to manage these phones e.g. through a VNC session.
:::::

::::::
