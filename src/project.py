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

def fix_end_joint(jnt):
    if not cmds.objExists(jnt):
        return
    tmp = cmds.spaceLocator()[0]
    cmds.delete(cmds.aimConstraint(tmp, jnt, aimVector=[1,0,0], upVector=[0,1,0], worldUpType="scene"))
    cmds.delete(tmp)
    cmds.makeIdentity(jnt, apply=True, jointOrient=True)

fix_end_joint("neck_JNT")
fix_end_joint("L_ankle_JNT")
fix_end_joint("R_ankle_JNT")

#
# PHASE 2 : Creating NURBS controls for each joint, setting colors, and building a basic 
# control hierarchy.
#

COLOR_LEFT = 6
COLOR_RIGHT = 13
COLOR_CENTER = 17

center_joints = ["pelvis_JNT", "spine01_JNT", "spine02_JNT", "spine03_JNT", "neck_JNT"]
left_joints = ["L_shoulder_JNT", "L_elbow_JNT", "L_wrist_JNT", "L_hip_JNT", "L_knee_JNT", "L_ankle_JNT"]
right_joints = ["R_shoulder_JNT", "R_elbow_JNT", "R_wrist_JNT", "R_hip_JNT", "R_knee_JNT", "R_ankle_JNT"]

def create_grp_con(jnt_name, side="C", radius=1.0):
    if not cmds.objExists(jnt_name):
        return None, None

    if jnt_name in ["L_shoulder_JNT","L_elbow_JNT","L_wrist_JNT","L_hip_JNT","L_knee_JNT","L_ankle_JNT",
                    "R_shoulder_JNT","R_elbow_JNT","R_wrist_JNT","R_hip_JNT","R_knee_JNT","R_ankle_JNT"]:
        con_name = jnt_name.replace("_JNT", "_FK_CON")
    else:
        con_name = jnt_name.replace("_JNT", "_CON")

    grp_name = jnt_name.replace("_JNT", "_GRP")

    con = cmds.circle(n=con_name, ch=False, o=True, nr=[1,0,0], r=radius)[0]
    grp = cmds.group(con, n=grp_name)

    cmds.delete(cmds.parentConstraint(jnt_name, grp))

    cmds.setAttr(con + ".overrideEnabled", 1)
    if side == "L":
        cmds.setAttr(con + ".overrideColor", COLOR_LEFT)
    elif side == "R":
        cmds.setAttr(con + ".overrideColor", COLOR_RIGHT)
    else:
        cmds.setAttr(con + ".overrideColor", COLOR_CENTER)

    cmds.parentConstraint(con, jnt_name)
    return grp, con

placement_con = cmds.circle(n="placement_CON", ch=False, o=True, nr=[0,1,0], r=20)[0]
placement_grp = cmds.group(placement_con, n="placement_GRP")
cmds.xform(placement_grp, ws=True, t=[0,0,0])
cmds.setAttr(placement_con + ".overrideEnabled", 1)
cmds.setAttr(placement_con + ".overrideColor", COLOR_CENTER)

parent = placement_con
for jnt in center_joints:
    grp, con = create_grp_con(jnt, side="C", radius=16)
    if grp:
        cmds.parent(grp, parent)
    parent = con

parent = None
for jnt in left_joints:
    grp, con = create_grp_con(jnt, side="L", radius=8)
    if grp:
        if jnt == "L_hip_JNT":
            cmds.parent(grp, "pelvis_CON")
        elif jnt == "L_shoulder_JNT":
            cmds.parent(grp, "spine02_CON")
        elif parent:
            cmds.parent(grp, parent)
    parent = con

parent = None
for jnt in right_joints:
    grp, con = create_grp_con(jnt, side="R", radius=8)
    if grp:
        if jnt == "R_hip_JNT":
            cmds.parent(grp, "pelvis_CON")
        elif jnt == "R_shoulder_JNT":
            cmds.parent(grp, "spine02_CON")
        elif parent:
            cmds.parent(grp, parent)
    parent = con