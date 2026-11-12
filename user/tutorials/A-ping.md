---
title: "nepi-ng A: the basics"
---

# nepi-ng A: the basics

::::::{tab-set}

:::::{tab-item} INTRO
In this series we run a few experiments that `ping` between various
locations, over the networks available to experimenters in R2lab.

The steps A1 to A5 are small incremental changes, so that each concept
is introduced one at a time. From A2 on, the code is shown as a **diff**
against the previous step: inserted and deleted lines are highlighted so
you can see what is new. The plain code is available in a dropdown.

### Preparation

Before running these experiments we need

* a valid reservation in the booking system;
* the 2 nodes `fit01` and `fit02` up and running.

For this first series we assume these 2 steps are performed manually.

#### Getting a reservation

Once logged in on the website, go to the booking page (TODO: link once
ported). In a nutshell, in the calendar:

* click once in a free slot to create a reservation;
* drag a reservation to change it;
* double-click a reservation to cancel it;
* when you belong to several slices, drag a slice from the left-hand
  list right into the calendar. The *current* slice is the one with a
  back arrow; it is the one used when you single-click to reserve.

The code in this series assumes a slice named `r2lab-tutorial`, which of
course you need to replace with your actual slice name.

#### Loading images

To load the images manually on the 2 nodes (use **your slice name**):

```bash
ssh your_slicename@faraday.inria.fr
```

If your public key is not at its standard location, add the `-i`
option with the path to it. On `Permission denied`, go back to the
registration tutorial (TODO: link once ported) to troubleshoot access.

Once on `faraday`, type the following (explained in the shell-tools
tutorial):

```bash
# always a good idea to check you currently own the reservation
rleases --check
# turn off the whole testbed - just in case
all-off
# select nodes 1 and 2
n 1 2
# load the default image (on the selected nodes)
rload
# wait for ssh to be up (still on the selected nodes)
rwait
```

`rload` takes a couple of minutes. Your output should look like this:

````{dropdown} Sample output
```{literalinclude} A-ping/prep.out
:language: console
```
````

Both nodes now run the default image. You can log out of `faraday` and
go back to your laptop to run the steps below.

Continue with the **A1** tab above.
:::::

:::::{tab-item} A1
### Objective

Our first experiment code is designed to run on YOUR computer. From
there we trigger a simple command on the R2lab gateway, that is to say
`faraday.inria.fr`; namely we simply ping `google.fr` from `faraday`, as depicted below.

```{figure} A-ping/A1.png
:width: 60%
:align: center
:class: text-center

The A1 scenario
```

### Introduction to `nepi-ng`

This example introduces the following classes:

`SshNode`
: represents an ssh connection; here we create one such object, with
  our credentials to enter `faraday`;

`SshJob`
: describes what commands we want to run in an `SshNode`; here a
  single command is needed;

`Scheduler`
: runs a collection of `SshJob`s - even with only one job, it will
  prove useful when several nodes are active at the same time.

You should be able to run this script as-is, except for the slice name
that you need to change manually in the code.

:::{div}
:class: text-right
{download}`⬇ Download A1-ping.py <A-ping/A1-ping.py>`
:::

```{literalinclude} A-ping/A1-ping.py
:language: python
:caption: A1-ping.py
```

````{dropdown} Sample output: python3 A1-ping.py
```{literalinclude} A-ping/A1.out
```
````

**Next:** the **A2** tab - specifying your slice on the command line.

:::::

:::::{tab-item} A2
### Objectives

* using the standard `argparse` module, we let users specify their
  slice on the command line with `--slice your_slicename`, without
  having to edit the source;

* we introduce the `Run` class, a companion to `SshNode`, stating that
  `ping` is to be run on the remote side as a standard, preinstalled
  command. Other kinds of commands exist, like shell scripts or file
  transfers;

* finally, a good practice: have your script return a meaningful
  return code to the OS, using `exit()`. A process is expected to
  `exit(0)` when everything went fine.

The verbose ssh messages are gone; add `-v` / `--verbose-ssh` to get
them back.

:::{div}
:class: text-right
{download}`⬇ Download A2-ping.py <A-ping/A2-ping.py>`
:::

````{dropdown} Full code of A2-ping.py (without the diff highlighting)
```{literalinclude} A-ping/A2-ping.py
:language: python
:caption: A2-ping.py
```
````

```{literalinclude} A-ping/A2-ping.diff
:language: diff
:caption: Changes from A1-ping.py to A2-ping.py
```

````{dropdown} Sample output: python3 A2-ping.py -s inria_radiomap
```{literalinclude} A-ping/A2.out
```
````

**Next:** the **A3** tab - running commands on a node rather than on the gateway.

:::::

:::::{tab-item} A3
### Objective: controlling a node beyond the gateway

This time we want to run the same `ping` command, but from a node, and
not from the gateway.

To this end we only need a second `SshNode`, created with the
`gateway=` argument. This materializes the fact that we reach node
`fit01` *through* the gateway. It also ensures that a single ssh
connection is established to the gateway, regardless of the number of
nodes actually controlled.

:::{important}
For this to work you need a currently valid reservation (and to use
the code with the `--slice` option if needed), and `fit01` must be up
and running.
:::

```{figure} A-ping/A3.png
:width: 60%
:align: center
:class: text-center

The A3 scenario
```

:::{div}
:class: text-right
{download}`⬇ Download A3-ping.py <A-ping/A3-ping.py>`
:::

````{dropdown} Full code of A3-ping.py (without the diff highlighting)
```{literalinclude} A-ping/A3-ping.py
:language: python
:caption: A3-ping.py
```
````

```{literalinclude} A-ping/A3-ping.diff
:language: diff
:caption: Changes from A2-ping.py to A3-ping.py
```

````{dropdown} Sample output: python3 A3-ping.py -v
```{literalinclude} A-ping/A3.out
```
````

**Next:** the **A4** tab - checking for leases before running.

:::::

:::::{tab-item} A4
### Objectives

Our experiment performs the exact same thing, but before it does
anything, it checks that we do have a valid reservation. This

* implements a good practice: ssh access to the gateway is essentially
  open once and for good, so it is wise to check for the reservation
  early, rather than get obscure errors later on;

* gives us a first glimpse at running one command on the gateway and
  one on the node.

### `asynciojobs` basics

* a `Scheduler` is filled with any number of jobs; the order in which
  jobs are defined and added has no meaning whatsoever;

* what truly matters is the set of `required` relationships between
  jobs. Here we run 2 jobs in sequence, so `ping` is defined with
  `required = check_lease`;

* a `Scheduler` does not propagate result values from one job to its
  successors. The only logic it knows about is that if a job raises an
  exception and that job is `critical`, the scheduler bails out
  immediately;

* here `rhubarbe leases --check` returns 0 when you currently own the
  reservation, and 1 otherwise; declaring `check_lease` as `critical`
  ensures the scenario fails right away if you do not.

### Graphical view

% TODO: once nested tabs work in the theme, move this graphical view (and the
% figure) into the tabbed navbar of the A4 code section, next to the code and
% diff, as in the original Graph tab - instead of showing it inline here.

For the first time we use `export_as_dotfile` on the `Scheduler` to
produce a graphical representation of the jobs' `required`
dependencies, shown below.

The code only produces a `dot` file, so it runs even without the
`graphviz` library installed. Turn it into a `png` with any program
that supports [the dot format](https://en.wikipedia.org/wiki/DOT_(graph_description_language)),
e.g. the `dot` binary from the `graphviz` package.

:::{note}
From within a jupyter notebook, and provided the `graphviz` python
package is installed, you can use `Scheduler.graph()` to create and
display a `graphviz.Digraph` natively, with no intermediary `dot`
file. See the
[asynciojobs documentation](http://asynciojobs.readthedocs.io/en/latest/README.html#visualization-in-a-notebook-scheduler-graph).
:::

```{figure} A-ping/A4.png
:width: 60%
:align: center
:class: text-center

The A4 scenario
```

:::{div}
:class: text-right
{download}`⬇ Download A4-ping.py <A-ping/A4-ping.py>`
:::

````{dropdown} Full code of A4-ping.py (without the diff highlighting)
```{literalinclude} A-ping/A4-ping.py
:language: python
:caption: A4-ping.py
```
````

```{literalinclude} A-ping/A4-ping.diff
:language: diff
:caption: Changes from A3-ping.py to A4-ping.py
```

````{dropdown} Sample output: python3 A4-ping.py
```{literalinclude} A-ping/A4.out
```
````

Or, with a slice that is valid but does not have the reservation right now:

```console
$ python3 A4-ping.py -s inria_inria.oai.oai_build
faraday.inria.fr:Checking current reservation for inria_inria.oai.oai_build WARNING: Access currently denied
```

**Next:** the **A5** tab - using other network interfaces.

:::::

:::::{tab-item} A5
### Objectives

This time we run ping between two nodes of the testbed, over the
`data` wired network.

Each R2lab node has 4 network interfaces (not counting the special
`reboot` interface, which can reset the node but is not visible from
linux). With the images we offer, they are managed as follows:

`control`
: a wired interface, the one you use when you first ssh into the node;
  turned on automatically at boot; known as e.g. `fit01`, on the
  `192.168.3.0/24` subnet;

`data`
: another wired interface, **NOT** turned on at boot; it is dedicated
  to your usage, so you can turn it on or off as you please, even using
  DHCP, in which case its address is on `192.168.2.x/24` and known to
  DNS as e.g. `data01`;

`atheros` and `intel`
: the 2 WiFi interfaces, also **NOT** turned on at boot - setting them
  up is entirely your responsibility (see the B-series).

Worth noticing in the code:

* every node has a command named `turn-on-data`, not a standard command
  but preinstalled for your convenience: it turns on the data interface
  using DHCP. Type `help` on any node to see the available commands;
  similar utilities are in
  [r2lab-embedded](https://github.com/fit-r2lab/r2lab-embedded/blob/master/shell/nodes.sh);

* to run `ping` once **BOTH** nodes have configured their data
  interface, the ping job simply lists 2 jobs in its `required`;

* in the epilogue we check that ping actually succeeded, using
  `result()` on an `SshJob` instance.

```{figure} A-ping/A5.png
:width: 60%
:align: center
:class: text-center

The A5 scenario
```

:::{div}
:class: text-right
{download}`⬇ Download A5-ping.py <A-ping/A5-ping.py>`
:::

````{dropdown} Full code of A5-ping.py (without the diff highlighting)
```{literalinclude} A-ping/A5-ping.py
:language: python
:caption: A5-ping.py
```
````

```{literalinclude} A-ping/A5-ping.diff
:language: diff
:caption: Changes from A4-ping.py to A5-ping.py
```

````{dropdown} Sample output: python3 A5-ping.py
```{literalinclude} A-ping/A5.out
```
````

**Next:** the **WRAP UP** tab.

:::::

:::::{tab-item} WRAP UP
### Summary

At this point you should have a good grasp of these R2lab fundamentals.
#### Interfaces

Each node has 4 network interfaces; `control` is reserved for testbed
administration, the others are for the experimenter, who is in charge of
setting them up.

#### `nepi-ng`

By leveraging the standard `asyncio` library, and combining `asynciojobs`
and `apssh` on top of it, you can write scripts that are

* reasonably simple and short;
* able to run as many jobs as needed simultaneously, in a single thread;
* able to deal with simple synchronization constraints.

#### Next

The B-series deals with the more complex task of setting up a wireless
network; the C-series addresses file transfers to and from `SshNode`s.
(Links to be added as these get ported.)
:::::

::::::
