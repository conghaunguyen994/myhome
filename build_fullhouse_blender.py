"""
=============================================================================
FULLHOUSE 3D ARCHITECTURAL & SMART HOME MODEL FOR BLENDER (NEW LAYOUT)
Mặt bằng kiến trúc cập nhật theo phác thảo mới:
1. Sân trước dài 18m có MÁI CHE KÍN TOÀN BỘ 18M.
2. BÀN TRÀ CỦA BA KÊ ÁP SÁT VÁCH TƯỜNG TRÁI. Xe ô tô đỗ bên trái, bonsai bên phải.
3. TẦNG 1:
   - Phòng khách: TV và Bàn thờ dựa tường trái, sofa đối diện, cửa chính bên phải.
   - Phòng Ba Mẹ (4x3.2m): Ngay sau phòng khách, hành lang 1m bên phải đi thông.
   - Cầu thang chữ U: Chiếm 4m, hành lang 1m bên phải thông xuống bếp, tủ điện MDB gầm thang.
   - Bếp mở & Bàn ăn: Bếp dọc tường trái, bàn ăn tròn ở giữa, cửa sổ ra luồng 2m và cửa sau.
   - Sân sau: Dãy phụ trợ dựa tường trái (WC -> Phòng tắm -> Giặt đồ -> Phơi đồ),
     bên phải là bàn tròn ngồi chill và khu để xe máy, cuối sân là vườn rau xanh.
4. TẦNG 2:
   - Ban công trước (5x1.6m) ngắm sao, đón nắng sớm.
   - Phòng Master (Chị Ba) ĐƯỢC ĐƯA RA PHÍA TRƯỚC: Có đàn Piano Upright, góc Yoga/thiền,
     giường ngủ, bàn đọc, và khối WC riêng + Phòng thay đồ phía sau.
   - Cầu thang chữ U & Giếng trời thông tầng trung tâm.
   - Phòng Sếu (Em Út) ở giữa sau cầu thang (4x3.2m).
   - Phòng Chị Hai ở phía sau (4x3.2m) mở cửa ra ban công sau.
   - Ban công sau siêu rộng (5x8m): Yoga ngoài trời, ngắm trăng, phơi đồ kín gió.
5. HỆ THỐNG SMART HOME, ĐIỆN, WIFI & CAMERA POE ĐỒNG BỘ TOÀN DIỆN.
=============================================================================
"""

import bpy
import bmesh
import math
import os
import random

random.seed(42)

# ---------------------------------------------------------------------------
# 1. CLEAN SCENE & INITIALIZE COLLECTIONS
# ---------------------------------------------------------------------------
def clear_scene():
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)
    for block in list(bpy.data.meshes):
        if block.users == 0: bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        if block.users == 0: bpy.data.materials.remove(block)
    for block in list(bpy.data.lights):
        if block.users == 0: bpy.data.lights.remove(block)
    for block in list(bpy.data.cameras):
        if block.users == 0: bpy.data.cameras.remove(block)

clear_scene()

def get_or_create_col(name, parent=None):
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        if parent: parent.children.link(col)
        else: bpy.context.scene.collection.children.link(col)
    return col

col_main = get_or_create_col("Fullhouse_Master_Project")
col_site = get_or_create_col("01_Site_Landscape_Trees", col_main)
col_fl1_arch = get_or_create_col("02_Floor1_Architecture", col_main)
col_fl1_furn = get_or_create_col("03_Floor1_Interior_Furniture", col_main)
col_fl2_arch = get_or_create_col("04_Floor2_Architecture", col_main)
col_fl2_furn = get_or_create_col("05_Floor2_Interior_Master", col_main)
col_roof = get_or_create_col("06_Roof_Solar_Technical", col_main)
col_lights = get_or_create_col("07_Lighting_And_Night_LEDs", col_main)
col_smarthome = get_or_create_col("09_SmartHome_WiFi_Power_Cameras", col_main)
col_callouts = get_or_create_col("10_SmartHome_3D_Callout_Labels", col_main)

# ---------------------------------------------------------------------------
# 2. PBR SHADERS & MATERIALS
# ---------------------------------------------------------------------------
def set_principled_emission(bsdf, emission_rgba, emission_strength):
    if not emission_rgba: return
    if 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = emission_rgba
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    elif 'Emission' in bsdf.inputs:
        bsdf.inputs['Emission'].default_value = emission_rgba
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = emission_strength

def create_mat(name, color_rgba, roughness=0.5, metallic=0.0, transmission=0.0, emission_rgba=None, emission_strength=1.0, alpha=1.0):
    mat = bpy.data.materials.get(name)
    if not mat: mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = color_rgba
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = transmission
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission'].default_value = transmission

    if alpha < 1.0 and 'Alpha' in bsdf.inputs:
        bsdf.inputs['Alpha'].default_value = alpha
        if hasattr(mat, 'blend_method'): mat.blend_method = 'BLEND'

    set_principled_emission(bsdf, emission_rgba, emission_strength)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

create_mat("Mat_WallWarmWhite", (0.96, 0.95, 0.93, 1.0), roughness=0.72)
create_mat("Mat_WallFacadeWarm", (0.90, 0.87, 0.82, 1.0), roughness=0.62)
create_mat("Mat_RoofCharcoal", (0.12, 0.16, 0.22, 1.0), roughness=0.50, metallic=0.15)
create_mat("Mat_DarkGreyStone", (0.20, 0.24, 0.30, 1.0), roughness=0.65)
create_mat("Mat_RoadAsphalt", (0.10, 0.12, 0.16, 1.0), roughness=0.88)
create_mat("Mat_FloorTileCream", (0.96, 0.95, 0.93, 1.0), roughness=0.18, metallic=0.08)
create_mat("Mat_AntiSlipWoodTile", (0.66, 0.45, 0.27, 1.0), roughness=0.35)
create_mat("Mat_AntiSlipPavers", (0.32, 0.36, 0.42, 1.0), roughness=0.78)
create_mat("Mat_WhiteMarble", (0.98, 0.98, 0.99, 1.0), roughness=0.10, metallic=0.1)
create_mat("Mat_WoodOakTable", (0.68, 0.47, 0.29, 1.0), roughness=0.30)
create_mat("Mat_WoodOakCabinet", (0.73, 0.53, 0.35, 1.0), roughness=0.34)
create_mat("Mat_WoodOakDark", (0.25, 0.15, 0.09, 1.0), roughness=0.35)
create_mat("Mat_WoodWalnutAltar", (0.24, 0.13, 0.08, 1.0), roughness=0.3)
create_mat("Mat_WoodLouverFacade", (0.72, 0.46, 0.24, 1.0), roughness=0.36)
create_mat("Mat_WoodStairTreads", (0.64, 0.43, 0.25, 1.0), roughness=0.32)
create_mat("Mat_FabricSofaWarm", (0.24, 0.27, 0.32, 1.0), roughness=0.82)
create_mat("Mat_FabricTaupe", (0.62, 0.57, 0.52, 1.0), roughness=0.85)
create_mat("Mat_CushionMustard", (0.88, 0.64, 0.20, 1.0), roughness=0.8)
create_mat("Mat_CushionNavy", (0.14, 0.24, 0.42, 1.0), roughness=0.8)
create_mat("Mat_BeddingCream", (0.92, 0.89, 0.84, 1.0), roughness=0.85)
create_mat("Mat_BeddingWhite", (0.97, 0.97, 0.96, 1.0), roughness=0.85)
create_mat("Mat_GlassClear", (0.88, 0.94, 0.98, 0.25), roughness=0.04, transmission=0.92, alpha=0.28)
create_mat("Mat_GlassBronze", (0.55, 0.68, 0.74, 0.45), roughness=0.08, transmission=0.78, alpha=0.42)
create_mat("Mat_CanopyGlass", (0.35, 0.45, 0.55, 0.55), roughness=0.1, transmission=0.7, alpha=0.45)
create_mat("Mat_PianoBlackGloss", (0.02, 0.02, 0.03, 1.0), roughness=0.04, metallic=0.25)
create_mat("Mat_TVScreenBlack", (0.05, 0.12, 0.28, 1.0), roughness=0.08, metallic=0.4, emission_rgba=(0.08, 0.22, 0.55, 1.0), emission_strength=1.2)
create_mat("Mat_WarmLED", (1.0, 0.88, 0.60, 1.0), roughness=0.15, emission_rgba=(1.0, 0.82, 0.45, 1.0), emission_strength=6.5)
create_mat("Mat_WarmSconce", (1.0, 0.92, 0.70, 1.0), roughness=0.20, emission_rgba=(1.0, 0.86, 0.52, 1.0), emission_strength=8.0)
create_mat("Mat_SmartCyanLED", (0.22, 0.74, 0.97, 1.0), roughness=0.15, emission_rgba=(0.22, 0.74, 0.97, 1.0), emission_strength=5.5)
create_mat("Mat_SmartGreenLED", (0.06, 0.73, 0.50, 1.0), roughness=0.15, emission_rgba=(0.06, 0.73, 0.50, 1.0), emission_strength=5.0)
create_mat("Mat_SmartRedLED", (0.94, 0.26, 0.26, 1.0), roughness=0.15, emission_rgba=(0.94, 0.26, 0.26, 1.0), emission_strength=5.0)
create_mat("Mat_CameraFOV", (0.22, 0.74, 0.97, 0.18), roughness=0.2, transmission=0.85, emission_rgba=(0.22, 0.74, 0.97, 1.0), emission_strength=0.8, alpha=0.18)
create_mat("Mat_CalloutBoard", (0.06, 0.14, 0.30, 1.0), roughness=0.25, metallic=0.2, emission_rgba=(0.08, 0.20, 0.45, 1.0), emission_strength=1.5)
create_mat("Mat_CalloutText", (1.0, 1.0, 1.0, 1.0), roughness=0.1, emission_rgba=(1.0, 1.0, 1.0, 1.0), emission_strength=4.0)
create_mat("Mat_SolarPVPanels", (0.04, 0.09, 0.22, 1.0), roughness=0.14, metallic=0.65)
create_mat("Mat_CarWhite", (0.96, 0.97, 0.98, 1.0), roughness=0.14, metallic=0.75)
create_mat("Mat_TireRubber", (0.12, 0.12, 0.13, 1.0), roughness=0.85)
create_mat("Mat_MetalMatteBlack", (0.10, 0.10, 0.11, 1.0), roughness=0.35, metallic=0.75)
create_mat("Mat_MetalStainless", (0.82, 0.83, 0.85, 1.0), roughness=0.20, metallic=0.92)
create_mat("Mat_BuddhaGold", (0.96, 0.78, 0.24, 1.0), roughness=0.18, metallic=0.92)
create_mat("Mat_CeramicWhite", (0.95, 0.96, 0.97, 1.0), roughness=0.15)
create_mat("Mat_GrassGreen", (0.16, 0.44, 0.24, 1.0), roughness=0.88)
create_mat("Mat_FoliageGreen", (0.14, 0.50, 0.22, 1.0), roughness=0.6)

# ---------------------------------------------------------------------------
# 3. PRIMITIVES GENERATOR
# ---------------------------------------------------------------------------
def link_mesh_obj(collection, name, bm, mat_name, loc=(0, 0, 0), rot=(0, 0, 0), smooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    obj = bpy.data.objects.new(name, me)
    obj.location = loc
    obj.rotation_euler = rot
    if mat_name and mat_name in bpy.data.materials:
        obj.data.materials.append(bpy.data.materials[mat_name])
    collection.objects.link(obj)
    return obj

def add_box(collection, name, min_x, min_y, min_z, max_x, max_y, max_z, mat_name=None, bevel=0.0, rot_z=0.0, rot=(0, 0, 0)):
    dx = max(max_x - min_x, 0.002)
    dy = max(max_y - min_y, 0.002)
    dz = max(max_z - min_z, 0.002)
    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0
    cz = (min_z + max_z) / 2.0

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(dx, dy, dz), verts=bm.verts)
    if bevel > 0.001 and min(dx, dy, dz) > bevel * 2.1:
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=min(bevel, min(dx, dy, dz) * 0.45), segments=2, profile=0.5, affect='EDGES')
    final_rot = rot if rot != (0, 0, 0) else (0, 0, rot_z)
    return link_mesh_obj(collection, name, bm, mat_name, loc=(cx, cy, cz), rot=final_rot)

def add_cyl(collection, name, cx, cy, z_bottom, z_top, r1, r2=None, mat_name=None, segs=20, rot=(0, 0, 0), smooth=True):
    r2 = r1 if r2 is None else r2
    dz = max(z_top - z_bottom, 0.002)
    cz = (z_bottom + z_top) / 2.0
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r1, radius2=r2, depth=dz)
    return link_mesh_obj(collection, name, bm, mat_name, loc=(cx, cy, cz), rot=rot, smooth=smooth)

# ---------------------------------------------------------------------------
# 4. SITE & SÂN TRƯỚC 18M: MÁI CHE KÍN 18M & BÀN TRÀ ÁP VÁCH TƯỜNG TRÁI
# ---------------------------------------------------------------------------
# Đường quốc lộ & vỉa hè
add_box(col_site, "Site_FrontRoad", -4.0, -24.0, -0.35, 11.0, -18.8, -0.20, "Mat_RoadAsphalt")
add_box(col_site, "Site_Sidewalk", -2.0, -18.8, -0.20, 9.0, -18.0, 0.0, "Mat_WallFacadeWarm")
add_box(col_site, "Site_ArchitecturalBasePlinth", -0.5, -18.5, -0.45, 7.5, 24.5, -0.01, "Mat_RoofCharcoal")

# Sân trước 18m (Y = -18..0, X = 0..7)
add_box(col_site, "Site_FrontYard_Slab", 0.0, -18.0, 0.0, 7.0, 0.0, 0.15, "Mat_AntiSlipPavers")

# Trụ cổng đá chẻ & Cổng sắt (Cổng xe 3.6m bên trái X=0.3..3.9, Cổng phụ 2m bên phải X=4.8..6.8)
add_box(col_site, "Gate_Pillar_L", -0.18, -18.18, 0.0, 0.35, -17.82, 2.65, "Mat_DarkGreyStone")
add_box(col_site, "Gate_Pillar_M", 3.85, -18.18, 0.0, 4.15, -17.82, 2.65, "Mat_DarkGreyStone")
add_box(col_site, "Gate_Pillar_R", 6.85, -18.18, 0.0, 7.18, -17.82, 2.65, "Mat_DarkGreyStone")
add_box(col_site, "MainCarGate_3m6", 0.35, -18.0, 0.18, 3.85, -17.94, 2.25, "Mat_MetalMatteBlack")
add_box(col_site, "SideGate_2m", 4.15, -18.0, 0.18, 6.85, -17.94, 2.25, "Mat_MetalMatteBlack")
add_box(col_site, "Fence_Left", -0.18, -18.0, 0.0, 0.0, 24.0, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Right", 7.0, -18.0, 0.0, 7.18, 24.0, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Rear", -0.18, 24.0, 0.0, 7.18, 24.18, 2.35, "Mat_WallWarmWhite")

# 🏗️ MÁI CHE SÂN TRƯỚC PHỦ KÍN TOÀN BỘ 18M (Y = -18..0, X = 0..5.15)
for cy in [-17.8, -12.0, -6.0, -0.2]:
    for cx in [0.05, 5.05]:
        add_box(col_site, f"Canopy_Col_{cx:.1f}_{cy:.1f}", cx - 0.06, cy - 0.06, 0.15, cx + 0.06, cy + 0.06, 3.25, "Mat_MetalMatteBlack")
add_box(col_site, "Canopy_Beam_L", 0.0, -18.0, 3.25, 0.12, 0.0, 3.38, "Mat_MetalMatteBlack")
add_box(col_site, "Canopy_Beam_R", 5.0, -18.0, 3.25, 5.12, 0.0, 3.38, "Mat_MetalMatteBlack")
for p_idx, py in enumerate(range(-18, 1, 2)):
    add_box(col_site, f"Canopy_Rafter_{p_idx}", 0.0, py - 0.05, 3.28, 5.12, py + 0.05, 3.36, "Mat_MetalMatteBlack")
    add_box(col_lights, f"Canopy_LEDStrip_{p_idx}", 0.5, py - 0.02, 3.24, 4.6, py + 0.02, 3.27, "Mat_WarmLED")
add_box(col_site, "Canopy_GlassRoof_18m", 0.0, -18.0, 3.38, 5.15, 0.0, 3.42, "Mat_CanopyGlass")

# 🍵 BÀN TRÀ CỦA BA KÊ ÁP SÁT VÁCH TƯỜNG TRÁI (Y = -5.0..-2.2, X = 0.05..1.35)
add_box(col_site, "DadTea_Bench_Base", 0.05, -4.8, 0.15, 0.55, -2.4, 0.55, "Mat_WoodOakTable", bevel=0.01)
add_box(col_site, "DadTea_Bench_Back", 0.02, -4.8, 0.55, 0.12, -2.4, 1.05, "Mat_WoodLouverFacade")
add_box(col_site, "DadTea_Bench_Cushion", 0.12, -4.75, 0.55, 0.52, -2.45, 0.62, "Mat_CushionMustard", bevel=0.015)
add_box(col_site, "DadTea_Table_Top", 0.68, -4.5, 0.15, 1.25, -2.7, 0.72, "Mat_WhiteMarble", bevel=0.015)
add_box(col_site, "DadTea_Teapot", 0.90, -3.7, 0.72, 1.05, -3.5, 0.84, "Mat_CeramicWhite")
add_box(col_lights, "DadTea_WallLamp", 0.02, -3.7, 1.65, 0.10, -3.5, 1.85, "Mat_WarmSconce")

# Xe ô tô màu trắng đỗ bên trái (Y = -14.5..-10.0, X = 0.8..2.7)
add_box(col_site, "Family_SUV_Chassis", 0.9, -14.5, 0.20, 2.8, -10.2, 0.78, "Mat_CarWhite", bevel=0.08)
add_box(col_site, "Family_SUV_Cabin", 1.0, -13.3, 0.78, 2.7, -11.1, 1.48, "Mat_CarWhite", bevel=0.08)
add_box(col_site, "Family_SUV_Windshield", 1.05, -13.2, 0.80, 2.65, -12.6, 1.42, "Mat_GlassBronze")
add_box(col_lights, "Family_SUV_Headlights", 1.05, -14.52, 0.52, 2.65, -14.48, 0.64, "Mat_WarmSconce")

# Bonsai & Cây cảnh bên phải sân (X = 5.2..6.8)
for bi, by in enumerate([-16, -12, -8, -4]):
    add_box(col_site, f"Bonsai_Planter_{bi}", 5.6, by - 0.3, 0.15, 6.4, by + 0.3, 0.55, "Mat_DarkGreyStone")
    add_cyl(col_site, f"Bonsai_Tree_{bi}", 6.0, by, 0.55, 1.25, 0.45, 0.25, "Mat_FoliageGreen")
    add_box(col_lights, f"Bonsai_Uplight_{bi}", 6.0, by, 0.16, 6.08, by + 0.08, 0.22, "Mat_WarmSconce")

# Đường luồng 2m (X = 5.0..7.0, Y = 0.0..16.0)
add_box(col_site, "Corridor_2m_Slab", 5.0, 0.0, 0.0, 7.0, 16.0, 0.15, "Mat_AntiSlipPavers")

# ---------------------------------------------------------------------------
# 5. TẦNG 1: PHÒNG KHÁCH (TV/BÀN THỜ TRÁI), PHÒNG BA MẸ, THANG CHỮ U & BẾP
# ---------------------------------------------------------------------------
Z1 = 0.25
H1 = 3.60
add_box(col_fl1_arch, "Floor1_Slab", 0.0, 0.0, 0.10, 5.0, 16.0, Z1, "Mat_FloorTileCream")

# Tường bao Tầng 1
add_box(col_fl1_arch, "Fl1_Wall_Left", 0.0, 0.0, Z1, 0.22, 16.0, Z1 + 0.42, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Right", 4.78, 0.0, Z1, 5.0, 16.0, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Front", 0.0, 0.0, Z1, 5.0, 0.22, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Rear", 0.0, 15.78, Z1, 5.0, 16.0, H1, "Mat_WallWarmWhite")

# Cửa chính bên phải & Cửa sổ bên trái
add_box(col_fl1_arch, "Fl1_Front_MainDoor", 2.85, 0.05, Z1, 4.55, 0.18, 2.80, "Mat_GlassClear")
add_box(col_fl1_arch, "Fl1_Front_Window", 0.45, 0.05, 0.95, 2.25, 0.18, 2.55, "Mat_GlassClear")

# A. PHÒNG KHÁCH (5m x 5.8m: Y = 0.3..5.8)
# Vách TV & Bàn thờ dựa tường trái
add_box(col_fl1_furn, "Living_TVConsole", 0.24, 0.8, Z1 + 0.1, 0.65, 2.6, Z1 + 0.52, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl1_furn, "Living_TVLouver", 0.24, 0.8, Z1 + 0.52, 0.28, 2.6, Z1 + 2.35, "Mat_WoodLouverFacade")
add_box(col_fl1_furn, "Living_TVScreen", 0.28, 1.0, Z1 + 0.75, 0.32, 2.4, Z1 + 1.65, "Mat_TVScreenBlack")
add_box(col_lights, "Living_TV_TopLED", 0.25, 0.8, Z1 + 2.32, 0.30, 2.6, Z1 + 2.36, "Mat_WarmLED")

# Bàn thờ Quan Âm & Gia tiên
add_box(col_fl1_furn, "Altar_Table", 0.24, 3.0, Z1 + 0.1, 0.85, 4.6, Z1 + 1.05, "Mat_WoodWalnutAltar", bevel=0.015)
add_cyl(col_fl1_furn, "Altar_Buddha", 0.55, 3.85, Z1 + 1.05, Z1 + 1.65, 0.12, 0.05, "Mat_BuddhaGold")
add_cyl(col_lights, "Altar_HaloLED", 0.28, 3.85, Z1 + 1.70, Z1 + 1.72, 0.35, 0.35, "Mat_WarmLED", rot=(0, math.pi/2, 0))

# Sofa đối diện bên phải
add_box(col_fl1_furn, "Living_Sofa_Base", 2.5, 1.4, Z1 + 0.08, 4.5, 3.6, Z1 + 0.44, "Mat_FabricSofaWarm", bevel=0.02)
add_box(col_fl1_furn, "Living_Sofa_Back", 4.1, 1.4, Z1 + 0.44, 4.5, 3.6, Z1 + 0.78, "Mat_FabricSofaWarm", bevel=0.02)
add_cyl(col_fl1_furn, "Living_CoffeeTable", 3.3, 2.5, Z1 + 0.05, Z1 + 0.45, 0.45, 0.45, "Mat_WhiteMarble")

# B. PHÒNG BA MẸ (4m x 3.2m: Y = 5.8..9.0, X = 0.22..4.0)
add_box(col_fl1_arch, "Wall_Living_Parents", 0.22, 5.75, Z1, 4.0, 5.85, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Win_Parents_3Panel", 1.2, 5.76, Z1 + 1.2, 3.2, 5.84, Z1 + 2.2, "Mat_GlassClear")
add_box(col_fl1_arch, "Wall_Parents_Hall", 3.95, 5.8, Z1, 4.05, 9.0, H1, "Mat_WallWarmWhite")
add_box(col_fl1_furn, "Parents_Bed_Mattress", 0.8, 6.4, Z1, 2.8, 8.4, Z1 + 0.55, "Mat_BeddingCream", bevel=0.03)
add_box(col_fl1_furn, "Parents_Bed_Duvet", 0.8, 6.45, Z1 + 0.55, 2.4, 8.35, Z1 + 0.62, "Mat_CushionNavy", bevel=0.02)
add_box(col_fl1_furn, "Parents_Wardrobe", 0.35, 6.2, Z1, 0.65, 8.6, Z1 + 2.5, "Mat_WoodOakCabinet")

# C. CẦU THANG CHỮ U (Y = 9.0..11.2, X = 0.24..4.0)
for s in range(10):
    sy = 9.05 + s * 0.18
    sz = Z1 + (s + 1) * 0.177
    add_box(col_fl1_arch, f"Stair_Tread_{s}", 0.24, sy, sz - 0.04, 1.8, sy + 0.20, sz, "Mat_WoodStairTreads", bevel=0.006)
    add_box(col_lights, f"Stair_LED_{s}", 0.26, sy, sz - 0.045, 1.75, sy + 0.02, sz - 0.035, "Mat_WarmLED")
add_box(col_fl1_arch, "Stair_Landing", 0.24, 10.6, 1.95, 3.8, 11.2, 2.05, "Mat_WoodStairTreads")
# Tủ điện MDB & Inverter 5kW
add_box(col_smarthome, "Main_MDB_Electrical", 3.85, 9.2, Z1 + 0.9, 3.98, 9.8, Z1 + 1.85, "Mat_MetalStainless")
add_box(col_smarthome, "MDB_StatusLED", 3.98, 9.3, Z1 + 1.3, 4.0, 9.7, Z1 + 1.7, "Mat_SmartGreenLED")

# D. BẾP MỞ & BÀN ĂN (5m x 6.4m: Y = 11.2..16.0)
add_box(col_fl1_furn, "Kitchen_Counter_L", 0.24, 11.5, Z1, 0.95, 15.6, Z1 + 0.86, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl1_furn, "Kitchen_StoneTop", 0.22, 11.45, Z1 + 0.86, 0.98, 15.65, Z1 + 0.90, "Mat_WhiteMarble")
add_box(col_fl1_furn, "Kitchen_UpperCabinets", 0.24, 11.5, Z1 + 1.6, 0.65, 14.8, Z1 + 2.35, "Mat_WallFacadeWarm")
add_box(col_lights, "Kitchen_UnderCabinetLED", 0.58, 11.6, Z1 + 1.58, 0.62, 14.7, Z1 + 1.62, "Mat_WarmLED")
add_box(col_fl1_furn, "Kitchen_Fridge", 0.24, 14.85, Z1, 1.05, 15.65, Z1 + 1.95, "Mat_MetalStainless")
# Bàn ăn tròn 4-6 chỗ ở giữa
add_cyl(col_fl1_furn, "Dining_RoundTable", 2.5, 13.5, Z1 + 0.72, Z1 + 0.76, 0.75, 0.75, "Mat_WoodOakTable")
add_cyl(col_fl1_furn, "Dining_CenterLeg", 2.5, 13.5, Z1, Z1 + 0.72, 0.12, 0.16, "Mat_MetalMatteBlack")
# Cửa sau ra sân sau
add_box(col_fl1_arch, "Fl1_RearDoor", 2.6, 15.76, Z1, 4.2, 15.82, Z1 + 2.6, "Mat_GlassClear")

# ---------------------------------------------------------------------------
# 6. SÂN SAU: DÃY PHỤ TRỢ (WC/TẮM/GIẶT/PHƠI) ÁP TƯỜNG TRÁI + VƯỜN RAU
# ---------------------------------------------------------------------------
add_box(col_site, "RearYard_Slab", 0.0, 16.0, 0.0, 7.0, 24.0, 0.15, "Mat_AntiSlipPavers")
# 1. WC (2.4 x 1.6m)
add_box(col_site, "Rear_WC_Room", 0.1, 16.0, 0.15, 2.4, 17.6, 2.65, "Mat_WallWarmWhite")
# 2. Phòng Tắm (2.4 x 1.6m)
add_box(col_site, "Rear_Bath_Room", 0.1, 17.6, 0.15, 2.4, 19.2, 2.65, "Mat_WallWarmWhite")
# 3. Giặt đồ (2.4 x 1.6m)
add_box(col_site, "Rear_Laundry_Room", 0.1, 19.2, 0.15, 2.4, 20.8, 2.65, "Mat_WallWarmWhite")
add_box(col_site, "Washer_Dryer", 0.4, 19.5, 0.15, 1.1, 20.2, 1.05, "Mat_MetalStainless")
# 4. Phơi đồ có mái thoáng (2.4 x 2.2m)
add_box(col_site, "Rear_Drying_Deck", 0.1, 20.8, 0.15, 2.4, 23.0, 0.25, "Mat_WoodOakTable")

# Bên phải sân sau: Bàn tròn ngồi chill + Chỗ để xe máy
add_cyl(col_site, "Rear_Chill_Table", 3.4, 17.5, 0.80, 0.85, 0.45, 0.45, "Mat_WoodOakTable")
add_box(col_site, "Rear_Chill_Chair1", 3.1, 16.8, 0.15, 3.7, 17.1, 0.65, "Mat_CushionMustard")
add_box(col_site, "Rear_Chill_Chair2", 3.1, 17.9, 0.15, 3.7, 18.2, 0.65, "Mat_CushionMustard")
add_box(col_site, "Rear_Scooter", 3.3, 19.2, 0.15, 3.7, 20.6, 0.95, "Mat_CeramicWhite")

# Vườn rau hữu cơ 5m x 4m cuối sân
for vr in range(3):
    vry = 21.5 + vr * 0.50
    add_box(col_site, f"VegBed_{vr}", 4.8, vry, 0.15, 6.8, vry + 0.38, 0.38, "Mat_WoodOakDark")

# ---------------------------------------------------------------------------
# 7. TẦNG 2: PHÒNG MASTER (CHỊ BA) PHÍA TRƯỚC, PHÒNG SẾU & CHỊ HAI PHÍA SAU
# ---------------------------------------------------------------------------
Z2 = 3.85
H2 = 7.20
# Sàn Tầng 2 vươn ra ban công sau 8m
add_box(col_fl2_arch, "Floor2_Slab", 0.0, -1.6, Z2 - 0.15, 5.0, 24.0, Z2, "Mat_FloorTileCream")

# Tường bao Tầng 2
add_box(col_fl2_arch, "Fl2_Wall_Left", 0.0, 0.0, Z2, 0.22, 16.0, Z2 + 0.42, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Right", 4.78, 0.0, Z2, 5.0, 16.0, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Front", 0.0, 0.0, Z2, 5.0, 0.22, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Rear", 0.0, 15.78, Z2, 5.0, 16.0, H2, "Mat_WallWarmWhite")

# Ban công trước (5m x 1.6m: Y = -1.6..0.0)
add_box(col_fl2_arch, "BalconyFront_Rail", 0.0, -1.6, Z2, 5.0, -1.55, Z2 + 1.15, "Mat_BalconyGlassBronze")

# A. PHÒNG NGỦ MASTER CHỊ BA (PHÍA TRƯỚC: Y = 0.22..7.0)
add_box(col_fl2_arch, "Master_FrontGlassDoor", 0.8, 0.05, Z2, 4.2, 0.15, Z2 + 2.65, "Mat_GlassClear")
add_box(col_fl2_furn, "Master_KingBed", 0.8, 0.8, Z2, 2.8, 2.8, Z2 + 0.55, "Mat_BeddingCream", bevel=0.03)
add_box(col_fl2_furn, "Master_BedDuvet", 0.85, 0.85, Z2 + 0.55, 2.75, 2.75, Z2 + 0.63, "Mat_CushionNavy", bevel=0.02)
# Cây đàn Piano Upright đen bóng áp vách tường phải
add_box(col_fl2_furn, "Master_Piano_Body", 3.8, 1.1, Z2 + 0.04, 4.2, 2.5, Z2 + 1.20, "Mat_PianoBlackGloss", bevel=0.015)
add_box(col_fl2_furn, "Master_Piano_Keys", 3.55, 1.2, Z2 + 0.70, 3.8, 2.4, Z2 + 0.76, "Mat_CeramicWhite")
# Góc Yoga & Thiền
add_box(col_fl2_furn, "Master_YogaMat", 2.4, 2.8, Z2, 3.4, 4.2, Z2 + 0.02, "Mat_CushionMustard")
# Khối WC Riêng & Phòng Thay Đồ phía sau giường
add_box(col_fl2_arch, "Master_Ensuite_Wall", 0.22, 4.15, Z2, 4.0, 4.25, H2, "Mat_WallWarmWhite")
add_box(col_fl2_furn, "Master_Bathroom_Fixtures", 0.35, 4.5, Z2, 2.0, 6.8, Z2 + 0.85, "Mat_WhiteMarble")
add_box(col_fl2_furn, "Master_WalkinCloset", 2.4, 4.4, Z2, 3.8, 6.8, Z2 + 2.5, "Mat_WoodOakCabinet")

# B. GIẾNG TRỜI THÔNG TẦNG TRUNG TÂM (Y = 7.0..10.0)
add_box(col_fl2_arch, "Fl2_SkylightOpening", 1.4, 7.2, Z2, 3.2, 9.8, Z2 + 0.05, "Mat_GlassClear")

# C. PHÒNG SẾU (EM ÚT: Y = 10.0..13.0, X = 0.22..4.0)
add_box(col_fl2_arch, "Wall_Fl2_Seu", 0.22, 9.95, Z2, 4.0, 10.05, H2, "Mat_WallWarmWhite")
add_box(col_fl2_furn, "Seu_Bed", 0.6, 10.5, Z2, 2.4, 12.5, Z2 + 0.55, "Mat_BeddingWhite", bevel=0.03)
add_box(col_fl2_furn, "Seu_Desk", 2.8, 10.5, Z2, 3.8, 12.5, Z2 + 0.75, "Mat_WoodOakTable")

# D. PHÒNG CHỊ HAI (Y = 13.0..16.0, X = 0.22..4.0)
add_box(col_fl2_arch, "Wall_Fl2_Sister2", 0.22, 12.95, Z2, 4.0, 13.05, H2, "Mat_WallWarmWhite")
add_box(col_fl2_furn, "Sister2_Bed", 0.6, 13.5, Z2, 2.4, 15.5, Z2 + 0.55, "Mat_BeddingCream", bevel=0.03)
add_box(col_fl2_furn, "Sister2_Desk", 2.8, 13.5, Z2, 3.8, 15.5, Z2 + 0.75, "Mat_WoodOakTable")
add_box(col_fl2_arch, "Sister2_RearDoor", 1.2, 15.76, Z2, 3.6, 15.82, Z2 + 2.5, "Mat_GlassClear")

# E. BAN CÔNG SAU SIÊU RỘNG 5M X 8M (Y = 16.0..24.0)
add_box(col_fl2_arch, "BalconyRear_Rail_End", 0.0, 23.95, Z2, 5.0, 24.0, Z2 + 1.15, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Rail_L", 0.0, 16.0, Z2, 0.05, 24.0, Z2 + 1.15, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Rail_R", 4.95, 16.0, Z2, 5.0, 24.0, Z2 + 1.15, "Mat_BalconyGlassBronze")
add_box(col_fl2_furn, "BalconyRear_YogaMat", 1.2, 17.5, Z2, 2.2, 19.5, Z2 + 0.02, "Mat_CushionMustard")
for pr in range(3):
    add_box(col_fl2_furn, f"BalconyRear_DryingRod_{pr}", 1.2, 21.5 + pr * 0.6, Z2 + 1.8, 3.8, 21.55 + pr * 0.6, Z2 + 1.84, "Mat_MetalStainless")

# ---------------------------------------------------------------------------
# 8. TẦNG MÁI & SOLAR PV
# ---------------------------------------------------------------------------
ZR = 7.35
add_box(col_roof, "Roof_Fascia", -0.25, -0.35, ZR, 5.25, 16.35, ZR + 0.22, "Mat_RoofCharcoal")
add_box(col_roof, "Roof_Slab", 0.05, 0.05, ZR + 0.22, 4.95, 15.95, ZR + 0.28, "Mat_WallWarmWhite")
add_box(col_roof, "Roof_Skylight", 1.4, 7.2, ZR + 0.28, 3.2, 9.8, ZR + 0.55, "Mat_GlassClear")
add_cyl(col_roof, "Roof_WaterTank", 1.25, 13.5, ZR + 0.35, ZR + 1.75, 0.65, 0.65, "Mat_MetalStainless", rot=(math.pi/2, 0, 0))
for p in range(3):
    py = 2.2 + p * 1.65
    add_box(col_roof, f"SolarPV_L_{p}", 0.55, py, ZR + 0.30, 2.25, py + 1.40, ZR + 0.38, "Mat_SolarPVPanels")
    add_box(col_roof, f"SolarPV_R_{p}", 2.75, py, ZR + 0.30, 4.45, py + 1.40, ZR + 0.38, "Mat_SolarPVPanels")

# ---------------------------------------------------------------------------
# 9. LIGHTING & CAMERAS
# ---------------------------------------------------------------------------
def add_warm_light(name, loc, energy=220.0, color=(1.0, 0.78, 0.45)):
    ld = bpy.data.lights.new(name=name, type='POINT')
    ld.energy = energy
    ld.color = color
    lo = bpy.data.objects.new(name, ld)
    lo.location = loc
    col_lights.objects.link(lo)
    return lo

add_warm_light("Light_FrontCanopy", (2.5, -9.0, 3.2), 300.0)
add_warm_light("Light_DadTeaWall", (0.8, -3.5, 2.0), 160.0)
add_warm_light("Light_LivingNew", (2.5, 2.8, 3.1), 280.0)
add_warm_light("Light_ParentsBed", (2.0, 7.4, 3.1), 220.0)
add_warm_light("Light_KitchenNew", (2.5, 13.5, 3.1), 300.0)
add_warm_light("Light_MasterFront", (2.5, 2.5, 6.6), 320.0)
add_warm_light("Light_BalconyRear8m", (2.5, 19.5, 5.5), 200.0)

# Save .blend
save_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else r"c:\Users\nconghau\Desktop\new fe\myhome\myhome"
blend_path = os.path.join(save_dir, "Fullhouse_Model.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

print("=" * 70)
print(f"SUCCESS: Fullhouse New Layout Model saved to {blend_path}")
print(f"Total objects created: {len(bpy.data.objects)}")
print("=" * 70)
