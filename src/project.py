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
    "L_clavicle_LOC",
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

    "L_clavicle_LOC": "spine03_LOC",
    "L_shoulder_LOC": "L_clavicle_LOC",

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
if joint_map.get("L_clavicle_LOC"):
    cmds.select(joint_map["L_clavicle_LOC"], hi=True)
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
        "L_clavicle_JNT",
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

center_joints = [
    "pelvis_JNT", "spine01_JNT", "spine02_JNT", "spine03_JNT", "neck_JNT"
]

left_joints = [
    "L_clavicle_JNT",
    "L_shoulder_JNT", "L_elbow_JNT", "L_wrist_JNT",
    "L_hip_JNT", "L_knee_JNT", "L_ankle_JNT"
]

right_joints = [
    "R_clavicle_JNT",
    "R_shoulder_JNT", "R_elbow_JNT", "R_wrist_JNT",
    "R_hip_JNT", "R_knee_JNT", "R_ankle_JNT"
]

def create_grp_con(jnt_name, side="C", radius=1.0):
    if not cmds.objExists(jnt_name):
        return None, None

    if jnt_name.endswith(("shoulder_JNT","elbow_JNT","wrist_JNT",
                          "hip_JNT","knee_JNT","ankle_JNT","clavicle_JNT")):
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
        elif jnt == "L_clavicle_JNT":
            cmds.parent(grp, "spine03_CON")
        elif parent:
            cmds.parent(grp, parent)
    parent = con

parent = None
for jnt in right_joints:
    grp, con = create_grp_con(jnt, side="R", radius=8)
    if grp:
        if jnt == "R_hip_JNT":
            cmds.parent(grp, "pelvis_CON")
        elif jnt == "R_clavicle_JNT":
            cmds.parent(grp, "spine03_CON")
        elif parent:
            cmds.parent(grp, parent)
    parent = con

#
# PHASE 3 : Build IK chains, create corrctly positioned and bold IK controls for 
# arms and legs, and add pole vector controls for elbows.
#

# Duplicate FK joints for each arm and leg to make IK joint chains
def duplicate_for_ik(joints):
    new = []
    for j in joints:
        if not cmds.objExists(j): continue
# Rename it to _ik_JNT
        ik_name = j.replace("_JNT","_ik_JNT")
# Parent duplicate like FK chain
        dup = cmds.duplicate(j,po=True,n=ik_name)[0]
        cmds.parent(dup,w=True)
        new.append(dup)
    for i in range(1,len(new)):
        cmds.parent(new[i],new[i-1])
    return new

left_arm_fk  = ["L_shoulder_JNT","L_elbow_JNT","L_wrist_JNT"]
right_arm_fk = ["R_shoulder_JNT","R_elbow_JNT","R_wrist_JNT"]
left_leg_fk  = ["L_hip_JNT","L_knee_JNT","L_ankle_JNT"]
right_leg_fk = ["R_hip_JNT","R_knee_JNT","R_ankle_JNT"]

L_arm_ik  = duplicate_for_ik(left_arm_fk)
R_arm_ik  = duplicate_for_ik(right_arm_fk)
L_leg_ik  = duplicate_for_ik(left_leg_fk)
R_leg_ik  = duplicate_for_ik(right_leg_fk)

# Create IKH for each chain
def make_ikh(start,end,name_prefix):
    ikh_name = name_prefix + "_IKH"
    ikh,eff = cmds.ikHandle(n=ikh_name,sj=start,ee=end,sol="ikRPsolver")
    return ikh

L_arm_IKH = make_ikh(L_arm_ik[0],L_arm_ik[-1],"L_arm")
R_arm_IKH = make_ikh(R_arm_ik[0],R_arm_ik[-1],"R_arm")
L_leg_IKH = make_ikh(L_leg_ik[0],L_leg_ik[-1],"L_leg")
R_leg_IKH = make_ikh(R_leg_ik[0],R_leg_ik[-1],"R_leg")

# Define function to create IK con for a target IK handle:
def make_ik_ctrl_upright_thick(name_prefix,target_ikh,color=17,radius=6,thickness=3):
    con_name = name_prefix + "_ik_CON"
    grp_name = name_prefix + "_ik_GRP"
#   Create con circle
    con = cmds.circle(n=con_name,ch=False,o=True,nr=[1,0,0],r=radius)[0]
#   Grp
    grp = cmds.group(con,n=grp_name)
#   Parent under the con
    cmds.delete(cmds.parentConstraint(target_ikh,grp))
    cmds.parent(target_ikh,con)
#   Set color
    cmds.setAttr(con+".overrideEnabled",1)
    cmds.setAttr(con+".overrideColor",color)
    shape = cmds.listRelatives(con,shapes=True)[0]
#   Make con bold
    cmds.setAttr(shape+".lineWidth",thickness)
    return grp,con

L_arm_grp,L_arm_con = make_ik_ctrl_upright_thick("L_arm",L_arm_IKH,COLOR_LEFT,6,3)
R_arm_grp,R_arm_con = make_ik_ctrl_upright_thick("R_arm",R_arm_IKH,COLOR_RIGHT,6,3)
L_leg_grp,L_leg_con = make_ik_ctrl_upright_thick("L_leg",L_leg_IKH,COLOR_LEFT,6,3)
R_leg_grp,R_leg_con = make_ik_ctrl_upright_thick("R_leg",R_leg_IKH,COLOR_RIGHT,6,3)

if cmds.objExists("placement_CON"):
    try:
        cmds.parent(L_arm_grp,"placement_CON")
        cmds.parent(R_arm_grp,"placement_CON")
        cmds.parent(L_leg_grp,"placement_CON")
        cmds.parent(R_leg_grp,"placement_CON")
    except: pass
# Apply to arm and leg IKH
# Parent IK con grps under placement_CON

# Create arm PV con
#   To calculate PV position:
#       Level with elbow
#       Push back along negative Z
#   Create con circle and grp
#   Set color
#   Constrain PV con to IKH
#   Parent PV grp under placement_CON