# Pseudocode for STEP 1 OF PROJECT

# Locator names
    # Center
center_locs = [
    "pelvis_LOC",
    "spine01_LOC",
    "spine02_LOC",
    "spine03_LOC",
    "neck_LOC",
]
    # Left Side
left_locs = [
    "L_shoulder_LOC",
    "L_elbow_LOC",
    "L_wrist_LOC",
    "L_hip_LOC",
    "L_knee_LOC",
    "L_ankle_LOC",
]

# Parenting Locators
parents = {
    # Center
    "spine01_LOC": "pelvis_LOC",
    "spine02_LOC": "spine01_LOC",
    "spine03_LOC": "spine02_LOC",
    "neck_LOC": "spine03_LOC",
    # Left Arm
    # Left Leg
    }
# Making Joints Out Of Locators
    # Center
    # Left

# Parenting Joints

# Orienting Joints
    # Center Chain
    # Left Arm Chain
    # Left Leg Chain

# Mirror Left Joints to Right
    # Mirror Arm
    # Mirror leg