
# Maya Assist Biped Rig

## Repository
<https://github.com/raccooncow/maya-assist-biped-rig.git>

## Description
1-2 sentence description of what it will do and how it relevant to media and digital arts.
A Python rigging tool for Autodesk Maya, the user manually places key joints, and the program builds the rest of the rig, including hierarchy, controls, and IK/FK uses. This program will streamline the rigging process for animation, which is relevant to digital arts/media.

## Features
- User-placed joints/markers
    - The user will place core markers/joints that will be markers for the program to automatically make the remaining joints, set up hierarchy, orient them correctly, and apply constraints.
- IK/FK setup
    - The program will create inverse kinematics for the model's legs and forward kinematics for arms.
- Control curves
    - The program will create colored NURBS controls for joints and constrain them to the rig.
- Autonamic naming & organization
    - Automatically name joins, controls, groups, IK/FK setups and arrange them in a clean hierarchy.

## Challenges
- Learning how to use Maya Python and how to implement this program correctly.
- Arranging the hierarchy of all elements in the proper way.
- Creating IK/FK setup and correct implementation
- Handling mistake/error cases
- Making the program beginner-friendly

## Outcomes
Ideal Outcome:
- The user will place important markers on already made joints, and the program will create the rest of the rig, which the program will instantly generate.

Minimal Viable Outcome:
- Correctly oriented joints, IK/FK joints, Controls + groups, proper hierarchy for all groups, IK/FK joints, Controls + groups, proper hierarchy for controls.

## Milestones
- Week 1 (Nov 9 - Nov 15)
  1. Set up a GitHub repository
  2. Finalize PROPOSAL
  3. Create code for user-made joints/markers in MAYA
  4. Create code for basic hierarchy for the rig and orienting joints

- Week 2 (Nov 16 - Nov 22)
  1. Create code for colored Nurbs controls and constrain properly
  2. Create code for IK/FK legs and arms
  3. Create code for naming conventions and organizing into a basic hierarchy

- Week 3 (Nov 23 - Dec 7)
  1. Test programs and rigs, fix any errors
  2. Finalize READ ME, push final changes
  3. Record video demonstration
  4. Submit everything.