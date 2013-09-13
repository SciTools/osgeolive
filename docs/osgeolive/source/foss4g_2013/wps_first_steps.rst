========================
Getting started with WPS
========================

In this section we will look at how to use a Python script to provide
the processing power behind a Web Processing Service (WPS) service, and
how to explore the WPS service with a web browser.

We will use the ZOO Project on OSGeo Live to handle the WPS protocol and
translate it into a Python-friendly interface.

The ZOO kernel
--------------

First, check that ZOO is installed and is running correctly. Navigate to:
    http://localhost/zoo/?Request=GetCapabilities&Service=WPS

If ZOO Kernel is installed correctly you will see a screen full of
XML that lists the capabilities available on this server. This XML is
not intended for human consumption, so don't be put off by the apparent
complexity!

On OSGeo-Live, all the files used by ZOO are found in `/usr/lib/cgi-bin`.
During this tutorial you will need to add/edit files in this directory,
but by default this directory can only be modified with `root` user
permissions. So to avoid the need to use the `root` user or `sudo`, you
should modify the permission for the directory to allow anyone to update
the contents.

.. code-block:: bash

   sudo chmod o+w /usr/lib/cgi-bin

NB. This is a hack to simplify the tutorial. You should never use this
technique in real life!

.. admonition:: Technical note:

   On OSGeo Live, making a request to http://localhost/zoo (/var/www/zoo/)
   results in a redirection to http://localhost/cgi-bin/zoo_loader.cgi
   (/usr/lib/cgi-bin/).

   ZOO Kernel's main.cfg file can be found in the same location as
   zoo_loader.cgi (e.g. /usr/lib/cgi-bin/main.cfg).


"Hello world!" example
----------------------

Let's start with a simple "Hello world!" example from the ZOO workshop
examples [#f1]_.

A ZOO service is composed of two pieces. A textual configuration file
which describes the service, and a corresponding code file containing
the implementation of that service.

First you'll create the configuration file which will let ZOO
list your service in its catalogue, and describe your service to anyone
who requests more information. Then you'll create the Python code which
will perform the computation of the service.

Declaring your service
^^^^^^^^^^^^^^^^^^^^^^
    *Lions and tigers, and bears! Oh my!*

First, you need to create your own version of `Hello.zcfg`. Remember,
all the files for ZOO services are located in `/usr/lib/cgi-bin/`.

.. literalinclude:: ../solutions/zoo_helloworld/Hello.zcfg
    :language: xml

This file declares a new ZOO service named "Hello", which accepts the
parameter "name" (which must be a string) and returns a value called
"Result" (which is also a string).

The `serviceType` parameter tells ZOO to use Python to process the
request. The `serviceProvider` parameter defines which Python file
contains the code to execute. And the name of the servce ("Hello" in
this case) defines the name of the Python function that ZOO will
execute. For our example, ZOO is performing the equivalent of:

.. code-block:: python

    import test_service
    test_service.Hello(...)

Further details on this configuration file format can be found in the
`ZOO reference documentation
<http://zoo-project.org/docs/services/zcfg-reference.html>`_.

To test that your new capability now exists, repeat the WPS
GetCapabilities request. If you search the page for "Hello" you will
find that your new web processing service is now listed:

.. code-block:: xml

   <wps:Process wps:processVersion="2">
     <ows:Identifier>Hello</ows:Identifier>
     <ows:Title>Return a hello message.</ows:Title>
     <ows:Abstract>Create a welcome string.</ows:Abstract>
   </wps:Process>

To get more details of the Hello service, make a DescribeProcess request:
   http://localhost/cgi-bin/zoo_loader.cgi?request=DescribeProcess&service=WPS&version=1.0.0&Identifier=Hello

This will return the full description from Hello.zcfg as an XML document:

.. literalinclude:: hello_description.xml
    :language: xml

Providing the engine
^^^^^^^^^^^^^^^^^^^^
    *Pay no attention to that man behind the curtain.*

Now that you've described the service, you need to supply the
implementation. At its simplest, this is just a single Python file
containing a single function.

As with the configuration file, the Python file should be located in
`/usr/lib/cgi-bin/`. And remember, the Python file name must match the
value of the `serviceProvider` field in the configuration file, and the
function name must match the name of the service.

The arguments supplied to the function are:

`conf`
    The information from ZOO's main configuration file (`main.cfg`)
    supplied as nested dictionaries. For this workshop we won't need
    to use this information.

`inputs`
    The argument definitions and incoming values from the WPS request,
    supplied as nested dictionaries. NB. This is *not* a simple
    dictionary mapping from input names to values.

    For your example service which declares the single parameter `name`,
    this will be something like:

.. code-block:: python

    {
        'name': {
            'maxOccurs': '1',
            'dataType': 'string',
            'minOccurs': '1',
            'value': ... whatever value was submitted ...,
            'inRequest': 'true'
        }
    }

`outputs`
    The output definitions, supplied as nested dictionaries.

    For your example service which declares the single output `Result`,
    this will initially be:

.. code-block:: python

    {
        'Result': {
            'dataType': 'string',
            'inRequest': 'false'
        }
    }


It is the job of your function to add a `'value'` key and its
corresponding value to each relevant output dictionary, and to return
a success/failure code as appropriate. The success code is 3, the
failure code is 4.

Now you're all set to write your `Hello()` function to give a friendly,
personalised message. From the description above we can see that to
access the incoming value you need to use `inputs['name']['value']`, and
you need to place the outgoing result in `outputs['Result']['value']`.

Your function should look something like:

.. literalinclude:: ../solutions/zoo_helloworld/test_service.py
    :language: python

Testing the service
^^^^^^^^^^^^^^^^^^^
    *We're off to see the wizard!*

To see your service in action, the simplest request is:
   http://localhost/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0&Identifier=Hello&DataInputs=name=Dorothy

This will return an XML document which contains the output of your
`Hello()` function embedded within it. For example:

.. literalinclude:: hello_response.xml
    :language: python

.. note::

    The inputs for a WPS service are not encoded in the same way as
    normal URL arguments. Instead, they are all combined into a single
    URL argument `DataInputs`. For simple inputs, as used in this
    tutorial, this argument has the value: `key1=value1;key2=value2;...`.

    For more complex inputs with multiple associated attributes, the
    geoprocessing.info website contains a `detailed description
    <http://geoprocessing.info/wpsdoc/1x0ExecuteGETEncoding>`_ of the
    encoding process.

You can also ask for raw output by specifying the name of an output. In
this case you can ask for `Result` and it will give you a simple string:

   http://localhost/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0&Identifier=Hello&DataInputs=name=Dorothy&RawDataOutput=Result

.. code-block:: none

    Hello Dorothy from ZOO!

Congratulations! You have successfully created a genuine WPS service!


.. rubric:: Footnotes

.. [#f1] `ZOO workshop examples <http://zoo-project.org/docs/workshop/2012/first_service.html>`_

   You can find other ZOO Services examples in the ZOO code repository
   at:

      http://zoo-project.org/trac/browser/trunk/zoo-project/zoo-services
