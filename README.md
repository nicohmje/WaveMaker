# Wave Generator for TECQUIPMENT FC80-5
Add-on accessory designed for the TECQUIPMENT 5m Flow and sediment transport channel.

Intended use is to simulate various waves, including rogue waves, which are chosen by the user through a computer or a Raspberry Pi. 

Mechanical design inspired by FC80N Wave Generator, but using two Dynamixel XL330-M288 servos and 3D printed parts. 

## Design / CAD  

First, the FC80-5 is measured, and the different parameters are defined. Chosen amplitude entails a 4 cm crankshaft, and the overall speed and responsiveness required makes the XL330-M288 the perfect motors for this use case. 

The existing FC80N is modeled, and the decision is made to keep the base and shaft bushing as they are machined aluminum which gives a nice heft that 3D printed parts wouldn't have. This significantly improves stability when displacing water. The use of the existing shaft bushing limits the shaft to a 20 cm diameter.

### 1. Bearings

The original design's joints use simple metal bushings for the pivots. The ensuing friction requires a lot of torque to smoothly overcome; this limits speed and requires a powerful motor with a significant amount of reduction (148:1 on the FC80N). Because Dynamixel Servos are to be used, all pivots will utilize ball bearings to smoothen motion and reduce motor load. 

Availability and price of bearings are a key factor in their selection; standard skateboard bearings can be found used for free in any skateboarding-related shop, and a smaller MR105-2RS bearing is used when the former don't fit. For the shaft linear motion, the original aluminum bushing provides a low enough friction coefficient that, with the right tolerance, the shaft slides smoothly back and forth with minimal side-to-side play.

### 2. 3D Printing

Every part is printed in PLA, as strength is not an issue at this scale. The shaft is printed vertically, which could lead to delamination of the layers in case of high tensile forces, but this has not been observed yet. If that were to be the case, a solution would be to print two shaft halves and glue them together. This would require support material for the joint-shaft inteface, which can increase friction because of poor surface finish. 

The plunger is printed with 10% infill to lighten it as much as possible. Possible upgrades include add-on surfaces to push the water more efficiently / in different ways. 


## Assembly

Every part fits together nicely. The U2D2 cables that go all the way to the servos don't have any routing guides, which could be added to the motor mount, as it must be ensured that they do not interfere with the crankshaft, which could lead to catastrophic tangles. 

The servos are held in place by screws, but a lack of the right sized screw prevents the crankshaft from being bolted to the motors; they are friction fitted, which works well but requires good alignment to work reliably. The plunger and shaft interface nicely with each other, with some light sanding done to the latter to improve surface finish.

## Testing

This has not been tested as of 24/11. 
