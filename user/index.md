---
title: User guide
subtitle: The R2lab tutorials - let's get you started
---

# User guide

::::::{tab-set}

:::::{tab-item} INTRO
:label: tab-index-intro
### Infrastructure

[Sign up for an R2lab account](getting-started/registration.md)
: all information about how to register and schedule a node.

[Shell tools](getting-started/shell-tools.md) available in the R2lab gateway
: discover how to do basic control of the nodes by logging in at the
  `faraday.inria.fr` gateway from a regular `ssh` session: how to check for
  the nodes status, leases, images, and even phones.

[About graphic sessions](getting-started/graphic-sessions.md)
: running X11 and VNC sessions on the gateway and on the nodes.

### Examples of experimentation scripts with `nepi-ng`

[nepi-ng: install](nepi-ng/install.md)
: how to install `nepi-ng` on your laptop.

[nepi-ng: the basics](nepi-ng/A-ping.md) - a.k.a. the **A** series
: a couple of examples to get started with the `nepi-ng` network tool:

  - **A1**: simplest way to run a simple ping from `faraday.inria.fr` to
    `google.fr`;
  - **A2**: same functions, but can pass a slice name on the command line;
  - **A3**: run the ping from a node instead of from the gateway;
  - **A4**: check for a valid reservation;
  - **A5**: run ping between two nodes inside the chamber, on the wired
    network.

[nepi-ng: wireless](nepi-ng/B-wireless.md) - a.k.a. the **B** series
: a few more pings to see how one can initialize and configure wireless links:

  - **B1**: like A5, but on a wireless ad hoc network;
  - **B2**: same scenario, simplified by using `r2lab-id`;
  - **B3**: same scenario, but extract all the shell code in a single external
    file;
  - **B4**: add an infinite loop that prints out TICK every second;
  - **B5**: same but using a `Watch` instance for showing elapsed time instead.

[nepi-ng: file exchange](nepi-ng/C-files.md) - a.k.a. the **C** series
: a full loop doing file transfers, using SFTP to and from the nodes, and an
  example of file transfer between two nodes:

  - **C1**: a random file is produced locally, and pushed on one node;
  - **C2**: then transferred to a second node using netcat over the wired
    network;
  - **C3**: and retrieved back on the local laptop where it is compared with
    the original;
  - **C3bis**: a variant on C2, that deals with a service that is started and
    stopped in sync with another job.

[nepi-ng: preparation](nepi-ng/D-prep.md) - a.k.a. the **D** series
: examples that deal with preparing the testbed from a `nepi-ng` script:

  - **D1**: adding a command-line option to load images;
  - **D2**: turning off unused nodes while loading images;
  - **D3**: passing chosen nodes on the command line;
  - **D4**: using a nested scheduler, for more modular scripts.

[nepi-ng: troubleshooting guidelines](nepi-ng/troubleshooting.md)
: how to check for common mistakes, how to check your software environment,
  how to enable more verbosity.

[nepi-ng: real scale examples](nepi-ng/real-scale.md)
: dealing with any number of nodes, run pings between all couples of nodes.

### Other stuff

[R2lab and OpenAirInterface](offering-5g.md)
: some indications on the features present on R2lab to deploy experiments
  based on OpenAirInterface.

[FAQ](resources/faq.md)

[Video tutorials on YouTube](resources/youtube.md)
: an end-to-end wireless experiment, and an OAI 5G experiment (setting up an
  OpenAirInterface-based 5G infrastructure, and a tour in the chamber using
  Skype on a commercial android phone).

[Using notebooks](resources/notebooks.md)
:::::

:::::{tab-item} CONTACT
:label: tab-index-contact
### Contacts

If you have any issue with these tutorials, or with using R2lab more
generally, please contact us at
[fit-r2lab-users@inria.fr](mailto:fit-r2lab-users@inria.fr).

You can subscribe to the `fit-r2lab-users` discussion list by sending an email
to `sympa@inria.fr` with `subscribe fit-r2lab-users` in the body of the
message; or [simply click this link](mailto:sympa@inria.fr?subject=subscribe%20fit-r2lab-users).

### Chat room

% TODO: the legacy text mentions the `#r2lab` channel on freenode, which is
% most likely obsolete; to be verified and updated.

We use the `#r2lab` channel on freenode; also once you are logged into the
website, in [the RUN page](https://r2lab.inria.fr/run.md), you will find on top
of the page a button that will let you join this chat room in a single click.
:::::

::::::
