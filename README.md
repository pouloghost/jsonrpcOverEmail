jsonrpcOverEmail
================
rpc is a really useful feature, but is grounded that one must have a server with a public ip.
to use rpc everywhere for everyone, a novel way of rpc is brought out: rpc over email.
this is not so good as a normal rpc with a server, mainly because of the delay of polling, but is good enough
to use as a small toy for fun.

the structure is as follows:

*server sends a private id to the client's email inbox
*client initalizes poller rpc sender based on the id
*the two can interact with each other by sending emails consists of jsonrpc objs
