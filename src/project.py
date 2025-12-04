# note: Maya.cmds is for running this code in maya script editor. Ignore import error.
import maya.cmds as cmds

#
# PHASE 1 : Using markers to create basic biped heriarchy, groups, joints, joint heirarchy,
# and orienting joints. (No hands, feet, or head)
#

center_locs = [
    "pelvis_LOC",
    "spine01_LOC",
    "spine02_LOC",
    "spine03_LOC",
    "neck_LOC",
]
left_locs = [
    "L_shoulder_LOC",
    "L_elbow_LOC",
    "L_wrist_LOC",
    "L_hip_LOC",
    "L_knee_LOC",
    "L_ankle_LOC",
]
parents = {
    "spine01_LOC": "pelvis_LOC",
    "spine02_LOC": "spine01_LOC",
    "spine03_LOC": "spine02_LOC",
    "neck_LOC": "spine03_LOC",
    "L_shoulder_LOC": "spine03_LOC",
    "L_elbow_LOC": "L_shoulder_LOC",
    "L_wrist_LOC": "L_elbow_LOC",
    "L_hip_LOC": "pelvis_LOC",
    "L_knee_LOC": "L_hip_LOC",
    "L_ankle_LOC": "L_knee_LOC",
}

joint_map = {}
def create_joint(loc):
    if not cmds.objExists(loc):
        return None
    pos = cmds.xform(loc, q=True, ws=True, t=True)
    jnt_name = loc.replace("_LOC", "_JNT")
    jnt = cmds.joint(n=jnt_name, p=pos)
    cmds.select(clear=True)
    return jnt

for loc in center_locs:
    joint_map[loc] = create_joint(loc)
for loc in left_locs:
    joint_map[loc] = create_joint(loc)


for loc, parent_loc in parents.items():
    if joint_map.get(loc) and joint_map.get(parent_loc):
        cmds.parent(joint_map[loc], joint_map[parent_loc])

if joint_map.get("pelvis_LOC"):
    cmds.select(joint_map["pelvis_LOC"], hi=True)
    cmds.joint(e=True, orientJoint="xyz", secondaryAxisOrient="yup", zeroScaleOrient=True)
    cmds.select(clear=True)
if joint_map.get("L_shoulder_LOC"):
    cmds.select(joint_map["L_shoulder_LOC"], hi=True)
    cmds.joint(e=True, orientJoint="xyz", secondaryAxisOrient="yup", zeroScaleOrient=True)
    cmds.select(clear=True)
if joint_map.get("L_hip_LOC"):
    cmds.select(joint_map["L_hip_LOC"], hi=True)
    cmds.joint(e=True, orientJoint="xyz", secondaryAxisOrient="yup", zeroScaleOrient=True)
    cmds.select(clear=True)

if joint_map.get("L_shoulder_LOC"):
    cmds.mirrorJoint(
        "L_shoulder_JNT",
        mirrorYZ=True,
        mirrorBehavior=True,
        searchReplace=("L_", "R_")
    )
if joint_map.get("L_hip_LOC"):
    cmds.mirrorJoint(
        "L_hip_JNT",
        mirrorYZ=True,
        mirrorBehavior=True,
        searchReplace=("L_", "R_")
    )

#
# PHASE 2 : Creating NURBS controls for each joint, setting colors, and building a basic 
# control hierarchy.
#

# Add color to _CON

# Create _CON and _GRP
    # Create circle control
    # Move group to joint
    # Color override
    # Parent constraint joint to control

# Make hierarchy