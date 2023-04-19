# STALKR (Self Transiting Autonomous Lurking Killer Robot)
This Repository contains the Code and other resources used in the STALKR project. The STALKR project is a course project of the [MECH 464 Industrial Robotics Course](https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept=MECH&course=464) at University of British Columbia (UBC). 

The goal of the project was to create a robot that could follow a person using input from an RGB camera.

## Robot Architecture
The Robot is built using the following components:
* iRobot Create 
* Raspberry Pi 4 (with raspian OS)
* Powerbank
* Raspberry Camera
* Raspberrry Pi Screen Module

We mounted the components to the iRobot create in the following way:

![picture alt](https://github.com/aurelappius/STALKR/blob/master/documentation/images/system_architecture.png "System Architecture")

## Computer Vision

## Controls
To control the robot, we use this exteremly simple control approach. If we detect the person on the left side of the image, we go right, and if we see it on the right side of the image we go left. This makes the robot follow the person. Based on the size of the bounding box, we define a stopping criterion which makes the robot stop once it is sufficiently close to the person.

## Code
The code uses the ```pycreate2``` python library to communicate with the iRobot. The Computervision algorithms are based on ```openCV```. The codebase contains the following two executables:
* ```follow_face.py``` was the first app that we used during development. It uses the Haar-Cascade Face Detection Algorithm to find a face in the camera image. After a successful try, we switched to ```follow_person``` because when following a person from behind, the face is usually not visible. 
* ```follow_person.py``` 

## Demonstration
The following youtube video shows a successful demonstration of the ```follow_person.py``` script runnning on our robot.

[ ![IMAGE ALT TEXT](http://img.youtube.com/vi/n8nV72KoJ5c/0.jpg) ](http://www.youtube.com/watch?v=n8nV72KoJ5c  "MECH 464 Project Video")