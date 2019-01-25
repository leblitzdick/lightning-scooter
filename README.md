## ⚡lightning⚡ payable e-scooter mit streamr support

The lightning-scooter is an e-scooter whose electric drive can be booked for a certain period of time. For the payment Bitcoin
Lightning is used. You choose on the display how long you want to drive, get a qr-code generated which you scan with a mobile 
phone lightning APP and pay. Then the power is switched on for the selected period and you can use the scooter. The special 
thing about this system is that it is mobile, i.e. the communication is completely realized via the mobile network.

On the 35C3 I offered the lightning-scooter for rent, it was a success.

Here is a small video of the booking process:

## streamr:

In addition to my previous project, the lightning-bike, the lightning-scooter has an integration with streamr, an open-source 
platform for the worldwide exchange of real-time data. Now every time you make a booking, data about the lightning-scooter is 
transmitted to the streamr network, including date, location, battery charge status and much more.

It is thus possible to document the use of the lightning-scooter and to receive information about the scooter online via the 
streamr platform at any time.

The following information is transferred to streamr during every new rental process, in the next picture you can see the content of
the stream:

In a test run I rented the scooter 4 times and then drove 1 minute, each time the status information was sent to streamr. From this
data I created a canvas with the streamr editor which collects the data from the stream. It is now possible to visualize the GPS
data in the canvas via the map module, so that the locations of the rent can be displayed. Since also date and time can be captured
now e.g. motion profiles can be generated.

## How does it work?

After the boot process, the client automatically starts the program on whose start screen you can currently choose between three
different usage times, 1, 3 and 5 minutes. The costs per minute are 250 satoshi that is approx. 0.01€.

The customer now selects the desired rental time and the program first determines the exact position of the scooter via GPS.
Then the current status data of the scooter is read out via Bluetooth. An internet connection is then established and the
collected information is transmitted to the streamr platform.

In the second step, an invoice is generated for the requested amount, which is transmitted to the lightning node via lightning-
charge. The client gets the payment information back from the lightning node and generates a qr-code which is shown to the
customer on the display.

The customer now has 60 seconds to scan the qr-code with his lightning APP in his mobile phone and then pay th invoice. During
this time the client tests the lightning node to see if the invoice is marked as paid.

If the payment is not confirmed within 60 seconds, the data is discarded and the program returns to the start screen. Here you
have the possibility to repeat the process.

If the payment has worked, the Internet connection will be disconnected and the system will turn on the power for the selected
time. The scooter is now ready to go! After the end of the paid time the power supply is interrupted and the rent is finished -
of course it rolls on, but only with muscle power. The program returns to the start screen and is ready for a new rental 
process.

