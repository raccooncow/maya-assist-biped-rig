# Maya Assist Biped Rig

## Demo
Demo Video: <URL>

## GitHub Repository
GitHub Repo: <https://github.com/raccooncow/maya-assist-biped-rig.git>

## Description
This project is a Python script that automates the creation of a basic bipedal rig in Autodesk Maya. It generates joints, FK/IK systems for arms and legs, and organizes everything into a clean hierarchy. By placing center and left-side locators, the script will create joints, mirror them to the right side, and generate controls for each joint, making the rig almost ready for animation.  

*All the user has to do is place key locators at the following positions:*

**Center Locators:**
  - pelvis_LOC
  - spine01_LOC
  - spine02_LOC
  - spine03_LOC
  - neck_LOC

**Left Side Locators:**
  - L_clavicle_LOC
  - L_shoulder_LOC
  - L_elbow_LOC
  - L_wrist_LOC
  - L_hip_LOC
  - L_knee_LOC
  - L_ankle_LOC

When the locators are placed, when running the script in Maya's "Script Editor" will build the rig, including mirrored right-side joints, FK and IK controls, pole vector controls for elbows, and a master hierarchy for easy scene management.

### Key Features
### File Structure
### Design Considerations