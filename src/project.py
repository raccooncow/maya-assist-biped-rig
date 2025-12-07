# note: Maya.cmds is for running this code in maya script editor. Ignore import error. 
import maya.cmds as cmds
import math

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

for orient_jnt in ["pelvis_LOC", "L_clavicle_LOC", "L_shoulder_LOC", "L_hip_LOC"]:
    if joint_map.get(orient_jnt):
        cmds.select(joint_map[orient_jnt], hi=True)
        cmds.joint(e=True, orientJoint="xyz", secondaryAxisOrient="yup", zeroScaleOrient=True)
        cmds.select(clear=True)

for mirror_jnt in ["L_clavicle_JNT", "L_hip_JNT"]:
    if cmds.objExists(mirror_jnt):
        mirror_name = "R_" + mirror_jnt[2:]
        cmds.mirrorJoint(
            mirror_jnt,
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

for end_jnt in ["neck_JNT", "L_ankle_JNT", "R_ankle_JNT"]:
    fix_end_joint(end_jnt)

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
    if jnt_name.endswith("_FK_JNT"):
        con_name = jnt_name.replace("_FK_JNT", "_FK_CON")
        grp_name = jnt_name.replace("_FK_JNT", "_FK_GRP")
        target_joint = jnt_name
    else:
        if jnt_name.endswith(("shoulder_JNT","elbow_JNT","wrist_JNT",
                              "hip_JNT","knee_JNT","ankle_JNT")):
            con_name = jnt_name.replace("_JNT", "_FK_CON")
        else:
            con_name = jnt_name.replace("_JNT", "_CON")
        grp_name = jnt_name.replace("_JNT", "_GRP")
        target_joint = jnt_name

    con = cmds.circle(n=con_name, ch=False, o=True, nr=[1,0,0], r=radius)[0]
    grp = cmds.group(con, n=grp_name)
    cmds.delete(cmds.parentConstraint(target_joint, grp))

    cmds.setAttr(con + ".overrideEnabled", 1)
    if side == "L":
        cmds.setAttr(con + ".overrideColor", COLOR_LEFT)
    elif side == "R":
        cmds.setAttr(con + ".overrideColor", COLOR_RIGHT)
    else:
        cmds.setAttr(con + ".overrideColor", COLOR_CENTER)

    cmds.parentConstraint(con, target_joint)
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
            try: cmds.parent(grp, "pelvis_CON")
            except: pass
        elif jnt == "L_clavicle_JNT":
            try: cmds.parent(grp, "spine03_CON")
            except: pass
        elif parent:
            try: cmds.parent(grp, parent)
            except: pass
    parent = con

parent = None
for jnt in right_joints:
    grp, con = create_grp_con(jnt, side="R", radius=8)
    if grp:
        if jnt == "R_hip_JNT":
            try: cmds.parent(grp, "pelvis_CON")
            except: pass
        elif jnt == "R_clavicle_JNT":
            try: cmds.parent(grp, "spine03_CON")
            except: pass
        elif parent:
            try: cmds.parent(grp, parent)
            except: pass
    parent = con

#
# PHASE 3 : Build IK chains, create corrctly positioned and bold IK controls for 
# arms and legs, and add pole vector controls for elbows.
#

def duplicate_for_IK(joints):
    new = []
    for j in joints:
        if not cmds.objExists(j): continue
        IK_name = j.replace("_JNT","_IK_JNT")
        if cmds.objExists(IK_name):
            try: cmds.delete(IK_name)
            except: pass
        dup = cmds.duplicate(j,po=True,n=IK_name)[0]
        cmds.parent(dup,w=True)
        new.append(dup)
    for i in range(1,len(new)):
        try: cmds.parent(new[i],new[i-1])
        except: pass
    return new

def duplicate_for_FK(joints):
    new = []
    for j in joints:
        if not cmds.objExists(j): continue
        FK_name = j.replace("_JNT","_FK_JNT")
        if cmds.objExists(FK_name):
            try: cmds.delete(FK_name)
            except: pass
        dup = cmds.duplicate(j, po=True, n=FK_name)[0]
        cmds.parent(dup, w=True)
        new.append(dup)
    for i in range(1,len(new)):
        try: cmds.parent(new[i], new[i-1])
        except: pass
    return new

left_arm_fk  = ["L_shoulder_JNT","L_elbow_JNT","L_wrist_JNT"]
right_arm_fk = ["R_shoulder_JNT","R_elbow_JNT","R_wrist_JNT"]
left_leg_fk  = ["L_hip_JNT","L_knee_JNT","L_ankle_JNT"]
right_leg_fk = ["R_hip_JNT","R_knee_JNT","R_ankle_JNT"]

L_arm_IK  = duplicate_for_IK(left_arm_fk)
R_arm_IK  = duplicate_for_IK(right_arm_fk)
L_leg_IK  = duplicate_for_IK(left_leg_fk)
R_leg_IK  = duplicate_for_IK(right_leg_fk)

L_arm_FK  = duplicate_for_FK(left_arm_fk)
R_arm_FK  = duplicate_for_FK(right_arm_fk)
L_leg_FK  = duplicate_for_FK(left_leg_fk)
R_leg_FK  = duplicate_for_FK(right_leg_fk)

try:
    if L_arm_FK and cmds.objExists("L_clavicle_JNT"):
        cmds.parent(L_arm_FK[0], "L_clavicle_JNT")
    if R_arm_FK and cmds.objExists("R_clavicle_JNT"):
        cmds.parent(R_arm_FK[0], "R_clavicle_JNT")
    if L_arm_IK and cmds.objExists("L_clavicle_JNT"):
        cmds.parent(L_arm_IK[0], "L_clavicle_JNT")
    if R_arm_IK and cmds.objExists("R_clavicle_JNT"):
        cmds.parent(R_arm_IK[0], "R_clavicle_JNT")
    if L_leg_FK and cmds.objExists("pelvis_JNT"):
        cmds.parent(L_leg_FK[0], "pelvis_JNT")
    if R_leg_FK and cmds.objExists("pelvis_JNT"):
        cmds.parent(R_leg_FK[0], "pelvis_JNT")
    if L_leg_IK and cmds.objExists("pelvis_JNT"):
        cmds.parent(L_leg_IK[0], "pelvis_JNT")
    if R_leg_IK and cmds.objExists("pelvis_JNT"):
        cmds.parent(R_leg_IK[0], "pelvis_JNT")
except:
    pass
def make_IKH(start,end,name_prefix):
    IKH_name = name_prefix + "_IKH"
    ikh,eff = cmds.ikHandle(n=IKH_name,sj=start,ee=end,sol="ikRPsolver")
    return ikh

L_arm_IKH = make_IKH(L_arm_IK[0],L_arm_IK[-1],"L_arm") if L_arm_IK else None
R_arm_IKH = make_IKH(R_arm_IK[0],R_arm_IK[-1],"R_arm") if R_arm_IK else None
L_leg_IKH = make_IKH(L_leg_IK[0],L_leg_IK[-1],"L_leg") if L_leg_IK else None
R_leg_IKH = make_IKH(R_leg_IK[0],R_leg_IK[-1],"R_leg") if R_leg_IK else None

def make_IK_ctrl(name_prefix, target_ikh, color=17, radius=6, thickness=3, normal=[1,0,0]):
    con_name = name_prefix + "_IK_CON"
    grp_name = name_prefix + "_IK_GRP"
    if cmds.objExists(con_name):
        try: cmds.delete(con_name)
        except: pass
    if cmds.objExists(grp_name):
        try: cmds.delete(grp_name)
        except: pass
    con = cmds.circle(n=con_name, ch=False, o=True, nr=normal, r=radius)[0]
    grp = cmds.group(con, n=grp_name)
    if target_ikh:
        cmds.delete(cmds.parentConstraint(target_ikh, grp))
        cmds.parent(target_ikh, con)
    cmds.setAttr(con+".overrideEnabled", 1)
    cmds.setAttr(con+".overrideColor", color)
    try:
        shape = cmds.listRelatives(con, shapes=True)[0]
        cmds.setAttr(shape+".lineWidth", thickness)
    except:
        pass
    return grp, con

L_arm_grp, L_arm_con = make_IK_ctrl("L_arm", L_arm_IKH, COLOR_LEFT, 6, 3, normal=[1,0,0])
R_arm_grp, R_arm_con = make_IK_ctrl("R_arm", R_arm_IKH, COLOR_RIGHT, 6, 3, normal=[1,0,0])
L_leg_grp, L_leg_con = make_IK_ctrl("L_leg", L_leg_IKH, COLOR_LEFT, 6, 3, normal=[0,1,0])
R_leg_grp, R_leg_con = make_IK_ctrl("R_leg", R_leg_IKH, COLOR_RIGHT, 6, 3, normal=[0,1,0])

if cmds.objExists("placement_CON"):
    try:
        cmds.parent(L_arm_grp,"placement_CON")
        cmds.parent(R_arm_grp,"placement_CON")
        cmds.parent(L_leg_grp,"placement_CON")
        cmds.parent(R_leg_grp,"placement_CON")
    except: pass

def create_arm_pv_control(shoulder_jnt, elbow_jnt, wrist_jnt, ikh, prefix, side_color, offset_scale=1.0):
    S = cmds.xform(shoulder_jnt, q=True, ws=True, t=True)
    E = cmds.xform(elbow_jnt, q=True, ws=True, t=True)
    W = cmds.xform(wrist_jnt, q=True, ws=True, t=True)
    arm_len = math.sqrt(sum((W[i]-S[i])**2 for i in range(3)))
    PV_pos = [E[0], E[1], E[2] - arm_len * offset_scale]
    ctrl_name = prefix + "_pv_IK_CON"
    grp_name = prefix + "_pv_IK_GRP"
    if cmds.objExists(ctrl_name): cmds.delete(ctrl_name)
    if cmds.objExists(grp_name): cmds.delete(grp_name)
    pv_ctrl = cmds.circle(n=ctrl_name, ch=False, o=True, nr=[1,0,0], r=2.0)[0]
    pv_grp = cmds.group(pv_ctrl, n=grp_name)
    cmds.xform(pv_grp, ws=True, t=PV_pos)
    cmds.setAttr(pv_ctrl + ".overrideEnabled", 1)
    cmds.setAttr(pv_ctrl + ".overrideColor", side_color)
    if ikh:
        cmds.poleVectorConstraint(pv_ctrl, ikh)
    if cmds.objExists("placement_CON"):
        cmds.parent(pv_grp, "placement_CON")
    return pv_grp, pv_ctrl

if L_arm_IKH:
    create_arm_pv_control("L_shoulder_IK_JNT","L_elbow_IK_JNT","L_wrist_IK_JNT",L_arm_IKH,"L_arm",COLOR_LEFT,1.0)
if R_arm_IKH:
    create_arm_pv_control("R_shoulder_IK_JNT","R_elbow_IK_JNT","R_wrist_IK_JNT",R_arm_IKH,"R_arm",COLOR_RIGHT,1.0)

def connect_fk_controls_and_clean(orig_jnt_list, fk_jnt_list):
    for orig_jnt, fk_jnt in zip(orig_jnt_list, fk_jnt_list):
        if not cmds.objExists(fk_jnt):
            continue
        con = orig_jnt.replace("_JNT", "_FK_CON")
        if cmds.objExists(orig_jnt):
            pcs = cmds.listRelatives(orig_jnt, type='parentConstraint') or []
            for pc in pcs:
                try: cmds.delete(pc)
                except: pass
        if con and cmds.objExists(fk_jnt):
            existing = cmds.listRelatives(fk_jnt, type='parentConstraint') or []
            for pc in existing:
                try: cmds.delete(pc)
                except: pass
            try:
                cmds.parentConstraint(con, fk_jnt, mo=True)
            except:
                pass
connect_fk_controls_and_clean(["L_shoulder_JNT","L_elbow_JNT","L_wrist_JNT"], L_arm_FK)
connect_fk_controls_and_clean(["R_shoulder_JNT","R_elbow_JNT","R_wrist_JNT"], R_arm_FK)
connect_fk_controls_and_clean(["L_hip_JNT","L_knee_JNT","L_ankle_JNT"], L_leg_FK)
connect_fk_controls_and_clean(["R_hip_JNT","R_knee_JNT","R_ankle_JNT"], R_leg_FK)