
cpm_serial_port_action_set -- Set Serial port connection/disconnection commands in WTI OOB and PDU devices
==========================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Set Serial port connection/disconnection commands in WTI OOB and PDU devices






Parameters
----------

  cpm_url (True, str, None)
    This is the URL of the WTI device to send the module.


  cpm_username (True, str, None)
    This is the Username of the WTI device to send the module.


  cpm_password (True, str, None)
    This is the Password of the WTI device to send the module.


  use_https (False, bool, True)
    Designates to use an https connection or http connection.


  validate_certs (False, bool, True)
    If false, SSL certificates will not be validated. This should only be used

    on personally controlled sites using self-signed certificates.


  use_proxy (False, bool, False)
    F

    l

    a

    g

     

    t

    o

     

    c

    o

    n

    t

    r

    o

    l

     

    i

    f

     

    t

    h

    e

     

    l

    o

    o

    k

    u

    p

     

    w

    i

    l

    l

     

    o

    b

    s

    e

    r

    v

    e

     

    H

    T

    T

    P

     

    p

    r

    o

    x

    y

     

    e

    n

    v

    i

    r

    o

    n

    m

    e

    n

    t

     

    v

    a

    r

    i

    a

    b

    l

    e

    s

     

    w

    h

    e

    n

     

    p

    r

    e

    s

    e

    n

    t

    .


  port (True, int, None)
    This is the port number that is getting the action performed on.


  portremote (True, int, None)
    This is the port number that is getting the action performed on.


  action (False, int, None)
    This is the baud rate to assign to the port.

    1=Connect, 2=Disconnect





Notes
-----

.. note::
   - Use ``groups/cpm`` in ``module_defaults`` to set common options used between CPM modules.




Examples
--------

.. code-block:: yaml+jinja

    
    # Set Serial Port Action (Connect)
    - name: Connect port 2 to port 3 of a WTI device
      cpm_serial_port_action_set:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        port: "2"
        portremote: "3"
        action: "1"

    # Set Serial port Action (Disconnect)
    - name: Disconnect port 2 and 3 of a WTI device
      cpm_serial_port_action_set:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        port: "2"
        action: "2"



Return Values
-------------

  data (always, str, )
    The output JSON returned from the commands sent




Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- W
- e
- s
- t
- e
- r
- n
-  
- T
- e
- l
- e
- m
- a
- t
- i
- c
-  
- I
- n
- c
- .
-  
- (
- @
- w
- t
- i
- n
- e
- t
- w
- o
- r
- k
- g
- e
- a
- r
- )

