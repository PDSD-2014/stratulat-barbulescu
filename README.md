stratulat-barbulescu
====================

Building and running the server
---------

The server is built using the Dockerfile, and packed in a LXC container.

To start the server you just need to run
`docker pull adrians/restraining_order_demo_server` and the `docker`
will download the virtual machine from the index of trusted builds.

To build the server locally, the command is `docker build - < Dockerfile`.
