


"""

此插件免费提供下载禁止倒卖

"""


import bpy
import math
import numpy as np

def euler_to_matrix(angles):
    # 将欧拉角转换为三维旋转矩阵
    x, y, z = angles
    rot_x = np.array([[1, 0, 0], [0, np.cos(x), -np.sin(x)], [0, np.sin(x), np.cos(x)]])
    rot_y = np.array([[np.cos(y), 0, np.sin(y)], [0, 1, 0], [-np.sin(y), 0, np.cos(y)]])
    rot_z = np.array([[np.cos(z), -np.sin(z), 0], [np.sin(z), np.cos(z), 0], [0, 0, 1]])
    R = np.dot(np.dot(rot_z, rot_y), rot_x)
    return R

def matrix_to_euler(matrix):
    # 将三维旋转矩阵转换为欧拉角
    x = np.arctan2(matrix[2,1], matrix[2,2])
    y = np.arctan2(-matrix[2,0], np.sqrt(matrix[2,1]**2 + matrix[2,2]**2))
    z = np.arctan2(matrix[1,0], matrix[0,0])
    angles = np.array([x, y, z])
    return angles

def old_rotation(original_angles, rotation_angles):
    # 计算旋转后的欧拉角
    original_matrix = euler_to_matrix(original_angles)
    rotation_matrix = euler_to_matrix(rotation_angles)
    rotated_matrix = np.dot(rotation_matrix, original_matrix)
    rotated_angles = matrix_to_euler(rotated_matrix)
    return rotated_angles

#全局坐标到局部坐标
def transform_point(old_location, translation, rotation):
    transformed_point = np.dot(euler_to_matrix(rotation), old_location) + translation
    return transformed_point


#局部坐标到全局坐标
def inv_transform_point(new_location, translation, rotation):
    inverse_rotation = np.linalg.inv(euler_to_matrix(rotation))
    original_point = np.dot(inverse_rotation, new_location - translation)
    return original_point







#插件信息
bl_info = {
    "name":"一键径向对称工具",
    "version": (2, 0),
    "author":"青梅酒票",
    "blender": (3,4,1),
    "description": "此插件可以快速生成径向对称物体（阵列修改器法），方便后续修改",
    "category":"工具"
}

#储存选中的轴
global_S_location = [True,False,False]  #分别对应xyz 默认选项为true


#选择世界坐标时主功能函数
def creat_mod(def_number,Radial_symmetry_tool):
    #获取选中物体 obj
    obj = bpy.context.active_object 
    #检测空物体是否已经存在，如果存在则删除
    if not Radial_symmetry_tool.is_muti_arr:
        for child in obj.children:
            if child.name =="axially_object":
                bpy.data.objects.remove(child)
    #创建空物体
    axially_object = bpy.data.objects.new("axially_object", None)
    bpy.context.view_layer.active_layer_collection.collection.objects.link(axially_object)
    #径向角度
    angel= math.pi * 2 / def_number
    #设置父级
    axially_object.parent = obj 
    #隐藏生成的物体
    axially_object.hide_render = True
    axially_object.hide_viewport = True
    #设置对称中心
    if Radial_symmetry_tool.s_location == 'OP3': #3D游标
        cursor = bpy.context.scene.cursor
        if global_S_location[0]:
           axially_object.location =(
            0
           , (obj.location[1]-cursor.location[1] )* math.math.cos(-1*angel) + (obj.location[2]-cursor.location[2]) * math.math.sin(-1*angel) -obj.location[1]+cursor.location[1]
           ,(obj.location[2]-cursor.location[2] )* math.math.cos(-1*angel) - (obj.location[1]-cursor.location[1]) * math.math.sin(-1*angel) -obj.location[2]+cursor.location[2]
           )   
        elif global_S_location[1]:
           axially_object.location =(
            (obj.location[0]-cursor.location[0] )* math.math.cos(angel) + (obj.location[2]-cursor.location[2] )* math.math.sin(angel) -obj.location[0]+cursor.location[0]
           ,0
           ,(obj.location[2]-cursor.location[2] )* math.math.cos(angel) - (obj.location[0]-cursor.location[0] )* math.math.sin(angel) -obj.location[2]+cursor.location[2]
           )
        elif global_S_location[2]:
           axially_object.location =(
            (obj.location[0]-cursor.location[0] )* math.math.cos(-1*angel) + (obj.location[1]-cursor.location[1] ) * math.math.sin(-1*angel) -obj.location[0]+cursor.location[0]
           ,(obj.location[1]-cursor.location[1] ) * math.math.cos(-1*angel) - (obj.location[0]-cursor.location[0]) * math.math.sin(-1*angel) -obj.location[1]+cursor.location[1]
           ,0
           )
    elif Radial_symmetry_tool.s_location == 'OP1' :
        axially_object.location = (0,0,0)
    
    elif Radial_symmetry_tool.s_location == 'OP2': #世界原点
        #坐标转换
        if global_S_location[0]:
           axially_object.location =(
            0
           ,obj.location[1] * math.math.cos(-1*angel) + obj.location[2] * math.math.sin(-1*angel) -obj.location[1]
           ,obj.location[2] * math.math.cos(-1*angel) - obj.location[1] * math.math.sin(-1*angel) -obj.location[2]
           )   
        elif global_S_location[1]:
           axially_object.location =(
            obj.location[0] * math.math.cos(angel) + obj.location[2] * math.math.sin(angel) -obj.location[0]
           ,0
           ,obj.location[2] * math.math.cos(angel) - obj.location[0] * math.math.sin(angel) -obj.location[2]
           )
        elif global_S_location[2]:
           axially_object.location =(
            obj.location[0] * math.math.cos(-1*angel) + obj.location[1] * math.math.sin(-1*angel) -obj.location[0]
           ,obj.location[1] * math.math.cos(-1*angel) - obj.location[0] * math.math.sin(-1*angel) -obj.location[1]
           ,0
           )    

    #设置空物体偏转角度
    if global_S_location[0]:
        axially_object.rotation_euler[0] = angel
    elif global_S_location[1]:
        axially_object.rotation_euler[1] = angel
    elif global_S_location[2]:
        axially_object.rotation_euler[2] = angel
    
    #检测同名修改器是否存在如果存在则删除
    if not Radial_symmetry_tool.is_muti_arr:
        modifier_name = "轴对称"
        if modifier_name in [m.name for m in obj.modifiers]:
            obj.modifiers.remove(obj.modifiers[modifier_name])
    #创建修改器
    mod = obj.modifiers.new("轴对称", "ARRAY")
    #设置修改器的“数量”参数
    mod.count = def_number
    #设置是否使用合并顶点
    mod.use_merge_vertices = Radial_symmetry_tool.is_merge_vert
    mod.use_merge_vertices_cap = Radial_symmetry_tool.is_merge_vert
    #设置阈值
    if Radial_symmetry_tool.is_merge_vert :
        mod.merge_threshold = Radial_symmetry_tool.merge_threshold
    #取消默认的相对偏移
    mod.use_relative_offset = False
    #设置物体偏移
    mod.use_object_offset = True
    #设置“物体偏移”对象
    mod.offset_object = axially_object

#选择游标坐标系时的主功能函数
def cursor_creat_mod(def_number,Radial_symmetry_tool):
    
    #获取游标
    cursor = bpy.context.scene.cursor
    #获取选中物体 obj
    obj = bpy.context.active_object 
    #检测空物体是否已经存在，如果存在则删除
    if not Radial_symmetry_tool.is_muti_arr:
        for child in obj.children:
            if child.name =="axially_object":
                bpy.data.objects.remove(child)
    #创建空物体
    axially_object = bpy.data.objects.new("axially_object", None)
    bpy.context.view_layer.active_layer_collection.collection.objects.link(axially_object)
    axially_object.rotation_euler = cursor.rotation_euler
    #径向角度
    angel= math.pi * 2 / def_number
    #设置父级
    axially_object.parent = obj 
    #隐藏生成的物体
    #axially_object.hide_render = True
    #axially_object.hide_viewport = True
    # #转换全局坐标到局部
    # obj_local_location=transform_point(obj.location,cursor.location,cursor.rotation_euler)
    
    # #设置偏移位置
    # if global_S_location[0]: 
    #        axially_object.location =(
    #         0
    #        ,obj_local_location[1] * math.cos(-1*angel) + obj_local_location[2] * math.sin(-1*angel) -obj_local_location[1]
    #        ,obj_local_location[2] * math.cos(-1*angel) - obj_local_location[1] * math.sin(-1*angel) -obj_local_location[2]
    #        )   
    # elif global_S_location[1]:
    #        axially_object.location =(
    #         obj_local_location[0] * math.cos(angel) + obj_local_location[2] * math.sin(angel) -obj_local_location[0]
    #        ,0
    #        ,obj_local_location[2] * math.cos(angel) - obj_local_location[0] * math.sin(angel) -obj_local_location[2]
    #        )
    # elif global_S_location[2]:
    #        axially_object.location =(
    #         obj_local_location[0] * math.cos(-1*angel) + obj_local_location[1] * math.sin(-1*angel) -obj_local_location[0]
    #        ,obj_local_location[1] * math.cos(-1*angel) - obj_local_location[0] * math.sin(-1*angel) -obj_local_location[1]
    #        ,0
    #        )    
    
    # #转化局部坐标到全局
    # axially_object.location = inv_transform_point(axially_object.location,cursor.location,cursor.rotation_euler)


    #设置空物体偏转角度
    if global_S_location[0]:
        axially_object.rotation_euler = old_rotation(cursor.rotation_euler,(angel,0,0))
    elif global_S_location[1]:
        axially_object.rotation_euler = old_rotation(cursor.rotation_euler,(0,angel,0))
    elif global_S_location[2]:
        axially_object.rotation_euler = old_rotation(cursor.rotation_euler,(0,0,angel))
    
    
    
    #检测同名修改器是否存在如果存在则删除
    if not Radial_symmetry_tool.is_muti_arr:
        modifier_name = "轴对称"
        if modifier_name in [m.name for m in obj.modifiers]:
            obj.modifiers.remove(obj.modifiers[modifier_name])
    #创建修改器
    mod = obj.modifiers.new("轴对称", "ARRAY")
    #设置修改器的“数量”参数
    mod.count = def_number
    #设置是否使用合并顶点
    mod.use_merge_vertices = Radial_symmetry_tool.is_merge_vert
    mod.use_merge_vertices_cap = Radial_symmetry_tool.is_merge_vert
    #设置阈值
    if Radial_symmetry_tool.is_merge_vert :
        mod.merge_threshold = Radial_symmetry_tool.merge_threshold
    #取消默认的相对偏移
    mod.use_relative_offset = False
    #设置物体偏移
    mod.use_object_offset = True
    #设置“物体偏移”对象
    mod.offset_object = axially_object






#ui界面
class MyProperties(bpy.types.PropertyGroup):
    #选择坐标系
    s_coordinate : bpy.props.EnumProperty(
        name= "坐标系",
        description= "对称轴使用的坐标系",
        items= [('OP1', "全局", ""),
                ('OP2', "游标(对称中心：游标)", "")
        ]
    )
    #选择对称原点
    s_location : bpy.props.EnumProperty(
        name= "对称点",
        description= "对称轴使用的原点",
        items= [('OP1', "物体", ""),
                ('OP2', "世界", ""), 
                ('OP3', "游标", "")
        ]
    )
    #是否允许多次轴对称
    is_muti_arr:bpy.props.BoolProperty(name="多次径向对称",default=False)
    #储存数量参数
    my_int: bpy.props.IntProperty(name="数量",soft_min= 0, soft_max= 1000, default=4)
    #是否使用合并顶点
    is_merge_vert: bpy.props.BoolProperty(name="合并顶点",default=False)
    #合并顶点阈值
    merge_threshold:bpy.props.FloatProperty(name="合并阈值",soft_min= 0, default=0.01,step=0.001)






#面板类
class Radial_symmetry_tool_main_panel(bpy.types.Panel):
    bl_label = "一键径向对称"
    bl_idname = "Radial_symmetry_tool_PT_ID"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "对称"
    def draw(self, context):
        layout =  self.layout
        scene = context.scene
        Radial_symmetry_tool = scene.Radial_symmetry_tool
        layout.prop(Radial_symmetry_tool,"my_int") 
        layout.prop(Radial_symmetry_tool,"s_coordinate")
        if Radial_symmetry_tool.s_coordinate == "OP1":
            layout.prop(Radial_symmetry_tool,"s_location")
        layout.prop(Radial_symmetry_tool,"is_muti_arr")
        layout.prop(Radial_symmetry_tool,"is_merge_vert")
        if Radial_symmetry_tool.is_merge_vert:
            layout.prop(Radial_symmetry_tool,"merge_threshold")
        row = layout.row(align = True,heading='对称轴')
        row.operator("axia.myop_operator_x",text='X',depress=global_S_location[0]) 
        row.operator("axia.myop_operator_y",text='Y',depress=global_S_location[1])
        row.operator("axia.myop_operator_z",text='Z',depress=global_S_location[2]) 
        layout.operator("radial_symmetry_tool.myop_operator")



#主操作类        
class Radial_symmetry_tool_op(bpy.types.Operator):
    bl_label = "一键径向对称"
    bl_idname = "radial_symmetry_tool.myop_operator"
    def execute(self, context):
        scene = context.scene
        Radial_symmetry_tool = scene.Radial_symmetry_tool
        if Radial_symmetry_tool.s_coordinate == 'OP1':     #选择全局的情况
            creat_mod(Radial_symmetry_tool.my_int,Radial_symmetry_tool)
        if Radial_symmetry_tool.s_coordinate == 'OP2':     #选择局部坐标系的情况
            cursor_creat_mod(Radial_symmetry_tool.my_int,Radial_symmetry_tool)
        return {'FINISHED'}


#判断选择的哪个轴
class adial_symmetry_tool_axis_X_OT_my_op(bpy.types.Operator):
    bl_label = "一键径向对称"
    bl_idname = "axia.myop_operator_x"
    def execute(self, context):
       scene = context.scene
       global_S_location[0] = True
       global_S_location[1] = False
       global_S_location[2] = False
       return {'FINISHED'}
class adial_symmetry_tool_axis_Y_OT_my_op(bpy.types.Operator):
    bl_label = "一键径向对称"
    bl_idname = "axia.myop_operator_y"
    def execute(self, context):
       scene = context.scene
       global_S_location[0] = False
       global_S_location[1] = True
       global_S_location[2] = False
       return {'FINISHED'}       
class adial_symmetry_tool_axis_Z_OT_my_op(bpy.types.Operator):
    bl_label = "一键径向对称"
    bl_idname = "axia.myop_operator_z"
    def execute(self, context):
       scene = context.scene
       global_S_location[0] = False
       global_S_location[1] = False
       global_S_location[2] = True
       return {'FINISHED'}



#类集合       
classes = [
MyProperties,
Radial_symmetry_tool_op,
Radial_symmetry_tool_main_panel,
adial_symmetry_tool_axis_X_OT_my_op,
adial_symmetry_tool_axis_Y_OT_my_op,
adial_symmetry_tool_axis_Z_OT_my_op
]




#注册类到blender
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.Radial_symmetry_tool = bpy.props.PointerProperty(type= MyProperties)
#取消插件时卸载类
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
if __name__ == "__main__":
    register()
