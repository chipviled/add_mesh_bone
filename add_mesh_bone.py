# Bla-Bla-Bla.
# GPL.
# Begining on Rigify code.
# Created by Chip Viled.
#
#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

bl_info = {
    "name": "Add Mesh Bone",
    "author": "Chip Viled",
    "version": (0, 3),
    "blender": (2, 70, 0),
    "location": "W (in pose mode)",
    "description": "Add Mesh Bone",
    "warning": "Development version",
    "wiki_url": "",
    "category": "Rigging",
}


import bpy


WGT_PREFIX = "WGT-"
WGT_LAYER = 19
WGT_LAYERS = [x == WGT_LAYER  for x in range(0, 20)]


class MError(Exception):
    """ Exception raised for errors.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


def obj_to_bone(obj, rig, bone_name):
    """ Places an object at the location/rotation/scale of the given bone.
    """
    if bpy.context.mode == 'EDIT_ARMATURE':
        raise MError("obj_to_bone(): does not work while in edit mode")

    bone = rig.data.bones[bone_name]

    mat = rig.matrix_world * bone.matrix_local

    obj.location = mat.to_translation()

    obj.rotation_mode = 'XYZ'
    obj.rotation_euler = mat.to_euler()

    scl = mat.to_scale()
    scl_avg = (scl[0] + scl[1] + scl[2]) / 3
    obj.scale = (bone.length * scl_avg), (bone.length * scl_avg), (bone.length * scl_avg)


def create_widget(rig, bone_name, bone_transform_name=None):
    """ Creates an empty widget object for a bone, and returns the object.
    """
    if bone_transform_name == None:
        bone_transform_name = bone_name

    obj_name = WGT_PREFIX + bone_name
    scene = bpy.context.scene

    # Check if it already exists in the scene
    if obj_name in scene.objects:
        # Move object to bone position, in case it changed
        obj = scene.objects[obj_name]
        obj_to_bone(obj, rig, bone_transform_name)

        return None
    else:
        # Delete object if it exists in blend data but not scene data.
        # This is necessary so we can then create the object without
        # name conflicts.
        if obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].user_clear()
            bpy.data.objects.remove(bpy.data.objects[obj_name])

        # Create mesh object
        mesh = bpy.data.meshes.new(obj_name)
        obj = bpy.data.objects.new(obj_name, mesh)
        scene.objects.link(obj)

        # Move object to bone position and set layers
        obj_to_bone(obj, rig, bone_transform_name)
        obj.layers = WGT_LAYERS

        return obj


def create_circle_widget(rig, bone_name, radius=1.0, head_tail=0.0, with_line=False, bone_transform_name=None):
    """ Creates a basic circle widget, a circle around the y-axis.
        radius: the radius of the circle
        head_tail: where along the length of the bone the circle is (0.0=head, 1.0=tail)
    """
    obj = create_widget(rig, bone_name, bone_transform_name)
    if obj is not None:
        v = [(0.7071068286895752, 2.980232238769531e-07, -0.7071065306663513), (0.8314696550369263, 2.980232238769531e-07, -0.5555699467658997), (0.9238795042037964, 2.682209014892578e-07, -0.3826831877231598), (0.9807852506637573, 2.5331974029541016e-07, -0.19509011507034302), (1.0, 2.365559055306221e-07, 1.6105803979371558e-07), (0.9807853698730469, 2.2351741790771484e-07, 0.19509044289588928), (0.9238796234130859, 2.086162567138672e-07, 0.38268351554870605), (0.8314696550369263, 1.7881393432617188e-07, 0.5555704236030579), (0.7071068286895752, 1.7881393432617188e-07, 0.7071070075035095), (0.5555702447891235, 1.7881393432617188e-07, 0.8314698934555054), (0.38268327713012695, 1.7881393432617188e-07, 0.923879861831665), (0.19509008526802063, 1.7881393432617188e-07, 0.9807855486869812), (-3.2584136988589307e-07, 1.1920928955078125e-07, 1.000000238418579), (-0.19509072601795197, 1.7881393432617188e-07, 0.9807854294776917), (-0.3826838731765747, 1.7881393432617188e-07, 0.9238795638084412), (-0.5555707216262817, 1.7881393432617188e-07, 0.8314695358276367), (-0.7071071863174438, 1.7881393432617188e-07, 0.7071065902709961), (-0.8314700126647949, 1.7881393432617188e-07, 0.5555698871612549), (-0.923879861831665, 2.086162567138672e-07, 0.3826829195022583), (-0.9807853698730469, 2.2351741790771484e-07, 0.1950896978378296), (-1.0, 2.365559907957504e-07, -7.290432222362142e-07), (-0.9807850122451782, 2.5331974029541016e-07, -0.195091113448143), (-0.9238790273666382, 2.682209014892578e-07, -0.38268423080444336), (-0.831468939781189, 2.980232238769531e-07, -0.5555710196495056), (-0.7071058750152588, 2.980232238769531e-07, -0.707107424736023), (-0.555569052696228, 2.980232238769531e-07, -0.8314701318740845), (-0.38268208503723145, 2.980232238769531e-07, -0.923879861831665), (-0.19508881866931915, 2.980232238769531e-07, -0.9807853102684021), (1.6053570561780361e-06, 2.980232238769531e-07, -0.9999997615814209), (0.19509197771549225, 2.980232238769531e-07, -0.9807847142219543), (0.3826850652694702, 2.980232238769531e-07, -0.9238786101341248), (0.5555717945098877, 2.980232238769531e-07, -0.8314683437347412)]
        verts = [(a[0] * radius, head_tail, a[2] * radius) for a in v]
        if with_line:
            edges = [(28, 12), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (0, 31)]
        else:
            edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (0, 31)]

        verts.append( (0,0,0) )
        verts.append( (0,1,0) )
        edges.append( (32,33) )

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()
        return obj
    else:
        return None



class AddMeshBone(bpy.types.Operator):
    """Add Mesh Bone"""
    bl_idname = "object.add_mesh_bone_operator"
    bl_label = "Add Mesh Bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.mode != 'POSE':
            raise MError("Does not work outside POSE mode. You must select some bone.")

        bdb = bpy.context.scene.objects.active
        bb = bpy.context.active_pose_bone.name

        bpy.ops.object.mode_set(mode='OBJECT')
        ls_temp = bpy.context.scene.layers[WGT_LAYER]
        bpy.context.scene.layers[WGT_LAYER] = True

        create_circle_widget(bdb, bb, 0.3, 0.5)

        bpy.context.scene.layers[WGT_LAYER] = ls_temp
        bpy.ops.object.mode_set(mode='POSE')

        bpy.context.active_pose_bone.custom_shape = bpy.data.objects[WGT_PREFIX + bb]
        bpy.context.active_bone.show_wire = True

        return {'FINISHED'}


class DelMeshBone(bpy.types.Operator):
    """Del Mesh Bone"""
    bl_idname = "object.del_mesh_bone_operator"
    bl_label = "Del Mesh Bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.mode != 'POSE':
            raise MError("Does not work outside POSE mode. You must select some bone.")

        bdb = bpy.context.scene.objects.active
        bb = bpy.context.active_pose_bone.name

        bpy.context.active_pose_bone.custom_shape = None
        bpy.context.active_bone.show_wire = False

        bpy.ops.object.mode_set(mode='OBJECT')
        ls_temp = bpy.context.scene.layers[WGT_LAYER]
        bpy.context.scene.layers[WGT_LAYER] = True

        for ob in bpy.context.scene.objects:
            ob.select = ob.type == 'MESH' and ob.name.startswith(WGT_PREFIX + bb)
        bpy.ops.object.delete()

        bpy.context.scene.layers[WGT_LAYER] = ls_temp
        bpy.ops.object.mode_set(mode='POSE')

        return {'FINISHED'}


def add_object_button(self, context):
    self.layout.operator(
        AddMeshBone.bl_idname,
        text=AddMeshBone.__doc__,
        icon='PLUGIN')
    self.layout.operator(
        DelMeshBone.bl_idname,
        text=DelMeshBone.__doc__,
        icon='PLUGIN')


def register():
    bpy.utils.register_class(AddMeshBone)
    bpy.utils.register_class(DelMeshBone)
    bpy.types.VIEW3D_MT_pose_specials.append(add_object_button)

def unregister():
    bpy.utils.unregister_class(AddMeshBone)
    bpy.utils.unregister_class(DelMeshBone)
    bpy.types.VIEW3D_MT_pose_specials.remove(add_object_button)

if __name__ == "__main__":
    register()
