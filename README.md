# ⚡lightning⚡ payable e-scooter

The lightning-scooter is an e-scooter (Xiaomi m365) whose electric drive can be booked for a certain period of time. 
It uses lightning as a payment system to activate this function. You choose on the display how long you want to drive, 
gets a qr-code generated which you can scan and pay with your mobile lightning APP, whereupon the power for the chosen
period is switched on. What is special about this system is that it is mobile, i.e. communication is via the mobile network.
and the power supply comes from the batteries of the e-scooter.   

![lscooter](img/IMG_20181212_150030.jpg)
![lscooter35c3](img/1.jpg)


## How does it work?

The client automatically establishes a connection to the Internet after the boot process with a GSM/GPRS GPIO HAT. The program starts
and the display shows the start screen where you can currently choose between three different times of use.
250 satoshi are required per minute. 

The customer selects the time period and the program generates a payment request, which is sent to the node of the
server is transmitted. The client gets the payment information back from the server, generates a qr-code from it which is
is shown to the customer on the display. The customer now has 60 seconds to scan the qr-code with his lightning APP in his mobile phone.
and to pay. As long as the client tests with the server whether the invoice is shown as paid.

If the payment has worked, the power is switched on by the system for the chosen time and you can drive!!! 
After the end of the paid time the system switches off and the power supply is interrupted - of course you can continue to roll,
but only with muscle power. The program returns to the start screen and you can book new time again. Doesn't it 
the start screen is called and you can try it again.



[![Lscooter-video](https://img.youtube.com/vi/Japhx4_71Qo/0.jpg)](https://www.youtube.com/watch?v=Japhx4_71Qo)
![Main](img/IMG_20181228_164816.jpg)
![QR](img/IMG_20181228_164839.jpg)
![Invoice](img/invoice.png)
![Payed](img/payed.png)
![Enjoy](img/enjoy.png)

## System setup:

The heart of the system is a Raspberry Pi Zero WH, which provides both the connection to the mobile network as well as the circuitry of the 
Power supply controlled by relay. An e-paper display is used as the monitor, which is also practically the same as the 
4 pressure switches for the control unit. I took the e-paper display because in display mode it is as good as 
does not actually consume electricity only when the image content changes. It has a high contrast and is easy to read even on sunny days. The picture construction is relatively tough with approx. 6 sec., but only 2 steps/pictures are displayed.
needed to complete the payment process.  

On the server side there is a Raspberry Pi 3B with the Bitcoin blockchain https://bitcoincore.org/ and a lightning node based on c-lightning https://github.com/ElementsProject/lightning installed. For the control of the lightning node lightning-charge API https://github.com/ElementsProject/lightning-charge is used, which made it very easy to program the payment processes.

On the client side I took care to use power saving components, so I made a lot of choices. 
on a raspberry Pi Zero WH with an e-paper display. On
maybe there's something better. The relay for switching the current is classically controlled via GPIO and also the 
4 Pressure switch of the e-paper polled via GPIO.

### Components Server:
- Raspberry Pi 3
- 16GB microSD card
- Standard housing black
- microUSB cable
- power supply
- network cables

### Components Client:
- Raspberry Pi Zero WH
- 16GB microSD card
- Waveshare 2.7inch E-Ink display 264x176 px 
- Waveshare GSM/GPRS/GNSS/Bluetooth HAT
  (prepaid by Tchibo :-) (Provider network O2)
- 2x 1 channel relay 5V/230V
- Yeeco DC/DC Converter 8-50V 12V/24V/36V/48V to 5V3A / 15W Watertight
- Self-designed housing made of PLA
- Cable, solder, hot glue, mounting tape, etc.


## To the e-scooter:

I took a Xiaomi m365 because it is one of the most popular scooters on the market and is also used by commercial e-scooter rental companies.    

