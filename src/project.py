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
COLOR_LEFT = 6
COLOR_RIGHT = 13
COLOR_CENTER = 17

center_joints = ["pelvis_JNT", "spine01_JNT", "spine02_JNT", "spine03_JNT", "neck_JNT"]
left_joints = ["L_shoulder_JNT", "L_elbow_JNT", "L_wrist_JNT", "L_hip_JNT", "L_knee_JNT", "L_ankle_JNT"]
right_joints = ["R_shoulder_JNT", "R_elbow_JNT", "R_wrist_JNT", "R_hip_JNT", "R_knee_JNT", "R_ankle_JNT"]

# Create _CON and _GRP
def create_grp_con(jnt_name, side="C", radius=1.0):
    if not cmds.objExists(jnt_name):
        return None, None

    con_name = jnt_name.replace("_JNT", "_CON")
    grp_name = jnt_name.replace("_JNT", "_GRP")
    # Create circle control
    con = cmds.circle(n=con_name, ch=False, o=True, nr=[1,0,0], r=radius)[0]
    grp = cmds.group(con, n=grp_name)
    # Move group to joint
    cmds.delete(cmds.parentConstraint(jnt_name, grp))
    # Color override
    cmds.setAttr(con + ".overrideEnabled", 1)
    if side == "L":
        cmds.setAttr(con + ".overrideColor", COLOR_LEFT)
    elif side == "R":
        cmds.setAttr(con + ".overrideColor", COLOR_RIGHT)
    else:
        cmds.setAttr(con + ".overrideColor", COLOR_CENTER)
    # Parent constraint joint to control
    cmds.parentConstraint(con, jnt_name)
    return grp, con

# Make hierarchy (Center, Left, Right)
parent = None
for jnt in center_joints:
    grp, con = create_grp_con(jnt, side="C", radius=1.5)
    if grp and parent:
        cmds.parent(grp, parent)
    parent = con
