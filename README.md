# Maya Assist Biped Rig

## Demo
Demo Video: <URL>

## GitHub Repository
GitHub Repo: <https://github.com/raccooncow/maya-assist-biped-rig.git>

## Description
This project is a Python script that automates the creation of a basic bipedal rig in Autodesk Maya. It generates joints, FK/IK systems for arms and legs, and organizes everything into a clean hierarchy. By placing center and left-side locators, the script will create joints, mirror them to the right side, and generate controls for each joint, making the rig almost ready for animation. All the user has to do is place key locators at the following positions:

**Center Locators:**
  pelvis_LOC, 
  spine01_LOC, 
  spine02_LOC, 
  spine03_LOC, 
  neck_LOC

**Left Side Locators:**
  L_clavicle_LOC, 
  L_shoulder_LOC, 
  L_elbow_LOC, 
  L_wrist_LOC, 
  L_hip_LOC, 
  L_knee_LOC, 
  L_ankle_LOC

When the locators are placed, when running the script in Maya's "Script Editor" will build the rig, including mirrored right-side joints, FK and IK controls, pole vector controls for elbows, and a master hierarchy for easy scene management.

### Key Features
 - Joint Creation: Generate center and left-side joints from locators, mirrors the left to the right side, and correctly orients all joints.

 - FK and IK Systems: Duplicate arm and leg joint chains to create FK/IK chains, add NURBS controls, and connect controls to joints.

 - Control Colors: Color code left, right, and center controls by overriding colors for clarity.

 - Pole Vector Controls: Position pole vector controls for elbows based on arm joint position.

 - Hierarchy Organization: Create groups for joints, locators, controls, and geometry, and add all to master group for clean organization.

### Design Considerations
The script was designed for quick rig setup for animation purposes. The emphasis is on automation, clean hierarchies, and easy extensibility. Users only need to place locators to define joint positions; the script handles the rest. For future implementation, I would include hand, finger, and facial rig automation. I may also consider adding a user interface for easier execution and parameter customization. With all that being said, this project was meant to demonstrate how Python scripting can simplify time-intensive tasks in Maya.

### File Structure
project.py – The Python script that generates the basic bipedal rig.

requirements.txt – Libraries that are neccessary for code.

README.md – Project overview, instructions, and descriptions.