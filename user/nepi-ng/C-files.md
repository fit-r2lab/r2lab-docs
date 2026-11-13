---
title: "nepi-ng - C - managing files"
---

# nepi-ng - C - managing files

::::::{tab-set}

:::::{tab-item} INTRO
:label: tab-c-files-intro

### Scenario

In this series, we will see how to transfer files between hosts, using
the `Push` and `Pull` commands in a `SshNode`.

The version in C3 will perform the following:

* generate a random file locally, and transfer it using SFTP onto fit01
* transfer it from fit01 to fit02 over the data network using netcat
* finally retrieve it locally from fit02 using SFTP again,
  and compare the result to make sure the file is intact.

The progression from C1 to C3 matches these bullets : C1 just
performs the first bullet, and C2 performs the first two bullets.

The last scenario, labelled C3bis, is a variant around C2. It is not
crucial to see it when first reading this tutorial.  In this scenario,
we perform the exact same scenario as in C2, but we see a recipe to
start and stop a process in sync with the jobs in a scheduler.

### New features

We will meet the `LocalNode` object that will let use run local
commands just like on remote nodes.

We will also take this chance to see that a `SshJob` object can be
defined with **several commands**, which can be helpful to avoid the
need to create long strings of jobs.

We also introduce the `Sequence` object, that is a convenience tool
for creating, well obviously, sequences of jobs, without the hassle of
managing the `required` relationship for each job.

Finally throughtout this series, we will also illustrate another
possible way to manage the components of the scheduler: instead of
creating the scheduler at the end with all the jobs, we create the
scheduler at the very beginning and create the jobs **right into the
scheduler**. Of course the result is exactly the same, it's just
another programming style that is probably worth considering.

Let us start with copying files over to the
node ([tab **C1**](#tab-c1)) with the `Push` command object.
:::::

:::::{tab-item} C1
:label: tab-c1

### C1: Objective

We start over from scratch here, and to begin with, we want to

* locally generate a random file,
* and push it over to node fit01

```{figure} C-files/C1.png
:width: 60%
:align: center
:class: text-center

The C1 scenario
```

This is what the code below carries out; the things to outline in this code are

* we see for the first time **the `LocalNode` object**, that can be used
  almost exactly as a `SshNode` object - except that it is of course
  simpler to build;

* once the local file is created, we use **a `Push` instance** instead of
  the `Run` and its variants that we have seen so far, to actually
  copy local files on the remote node;

* also note that inside a single `SshJob` instance, it is possible to
  provide an (ordered) **list of commands** to run on that node, mixing
  commands and file transfers as needed; this is how we can both push
  the `RANDOM` file over to node1, and display its size and SHA1 sum,
  using a single instance of `SshJob`.

### C1: The code

:::{div}
:class: text-right
{download}`⬇ Download C1-files.py <C-files/C1-files.py>`
:::

```{literalinclude} C-files/C1-files.py
:language: python
:caption: C1-files.py
```

### C1: Sample output

````{dropdown} Sample output: $ python3 C1-files.py
```{literalinclude} C-files/C1.out
```
````

### C1: Next

In the next section ([tab **C2**](#tab-c2)) we will extend this
scenario, and push the RANDOM file on another node using the wired network.
:::::

:::::{tab-item} C2
:label: tab-c2

### C2: Objective

We extend the C1 scenario and push the RANDOM file from fit01 to fit02 over the wired network.

```{figure} C-files/C2.png
:width: 60%
:align: center
:class: text-center

The C2 scenario
```

So we reuse the `turn-on-data` commands, that we had seen in the B
series already, to enable the `data` interface.

### File transfer per se

In order to transfer the file from fit01 to fit02: of course we could
have used simple tools like plain `scp`. Our goal however here is more
to show how to orchestrate such transfers in an environment closer to
typical experimental conditions.

So in this first variant, we will use `netcat`;  we start with running
a server instance of netcat on the receiving end (in our case
`fit02`), then run a client netcat on the sender side (here `fit01`).

In terms of synchronization, note how we

* start the server side in background (with a `&`); the corresponding
  job hence returns immediately;

* which lets us start the client side
  almost immediately afterwards (well, we add a 1s delay to stay on
  the safe side)

* and luckily enough, the server-side server will terminate as soon as
  the client side netcat is done; so we essentially do not need to
  worry about stopping the server, it stops itself at the exact right
  time

* so once the sender client is done, we can proceed and display the
  received file on fit02.

The purpose of the C3bis script is to show how one can use shell
tricks to deal with less fortunate situations, where typically the
server side runs forever, but you need to stop it once some other job
is done.

### The `Sequence` object

Note the use of the `Sequence` object in variable `transfer_job`, that
almost entirely relieves us of managing the `required` relationships.

All the jobs inserted in the `Sequence` have their `required`
relationship set to the previous job in the list, by setting
`required` on the `Sequence` object we actually deal with the
`required` jobs for the first job in the sequence.

Finally, by setting `scheduler` on this `transfer_job` object, we
automatically attach all the jobs in the sequence to the global
scheduler.

### C2: The code

:::{div}
:class: text-right
{download}`⬇ Download C2-files.py <C-files/C2-files.py>`
:::

::::{tab-set}
:::{tab-item} Full code
:sync: code-full

```{literalinclude} C-files/C2-files.py
:language: python
:caption: C2-files.py
```
:::
:::{tab-item} Diff from C1
:sync: code-diff

```{literalinclude} C-files/C2-files.diff
:language: diff
:caption: Changes from C1-files.py to C2-files.py
```
:::
::::

### C2: Sample output

````{dropdown} Sample output: $ python3 C2-files.py
```{literalinclude} C-files/C2.out
```
````

### C2: Next

In the next section ([tab **C3**](#tab-c3)) we will see
how to retrieve back that same file in order to close the loop.
:::::

:::::{tab-item} C3
:label: tab-c3

### C3: Objective

In this scenario, we extend again C2 to close the loop, and retrieve
our random file back on the local laptop.

```{figure} C-files/C3.png
:width: 60%
:align: center
:class: text-center

The C3 scenario
```

### The `Pull` object

The only new thing here is the use of a `Pull` object, which like for
the `Push` object, can be used in a list of commands to run on a given
node as part of a `SshJob`.

### C3: The code

:::{div}
:class: text-right
{download}`⬇ Download C3-files.py <C-files/C3-files.py>`
:::

::::{tab-set}
:::{tab-item} Full code
:sync: code-full

```{literalinclude} C-files/C3-files.py
:language: python
:caption: C3-files.py
```
:::
:::{tab-item} Diff from C2
:sync: code-diff

```{literalinclude} C-files/C3-files.diff
:language: diff
:caption: Changes from C2-files.py to C3-files.py
```
:::
::::

### C3: Sample output

````{dropdown} Sample output: $ python3 C3-files.py
```{literalinclude} C-files/C3.out
```
````

### C3: Next

If this is your first reading, we suggest you skip
C3bis ([tab **C3bis**](#tab-c3bis)) and go directly to
WRAPUP ([tab **WRAP UP**](#tab-c-files-wrap-up)) for a conclusion on this
series.
:::::

:::::{tab-item} C3bis
:label: tab-c3bis

### C3bis: Objective

In this particular scenario, we restart from C2.

Remember C2 is about transferring a file from node 1 to node 2 over
the data network, thanks to `netcat`. As we had seen at the time, it
is rather fortunate that `netcat` in server mode returns as soon as
its (single) client terminates.

There are a lot of cases though, where things are not that simple, and
where there is a need to manually terminate / cleanup dangling processes
that are no longer useful.

Sometimes, it is only a matter of starting and stopping packaged
services like apache or similar, and in this case all we need to do is
to call things like e.g. `systemctl start apache2` and `systemctl stop
apache2`.

In the code below, we will see a technique that can be used to start
and stop, and even monitor, a custom process. This is in
`receiver_manager_script`, a small shell script that knows how to
start, stop, and even monitor, a single-process service.

### C3bis: The code

Below you can see the difference with `C2-files.py`; the plain code for `C3bis-files.py` is in the dropdown.

```{figure} C-files/C3bis.png
:width: 60%
:align: center
:class: text-center

The C3bis scenario
```

:::{div}
:class: text-right
{download}`⬇ Download C3bis-files.py <C-files/C3bis-files.py>`
:::

::::{tab-set}
:::{tab-item} Full code
:sync: code-full

```{literalinclude} C-files/C3bis-files.py
:language: python
:caption: C3bis-files.py
```
:::
:::{tab-item} Diff from C2
:sync: code-diff

```{literalinclude} C-files/C3bis-files.diff
:language: diff
:caption: Changes from C2-files.py to C3bis-files.py
```
:::
::::

### C3bis: Sample output

````{dropdown} Sample output: $ python3 C3bis-files.py
```{literalinclude} C-files/C3bis.out
```
````

### C3bis: Next
We can now conclude this section ([tab **WRAP UP**](#tab-c-files-wrap-up))
:::::

:::::{tab-item} WRAP UP
:label: tab-c-files-wrap-up

In this C series , we have seen:

* how to use the `Push` and `Pull` commands to copy files back and
  forth on and from nodes;

* how to use the `LocalNode` to augment our scripts with commands run
  locally;

* how a single `SshJob` can trigger several commands, mixing `Run`,
  `RunString`, `Push` and `Pull` types of commands;

* how to implement (in C3bis) a rustic service management feature, for
  housekeeping purposes;

* and finally, still in C3bis, how to produce a graphical view of a
  `Scheduler` for documentation and/or troubleshooting.

In [the next tutorial](D-prep.md) we will see how to simply provide a
command-line option for loading images on nodes.
:::::

::::::
