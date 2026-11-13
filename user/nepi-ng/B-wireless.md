---
title: "nepi-ng - B - wireless"
---

# nepi-ng - B - wireless

::::::{tab-set}

:::::{tab-item} INTRO
:label: tab-b-wireless-intro

### Prerequisites

For this series of experiments, we make the same assumptions as in the
previous series. In a nutshell, we expect you have a valid
reservation, and the 2 nodes `fit01`and `fit02` are properly loaded with
the default image, and turned on of course.

Please [visit this page](A-ping.md)
to review how to reach that point, if necessary.

### Objectives

In this series we will start playing with the wireless interfaces. Of
course a minimal background is assumed in terms of dealing with
wireless interfaces under linux; further information can be found at
the following locations :

* we recommend to see [this quick introduction to `iw`, that is
  instrumental in these
  tasks](https://wireless.wiki.kernel.org/en/users/documentation/iw)

* as well as [this helpful page on how to use `iw` if you were more
  familiar with `iwconfig` that is now considered
  obsolete](https://wireless.wiki.kernel.org/en/users/documentation/iw/replace-iwconfig) -
  much like `ip` has now replaced `ifconfig`.

### `nepi-ng`

Now as far as `nepi-ng` is concerned, in the previous series we have
seen ways to run remotely simple commands. In this section we will see
simple means to come up with more complex logic, simply by using shell
scripts that are pushed remotely under the hood before they are
triggered. This is what the `RunString` and `RunScript` classes are
about. Let us see them in action right away ([tab **B1**](#tab-b1)).
:::::

:::::{tab-item} B1
:label: tab-b1

### B1: Objective

We are going to run the exact same experiment [as in the previous run
A5](A-ping.md), that is to say a simple ping triggered on
`fit01` towards `fit02`, but this time on one of the **wireless
interfaces**.

```{figure} B-wireless/B1.png
:width: 60%
:align: center
:class: text-center

The B1 scenario
```

What changes then, as compared with our previous experiment, is that
we cannot anymore simply run the predefined convenience command
`turn-on-data`, and we are going to have to put a little more work in this
step.

We are going to configure a small *ad hoc* network between both nodes,
using their Atheros WiFi card, and this is the purpose of the bash
shell script named `turn_on_wireless_script`; as you will see, this
script uses some hard-wired settings like the channel and SSID, but
you can easily tweak the code so as to make this a parameter.

### New features

The `B1 code` below exhibits the use of a new class, `RunString`,
which is a very convenient variation around the `Run` class.

Instead of remotely invoking a command that is supposed to be
available there already, like we have done so far when e.g. invoking
`ping` or even `turn-on-data`, `RunString` allows you to invoke a command
that we provide **as a python variable**.

This means that we can write our own shell snippet, in charge of
creating a small ad-hoc network, and embed this script right inside
our nepi-ng script; see the `turn_on_wireless_script` variable in the
code below.

See also how the `init_node_01` job now uses `RunString` to pass it
python variables as arguments. For example this is how
`turn_on_wireless_script` gets passed the right IP address for each node.

As you will see in the sample output below, it takes some time for the
IP connectivity to be established after the driver is configured.

### B1: The code

:::{div}
:class: text-right
{download}`⬇ Download B1-wireless.py <B-wireless/B1-wireless.py>`
:::

::::{tab-set}
:::{tab-item} Full code
:sync: code-full

```{literalinclude} B-wireless/B1-wireless.py
:language: python
:caption: B1-wireless.py
```
:::
:::{tab-item} Diff from A5
:sync: code-diff

```{literalinclude} B-wireless/B1-wireless.diff
:language: diff
:caption: Changes from A5-ping.py to B1-wireless.py
```
:::
::::

### B1: Sample output

````{dropdown} Sample output: $ python3 B1-wireless.py
```{literalinclude} B-wireless/B1.out
```
````

### B1: Next

Let us see some variants on that theme in [the next tab (**B2**)](#tab-b2)
:::::

:::::{tab-item} B2
:label: tab-b2

### B2: Objective

In this new variant, we are going to illustrate a few convenient tricks:

* we add a new option to the script so that one can choose, right on
  the command line, whether we want to use the intel or the atheros
  WiFi card; this simply relies on the [standard argparse
  module](https://docs.python.org/3/library/argparse.html) that we
  have already used for other options, the only new thing being the
  use of the `choices` keyword, so that only the 2 supported driver
  names can be used;

* more interestingly, we can remove the `wireless_interface` variable
  from that script altogether, thanks to a shell utilily available on
  all nodes and named `wait-for-interface-on-driver`. This shell
  function returns the name of the network interface associated with a
  given driver name, so it is enough to load, say, module `ath9k` and
  let this function figure out that the actual interface name is
  `atheros`;

* in much the same way, we will remove the need to pass an IP address
  to the `turn_on_wireless_script`, by computing this address based on
  the node rank in r2lab, using another convenience tool named
  `r2lab-ip`; there actually are 2 similar functions available on each node

  * `r2lab-ip`: will return the number of the current node, under **1 or 2 digits**;
    for example on node 8, this returns `8`;
    this is suitable to build IP addresses;

  * `r2lab-id`: will return the number of the current node, but **always in 2 digits**;
    for example on node 8, this returns `08`;
    this is suitable to build hostnames; so for example you would do

#

```
my_data_hostname="data$(r2lab-id)"
echo $my_data_hostname
data08
my_wireless_ip_address="10.0.0.$(r2lab-ip)"
echo my_wireless_ip_address
10.0.0.8
```

* finally, this new script displays the outputs of the ssh commands
  with a slightly different format, in that every line will now
  receive a timestamp in addition to the hostname. This is achieved
  through the use of the `TimeColonFormatter()` class; we create one
  instance of this class for each instance of `SshNode`.

So for example we would issue lines like

```
14-37-28:fit01:turn-off-wireless: shutting down device intel
```

  instead of just

```
fit01:turn-off-wireless: shutting down device intel
```

About that last point, note that other types of formatters are
  available, that will let you store output in a given directory, and
  in files named after each individual hostname. See [this
  page](http://apssh.readthedocs.io/en/latest/API.html#module-apssh.formatters)
  for more info on other available formatters.

### B2: The code

```{figure} B-wireless/B2.png
:width: 60%
:align: center
:class: text-center

The B2 scenario
```

:::{div}
:class: text-right
{download}`⬇ Download B2-wireless.py <B-wireless/B2-wireless.py>`
:::

::::{tab-set}
:::{tab-item} Full code
:sync: code-full

```{literalinclude} B-wireless/B2-wireless.py
:language: python
:caption: B2-wireless.py
```
:::
:::{tab-item} Diff from B1
:sync: code-diff

```{literalinclude} B-wireless/B2-wireless.diff
:language: diff
:caption: Changes from B1-wireless.py to B2-wireless.py
```
:::
::::

### B2: Sample output

````{dropdown} Sample output: $ python3 B2-wireless.py
```{literalinclude} B-wireless/B2.out
```
````

### B2: Next

In the next variant ([tab **B3**](#tab-b3)), we are going to see
how we can better esimate the time it takes for the ad hoc network to
actually come up.
:::::

:::::{tab-item} B3
:label: tab-b3

### B3: Objective

In this variant, we will see how we can even design our experiment so
that all **the shell code** goes **in a single file**, working as a
companion for the python script that will only deal with overall
logic.

Our pretext for doing so is that we would like to better understand
the startup sequence observed in the previous runs B1 and B2. And for
doing that it is not good enough to just run `ping` like we did, but
instead we would need run something a little more elaborate - that
we'll write in shell.

As much as it is convenient to have the ability to insert shell script
right in the python code, when things become more complex, the shell
code tends to become in the way.

So, two features are at work in the following code

* Using `RunScript` instead of `RunString` as a way to define commands
  allows us to separate the shell script in a separate file.

* Also you can note at the end of the shell script, a very simple
  trick that lets you group any number of functions in a shell script,
  and call each individual function by just stating its name and arguments.

In other words, it means that if you write the following in a file named `myscript.sh`:

```bash
#!/bin/bash
function foo () {
    echo "in function foo"
    for arg in "$@"; do echo "foo arg: " $arg; done
}

function bar () {
    echo "in function bar"
    for arg in "$@"; do echo "bar arg: " $arg; done
}

"$@"
```

and then you invoke `myscript.sh foo 1 2 "3 4"` you will get this ouput

```console
$ myscript.sh foo 1 2 "3 4"
in function foo
foo arg:  1
foo arg:  2
foo arg:  3 4
```

### B3: The code

Make sure you download both files in the same location before trying to run the python script.

```{figure} B-wireless/B3.png
:width: 60%
:align: center
:class: text-center

The B3 scenario
```

:::{div}
:class: text-right
{download}`⬇ Download B3-wireless.py <B-wireless/B3-wireless.py>`
:::

::::{tab-set}
:::{tab-item} Full code
:sync: code-full

```{literalinclude} B-wireless/B3-wireless.py
:language: python
:caption: B3-wireless.py
```
:::
:::{tab-item} Diff from B2
:sync: code-diff

```{literalinclude} B-wireless/B3-wireless.diff
:language: diff
:caption: Changes from B2-wireless.py to B3-wireless.py
```
:::
::::

:::{div}
:class: text-right
{download}`⬇ Download B3-wireless.sh <B-wireless/B3-wireless.sh>`
:::

```{literalinclude} B-wireless/B3-wireless.sh
:language: bash
:caption: B3-wireless.sh
```

### B3: Sample output

````{dropdown} Sample output: $ python3 B3-wireless.py
```{literalinclude} B-wireless/B3.out
```
````

### B3: Next

Let us proceed on this series with an example that adds a
cyclic task ([tab **B4**](#tab-b4)) to this scenario.
:::::

:::::{tab-item} B4
:label: tab-b4

### B4: Objective

In this example, we will just for fun add an
infinite cyclic task in the scheduler. Here we will simply write a TICK
mark every second, but this technique is most useful for consuming
events in a message queue, or any other similar approach.

The trick is to use the plain `Job` class from `asynciojobs`, which
expects a regular `asyncio` coroutine object, that we implement as
`infinite_clock()`. We just need to define the associated job
`clock_job` with `forever = True`, which tells the scheduler that this
job never ends, so that it knows that there is no point in waiting for
it to complete.

### More on graphical views

Note in this example that, with respect to the graphical representation of
schedulers:

* each job needs a specific label to be displayed in such a graph - as
  well as in `list()` and `debrief()` by the way

* the system does its best to provide a meaningful label, but

* you are always free to define your own label on a given job, like we
  do here with the `infinite clock` job.

### B4: The code

```{figure} B-wireless/B4.png
:width: 60%
:align: center
:class: text-center

The B4 scenario
```

:::{div}
:class: text-right
{download}`⬇ Download B4-wireless.py <B-wireless/B4-wireless.py>`
:::

::::{tab-set}
:::{tab-item} Full code
:sync: code-full

```{literalinclude} B-wireless/B4-wireless.py
:language: python
:caption: B4-wireless.py
```
:::
:::{tab-item} Diff from B3
:sync: code-diff

```{literalinclude} B-wireless/B4-wireless.diff
:language: diff
:caption: Changes from B3-wireless.py to B4-wireless.py
```
:::
::::

### B4: Sample output

````{dropdown} Sample output: $ python3 B4-wireless.py
```{literalinclude} B-wireless/B4.out
```
````

### B4: Next

In the next example ([tab **B5**](#tab-b5)),
we will see a convenience class named `Watch`, that comes in
handy in most experiments as it allows to keep track of elapsed time since the beginning of an experiment.
:::::

:::::{tab-item} B5
:label: tab-b5

### B5: Objective

In this final example in the series, we will take the chance to illustrate
a convenience class named `Watch` from `asynciojobs`, that allows to keep
track of elapsed time since some reference point in time, generally the
beginning of the experiment.

So here, we create a `Watch` instance, and use it when the clock is ticking,
instead of showing plain wall clock time.

### B5: The code

```{figure} B-wireless/B5.png
:width: 60%
:align: center
:class: text-center

The B5 scenario
```

:::{div}
:class: text-right
{download}`⬇ Download B5-wireless.py <B-wireless/B5-wireless.py>`
:::

::::{tab-set}
:::{tab-item} Full code
:sync: code-full

```{literalinclude} B-wireless/B5-wireless.py
:language: python
:caption: B5-wireless.py
```
:::
:::{tab-item} Diff from B4
:sync: code-diff

```{literalinclude} B-wireless/B5-wireless.diff
:language: diff
:caption: Changes from B4-wireless.py to B5-wireless.py
```
:::
::::

### B5: Sample output

````{dropdown} Sample output: $ python3 ./B5-wireless.py
```{literalinclude} B-wireless/B5.out
```
````

### B5: Next

It is now time to wrap up this series ([tab **WRAP UP**](#tab-b-wireless-wrap-up)).
:::::

:::::{tab-item} WRAP UP
:label: tab-b-wireless-wrap-up

We now know how to:

* have local scripts executed remotely; we have seen that we can either
  * write them as plain shell scripts - using `RunScript`,
  * or embed them right in python strings - using `RunString`;

* obtain remote outputs using alternate formats, using
  e.g. `TimeColonFormatter`; see [this
  page](http://apssh.readthedocs.io/en/latest/API.html#module-apssh.formatters)
  for more info on other available formatters;

* run infinite jobs, that will get properly terminated when all the
  finite jobs in the scenario are done;

* use the `Watch` class to keep track of elapsed time,
  as opposed to displaying wall clock time.

In [the next series of tutorials](C-files.md), we will learn
more about transferring files back and forth.
:::::

::::::
