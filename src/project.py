# Pseudocode for STEP 1 OF PROJECT

# note: Maya.cmds is for running this code in maya script editor. Ignore import error.
def build_skeleton():
    import maya.cmds as cmds
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
    "L_shoulder_LOC": "spine03_LOC",
    "L_elbow_LOC": "L_shoulder_LOC",
    "L_wrist_LOC": "L_elbow_LOC",
    # Left Leg
    "L_hip_LOC": "pelvis_LOC",
    "L_knee_LOC": "L_hip_LOC",
    "L_ankle_LOC": "L_knee_LOC",
    }

# Making Joints Out Of Locators
joint_map = {}
def create_joint(loc):
        if not cmds.objExists(loc):
            return None
        pos = cmds.xform(loc, q=True, ws=True, t=True)
        jnt_name = loc.replace("_LOC", "_JNT")
        jnt = cmds.joint(n=jnt_name, p=pos)
        cmds.select(clear=True)
        return jnt
    # Center
for loc in center_locs:
    joint_map[loc] = create_joint(loc)
    # Left
for loc in left_locs:
    joint_map[loc] = create_joint(loc)

# Parenting Joints

# Orienting Joints
    # Center Chain
    # Left Arm Chain
    # Left Leg Chain

# Mirror Left Joints to Right
    # Mirror Arm
    # Mirror leg