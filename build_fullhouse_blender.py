"""
=============================================================================
FULLHOUSE 3D ARCHITECTURAL MASTER MODEL FOR BLENDER (BẢN NÂNG CẤP CAO CẤP)
Dự án: Nhà phố 2 tầng hiện đại, phong cách Nhiệt đới Tối giản (Japandi Tropical)
Đặc điểm nâng cấp:
- Cảnh quan cây xanh tươi tốt: Cây bóng mát sân trước, cây ăn quả vườn sau, luống rau gỗ
- Đàn Piano upright cao cấp có bàn phím và pedal vàng đồng
- Gian thờ Phật Quan Âm trang nghiêm với vách lam gỗ CNC
- Đảo bếp đá trắng làm bánh, bàn ăn gỗ ấm cúng
- Hệ thống đèn nội thất ấm áp (Warm 3000K) + Ánh nắng mặt trời rọi qua lam gỗ
=============================================================================
HƯỚNG DẪN CHẠY:
1. Mở Blender (3.x hoặc 4.x).
2. Vào thẻ 'Scripting' -> Bấm 'Open' chọn file này.
3. Bấm nút Play ▶️ 'Run Script' (hoặc Alt+P).
4. Nhấn phím 'Z' -> chọn 'Material Preview' hoặc 'Rendered' để chiêm ngưỡng!
=============================================================================
"""

import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

clear_scene()

def get_or_create_col(name, parent=None):
    if name in bpy.data.collections:
        col = bpy.data.collections[name]
    else:
        col = bpy.data.collections.new(name)
        if parent is None:
            bpy.context.scene.collection.children.link(col)
        else:
            parent.children.link(col)
    return col

col_main = get_or_create_col("Fullhouse_Master_Project")
col_site = get_or_create_col("01_Site_Landscape_Trees", col_main)
col_fl1_arch = get_or_create_col("02_Floor1_Architecture", col_main)
col_fl1_furn = get_or_create_col("03_Floor1_Interior_Furniture", col_main)
col_fl2_arch = get_or_create_col("04_Floor2_Architecture", col_main)
col_fl2_furn = get_or_create_col("05_Floor2_Interior_Master", col_main)
col_roof = get_or_create_col("06_Roof_Solar_Technical", col_main)
col_lights = get_or_create_col("07_Lighting_Cameras", col_main)

materials = {}

def create_mat(name, color_rgba, roughness=0.5, metallic=0.0, transmission=0.0, emission_rgba=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = color_rgba
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = transmission
        elif "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = transmission
        if emission_rgba and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_rgba
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = 1.0

    if transmission > 0.1:
        mat.blend_method = 'BLEND'
    materials[name] = mat
    return mat

create_mat("Mat_WallWarmWhite", (0.96, 0.95, 0.93, 1.0), roughness=0.8)
create_mat("Mat_WallFacadeWarm", (0.85, 0.82, 0.78, 1.0), roughness=0.6)
create_mat("Mat_DarkGreyStone", (0.22, 0.24, 0.27, 1.0), roughness=0.3, metallic=0.1)
create_mat("Mat_FloorTileCream", (0.94, 0.92, 0.88, 1.0), roughness=0.25)
create_mat("Mat_AntiSlipPavers", (0.62, 0.60, 0.58, 1.0), roughness=0.85)
create_mat("Mat_GrassGreen", (0.18, 0.55, 0.22, 1.0), roughness=0.9)
create_mat("Mat_FoliageGreen", (0.15, 0.65, 0.20, 1.0), roughness=0.6)
create_mat("Mat_FoliageDark", (0.08, 0.45, 0.14, 1.0), roughness=0.7)
create_mat("Mat_TreeTrunk", (0.36, 0.25, 0.18, 1.0), roughness=0.85)
create_mat("Mat_FlowerPink", (0.92, 0.25, 0.45, 1.0), roughness=0.5)
create_mat("Mat_WhiteMarble", (0.96, 0.97, 0.98, 1.0), roughness=0.15)
create_mat("Mat_WoodOakTable", (0.70, 0.50, 0.32, 1.0), roughness=0.35)
create_mat("Mat_WoodOakCabinet", (0.74, 0.54, 0.36, 1.0), roughness=0.35)
create_mat("Mat_WoodOakDark", (0.35, 0.22, 0.14, 1.0), roughness=0.4)
create_mat("Mat_WoodLouverFacade", (0.68, 0.48, 0.30, 1.0), roughness=0.4)
create_mat("Mat_WoodStairTreads", (0.65, 0.45, 0.28, 1.0), roughness=0.35)
create_mat("Mat_BuddhaGold", (0.95, 0.78, 0.18, 1.0), roughness=0.2, metallic=0.9)
create_mat("Mat_FabricSofaWarm", (0.78, 0.76, 0.72, 1.0), roughness=0.85)
create_mat("Mat_BeddingComfort", (0.94, 0.94, 0.94, 1.0), roughness=0.8)
create_mat("Mat_GlassClear", (0.85, 0.92, 0.96, 0.35), roughness=0.05, transmission=0.85)
create_mat("Mat_BalconyGlassBronze", (0.60, 0.70, 0.75, 0.5), roughness=0.1, transmission=0.75)
create_mat("Mat_PianoBlackGloss", (0.02, 0.02, 0.02, 1.0), roughness=0.05, metallic=0.2)
create_mat("Mat_TVScreenBlack", (0.05, 0.05, 0.05, 1.0), roughness=0.1, metallic=0.5)
create_mat("Mat_YogaMatPastel", (0.75, 0.60, 0.88, 1.0), roughness=0.8)
create_mat("Mat_MetalStainless", (0.86, 0.87, 0.88, 1.0), roughness=0.2, metallic=0.9)
create_mat("Mat_BronzeGateMetal", (0.30, 0.24, 0.18, 1.0), roughness=0.3, metallic=0.8)
create_mat("Mat_SolarPVPanels", (0.12, 0.18, 0.30, 1.0), roughness=0.2, metallic=0.7)
create_mat("Mat_CarBlue", (0.15, 0.38, 0.85, 1.0), roughness=0.2, metallic=0.85)
create_mat("Mat_AntiSlipWoodTile", (0.72, 0.56, 0.40, 1.0), roughness=0.4)
create_mat("Mat_AntiSlipTileGrey", (0.42, 0.44, 0.46, 1.0), roughness=0.7)
create_mat("Mat_AntiSlipOutdoorTile", (0.56, 0.54, 0.52, 1.0), roughness=0.8)
create_mat("Mat_PlanterWood", (0.48, 0.32, 0.20, 1.0), roughness=0.5)

def add_box(collection, name, min_x, min_y, min_z, max_x, max_y, max_z, mat_name=None):
    dx = max_x - min_x
    dy = max_y - min_y
    dz = max_z - min_z
    cx = min_x + dx / 2.0
    cy = min_y + dy / 2.0
    cz = min_z + dz / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (dx, dy, dz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for col in obj.users_collection:
        col.objects.unlink(obj)
    collection.objects.link(obj)
    if mat_name and mat_name in materials:
        obj.data.materials.append(materials[mat_name])
    return obj

def add_blender_tree(collection, name, x, y, z, scale=1.0):
    # Trunk
    add_box(collection, f"{name}_Trunk", x - 0.15*scale, y - 0.15*scale, z, x + 0.15*scale, y + 0.15*scale, z + 2.4*scale, "Mat_TreeTrunk")
    # Foliage clusters (icosphere in Blender)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.1*scale, location=(x, y, z + 2.8*scale))
    leaves1 = bpy.context.active_object
    leaves1.name = f"{name}_Foliage1"
    for col in leaves1.users_collection: col.objects.unlink(leaves1)
    collection.objects.link(leaves1)
    leaves1.data.materials.append(materials["Mat_FoliageGreen"])

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.9*scale, location=(x + 0.5*scale, y + 0.3*scale, z + 3.2*scale))
    leaves2 = bpy.context.active_object
    leaves2.name = f"{name}_Foliage2"
    for col in leaves2.users_collection: col.objects.unlink(leaves2)
    collection.objects.link(leaves2)
    leaves2.data.materials.append(materials["Mat_FoliageDark"])

# 1. SITE & GREENERY
add_box(col_site, "Site_FrontRoad", -4.0, -12.0, -0.4, 12.0, -6.0, -0.25, "Mat_DarkGreyStone")
add_box(col_site, "Site_Sidewalk", -2.0, -6.0, -0.25, 10.0, -5.0, 0.0, "Mat_WallWarmWhite")
add_box(col_site, "Site_FrontYard", 0.0, -5.0, 0.0, 7.0, 0.0, 0.1, "Mat_AntiSlipPavers")
add_box(col_site, "Site_FrontLawn", 0.3, -4.7, 0.11, 2.5, -0.3, 0.13, "Mat_GrassGreen")
add_box(col_site, "Site_SideCorridor", 5.0, 0.0, 0.0, 7.0, 18.0, 0.1, "Mat_AntiSlipPavers")
add_box(col_site, "Site_SideLawn", 6.4, 0.2, 0.11, 6.9, 17.8, 0.13, "Mat_GrassGreen")
add_box(col_site, "Site_RearPatio", 0.0, 18.0, 0.0, 7.0, 20.0, 0.1, "Mat_AntiSlipPavers")
add_box(col_site, "Site_RearVegGarden", 0.0, 20.0, 0.0, 7.0, 22.8, 0.1, "Mat_GrassGreen")

# Raised Veggie planter boxes
for r in range(3):
    vy = 20.3 + (r * 0.8)
    add_box(col_site, f"Site_VegBox_{r}", 0.5, vy, 0.1, 4.5, vy + 0.55, 0.35, "Mat_PlanterWood")
    add_box(col_site, f"Site_VegGreen_{r}", 0.6, vy + 0.05, 0.35, 4.4, vy + 0.5, 0.45, "Mat_FoliageGreen")

# Trees in Landscape
add_blender_tree(col_site, "Tree_Front_Shade", 0.8, -4.0, 0.1, 1.35)
add_blender_tree(col_site, "Tree_Rear_Fruit1", 6.2, 19.5, 0.1, 1.2)
add_blender_tree(col_site, "Tree_Rear_Fruit2", 6.2, 21.8, 0.1, 1.1)

# Fences & Gates
add_box(col_site, "Fence_Left", -0.15, -5.0, 0.0, 0.0, 22.8, 2.3, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Right", 7.0, -5.0, 0.0, 7.15, 22.8, 2.3, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Rear", -0.15, 22.8, 0.0, 7.15, 22.95, 2.4, "Mat_WallWarmWhite")
add_box(col_site, "Gate_Main", 0.4, -5.0, 0.0, 4.6, -4.95, 2.3, "Mat_BronzeGateMetal")
add_box(col_site, "Gate_Side", 5.0, -5.0, 0.0, 6.8, -4.95, 2.3, "Mat_BronzeGateMetal")

# Hiên Trà Ngoài Trời Của Ba
add_box(col_site, "Porch_Canopy", 0.2, -4.6, 2.7, 3.2, -0.3, 2.85, "Mat_WoodLouverFacade")
add_box(col_site, "Porch_Table", 1.0, -3.2, 0.1, 2.2, -2.0, 0.75, "Mat_WhiteMarble")
add_box(col_site, "Porch_Stool1", 0.5, -2.8, 0.1, 0.8, -2.4, 0.45, "Mat_WoodOakTable")
add_box(col_site, "Porch_Stool2", 2.4, -2.8, 0.1, 2.7, -2.4, 0.45, "Mat_WoodOakTable")
add_box(col_site, "Porch_Stool3", 1.4, -3.7, 0.1, 1.8, -3.4, 0.45, "Mat_WoodOakTable")
add_box(col_site, "Porch_Stool4", 1.4, -1.8, 0.1, 1.8, -1.5, 0.45, "Mat_WoodOakTable")

# 2. FLOOR 1 ARCHITECTURE & INTERIOR
add_box(col_fl1_arch, "Floor1_Slab", 0.0, 0.0, 0.1, 5.0, 18.0, 0.25, "Mat_FloorTileCream")
add_box(col_fl1_arch, "Floor1_LeftWall", 0.0, 0.0, 0.25, 0.22, 18.0, 3.6, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Floor1_RightWall", 4.78, 0.0, 0.25, 5.0, 18.0, 3.6, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Floor1_FrontDoor", 0.8, 0.05, 0.25, 4.2, 0.15, 2.7, "Mat_GlassClear")
add_box(col_fl1_arch, "Floor1_FrontWall_Top", 0.8, 0.0, 2.7, 4.2, 0.22, 3.6, "Mat_WallFacadeWarm")
add_box(col_fl1_arch, "Floor1_RearWall", 0.0, 17.78, 0.25, 5.0, 18.0, 3.6, "Mat_WallWarmWhite")

# Altar & CNC Screen
add_box(col_fl1_furn, "Altar_CNC_Screen", 3.2, 0.25, 0.25, 3.3, 2.8, 3.0, "Mat_WoodLouverFacade")
add_box(col_fl1_furn, "Altar_Table", 3.4, 0.35, 0.25, 4.6, 1.2, 1.25, "Mat_WoodOakDark")
add_box(col_fl1_furn, "Altar_BuddhaStatue", 3.8, 0.6, 1.25, 4.2, 0.9, 1.85, "Mat_BuddhaGold")

# Living Room
add_box(col_fl1_furn, "Living_Sofa_Main", 0.5, 1.8, 0.25, 2.4, 2.6, 0.5, "Mat_FabricSofaWarm")
add_box(col_fl1_furn, "Living_Sofa_Chaise", 0.5, 2.6, 0.25, 1.3, 3.4, 0.5, "Mat_FabricSofaWarm")
add_box(col_fl1_furn, "Living_CoffeeTable", 1.4, 2.8, 0.25, 2.1, 3.5, 0.45, "Mat_WhiteMarble")
add_box(col_fl1_furn, "Living_TV_Wall", 4.6, 2.6, 0.25, 4.75, 4.7, 3.0, "Mat_WoodLouverFacade")
add_box(col_fl1_furn, "Living_TV_Screen", 4.5, 3.0, 1.0, 4.6, 4.3, 1.8, "Mat_TVScreenBlack")

# Parents Bedroom
add_box(col_fl1_furn, "Parents_Bed", 0.8, 8.2, 0.25, 2.6, 10.2, 0.55, "Mat_BeddingComfort")
add_box(col_fl1_furn, "Parents_Wardrobe", 0.3, 10.4, 0.25, 1.8, 11.3, 2.5, "Mat_WoodOakCabinet")

# Open Kitchen & Pastry Island
add_box(col_fl1_furn, "Kitchen_BakingIsland", 1.8, 14.8, 0.25, 3.8, 15.6, 0.88, "Mat_WoodOakCabinet")
add_box(col_fl1_furn, "Kitchen_Island_Marble", 1.75, 14.75, 0.88, 3.85, 15.65, 0.92, "Mat_WhiteMarble")
add_box(col_fl1_furn, "Kitchen_MainCounter", 0.3, 15.8, 0.25, 1.1, 17.6, 0.88, "Mat_WhiteMarble")
add_box(col_fl1_furn, "Kitchen_DiningTable", 1.8, 16.0, 0.25, 3.6, 16.8, 0.76, "Mat_WoodOakTable")

# 3. FLOOR 2 ARCHITECTURE & MASTER SUITE
add_box(col_fl2_arch, "Floor2_Slab", 0.0, -1.8, 3.6, 5.0, 18.0, 3.8, "Mat_AntiSlipWoodTile")
add_box(col_fl2_arch, "Floor2_Balcony_Rail", 0.0, -1.8, 3.82, 5.0, -1.75, 4.95, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "Floor2_Balcony_Sunbed", 0.3, -1.6, 3.82, 1.5, -0.6, 0.45, "Mat_WoodOakTable")

# Master Room: Piano, Yoga, King Bed
add_box(col_fl2_furn, "Master_Piano_Case", 0.3, 4.0, 3.82, 0.8, 5.1, 5.05, "Mat_PianoBlackGloss")
add_box(col_fl2_furn, "Master_Piano_Keys", 0.8, 4.15, 4.45, 1.1, 4.95, 4.58, "Mat_WallWarmWhite")
add_box(col_fl2_furn, "Master_Piano_Bench", 0.9, 4.4, 3.82, 1.25, 4.75, 4.3, "Mat_PianoBlackGloss")
add_box(col_fl2_furn, "Master_YogaMat", 3.0, 0.6, 3.82, 4.5, 1.8, 3.85, "Mat_YogaMatPastel")
add_box(col_fl2_furn, "Master_KingBed", 0.6, 1.5, 3.82, 2.6, 3.5, 4.4, "Mat_BeddingComfort")

# 4. ROOF & SOLAR
add_box(col_roof, "Roof_Slab", 0.0, -1.8, 7.2, 5.0, 18.0, 7.35, "Mat_WallWarmWhite")
add_box(col_roof, "Roof_WaterTank", 0.5, 12.0, 7.35, 1.8, 13.8, 8.6, "Mat_MetalStainless")
add_box(col_roof, "Roof_SolarHeater", 2.2, 12.0, 7.35, 4.5, 13.8, 8.2, "Mat_MetalStainless")
for sp in range(4):
    spy = 14.3 + (sp * 0.85)
    add_box(col_roof, f"Roof_PV_{sp}", 0.6, spy, 7.45, 4.4, spy + 0.75, 7.6, "Mat_SolarPVPanels")

# Sunshade Louvers
for l in range(8):
    lz = 4.0 + (l * 0.38)
    add_box(col_roof, f"Facade_Louver_{l}", 0.6, -0.3, lz, 4.4, -0.15, lz + 0.08, "Mat_WoodLouverFacade")

# 5. LIGHTING & CAMERAS & WORLD
# World Sky
world = bpy.context.scene.world
if not world:
    world = bpy.data.worlds.new("Fullhouse_World")
    bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.75, 0.85, 0.95, 1.0)
    bg_node.inputs["Strength"].default_value = 1.0

# Sun Light
bpy.ops.object.light_add(type='SUN', location=(20, -18, 25))
sun = bpy.context.active_object
sun.name = "Sun_Warm"
sun.data.energy = 4.5
sun.data.color = (1.0, 0.96, 0.88)
sun.rotation_euler = (math.radians(50), math.radians(15), math.radians(-40))
for col in sun.users_collection: col.objects.unlink(sun)
col_lights.objects.link(sun)

# Interior Warm Lights
def add_point_light(name, location, energy=80.0, color=(1.0, 0.75, 0.45)):
    bpy.ops.object.light_add(type='POINT', location=location)
    p = bpy.context.active_object
    p.name = name
    p.data.energy = energy
    p.data.color = color
    p.data.shadow_soft_size = 0.5
    for col in p.users_collection: col.objects.unlink(p)
    col_lights.objects.link(p)

add_point_light("Light_LivingRoom", (2.5, 3.0, 2.5), 100.0)
add_point_light("Light_Altar", (3.8, 0.8, 2.0), 40.0, (1.0, 0.8, 0.3))
add_point_light("Light_Kitchen", (2.5, 16.0, 2.5), 80.0)
add_point_light("Light_MasterBed", (2.5, 3.0, 5.5), 100.0)

# Main Camera
bpy.ops.object.camera_add(location=(-16.0, -20.0, 16.0))
cam = bpy.context.active_object
cam.name = "Cam_Beauty_Master"
cam.rotation_euler = (math.radians(58), 0, math.radians(-38))
cam.data.lens = 45
for col in cam.users_collection: col.objects.unlink(cam)
col_lights.objects.link(cam)
bpy.context.scene.camera = cam

# Save native .blend file
import os
save_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else r"C:\Users\Conghau\Desktop\My Home"
blend_path = os.path.join(save_dir, "Fullhouse_Model.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

print("="*60)
print(f"SUCCESS: Saved native Blender file to: {blend_path}")
print("You can now DOUBLE CLICK 'Fullhouse_Model.blend' directly!")
print("="*60)
