---
title: "nepi-ng - D - testbed preping"
---

# nepi-ng - D - testbed preping

::::::{tab-set}

:::::{tab-item} INTRO
:label: tab-d-prep-intro

### Preparation

At this point, you should have a clear understanding of how to design your
experiment using `nepi-ng`. In this tutorial section, we  come back to the
initialization and preparation stages, that we had done manually at first  -
i.e. using the shell tools - and show how to account
for these various preparation tasks in a `nepi-ng` script.

To this end we will improve our script so that it takes care of initializations,
and specifically we will add a command line option that, when enabled:

* loads the `ubuntu` image on the nodes that we do use,
* and makes sure that all the nodes that we do not use are actually turned off.

It is a rather common need for all experiments to take these aspects into
account. We do recommend to make image loading an option though, since
performing this for every run very quickly gets in the way when fine-tuning your
experiment.

Please note that the script **will not** try to **get a lease**
automatically, instead we keep the simple policy of **just checking** that
we have a valid lease.

Like always, we will improve the code by small incremental changes.

### Important note on shell tools

**Convenience tools are mostly just aliases**

Before we dive in this area, we need to stress an important point.
In the [tutorial on the shell tools](../getting-started/shell-tools.md),
we had seen sessions like this:

```
rleases
all-off
n 1-5 33,37 ~3
rload -i fedora
```

It is important to emphasize that the commands involved here are all
**volatile bash** materials like *aliases* or *functions*.
This means that, as of beginning of Feb. 2018 at least,
if you try to run from your laptop something like this:

```console
$ ssh r2lab-tutorial@faraday.inria.fr rleases
bash: rleases: command not found
```

you get an error, that is to be compared this with:

```console
$ ssh r2lab-tutorial@faraday.inria.fr rhubarbe leases
----- <Leases from PLCAPIproxy@https://r2labapi.inria.fr:443/PLCAPI/ - 25 lease(s)>
  1  < from 02-22 @ 08:00 until 09:00 CET inria_oai
...
```

The rationale being that there is a need for *very short* commands in an
*interactive* shell environment. But when invoking commands remotely
through ssh, you don't run `bash` and so the bash-written convenience
layer does not come into play.

### How to find out long commands

For starters, as a rule of thumb, all convenience commands that are derived from
`rhubarbe` are made up the same way. Just like `rleases` is an alias for
`rhubarbe leases`,  you will find that `rbye` is an alias for `rhubarbe bye`.

```
r2lab-tutorial@faraday:~$ type rload
rload is aliased to `rhubarbe load'
r2lab-tutorial@faraday:~$ type rwait
rwait is aliased to `rhubarbe wait'
```

As you can see, it is very easy to find out about a given command when logged on
faraday, using `bash`'s built-in `type` command; note that `type` is much more
powerful and accurate than the old-school `which` thing, that is only able to
locate a command along your path, while `type` knows about aliases and
functions as well.

```
r2lab-tutorial@faraday:~$ which rwait
r2lab-tutorial@faraday:~$
```

### How to use short commands in scripts

Finally, note that you can expose short commands in your scripts by adding
a line Like this in your shell script:

```
# this would define e.g. the 'rwait' command
source /etc/profile.d/faraday.sh
```

The same goes of course for convenience tools exposed from the nodes
environment; as we have seen on a few occasions before, if you need to use any
of these commands in code meant to run on nodes, you can insert this line in
your bash script:

```
# this would define e.g. the `r2lab-id` command
source /etc/profile.d/nodes.sh
```

All this being said, let us now see in [the next tab (**D1**)](#tab-d1) how to extend the A5 script and turn it into D1
that knows how to load images.
:::::

:::::{tab-item} D1
:label: tab-d1

### D1: Objective

When working on an experiment, you will find yourself making several
reservations, as not everything works as planned the first time.

For this reason it is useful to design your experiment script so that it can be
used both:

* at the beginning of your reserved timeslot, and in this case you will need the
  script to load the image of your choice on the nodes,

* or the rest of the time, when you just need to re-run everything, but not to
  necessarily to reload images, given that this is relatively time-consuming.

### Starting point

It is the purpose of the present step, to show you how to simply add a command
line option that, when provided, triggers image loading.

For this step, we start back from the last code in the A section - namely
`A5-ping.py`, remember:

```{figure} D-prep/A5.png
:width: 60%
:align: center
:class: text-center

The A5 scenario
```

### D1: The code

Every time we will see a piece of code, you can download the raw code
with the download link above it.

:::{div}
:class: text-right
{download}`⬇ Download D1-prep.py <D-prep/D1-prep.py>`
:::

::::{tab-set}
:::{tab-item} Graph
:sync: code-graph

```{figure} D-prep/D1.png
:width: 60%
:align: center
:class: text-center

The D1 scenario
```
:::
:::{tab-item} Full code
:sync: code-full

```{literalinclude} D-prep/D1-prep.py
:language: python
:caption: D1-prep.py
```
:::
:::{tab-item} Diff from A5
:sync: code-diff

```{literalinclude} D-prep/D1-prep.diff
:language: diff
:caption: Changes from A5-ping.py to D1-prep.py
```
:::
::::

### D1: Sample output

Here's the output of the script when run with the `-l` option.

````{dropdown} Sample output: $ python3 D1-prep.py -l
```{literalinclude} D-prep/D1.out
```
````

### D1: Next

We will now see in [tab **D2**](#tab-d2) how to also make sure all the rest of the testbed
is turned off.
:::::

:::::{tab-item} D2
:label: tab-d2

### D2: Objectives

In this section we study a variant `D2`, that is naturally based on `D1`, and
that also makes sure that the unused nodes in the testbed are properly turned
off.

### Selection in `rhubarbe`

For doing so, we take advantage of a feature in `rhubarbe`, that is designed to
make node selection a smooth process; in particular we use:

* the `--all` (or just `-a`) option that selects all nodes,
* and the `~` operator for removing nodes from the selection.

So for example

```
r2lab-tutorial@faraday:~$ rhubarbe nodes -a
fit01 fit02 fit03 fit04 fit05 fit06 fit07 fit08 fit09 fit10 fit11 fit12 fit13 fit14 fit15 fit16 fit17 fit18 fit19 fit20 fit21 fit22 fit23 fit24 fit25 fit26 fit27 fit28 fit29 fit30 fit31 fit32 fit33 fit34 fit35 fit36 fit37
```

selects all 37 nodes, while

```
r2lab-tutorial@faraday:~$ rhubarbe nodes -a ~1 ~2
fit03 fit04 fit05 fit06 fit07 fit08 fit09 fit10 fit11 fit12 fit13 fit14 fit15 fit16 fit17 fit18 fit19 fit20 fit21 fit22 fit23 fit24 fit25 fit26 fit27 fit28 fit29 fit30 fit31 fit32 fit33 fit34 fit35 fit36 fit37
```

selects all nodes but nodes number 1 and 2. This is the basic mechanism that we use to invoke the `rhubarbe bye` (*a.k.a.* `all-off`) command to turn off all the nodes that are not involved in our experiment.

### requirement(s)

Also you will notice in this code that the `required` value for a given job may
be either a plain job object, or a collection of jobs; in the code above, the
`ready_requirement` variable, that was a single job object in `D1-prep.py`, is
made a list with 2 jobs, and this is how we simply achieve the layout for the
new dependency graph.

### D2: The code

:::{div}
:class: text-right
{download}`⬇ Download D2-prep.py <D-prep/D2-prep.py>`
:::

::::{tab-set}
:::{tab-item} Graph
:sync: code-graph

```{figure} D-prep/D2.png
:width: 60%
:align: center
:class: text-center

The D2 scenario
```
:::
:::{tab-item} Full code
:sync: code-full

```{literalinclude} D-prep/D2-prep.py
:language: python
:caption: D2-prep.py
```
:::
:::{tab-item} Diff from D1
:sync: code-diff

```{literalinclude} D-prep/D2-prep.diff
:language: diff
:caption: Changes from D1-prep.py to D2-prep.py
```
:::
::::

### D2: Sample output

No great news here, just observe how all the other nodes, and the phones, get turned off while the 2 target nodes are being imaged.

````{dropdown} Sample output: $ python3 D2-prep.py -l
```{literalinclude} D-prep/D2.out
```
````

### D2: Next

We will now see in [tab **D3**](#tab-d3) how to pass target nodes on the command-line.
:::::

:::::{tab-item} D3
:label: tab-d3

### D3: Objectives

In this section, we will change the `D2` script so that the target nodes can be
passed on the command line, instead of using the hardwired nodes 1 and 2.

### The `r2lab` python library

We take this opportunity to introduce the `r2lab` python library,
that you need of course to install separately:

```
pip3 install r2lab
```

This library is designed to be, and hopefully to stay, very small;
in this example we just use convenience functions like `r2lab_hostname`
that lets us compute the [hostname for one of the nodes from a variety of inputs](http://r2lab.readthedocs.io/en/latest/API.html#r2lab.utils.r2lab_hostname),
that can be either `int` or `bytes` or `str`.

This mostly is convenient to avoid ending up with hostname like `fit1`
with a missing `0`, so as you can see it is very basic.

A complete reference can be [found on readthedocs.io](http://r2lab.readthedocs.io/).

### D3: The code

:::{div}
:class: text-right
{download}`⬇ Download D3-prep.py <D-prep/D3-prep.py>`
:::

::::{tab-set}
:::{tab-item} Graph
:sync: code-graph

```{figure} D-prep/D3.png
:width: 60%
:align: center
:class: text-center

The D3 scenario
```
:::
:::{tab-item} Full code
:sync: code-full

```{literalinclude} D-prep/D3-prep.py
:language: python
:caption: D3-prep.py
```
:::
:::{tab-item} Diff from D2
:sync: code-diff

```{literalinclude} D-prep/D3-prep.diff
:language: diff
:caption: Changes from D2-prep.py to D3-prep.py
```
:::
::::

### D3: Sample output

It is easy to select other nodes with the `-a` and `-b` option.

````{dropdown} Sample output: $ python3 D3-prep.py --load --node-a 10 --node-b 20
```{literalinclude} D-prep/D3.out
```
````

### D3: Next

In the next example ([tab **D4**](#tab-d4)), we will see how
to rewrite this example to use nested schedulers, for better modularity.
:::::

:::::{tab-item} D4
:label: tab-d4

### D4: Objectives

In this section, we will change the `D3` script and illustrate a very convenient feature,
that allows to create so-called **nested schedulers**; the idea is to be able to
insert a scheduler as a job in a higher-level scheduler.
This feature aims in particular at allowing a modular design of schedulers.

In a nutshell, all you need to know is that a `Scheduler` object can be inserted inside another scheduler, like e.g.:

```
s_high = Scheduler()
s_high.append(
    Sequence(
        SshJob(...),
        Scheduler(...),  # low-level scheduler
        SshJob()))
```

Of course in practice, the low-level scheduler is often built separately;
for example it could be built by a regular python function.

The other way around, it is also possible to implement a python
function that accepts a scheduler in argument, an returns a decorated scheduler that would,
for example, check for the lease before running the incoming scheduler.

A more detailed introduction to nested schedulers can be found
[in the asynciojobs documentation](http://asynciojobs.readthedocs.io/en/latest/README.html#nesting-schedulers).

So in this example we create a script that behaves exactly like in D3,
but using a nested scheduler to provide for more modularity.

### D4: The code

Notice:

* how nested schedulers are rendered graphically, and
* how the reusable `check_lease` function decorates `experiment_scheduler`
so as to first check for the lease.

:::{div}
:class: text-right
{download}`⬇ Download D4-prep.py <D-prep/D4-prep.py>`
:::

::::{tab-set}
:::{tab-item} Graph
:sync: code-graph

```{figure} D-prep/D4.png
:width: 60%
:align: center
:class: text-center

The D4 scenario
```
:::
:::{tab-item} Full code
:sync: code-full

```{literalinclude} D-prep/D4-prep.py
:language: python
:caption: D4-prep.py
```
:::
:::{tab-item} Diff from D3
:sync: code-diff

```{literalinclude} D-prep/D4-prep.diff
:language: diff
:caption: Changes from D3-prep.py to D4-prep.py
```
:::
::::

### D4: Sample output

````{dropdown} Sample output: $ python3 D4-prep.py --load --node-a 10 --node-b 20
```{literalinclude} D-prep/D4.out
```
````

### D4: Next

We can now wrap up this D-series ([tab **WRAP UP**](#tab-d-prep-wrap-up)).
:::::

:::::{tab-item} WRAP UP
:label: tab-d-prep-wrap-up

### Summary
You now have a complete toolset at your disposal, and should be able to create `nepi-ng` scripts for
writing a real scale experiment, including features like:

* setting up nodes from scratch,
* accounting for any node that the previous experimenter may have forgotten to switch off,
* passing node numbers on the command-line,
* and, last but not least, using nested schedulers to write more modular experiments.

### Next

Let us move to [the next tutorial](https://r2lab.inria.fr/troubleshooting.md)
for some guidelines and troubleshooting tips.
:::::

::::::
