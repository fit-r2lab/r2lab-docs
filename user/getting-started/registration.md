---
title: R2lab registration
---

# R2lab registration

::::::{tab-set}

:::::{tab-item} 1. REGISTER
### Introduction

First of all, welcome to R2lab; you are now part of a community of researchers
that use R2lab for their experiments, and we hope you will enjoy it.

You will do most of your interactions with R2lab through the **Reservation
Portal** at <https://r2lab.inria.fr>: it is the one used for daily operations,
like getting a reservation, and live monitoring of nodes status.

Since April 2017, you can also manage your ssh keys from this site.

### Entry point

Since March 2026, this site also manages user registration; click the
'Signup' link on the landing page to get to the registration form.

```{figure} img/tuto-register-0.png
:width: 80%
:align: center

The 'Signup' link on the landing page
```

At that point just fill in the form, shown below.

**Please** pay special attention to:

- the 'Your details' section; please provide as much background information as
  possible; this is the data upon which we will decide to accept or reject your
  registration request!
- the outlined checkbox: we appreciate that you are willing to cite the testbed
  in the event where you publish a paper that involved R2lab.

```{figure} img/tuto-register-1.png
:width: 80%
:align: center

The registration form
```

Once you register, and confirm your email address by acknowledging the
confirmation email, an **administrator will review** your request, and decide to
accept or reject it.

Upon acceptance, an email will be sent to confirm your subscription; it will
contain

- instructions to pick a password;
- the name of the slice that you can use to log in into the testbed.

From that point you can log in into the [Reservation Portal](https://r2lab.inria.fr/)
and you are almost ready to go, but you still need to **upload an SSH key**
before you can do anything useful. Let's move to the next tab, **2. SSHKEY**,
to do that.

:::{note}
Due to former abuse, we do not send an email in the case of a rejection; if
after a few days you believe your request has been rejected by mistake, please
contact us directly on the R2lab support mailing list
[fit-r2lab-dev@inria.fr](mailto:fit-r2lab-dev@inria.fr).
:::
:::::

:::::{tab-item} 2. SSHKEY
### Uploading your SSH public key to R2lab

Before you can start using the R2lab testbed, you'll need to **upload your SSH
public key** to R2lab. For this, let's follow 2 steps.

#### 1 - Generating an RSA key pair

- If you do not have a public key already, type in your terminal:

  ```bash
  ssh-keygen -t rsa
  ```

- Once you have entered the `ssh-keygen` command, you will get a few more
  questions. To simplify, you can press enter and use the given default values.

- The entire key generation process looks like this:

  ```{figure} img/tuto-register-2.png
  :width: 80%
  :align: center

  Generating a key pair
  ```

- The public key is now located under your home directory in
  `~/.ssh/id_rsa.pub`.

#### 2 - Upload your public key

In order to send us your **public key**, point your browser at the
[r2lab website](https://r2lab.inria.fr/), then:

- log in to your account using the *email*/*password* you already created;

- once inside your account, go to either the *BOOK* or *RUN* pages, and click
  the "slices & keys" link (gear icon; **A** in the figure below), which pops
  up a dialog dedicated to managing your slices and keys. If your public key is
  not listed there, use the "*Select public key file to add*" button (**B** in
  the figure) to choose the file that contains your public key, that will then
  be uploaded.

```{figure} img/tuto-register-3.png
:width: 80%
:align: center

Uploading your SSH key
```

:::{important}
- if you are not familiar with ssh keys, please be careful to **always select
  the public key**; the private key, as its name clearly states, is not
  supposed to be uploaded anywhere;

- in general, the key pair is located under a hidden folder (`~/.ssh/`). In the
  browser's file dialog, enable the *show hidden files* option to find it;

- under Windows, we have experienced issues when dealing with keys originating
  from the `putty` application; if this is your case we recommend that you
  generate another key pair with a more standard format.
:::

Once this is done, you should see something like this:

```{figure} img/tuto-register-4.png
:width: 80%
:align: center

An uploaded SSH key
```

You can then move to the next tab, **3. RESERVATION**, to book your slices in
R2lab.
:::::

:::::{tab-item} 3. RESERVATION
### Make the reservation

In order to use R2lab, you must reserve the testbed. The right way to do this
is using the [Reservation Portal - UI](https://r2lab.inria.fr/run.md). However,
you must be logged in to see the reservation page.

Once in the private area, just drag and drop the slice into the day calendar -
see **A** and **B** below.

If you want dates in the future, do the same as described above, but in the
[Reservation Portal - Calendar](https://r2lab.inria.fr/book.md).

Other actions you can do in the calendar:

- to **remove** or **cancel** a booking, double-click the slice already
  booked;

- to **move** a booked slice, drag it;

- to **increase** or **decrease** the duration of a booking, click and drag the
  tiny line at the bottom of each slice.

```{figure} img/tuto-reservation.png
:width: 80%
:align: center

Booking a slice in R2lab
```

When this is done, you can move to the next tab, **4. ACCESS**, to access the
R2lab platform and run your tests.
:::::

:::::{tab-item} 4. ACCESS
### The ssh agent

This step is optional, but worth reading for beginners.

When accessing R2lab, you will be authenticated through ssh. Your public key is
installed and authorized on the R2lab end, and in order to establish that you
are who you claim to be, you (i.e. your computer) will be challenged so as to
prove that you can access the corresponding private key.

When multiple ssh connections are created, it is traditionally easier to run an
ssh agent. The role of this software, that runs locally on your laptop, is to
work as a cache of private keys, so that you only need to enter the password
for your private key once when you log in into your laptop, rather than each
time an ssh session is created - which can happen a lot.

This is why, before you try to enter the R2lab gateway using your slice, we
recommend that you add your ssh **private** key in your ssh agent, for example

```bash
# in order to list the keys currently loaded in the agent
ssh-add -l
# in order to add one
ssh-add -K ~/.ssh/id_rsa
```

% TODO: `ssh-add -K` is deprecated on recent macOS, where it became
% `ssh-add --apple-use-keychain`; to be checked and documented properly.

### Your Unix account

The name that you need to use to enter the testbed using SSH is the name of the
unix account that has been created for you. The name of this unix account is
simply the **slice name**.

For example, in these tutorials we use the following names:

- slice name: `r2lab-tutorial`
- unix account / full slice name: `r2lab-tutorial`

At this point you should reach the R2lab platform by typing in your terminal:

```bash
ssh your_slicename@faraday.inria.fr
```

*If by any chance your public key is not at its standard location, and not
known to your ssh agent, then use the `-i` option on the command line to
specify its path.*

Once this command works for you, proceed to the next tutorial, where we see in
more detail [the tools available for manipulating the nodes](shell-tools.md).

### Problems?

Feel free to contact us on the **R2lab users mailing list**
[fit-r2lab-users@inria.fr](mailto:fit-r2lab-users@inria.fr) if you experience
trouble with ssh-logging into the R2lab gateway at `faraday.inria.fr`, or with
running your experiments, and/or none of those hints are helpful.
:::::

::::::
