===========================
Advanced processing via WPS
===========================

In this section we will look at how to initiate an Iris script by making a Web Processing Service (WPS) call in a web browser. We can use ZOO Project on OSGeo Live to execute Iris commands via WPS.

The `ZOO Services Documentation <http://zoo-project.org/docs/services/index.html>`_ explains that we need to create a script containing our Iris python code (.py) and a corresponding configuration file (.zcfg).


Check that the ZOO Kernel is running
------------------------------------

First we'll check that ZOO is installed and is running correctly. Navigate to: http://localhost/zoo/?Request=GetCapabilities&Service=WPS

If ZOO Kernel is installed correctly you will see a screen full of information that lets you know what capabilities are available.

.. admonition:: Technical note:

   On OSGeo Live, making a request to http://localhost/zoo (/var/www/zoo) results in a redirection to http://localhost/cgi-bin/zoo_loader.cgi (/usr/lib/cgi-bin).
   ZOO Kernel's main.cfg file can be found in the same location as zoo_loader.cgi (e.g. /usr/lib/cgi-bin/main.cfg).


Hello World example
-------------------

Let's start with a simple Hello World python example from the ZOO `workshop examples <http://zoo-project.org/docs/workshop/2012/first_service.html>`_ (read the example and create your own version of Hello.zcfg).

.. admonition:: Remember...

   After you're created your .zcfg file, copy it into the same folder as zoo_loader.cgi, e.g.

   ``sudo cp Hello.zcfg /usr/lib/cgi-bin/``
   
To test that your new capability now exists, repeat the WPS GetCapabilities request. If you search the page for "Hello" you will find that your new web processing service is now listed:

.. code-block:: xml

   <wps:Process wps:processVersion="2">
     <ows:Identifier>Hello</ows:Identifier>
     <ows:Title>Return a hello message.</ows:Title>
     <ows:Abstract>Create a welcome string.</ows:Abstract>
   </wps:Process>

To get more details of the Hello service, make a DescribeProcess request:

.. code-block: none

   http://localhost/cgi-bin/zoo_loader.cgi?request=DescribeProcess&service=WPS&version=1.0.0&Identifier=Hello

This will return the full description from Hello.zcfg as an XML document.

Return to the same ZOO workshop example and scroll down to the section titled `The Hello Service <http://zoo-project.org/docs/workshop/2012/first_service.html#the-hello-service>`_. This gives the corresponding python code to take the supplied input (a person's name) and return a hello message with the person's name.

Let's ask for the result as raw output (a string):

.. code-block: none

   http://localhost/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0&Identifier=Hello&DataInputs=name=toto&RawDataOutput=Result


.. Note::

   You can find other ZOO Services example in the ZOO code repository at:

   .. code-block:: none
      
      http://zoo-project.org/trac/browser/trunk/zoo-project/zoo-services

