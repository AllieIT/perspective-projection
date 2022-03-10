# Perspective Projection

I made this project to practice what I learned about projections and matrix transformations during Linear Algebra classes - this is implementation of a 3D camera using PyGame, 2D game engine. I plan to develop this further to change it into dynamic 3D function plotter or Graphing Calculator.

![Perspective Projection Example](https://i.imgur.com/MiopB05.jpg)

# Installation

To use the program, you need to install some basic dependencies using pip: `pip install numpy pygame`

# Usage and working principle

Main entry point is `main.py` file, in which the Camera and main PyGame loop is initialized. `game_math` module implements 3D functionalities, such as vectors in 3-dimensional space, 3D planes and 3D lines, which are used for mathematical calculations in the program. 

The technique I've been using is:

- Creating a virtual plane perpendicular to the line of sight of the camera and cropping it to match the resolution
- Create 3D lines connecting points and the camera
- Calculate positions of intersection of aforementioned lines and the virtual camera plane
- Translating those positions into pixel positions on rendered screen and displaying them to the user

Controls:

- **Arrows** to change the orientation of the camera around the central point
- **Shift** key to speed up the rotation
- **Q** and **E** buttons to change the camera plane scale (change FOV)
- **O** and **P** buttons to change distance of the camera

An interesting fact to note is that when using O and E the perspective projection almost changes to orthogonal projection - the camera moves very far away and maintains low FOV, giving an impression of orthogonal view.
