# Lumos
This is the source code repository: [Lumos: An Open-Source Device for Wearable Spectroscopy Research](https://dl.acm.org/doi/10.1145/3569502). 
It was accepted in the Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies (IMWUT), Dec round, 2022.
### What's Included?
1. Hardware & Schematics
2. Form Factor Designs
3. Arduino Code
4. Python Source Code for the Wavelength Detection Algorithm
5. Example Python Code for Detecting the Wavelength of Various Mediums

### Installation
Install dependencies for the project using pip: ``` pip install -r requiremnets.txt```

### 1. Hardware & Schematics
Hardware and Schematics contains a list of components needed to put together a Lumos device, the schematics for our custom PCB, and instructions for purchasing the PCB.
@Anush - Add instructions for how to put together the board. Eventually, would be useful to have a place to purchase a full put together device minus the form factors.

### 2. Form Factor Designs
Form factor designs contain the @Anush - need you input here. 3D printer files and the CAD renderings @Anush used in the paper. @Anush add any instructions here about how to print the form factors, for example, what kind of plastic? 

### 3. Arduino Code
Here we include the wiring/circuit diagram for our device and the code used to control it. 
To setup the hardware: 
  1. Use the Arduino Nano 33 IoT and the Adafruit AS7341 10-Channel Light / Color Sensor Breakout Board and follow the wiring diagram provided.
  2. Additional information on the Arduino Nano 33 IoT: https://docs.arduino.cc/hardware/nano-33-iot 
  3. Additional information on the Adafruit AS7341 10-Channel Light / Color Sensor Breakout Board: https://www.adafruit.com/product/4698 

To run the Arduino Code: 
  1. Download and open the Arduino IDE. 
  2. Download necessary libraries. 
  3. Fill in the blanks in the Arduino Code to customize it for your setup. 
  4. Compile and upload the code to the Arduino. 
  5. Additional information on Arduino: https://www.arduino.cc/ 
Our code is based off of: https://github.com/aawatson22/Raproto-Arduino

### 4. Algorithm that determines the spectral response of a medium. 
An example notebook as been provided under /Spectral_Response_of_Medium/Example.pynb, along with sample medium, LED, and PD data in CSV format. The associated .py files are found under the same directory (Spectral_Response.py, Theoretical_Approx.py, etc).