# Pet-Bot-NVIDIA-Jetson-Nano-And-JetBot

## Introduction
After the horrific pandemic of COVID-19, 
we are beginning to understand the 
importance of companionship in these 
isolated times. The presence of another 
being have helped us keep sane. In this 
project we have made a mere attempt to 
create a human-follower pet bot using 
Nvidia Jetson Nano. We have coupled the 
SSD Mobilenet object detection model 
along with Jetbot to control the motor
operations of the follower pet bot.

### Jetson Nano Developer Kit
The system uses an NVIDIA Jetson Nano™ 
Developer Kit2 which is a powerful single 
board computer that can be used to 
design systems having applications of 
machine learning algorithms like image 
classification, object detection, 
segmentation, and speech processing. 
It comes with a Quadcore ARM Cortex-A57
Processor operating at 1.43 GHz and a 
128-core Maxwell GPU. It has a 4 GB 
64-bit LPDDR4 memory, a 4K-capable HDMI 
Port to display output and MIPI-CSI camera
connector to connect camera modules.

### WaveShare JetBot AI Kit
In addition, the system was designed with 
Waveshare JetBot AI which equips the 
NVIDIA Jetson Nano™ with some new abilities
like moving around with its wheels and 
allows it to run on battery power as well. 
The kit can be purchased 
[here](https://www.waveshare.com/wiki/JetBot_AI_Kit).

<img src="https://m.media-amazon.com/images/I/61GVd95+FAL._AC_SL1000_.jpg" width="30%">
<img src="https://m.media-amazon.com/images/I/710Cq03jZzL._AC_SL1000_.jpg" width="34%">

Follow the instructions on the website on how to 
get started with the bot.


### JetPack OS
For configuring the OS for the NVIDIA® Jetson Nano™,
we used a pre-built JetBot SD card image published 
by NVIDIA. This image is based on the JetPack SDK 
developed by NVIDIA for all JetSon boards. It contains
bootloader, device drivers, a Linux kernel, file 
systems and necessary firmwares. They also provide
TensorRT, a deep learning inference runtime for 
machine learning tasks. We installed this image on 
SD card using the etcher software and that SD card
was used to boot up the JetBot.


### Jetson Inference Library
For inference and realtime DNN vision on NVIDIA 
Jetson Nano we use Jetson Inference Library. 
For installation guide, refer the GitHub repo 
[here](https://github.com/dusty-nv/jetson-inference).


## Workflow of Code
The PetBot follows the given steps:

1. The process starts by detecting the humans in the
frame using a ’ssd-mobilenet-v2’ model pre-trained
on Coco dataset and selecting the human with highest
confidence as a target human for interacting.


2. **Aligning Center:**
The bot now starts by aligning the center of the 
bounding box of the target human with the view. 
Once the bot has the target human, it finds it’s 
center(x,y) by using the bounding boxes and checks 
whether the x value is between the range of 600 and 680.
 
   * If the x value is less than 600, the robot moves
   towards left with:

         speed = 0.5 of max speed of robot for

         time = 0.5 × (600−x)/600 milliseconds
   
   * If the x value is more than 680, the robot moves 
    towards right with:

         speed = 0.5 of max speed of robot for

         time = 0.5 × (x−680)/680 milliseconds


3. **Move forward or backwards:**
   If the x value of center is between 600 
   and 680, the bot now decides whether to mode
   towards the human or to move away to keep a 
   safe distance. For this, we use the area of the
   bounding box of the target human.
   
   * If the value of area is less than 325000,
   the robot moves towards forwards towards the
   target human with:

         speed = 0.75 of max speed of robot for
         
         time = [(325000−area)/325000] milliseconds

   * If the value of area is more than 350000,
   the robot moves towards backward to stay
   away from the target human with:
      
         speed = 0.75 of max speed of robot for

         time = [(area−350000)/ 350000] milliseconds


4. Once all the conditions are satisfied, the bot 
remains stable and waits for interaction from
the target human and performs all above steps for 
every frame.

## Code Usage

1. Install Jetson Inference library, jetbot library,
opencv and any additional requirements if giving errors.
2. Run the main.py file provided as follows:
    ```python
    python main.py
    ```

# Conclusion
In this project, we successfully implemented a 
human-follower Pet robot. With the use of ssd-mobilenet-v2
Object Detection model, we were able to maintain a 
faster FPS as high as 22 with detection and motor 
controls on Jetson Nano board. The Robot library from 
Jetbot image made interfacing and controlling the 
motor functionalities really easy. There are many 
future prospects for this project such as adding more 
functionalities to the bot to equip it with ability to 
interact more with humans. For example, Pose 
Estimation/Gesture Recognition can be introduced to make
the bot perform some actions like 360°rotation. This 
way the bot can be enhanced to become more interactive.