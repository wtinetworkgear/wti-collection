
cpm_config_restore -- Send operational parameters to WTI OOB and PDU devices
============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Send operational parameters to WTI OOB and PDU devices






Parameters
----------

  cpm_url (True, str, None)
    This is the URL of the WTI device to get the parameters from.


  cpm_username (True, str, None)
    This is the Username of the WTI device to get the parameters from.


  cpm_password (True, str, None)
    This is the Password of the WTI device to get the parameters from.


  cpm_path (False, str, /tmp/)
    This is the directory path to the existing the WTI device configuration file.


  cpm_filename (True, str, None)
    This is the filename of the existing WTI device configuration file.


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





Notes
-----

.. note::
   - Use ``groups/cpm`` in ``module_defaults`` to set common options used between CPM modules.)




Examples
--------

.. code-block:: yaml+jinja

    
    -   name: Get the Parameters for a WTI device
        cpm_config_restore:
            cpm_url: "nonexist.wti.com"
            cpm_username: "super"
            cpm_password: "super"
            cpm_path: "/tmp/"
            cpm_filename: "wti-192-10-10-239-2020-02-13T16-05-57-xml"
            use_https: true
            validate_certs: false



Return Values
-------------

  data (always, complex, )
    The output XML configuration of the WTI device queried

    filelength (success, int, [{'filelength': 329439}])
      Length of the file uploaded in bytes

    status (success, list, [{'code': 0, 'text': 'ok', 'unittimestamp': '2020-02-14T00:18:57+00:00'}])
      List of status returns from backup operation





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

