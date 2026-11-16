"""
=============================================================================
FULLHOUSE 3D ARCHITECTURAL, NIGHT ILLUMINATION & SMART HOME MODEL FOR BLENDER
Dự án: Biệt thự phố 2 tầng hiện đại "Fullhouse" (5m × 16m trên khu đất 7m × 41m)
Phiên bản: Night Illumination (Lên đèn ban đêm lung linh) + Smart Home AI + PBR Procedural Textures
=============================================================================
Các nâng cấp nổi bật trong phiên bản này:
1. Họa tiết & Vật liệu Procedural PBR chân thực (Không cần file ảnh rời):
   - Sàn gỗ xương cá / ván gỗ sồi có vân gỗ tự nhiên và độ nhám Bump 3D.
   - Gạch đá Calacatta vân mây có đường ron mạch gạch rõ nét.
   - Đá chẻ tự nhiên (Split-Face Stone) ốp trụ cổng rào có chiều sâu khối.
   - Hệ tấm pin năng lượng mặt trời Monocrystalline có lưới cell quang điện.
2. Hệ thống Ánh sáng Ban Đêm Lung Linh (Collection: 07_Lighting_And_Night_LEDs):
   - Hệ lam gỗ mặt tiền thông tầng (Tầng 1 + Tầng 2) tích hợp dải đèn LED vàng ấm hắt khe.
   - Đèn LED hắt trần ban công, viền mái Charcoal, đèn hắt vách TV lam sóng, gầm tủ bếp,
     chân đảo làm bánh, kệ sách, gầm bậc cầu thang và tủ áo cánh kính Master.
   - Đèn rọi tranh treo tường, đèn ngủ chụp vải phát sáng ấm, đèn thả bàn ăn,
     8 trụ đèn nấm sân vườn, đèn trụ cổng và đèn pha/hậu xe SUV trắng.
3. Hệ sinh thái Smart Home, Điện, WiFi & Camera An Ninh (Collection: 09_SmartHome_WiFi_Power_Cameras):
   - Hệ thống WiFi Mesh 6E (3 Node: Kệ TV Phòng khách, Khu Đọc sách/Bếp, Hành lang Tầng 2) + Vòng sóng 3D.
   - Trung tâm điều khiển Smart Home (Màn hình cảm ứng 10 inch tại Phòng khách).
   - Tủ điện tổng MDB + Bộ hòa lưới Inverter Solar 5kW tại tường kỹ thuật cầu thang Tầng 1,
     Tủ điện nhánh Tầng 2 và Trạm sạc xe điện EV Wallbox tại sân đỗ ô tô.
   - 6 Camera An Ninh PoE góc rộng (Cổng chính, Sân trước/Hiên trà, Hành lang 2m, Vườn rau 7m,
     Trong phòng khách, Ban công Tầng 2) kèm nón vùng quét tia hồng ngoại 3D (FOV Cones).
   - 5 Điều hòa thông minh Inverter, Khóa cửa vân tay FaceID cửa chính & Hệ thống tưới rau tự động.
4. Nhãn nổi 3D (Collection: 10_SmartHome_3D_Callout_Labels):
   - Hiển thị trực tiếp các bảng tên thiết bị kèm đường chỉ dẫn trong không gian 3D Blender
     (giống hệt hình mẫu kiến trúc Smart Home), có thể bật/tắt nhanh trong Outliner.
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
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in list(bpy.data.lights):
        if block.users == 0:
            bpy.data.lights.remove(block)
    for block in list(bpy.data.cameras):
        if block.users == 0:
            bpy.data.cameras.remove(block)
    for block in list(bpy.data.curves):
        if block.users == 0:
            bpy.data.curves.remove(block)

clear_scene()

def get_or_create_col(name, parent=None):
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        if parent:
            parent.children.link(col)
        else:
            bpy.context.scene.collection.children.link(col)
    return col

col_main = get_or_create_col("Fullhouse_Master_Project")
col_site = get_or_create_col("01_Site_Landscape_Trees", col_main)
col_fl1_arch = get_or_create_col("02_Floor1_Architecture", col_main)
col_fl1_furn = get_or_create_col("03_Floor1_Interior_Furniture", col_main)
col_fl2_arch = get_or_create_col("04_Floor2_Architecture", col_main)
col_fl2_furn = get_or_create_col("05_Floor2_Interior_Master", col_main)
col_roof = get_or_create_col("06_Roof_Solar_Technical", col_main)
col_lights = get_or_create_col("07_Lighting_And_Night_LEDs", col_main)
col_enclosure = get_or_create_col("08_Left_Cutaway_Walls_Full", col_main)
col_smarthome = get_or_create_col("09_SmartHome_WiFi_Power_Cameras", col_main)
col_callouts = get_or_create_col("10_SmartHome_3D_Callout_Labels", col_main)

# Hide full left wall collection by default in viewport so cutaway interior is visible immediately
col_enclosure.hide_viewport = True
col_enclosure.hide_render = True

# ---------------------------------------------------------------------------
# 2. PROCEDURAL PBR SHADERS & MATERIALS (REALISTIC PATTERNS & BUMP MAPS)
# ---------------------------------------------------------------------------
def set_principled_emission(bsdf, emission_rgba, emission_strength):
    if not emission_rgba:
        return
    if 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = emission_rgba
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    elif 'Emission' in bsdf.inputs:
        bsdf.inputs['Emission'].default_value = emission_rgba
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = emission_strength

def create_mat(name, color_rgba, roughness=0.5, metallic=0.0, transmission=0.0, emission_rgba=None, emission_strength=1.0, alpha=1.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
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
        if hasattr(mat, 'blend_method'):
            mat.blend_method = 'BLEND'

    set_principled_emission(bsdf, emission_rgba, emission_strength)

    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_procedural_wood_mat(name, col1=(0.65, 0.44, 0.25, 1.0), col2=(0.48, 0.30, 0.16, 1.0), mortar=(0.22, 0.12, 0.06, 1.0), scale=14.0, roughness=0.34):
    """Procedural Wood Planks with grain noise & bump map"""
    mat = create_mat(name, col1, roughness=roughness)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    brick = nodes.new(type='ShaderNodeTexBrick')
    brick.offset = 0.5
    brick.inputs['Color1'].default_value = col1
    brick.inputs['Color2'].default_value = col2
    brick.inputs['Mortar'].default_value = mortar
    brick.inputs['Scale'].default_value = scale
    brick.inputs['Mortar Size'].default_value = 0.012
    brick.inputs['Brick Width'].default_value = 0.65
    brick.inputs['Row Height'].default_value = 0.14

    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.15
    bump.inputs['Distance'].default_value = 0.01

    links.new(tex_coord.outputs['Object'], brick.inputs['Vector'])
    links.new(brick.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(brick.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat

def create_procedural_marble_tile_mat(name, base_col=(0.96, 0.96, 0.95, 1.0), vein_col=(0.74, 0.70, 0.64, 1.0), scale=3.5, roughness=0.16):
    """Procedural Calacatta veined marble porcelain tiles with subtle grout"""
    mat = create_mat(name, base_col, roughness=roughness)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    wave = nodes.new(type='ShaderNodeTexWave')
    wave.wave_type = 'BANDS'
    wave.bands_direction = 'DIAGONAL'
    wave.inputs['Scale'].default_value = scale
    wave.inputs['Distortion'].default_value = 6.5
    wave.inputs['Detail'].default_value = 4.0

    mix = nodes.new(type='ShaderNodeMixRGB')
    mix.inputs['Color1'].default_value = base_col
    mix.inputs['Color2'].default_value = vein_col

    links.new(tex_coord.outputs['Object'], wave.inputs['Vector'])
    links.new(wave.outputs['Fac'], mix.inputs['Fac'])
    links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    return mat

def create_procedural_stone_mat(name):
    """Procedural Split-Face Slate Stone for Gate Pillars & Accent Walls"""
    mat = create_mat(name, (0.20, 0.24, 0.30, 1.0), roughness=0.65)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    brick = nodes.new(type='ShaderNodeTexBrick')
    brick.inputs['Color1'].default_value = (0.22, 0.27, 0.34, 1.0)
    brick.inputs['Color2'].default_value = (0.14, 0.18, 0.23, 1.0)
    brick.inputs['Mortar'].default_value = (0.07, 0.09, 0.12, 1.0)
    brick.inputs['Scale'].default_value = 9.0
    brick.inputs['Mortar Size'].default_value = 0.025
    brick.inputs['Brick Width'].default_value = 0.45
    brick.inputs['Row Height'].default_value = 0.18

    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.45
    bump.inputs['Distance'].default_value = 0.02

    links.new(tex_coord.outputs['Object'], brick.inputs['Vector'])
    links.new(brick.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(brick.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat

def create_procedural_solar_mat(name):
    """Procedural Monocrystalline Solar Panel Grid"""
    mat = create_mat(name, (0.04, 0.09, 0.22, 1.0), roughness=0.14, metallic=0.65)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    brick = nodes.new(type='ShaderNodeTexBrick')
    brick.offset = 0.0
    brick.inputs['Color1'].default_value = (0.04, 0.09, 0.22, 1.0)
    brick.inputs['Color2'].default_value = (0.05, 0.11, 0.26, 1.0)
    brick.inputs['Mortar'].default_value = (0.55, 0.72, 0.92, 1.0)
    brick.inputs['Scale'].default_value = 12.0
    brick.inputs['Mortar Size'].default_value = 0.015
    brick.inputs['Brick Width'].default_value = 0.20
    brick.inputs['Row Height'].default_value = 0.20

    links.new(tex_coord.outputs['Generated'], brick.inputs['Vector'])
    links.new(brick.outputs['Color'], bsdf.inputs['Base Color'])
    return mat

# Create Materials with Realistic Procedural Shaders
create_mat("Mat_WallWarmWhite", (0.96, 0.95, 0.93, 1.0), roughness=0.72)
create_mat("Mat_WallFacadeWarm", (0.90, 0.87, 0.82, 1.0), roughness=0.62)
create_mat("Mat_RoofCharcoal", (0.12, 0.16, 0.22, 1.0), roughness=0.50, metallic=0.15)
create_procedural_stone_mat("Mat_DarkGreyStone")
create_mat("Mat_RoadAsphalt", (0.10, 0.12, 0.16, 1.0), roughness=0.88)
create_procedural_marble_tile_mat("Mat_FloorTileCream", (0.96, 0.95, 0.93, 1.0), (0.78, 0.73, 0.66, 1.0), scale=2.8, roughness=0.16)
create_procedural_wood_mat("Mat_AntiSlipWoodTile", (0.66, 0.45, 0.27, 1.0), (0.52, 0.34, 0.19, 1.0), scale=12.0, roughness=0.35)
create_mat("Mat_AntiSlipTileGrey", (0.34, 0.37, 0.42, 1.0), roughness=0.65)
create_procedural_wood_mat("Mat_AntiSlipPavers", (0.32, 0.36, 0.42, 1.0), (0.26, 0.30, 0.36, 1.0), mortar=(0.16, 0.18, 0.22, 1.0), scale=4.5, roughness=0.78)
create_mat("Mat_WhitePebbles", (0.90, 0.89, 0.86, 1.0), roughness=0.7)
create_mat("Mat_SoilDark", (0.24, 0.16, 0.11, 1.0), roughness=0.95)
create_mat("Mat_GrassGreen", (0.16, 0.44, 0.24, 1.0), roughness=0.88)
create_mat("Mat_FoliageGreen", (0.14, 0.50, 0.22, 1.0), roughness=0.6)
create_mat("Mat_FoliageDark", (0.09, 0.36, 0.16, 1.0), roughness=0.65)
create_mat("Mat_FoliageLime", (0.28, 0.62, 0.24, 1.0), roughness=0.55)
create_mat("Mat_TreeTrunk", (0.35, 0.23, 0.15, 1.0), roughness=0.85)
create_mat("Mat_FlowerPink", (0.92, 0.26, 0.48, 1.0), roughness=0.5)
create_mat("Mat_FlowerYellow", (0.96, 0.76, 0.15, 1.0), roughness=0.5)
create_mat("Mat_FruitOrange", (0.95, 0.45, 0.10, 1.0), roughness=0.35)
create_mat("Mat_TomatoRed", (0.88, 0.15, 0.15, 1.0), roughness=0.3)

create_procedural_marble_tile_mat("Mat_WhiteMarble", (0.98, 0.98, 0.99, 1.0), (0.72, 0.76, 0.82, 1.0), scale=4.5, roughness=0.10)
create_mat("Mat_BlackGranite", (0.08, 0.09, 0.10, 1.0), roughness=0.15)
create_procedural_wood_mat("Mat_WoodOakTable", (0.68, 0.47, 0.29, 1.0), (0.58, 0.38, 0.22, 1.0), scale=16.0, roughness=0.30)
create_procedural_wood_mat("Mat_WoodOakCabinet", (0.73, 0.53, 0.35, 1.0), (0.62, 0.43, 0.27, 1.0), scale=14.0, roughness=0.34)
create_mat("Mat_WoodOakDark", (0.25, 0.15, 0.09, 1.0), roughness=0.35)
create_mat("Mat_WoodWalnutAltar", (0.24, 0.13, 0.08, 1.0), roughness=0.3)
create_procedural_wood_mat("Mat_WoodLouverFacade", (0.72, 0.46, 0.24, 1.0), (0.58, 0.35, 0.17, 1.0), scale=18.0, roughness=0.36)
create_procedural_wood_mat("Mat_WoodStairTreads", (0.64, 0.43, 0.25, 1.0), (0.52, 0.34, 0.19, 1.0), scale=15.0, roughness=0.32)
create_mat("Mat_RattanWeave", (0.76, 0.60, 0.40, 1.0), roughness=0.65)
create_mat("Mat_PlanterWood", (0.46, 0.30, 0.18, 1.0), roughness=0.55)

create_mat("Mat_FabricSofaWarm", (0.24, 0.27, 0.32, 1.0), roughness=0.82) # Modern Charcoal Sofa like reference image
create_mat("Mat_FabricTaupe", (0.62, 0.57, 0.52, 1.0), roughness=0.85)
create_mat("Mat_CushionMustard", (0.88, 0.64, 0.20, 1.0), roughness=0.8)
create_mat("Mat_CushionTerracotta", (0.78, 0.36, 0.26, 1.0), roughness=0.8)
create_mat("Mat_CushionSage", (0.48, 0.62, 0.52, 1.0), roughness=0.8)
create_mat("Mat_CushionRose", (0.82, 0.54, 0.58, 1.0), roughness=0.8)
create_mat("Mat_CushionNavy", (0.14, 0.24, 0.42, 1.0), roughness=0.8)
create_mat("Mat_RugWoven", (0.85, 0.82, 0.76, 1.0), roughness=0.92)
create_mat("Mat_BeddingCream", (0.92, 0.89, 0.84, 1.0), roughness=0.85)
create_mat("Mat_BeddingWhite", (0.97, 0.97, 0.96, 1.0), roughness=0.85)
create_mat("Mat_CurtainSheer", (0.95, 0.95, 0.94, 0.65), roughness=0.45, transmission=0.45)
create_mat("Mat_CurtainDrape", (0.75, 0.70, 0.64, 1.0), roughness=0.85)

create_mat("Mat_GlassClear", (0.88, 0.94, 0.98, 0.25), roughness=0.04, transmission=0.92, alpha=0.28)
create_mat("Mat_GlassFrosted", (0.90, 0.94, 0.96, 0.55), roughness=0.38, transmission=0.72, alpha=0.55)
create_mat("Mat_BalconyGlassBronze", (0.55, 0.68, 0.74, 0.45), roughness=0.08, transmission=0.78, alpha=0.42)
create_mat("Mat_MirrorSilver", (0.92, 0.95, 0.97, 1.0), roughness=0.02, metallic=0.98)
create_mat("Mat_PianoBlackGloss", (0.02, 0.02, 0.03, 1.0), roughness=0.04, metallic=0.25)
create_mat("Mat_TVScreenBlack", (0.05, 0.12, 0.28, 1.0), roughness=0.08, metallic=0.4, emission_rgba=(0.08, 0.22, 0.55, 1.0), emission_strength=1.2)

# Night Illumination & Smart Home Emissive Shaders
create_mat("Mat_WarmLED", (1.0, 0.88, 0.60, 1.0), roughness=0.15, emission_rgba=(1.0, 0.82, 0.45, 1.0), emission_strength=6.5)
create_mat("Mat_WarmSconce", (1.0, 0.92, 0.70, 1.0), roughness=0.20, emission_rgba=(1.0, 0.86, 0.52, 1.0), emission_strength=8.0)
create_mat("Mat_SmartCyanLED", (0.22, 0.74, 0.97, 1.0), roughness=0.15, emission_rgba=(0.22, 0.74, 0.97, 1.0), emission_strength=5.5)
create_mat("Mat_SmartGreenLED", (0.06, 0.73, 0.50, 1.0), roughness=0.15, emission_rgba=(0.06, 0.73, 0.50, 1.0), emission_strength=5.0)
create_mat("Mat_SmartRedLED", (0.94, 0.26, 0.26, 1.0), roughness=0.15, emission_rgba=(0.94, 0.26, 0.26, 1.0), emission_strength=5.0)
create_mat("Mat_CameraFOV", (0.22, 0.74, 0.97, 0.18), roughness=0.2, transmission=0.85, emission_rgba=(0.22, 0.74, 0.97, 1.0), emission_strength=0.8, alpha=0.18)
create_mat("Mat_CalloutBoard", (0.06, 0.14, 0.30, 1.0), roughness=0.25, metallic=0.2, emission_rgba=(0.08, 0.20, 0.45, 1.0), emission_strength=1.5)
create_mat("Mat_CalloutText", (1.0, 1.0, 1.0, 1.0), roughness=0.1, emission_rgba=(1.0, 1.0, 1.0, 1.0), emission_strength=4.0)

create_procedural_solar_mat("Mat_SolarPVPanels")
create_mat("Mat_CarWhite", (0.96, 0.97, 0.98, 1.0), roughness=0.14, metallic=0.75) # White SUV like reference image
create_mat("Mat_TireRubber", (0.12, 0.12, 0.13, 1.0), roughness=0.85)
create_mat("Mat_CeramicWhite", (0.95, 0.96, 0.97, 1.0), roughness=0.15)
create_mat("Mat_MetalMatteBlack", (0.10, 0.10, 0.11, 1.0), roughness=0.35, metallic=0.75)
create_mat("Mat_MetalStainless", (0.82, 0.83, 0.85, 1.0), roughness=0.20, metallic=0.92)
create_mat("Mat_BrassWarm", (0.86, 0.68, 0.34, 1.0), roughness=0.25, metallic=0.88)
create_mat("Mat_BuddhaGold", (0.96, 0.78, 0.24, 1.0), roughness=0.18, metallic=0.92)
create_mat("Mat_BronzeGateMetal", (0.18, 0.20, 0.22, 1.0), roughness=0.35, metallic=0.7)
create_mat("Mat_BookCream", (0.92, 0.88, 0.80, 1.0), roughness=0.7)
create_mat("Mat_BookOchre", (0.78, 0.52, 0.22, 1.0), roughness=0.7)

# ---------------------------------------------------------------------------
# 3. MESH PRIMITIVE GENERATORS (BMESH)
# ---------------------------------------------------------------------------
def link_mesh_obj(collection, name, bm, mat_name, loc=(0, 0, 0), rot=(0, 0, 0), smooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
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

def add_sphere(collection, name, cx, cy, cz, rx, ry=None, rz=None, mat_name=None, subdiv=2, smooth=True):
    ry = rx if ry is None else ry
    rz = rx if rz is None else rz

    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    bmesh.ops.scale(bm, vec=(rx, ry, rz), verts=bm.verts)
    return link_mesh_obj(collection, name, bm, mat_name, loc=(cx, cy, cz), smooth=smooth)

def add_wall_with_openings(collection, name, axis, fixed_coord, thickness, start_u, end_u, z_bot, z_top, openings, mat_name="Mat_WallWarmWhite"):
    events = sorted(set([start_u, end_u] + [op[0] for op in openings] + [op[1] for op in openings]))
    for i in range(len(events) - 1):
        u1 = events[i]
        u2 = events[i + 1]
        matching_ops = [op for op in openings if op[0] <= u1 and op[1] >= u2]
        if not matching_ops:
            if axis == 'Y':
                add_box(collection, f"{name}_P_{i}", fixed_coord, u1, z_bot, fixed_coord + thickness, u2, z_top, mat_name)
            else:
                add_box(collection, f"{name}_P_{i}", u1, fixed_coord, z_bot, u2, fixed_coord + thickness, z_top, mat_name)
        else:
            op_bot, op_top = matching_ops[0][2], matching_ops[0][3]
            if op_bot > z_bot + 0.01:
                if axis == 'Y':
                    add_box(collection, f"{name}_Sill_{i}", fixed_coord, u1, z_bot, fixed_coord + thickness, u2, op_bot, mat_name)
                else:
                    add_box(collection, f"{name}_Sill_{i}", u1, fixed_coord, z_bot, u2, fixed_coord + thickness, op_bot, mat_name)
            if op_top < z_top - 0.01:
                if axis == 'Y':
                    add_box(collection, f"{name}_Header_{i}", fixed_coord, u1, op_top, fixed_coord + thickness, u2, z_top, mat_name)
                else:
                    add_box(collection, f"{name}_Header_{i}", u1, fixed_coord, op_top, u2, fixed_coord + thickness, z_top, mat_name)

def add_framed_window(collection, name, axis, fixed_coord, thickness, u1, u2, z1, z2):
    ft = 0.045
    mid_u = (u1 + u2) / 2.0
    if axis == 'Y':
        cx = fixed_coord + thickness / 2.0
        add_box(collection, f"{name}_FrameBot", fixed_coord - 0.01, u1, z1, fixed_coord + thickness + 0.01, u2, z1 + ft, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameTop", fixed_coord - 0.01, u1, z2 - ft, fixed_coord + thickness + 0.01, u2, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameL", fixed_coord - 0.01, u1, z1, fixed_coord + thickness + 0.01, u1 + ft, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameR", fixed_coord - 0.01, u2 - ft, z1, fixed_coord + thickness + 0.01, u2, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_Mullion", cx - 0.015, mid_u - 0.02, z1 + ft, cx + 0.015, mid_u + 0.02, z2 - ft, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_Glass", cx - 0.008, u1 + ft, z1 + ft, cx + 0.008, u2 - ft, z2 - ft, "Mat_GlassClear")
    else:
        cy = fixed_coord + thickness / 2.0
        add_box(collection, f"{name}_FrameBot", u1, fixed_coord - 0.01, z1, u2, fixed_coord + thickness + 0.01, z1 + ft, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameTop", u1, fixed_coord - 0.01, z2 - ft, u2, fixed_coord + thickness + 0.01, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameL", u1, fixed_coord - 0.01, z1, u1 + ft, fixed_coord + thickness + 0.01, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameR", u2 - ft, fixed_coord - 0.01, z1, u2, fixed_coord + thickness + 0.01, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_Mullion", mid_u - 0.02, cy - 0.015, z1 + ft, mid_u + 0.02, cy + 0.015, z2 - ft, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_Glass", u1 + ft, cy - 0.008, z1 + ft, u2 - ft, cy + 0.008, z2 - ft, "Mat_GlassClear")

def add_interior_door(collection, name, axis, fixed_coord, thickness, u1, u2, z1, z2, open_angle=0.35):
    ft = 0.04
    if axis == 'Y':
        add_box(collection, f"{name}_JambL", fixed_coord - 0.01, u1, z1, fixed_coord + thickness + 0.01, u1 + ft, z2, "Mat_WoodOakDark")
        add_box(collection, f"{name}_JambR", fixed_coord - 0.01, u2 - ft, z1, fixed_coord + thickness + 0.01, u2, z2, "Mat_WoodOakDark")
        add_box(collection, f"{name}_Header", fixed_coord - 0.01, u1, z2 - ft, fixed_coord + thickness + 0.01, u2, z2, "Mat_WoodOakDark")
        cx = fixed_coord + thickness / 2.0
        add_box(collection, f"{name}_Leaf", cx - 0.022, u1 + ft, z1 + 0.01, cx + 0.022, u2 - ft, z2 - ft, "Mat_WoodOakCabinet", bevel=0.008, rot_z=open_angle)
        add_box(collection, f"{name}_Handle", cx - 0.05, u2 - ft - 0.12, z1 + 0.98, cx + 0.05, u2 - ft - 0.04, z1 + 1.02, "Mat_BrassWarm")
    else:
        add_box(collection, f"{name}_JambL", u1, fixed_coord - 0.01, z1, u1 + ft, fixed_coord + thickness + 0.01, z2, "Mat_WoodOakDark")
        add_box(collection, f"{name}_JambR", u2 - ft, fixed_coord - 0.01, z1, u2, fixed_coord + thickness + 0.01, z2, "Mat_WoodOakDark")
        add_box(collection, f"{name}_Header", u1, fixed_coord - 0.01, z2 - ft, u2, fixed_coord + thickness + 0.01, z2, "Mat_WoodOakDark")
        cy = fixed_coord + thickness / 2.0
        add_box(collection, f"{name}_Leaf", u1 + ft, cy - 0.022, z1 + 0.01, u2 - ft, cy + 0.022, z2 - ft, "Mat_WoodOakCabinet", bevel=0.008, rot_z=open_angle)
        add_box(collection, f"{name}_Handle", u2 - ft - 0.12, cy - 0.05, z1 + 0.98, u2 - ft - 0.04, cy + 0.05, z1 + 1.02, "Mat_BrassWarm")

# ---------------------------------------------------------------------------
# 4. REUSABLE ULTRA-DETAILED FURNITURE & LIGHTING BUILDERS
# ---------------------------------------------------------------------------
def build_tree(collection, name, x, y, z, scale=1.0, with_fruit=False):
    add_cyl(collection, f"{name}_Trunk", x, y, z, z + 1.8 * scale, 0.14 * scale, 0.09 * scale, "Mat_TreeTrunk")
    canopy_blobs = [
        (0.0, 0.0, 2.7, 1.05, 1.0, 0.85, "Mat_FoliageGreen"),
        (0.55, 0.35, 2.5, 0.80, 0.75, 0.68, "Mat_FoliageDark"),
        (-0.50, 0.30, 2.6, 0.82, 0.78, 0.70, "Mat_FoliageLime"),
        (0.20, -0.50, 2.5, 0.78, 0.80, 0.65, "Mat_FoliageGreen"),
    ]
    for i, (ox, oy, oz, rx, ry, rz, m) in enumerate(canopy_blobs):
        add_sphere(collection, f"{name}_Canopy_{i}", x + ox * scale, y + oy * scale, z + oz * scale, rx * scale, ry * scale, rz * scale, m, subdiv=2)
    # Warm Tree Uplight at base for Night Mode
    add_cyl(col_lights, f"{name}_Uplight", x + 0.25, y - 0.25, z, z + 0.08, 0.08, 0.08, "Mat_WarmSconce")
    if with_fruit:
        for fi, (fx, fy, fz) in enumerate([(0.5, 0.4, 2.3), (-0.45, 0.25, 2.35), (0.2, -0.5, 2.25)]):
            add_sphere(collection, f"{name}_Fruit_{fi}", x + fx * scale, y + fy * scale, z + fz * scale, 0.08 * scale, 0.08 * scale, 0.09 * scale, "Mat_FruitOrange", subdiv=1)

def build_potted_plant(collection, name, x, y, z, scale=1.0, style="monstera"):
    add_cyl(collection, f"{name}_Pot", x, y, z, z + 0.36 * scale, 0.15 * scale, 0.19 * scale, "Mat_CeramicWhite")
    add_cyl(collection, f"{name}_Soil", x, y, z + 0.33 * scale, z + 0.35 * scale, 0.17 * scale, 0.17 * scale, "Mat_SoilDark")
    for i in range(5):
        ang = i * 1.25
        lx = x + math.cos(ang) * 0.16 * scale
        ly = y + math.sin(ang) * 0.16 * scale
        lz = z + (0.55 + (i % 2) * 0.12) * scale
        add_sphere(collection, f"{name}_Leaf_{i}", lx, ly, lz, 0.14 * scale, 0.09 * scale, 0.03 * scale, "Mat_FoliageGreen" if i % 2 == 0 else "Mat_FoliageLime", subdiv=1)

def build_detailed_bed(collection, name, cx, cy, z, width=1.8, length=2.0, facing="+X", duvet_mat="Mat_BeddingCream", accent_mat="Mat_CushionNavy"):
    x0 = cx - length / 2.0
    x1 = cx + length / 2.0
    y0 = cy - width / 2.0
    y1 = cy + width / 2.0
    add_box(collection, f"{name}_Frame", x0, y0, z + 0.08, x1, y1, z + 0.28, "Mat_WoodOakTable", bevel=0.015)
    add_box(collection, f"{name}_HeadboardBoard", x0 - 0.02, y0 - 0.08, z, x0 + 0.06, y1 + 0.08, z + 1.22, "Mat_WoodLouverFacade", bevel=0.015)
    # Warm LED strip embedded at top of headboard
    add_box(col_lights, f"{name}_HeadboardLED", x0 + 0.04, y0 - 0.05, z + 1.22, x0 + 0.08, y1 + 0.05, z + 1.26, "Mat_WarmLED")
    add_box(collection, f"{name}_Mattress", x0 + 0.08, y0 + 0.04, z + 0.28, x1 - 0.04, y1 - 0.04, z + 0.54, "Mat_BeddingWhite", bevel=0.03)
    add_box(collection, f"{name}_Duvet", x0 + 0.50, y0 + 0.02, z + 0.32, x1 - 0.02, y1 - 0.02, z + 0.58, duvet_mat, bevel=0.045)
    add_box(collection, f"{name}_ThrowRunner", x1 - 0.55, y0 + 0.01, z + 0.34, x1 - 0.08, y1 - 0.01, z + 0.60, accent_mat, bevel=0.02)
    for pi in range(2):
        py = y0 + width * (0.28 + pi * 0.44)
        add_box(collection, f"{name}_Pillow_{pi}", x0 + 0.14, py - 0.30, z + 0.54, x0 + 0.35, py + 0.30, z + 0.70, "Mat_BeddingWhite", bevel=0.035)

def build_nightstand_with_lamp(collection, name, cx, cy, z):
    add_box(collection, f"{name}_Table", cx - 0.22, cy - 0.22, z, cx + 0.22, cy + 0.22, z + 0.52, "Mat_WoodOakCabinet", bevel=0.01)
    add_cyl(collection, f"{name}_LampStem", cx, cy, z + 0.52, z + 0.72, 0.02, 0.03, "Mat_BrassWarm")
    add_cyl(col_lights, f"{name}_LampShade", cx, cy, z + 0.72, z + 0.92, 0.14, 0.09, "Mat_WarmSconce")

def build_framed_wall_art_with_light(collection, name, cx, cy, cz, w=0.9, h=0.65, axis='X', theme_mat="Mat_CushionMustard"):
    if axis == 'X':
        add_box(collection, f"{name}_Frame", cx - w/2, cy - 0.02, cz - h/2, cx + w/2, cy + 0.02, cz + h/2, "Mat_WoodOakDark")
        add_box(collection, f"{name}_Canvas", cx - w/2 + 0.04, cy - 0.025, cz - h/2 + 0.04, cx + w/2 - 0.04, cy + 0.025, cz + h/2 - 0.04, theme_mat)
        add_box(col_lights, f"{name}_SpotLED", cx - w*0.35, cy - 0.08, cz + h/2 + 0.06, cx + w*0.35, cy + 0.08, cz + h/2 + 0.10, "Mat_WarmSconce")
    else:
        add_box(collection, f"{name}_Frame", cx - 0.02, cy - w/2, cz - h/2, cx + 0.02, cy + w/2, cz + h/2, "Mat_WoodOakDark")
        add_box(collection, f"{name}_Canvas", cx - 0.025, cy - w/2 + 0.04, cz - h/2 + 0.04, cx + 0.025, cy + w/2 - 0.04, cz + h/2 - 0.04, theme_mat)
        add_box(col_lights, f"{name}_SpotLED", cx - 0.08, cy - w*0.35, cz + h/2 + 0.06, cx + 0.08, cy + w*0.35, cz + h/2 + 0.10, "Mat_WarmSconce")

def build_wardrobe(collection, name, min_x, min_y, z, max_x, max_y, height=2.55, glass_doors=False):
    add_box(collection, f"{name}_Body", min_x, min_y, z, max_x, max_y, z + height, "Mat_WoodOakCabinet", bevel=0.012)
    door_mat = "Mat_GlassFrosted" if glass_doors else "Mat_WoodOakCabinet"
    add_box(collection, f"{name}_Doors", min_x, min_y + 0.02, z + 0.04, min_x + 0.02, max_y - 0.02, z + height - 0.04, door_mat)
    if glass_doors:
        add_box(col_lights, f"{name}_InternalLED", (min_x + max_x)/2, min_y + 0.08, z + height - 0.12, (min_x + max_x)/2 + 0.05, max_y - 0.08, z + height - 0.08, "Mat_WarmLED")

def build_dining_chair(collection, name, cx, cy, z, rot_z=0.0, seat_mat="Mat_RugWoven"):
    add_box(collection, f"{name}_Seat", cx - 0.22, cy - 0.22, z + 0.42, cx + 0.22, cy + 0.22, z + 0.48, seat_mat, bevel=0.02, rot_z=rot_z)
    add_box(collection, f"{name}_Back", cx - 0.22, cy + 0.18, z + 0.48, cx + 0.22, cy + 0.22, z + 0.88, "Mat_WoodOakTable", bevel=0.015, rot_z=rot_z)
    for lx in [cx - 0.18, cx + 0.18]:
        for ly in [cy - 0.18, cy + 0.18]:
            add_cyl(collection, f"{name}_Leg_{lx:.1f}_{ly:.1f}", lx, ly, z, z + 0.42, 0.02, 0.015, "Mat_WoodOakDark")

def build_desk_and_chair(collection, name, cx, cy, z, width=1.25, depth=0.58, facing="+X"):
    add_box(collection, f"{name}_Top", cx - depth / 2, cy - width / 2, z + 0.72, cx + depth / 2, cy + width / 2, z + 0.76, "Mat_WoodOakTable", bevel=0.01)
    add_box(collection, f"{name}_LegL", cx - depth / 2 + 0.04, cy - width / 2 + 0.04, z, cx + depth / 2 - 0.04, cy - width / 2 + 0.08, z + 0.72, "Mat_MetalMatteBlack")
    add_box(collection, f"{name}_LegR", cx - depth / 2 + 0.04, cy + width / 2 - 0.08, z, cx + depth / 2 - 0.04, cy + width / 2 - 0.04, z + 0.72, "Mat_MetalMatteBlack")
    add_box(collection, f"{name}_Laptop", cx - 0.12, cy - 0.16, z + 0.76, cx + 0.12, cy + 0.16, z + 0.775, "Mat_MetalStainless")
    build_dining_chair(collection, f"{name}_Chair", cx + depth / 2 + 0.35, cy, z, rot_z=math.pi)

def build_bathroom_fixtures(collection, name, min_x, min_y, z, max_x, max_y, has_bathtub=False):
    add_box(collection, f"{name}_Vanity", min_x + 0.15, min_y + 0.15, z + 0.20, min_x + 0.65, min_y + 0.95, z + 0.82, "Mat_WoodOakCabinet", bevel=0.01)
    add_box(collection, f"{name}_Counter", min_x + 0.12, min_y + 0.12, z + 0.82, min_x + 0.68, min_y + 0.98, z + 0.86, "Mat_WhiteMarble", bevel=0.01)
    add_box(collection, f"{name}_SinkBasin", min_x + 0.22, min_y + 0.32, z + 0.86, min_x + 0.58, min_y + 0.78, z + 0.96, "Mat_CeramicWhite", bevel=0.03)
    add_box(collection, f"{name}_MirrorLED", min_x + 0.14, min_y + 0.22, z + 1.15, min_x + 0.16, min_y + 0.88, z + 1.95, "Mat_MirrorSilver")
    add_box(col_lights, f"{name}_MirrorBacklight", min_x + 0.13, min_y + 0.20, z + 1.13, min_x + 0.14, min_y + 0.90, z + 1.97, "Mat_WarmLED")

    sh_y0, sh_y1 = max_y - 1.25, max_y - 0.10
    add_box(collection, f"{name}_ShowerDoor", min_x + 0.85, sh_y0, z, min_x + 0.87, sh_y1, z + 2.15, "Mat_GlassClear")
    add_cyl(collection, f"{name}_RainHead", min_x + 0.32, (sh_y0 + sh_y1) / 2.0, z + 2.06, z + 2.08, 0.13, 0.13, "Mat_BrassWarm")

    add_box(collection, f"{name}_ToiletTank", min_x + 0.15, min_y + 1.20, z + 0.42, min_x + 0.45, min_y + 1.62, z + 0.82, "Mat_CeramicWhite", bevel=0.02)
    add_box(collection, f"{name}_ToiletBowl", min_x + 0.35, min_y + 1.25, z, min_x + 0.72, min_y + 1.57, z + 0.42, "Mat_CeramicWhite", bevel=0.04)

    if has_bathtub:
        bx, by = (min_x + max_x) / 2.0 + 0.15, max_y - 0.55
        add_box(collection, f"{name}_Bathtub", bx - 0.75, by - 0.35, z + 0.02, bx + 0.75, by + 0.35, z + 0.58, "Mat_CeramicWhite", bevel=0.15)

def build_upright_piano(collection, name, x, y, z):
    add_box(collection, f"{name}_MainCase", x, y - 0.74, z + 0.04, x + 0.38, y + 0.74, z + 1.20, "Mat_PianoBlackGloss", bevel=0.015)
    add_box(collection, f"{name}_TopLid", x - 0.01, y - 0.76, z + 1.20, x + 0.42, y + 0.76, z + 1.24, "Mat_PianoBlackGloss", bevel=0.012)
    add_box(collection, f"{name}_UpperPanel", x + 0.38, y - 0.66, z + 0.80, x + 0.40, y + 0.66, z + 1.15, "Mat_PianoBlackGloss", bevel=0.008)
    add_box(collection, f"{name}_Keybed", x + 0.38, y - 0.72, z + 0.68, x + 0.66, y + 0.72, z + 0.76, "Mat_PianoBlackGloss", bevel=0.01)
    key_span = 1.22
    for k in range(52):
        ky = (y - key_span / 2) + k * (key_span / 52)
        add_box(collection, f"{name}_WKey_{k}", x + 0.42, ky + 0.002, z + 0.76, x + 0.64, ky + 0.021, z + 0.785, "Mat_CeramicWhite")
    for bki, bp in enumerate([0, 1, 3, 4, 5, 7, 8, 10, 11, 12, 14, 15, 17, 18, 19, 21, 22, 24, 25, 26, 28, 29, 31, 32, 33, 35, 36, 38, 39, 40, 42, 43, 45, 46, 47, 49]):
        ky = (y - key_span / 2) + bp * (key_span / 52) + 0.015
        add_box(collection, f"{name}_BKey_{bki}", x + 0.42, ky, z + 0.785, x + 0.57, ky + 0.013, z + 0.81, "Mat_PianoBlackGloss")
    add_box(collection, f"{name}_MusicStand", x + 0.40, y - 0.32, z + 0.88, x + 0.42, y + 0.32, z + 1.08, "Mat_PianoBlackGloss")
    add_box(collection, f"{name}_SheetMusic", x + 0.422, y - 0.24, z + 0.90, x + 0.428, y + 0.24, z + 1.06, "Mat_BookCream")
    for pi, py in enumerate([-0.09, 0.0, 0.09]):
        add_box(collection, f"{name}_Pedal_{pi}", x + 0.36, y + py - 0.018, z + 0.04, x + 0.44, y + py + 0.018, z + 0.08, "Mat_BuddhaGold")
    add_box(collection, f"{name}_Bench", x + 0.82, y - 0.38, z, x + 1.15, y + 0.38, z + 0.48, "Mat_WoodOakDark", bevel=0.02)

def build_detailed_car(collection, name, cx, cy, z):
    add_box(collection, f"{name}_Chassis", cx - 0.95, cy - 2.15, z + 0.18, cx + 0.95, cy + 2.15, z + 0.75, "Mat_CarWhite", bevel=0.08)
    add_box(collection, f"{name}_Cabin", cx - 0.85, cy - 0.95, z + 0.75, cx + 0.85, cy + 1.25, z + 1.48, "Mat_CarWhite", bevel=0.08)
    add_box(collection, f"{name}_Windshield", cx - 0.82, cy - 0.88, z + 0.80, cx + 0.82, cy - 0.45, z + 1.42, "Mat_BalconyGlassBronze")
    add_box(collection, f"{name}_RearWindow", cx - 0.82, cy + 0.85, z + 0.80, cx + 0.82, cy + 1.20, z + 1.42, "Mat_BalconyGlassBronze")
    # Glowing LED Headlights & Taillights
    add_box(col_lights, f"{name}_HeadlightL", cx - 0.82, cy - 2.17, z + 0.50, cx - 0.52, cy - 2.14, z + 0.64, "Mat_WarmSconce")
    add_box(col_lights, f"{name}_HeadlightR", cx + 0.52, cy - 2.17, z + 0.50, cx + 0.82, cy - 2.14, z + 0.64, "Mat_WarmSconce")
    add_box(col_lights, f"{name}_Taillight", cx - 0.84, cy + 2.14, z + 0.54, cx + 0.84, cy + 2.17, z + 0.63, "Mat_SmartRedLED")
    for wx in [cx - 0.98, cx + 0.98]:
        for wy in [cy - 1.35, cy + 1.35]:
            add_cyl(collection, f"{name}_Wheel_{wx:.1f}_{wy:.1f}", wx, wy, z, z + 0.35, 0.35, 0.35, "Mat_TireRubber", rot=(0, math.pi / 2, 0))

def build_scooter(collection, name, cx, cy, z):
    add_box(collection, f"{name}_Body", cx - 0.18, cy - 0.75, z + 0.22, cx + 0.18, cy + 0.65, z + 0.72, "Mat_CeramicWhite", bevel=0.04)
    add_box(collection, f"{name}_Seat", cx - 0.15, cy - 0.45, z + 0.72, cx + 0.15, cy + 0.25, z + 0.82, "Mat_FabricTaupe", bevel=0.02)
    add_cyl(collection, f"{name}_FrontWheel", cx, cy - 0.65, z, z + 0.22, 0.22, 0.22, "Mat_TireRubber", rot=(0, math.pi / 2, 0))
    add_cyl(collection, f"{name}_RearWheel", cx, cy + 0.55, z, z + 0.22, 0.22, 0.22, "Mat_TireRubber", rot=(0, math.pi / 2, 0))

# ---------------------------------------------------------------------------
# 5. SITE, LANDSCAPE & GARDEN BOLLARD LIGHTS (7m x 41m)
# ---------------------------------------------------------------------------
add_box(col_site, "Site_ArchitecturalBasePlinth", -0.5, -18.5, -0.45, 7.5, 23.5, -0.01, "Mat_RoofCharcoal")
add_box(col_site, "Site_FrontRoad", -4.0, -24.0, -0.35, 11.0, -18.8, -0.20, "Mat_RoadAsphalt")
for stripe in range(5):
    sx = -2.5 + stripe * 3.0
    add_box(col_site, f"Road_Stripe_{stripe}", sx, -21.4, -0.195, sx + 1.4, -21.22, -0.19, "Mat_CeramicWhite")
add_box(col_site, "Site_Sidewalk", -2.0, -18.8, -0.20, 9.0, -18.0, 0.0, "Mat_WallFacadeWarm")

# Sân trước 18m
add_box(col_site, "Site_FrontYard_Slab", 0.0, -18.0, 0.0, 7.0, 0.0, 0.15, "Mat_AntiSlipPavers")
add_box(col_site, "Site_FrontLawn", 2.8, -17.5, 0.15, 6.8, -6.0, 0.18, "Mat_GrassGreen")
build_tree(col_site, "Tree_Front_Shade", 4.8, -14.0, 0.18, scale=1.35, with_fruit=False)
build_tree(col_site, "Tree_Front_Shade2", 5.2, -8.5, 0.18, scale=1.1, with_fruit=False)

# 8 Garden Pathway Bollard Lights (Đèn trụ nấm sân vườn)
for b_idx, by in enumerate([-16.2, -12.5, -8.8, -5.2, 3.0, 8.5, 14.0, 18.5]):
    bx = 2.65 if by < 0 else 6.75
    add_box(col_lights, f"Garden_BollardPost_{b_idx}", bx - 0.05, by - 0.05, 0.15, bx + 0.05, by + 0.05, 0.62, "Mat_MetalMatteBlack")
    add_box(col_lights, f"Garden_BollardGlow_{b_idx}", bx - 0.08, by - 0.08, 0.62, bx + 0.08, by + 0.08, 0.72, "Mat_WarmSconce")

# Boundary Fences & Split-Stone Gate Pillars
add_box(col_site, "Fence_Front_Left", -0.18, -18.0, 0.0, 0.0, 23.0, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Right", 7.0, -18.0, 0.0, 7.18, 23.0, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Rear_Solid", -0.18, 23.0, 0.0, 7.18, 23.18, 2.35, "Mat_WallWarmWhite")

# Gate Pillars with Split-Stone Texture & Glowing Cap Lamps
for pname, gx0, gx1 in [("Gate_Pillar_L", -0.18, 0.35), ("Gate_Pillar_M", 2.65, 2.95), ("Gate_Pillar_R", 6.85, 7.18)]:
    add_box(col_site, pname, gx0, -18.18, 0.0, gx1, -17.82, 2.65, "Mat_DarkGreyStone")
    add_box(col_lights, f"{pname}_CapLamp", gx0 + 0.06, -18.12, 2.65, gx1 - 0.06, -17.88, 2.82, "Mat_WarmSconce")

for gx0, gx1, gname in [(0.35, 2.65, "MainCarGate"), (2.95, 6.85, "FrontPedestrianFence")]:
    add_box(col_site, f"{gname}_RailBot", gx0, -18.0, 0.18, gx1, -17.94, 0.26, "Mat_BronzeGateMetal")
    add_box(col_site, f"{gname}_RailTop", gx0, -18.0, 2.22, gx1, -17.94, 2.30, "Mat_BronzeGateMetal")
    num_slats = int((gx1 - gx0) / 0.14)
    for s in range(num_slats):
        sx = gx0 + 0.04 + s * 0.14
        add_box(col_site, f"{gname}_Slat_{s}", sx, -17.99, 0.24, sx + 0.06, -17.95, 2.24, "Mat_BronzeGateMetal")

# White Family SUV in Driveway
build_detailed_car(col_site, "Family_SUV_White", 1.45, -11.5, 0.15)

# HIÊN NHÀ & GÓC GIAO LƯU TRÀ / BBQ NGOÀI TRỜI CỦA BA (X = 2.4..4.9, Y = -4.8..-0.6)
add_box(col_site, "Porch_Deck", 2.45, -4.8, 0.15, 4.95, -0.6, 0.24, "Mat_AntiSlipWoodTile", bevel=0.01)
for px in [2.52, 4.88]:
    for py in [-4.70, -0.70]:
        add_box(col_site, f"Porch_Post_{px:.1f}_{py:.1f}", px - 0.05, py - 0.05, 0.24, px + 0.05, py + 0.05, 2.85, "Mat_MetalMatteBlack")
for r in range(9):
    ry = -4.8 + r * 0.52
    add_box(col_site, f"Porch_Rafter_{r}", 2.40, ry, 2.85, 5.00, ry + 0.10, 2.95, "Mat_WoodLouverFacade")
    if r % 2 == 1:
        add_box(col_lights, f"Porch_PergolaLED_{r}", 2.75, ry + 0.02, 2.81, 4.65, ry + 0.08, 2.85, "Mat_WarmLED")
add_box(col_site, "Porch_GlassRoof", 2.35, -4.95, 2.95, 5.05, -0.55, 2.99, "Mat_BalconyGlassBronze")

# Table for Dad & Uncles
add_box(col_site, "Porch_TableTop", 3.20, -3.30, 0.90, 4.20, -2.10, 0.96, "Mat_WhiteMarble", bevel=0.015)
add_box(col_site, "Porch_TableBase", 3.45, -3.00, 0.24, 3.95, -2.40, 0.90, "Mat_WoodOakDark")
build_dining_chair(col_site, "Porch_Chair_L", 2.85, -2.70, 0.24, rot_z=-math.pi / 2.0, seat_mat="Mat_CushionMustard")
build_dining_chair(col_site, "Porch_Chair_R", 4.55, -2.70, 0.24, rot_z=math.pi / 2.0, seat_mat="Mat_CushionMustard")
build_dining_chair(col_site, "Porch_Chair_F", 3.70, -3.70, 0.24, rot_z=math.pi, seat_mat="Mat_CushionMustard")
build_dining_chair(col_site, "Porch_Chair_B", 3.70, -1.70, 0.24, rot_z=0.0, seat_mat="Mat_CushionMustard")
add_sphere(col_site, "Porch_Teapot", 3.65, -2.70, 1.04, 0.07, 0.07, 0.06, "Mat_CeramicWhite")
add_cyl(col_site, "Porch_Beer1", 3.38, -2.35, 0.96, 1.08, 0.035, 0.038, "Mat_CushionMustard")
add_cyl(col_site, "Porch_Beer2", 4.02, -2.35, 0.96, 1.08, 0.035, 0.038, "Mat_CushionMustard")

# Đường luồng 2m (X = 5.0 to 7.0, Y = 0.0 to 16.0)
add_box(col_site, "Site_SideCorridor", 5.0, 0.0, 0.0, 7.0, 16.0, 0.15, "Mat_AntiSlipPavers")
for step_i in range(12):
    sy = 0.8 + step_i * 1.25
    add_box(col_site, f"Side_SteppingStone_{step_i}", 5.35, sy, 0.15, 6.10, sy + 0.65, 0.18, "Mat_WhiteMarble", bevel=0.01)
    add_sphere(col_site, f"Side_Flower_{step_i}", 6.65, sy + 0.3, 0.42, 0.15, 0.15, 0.15, "Mat_FoliageDark", subdiv=1)

# Sân sau 7m (Y = 16.0 to 23.0) + Smart Drip Irrigation
add_box(col_site, "Site_RearYard_Slab", 0.0, 16.0, 0.0, 7.0, 19.5, 0.15, "Mat_AntiSlipPavers")
add_box(col_site, "Site_RearGarden_Soil", 0.0, 19.5, 0.0, 7.0, 23.0, 0.15, "Mat_GrassGreen")
for r in range(3):
    vy = 20.0 + r * 0.95
    add_box(col_site, f"VegBox_Frame_{r}", 0.5, vy, 0.15, 4.8, vy + 0.65, 0.42, "Mat_PlanterWood", bevel=0.01)
    add_box(col_site, f"VegBox_Soil_{r}", 0.58, vy + 0.06, 0.16, 4.72, vy + 0.59, 0.39, "Mat_SoilDark")
    # Smart Drip Irrigation Line
    add_box(col_smarthome, f"Smart_Irrigation_Pipe_{r}", 0.52, vy + 0.30, 0.42, 4.75, vy + 0.34, 0.45, "Mat_SmartCyanLED")
    for vx_i in range(8):
        vx = 0.85 + vx_i * 0.50
        add_sphere(col_site, f"Veg_Plant_{r}_{vx_i}", vx, vy + 0.32, 0.48, 0.14, 0.14, 0.12, "Mat_FoliageLime" if (r + vx_i) % 2 == 0 else "Mat_FoliageGreen", subdiv=1)
build_tree(col_site, "Tree_Rear_Mango", 6.0, 21.2, 0.15, scale=1.2, with_fruit=True)

# ---------------------------------------------------------------------------
# 6. FLOOR 1 ARCHITECTURE & FACADE WOOD LOUVERS WITH LED (Y = 0.0 to 16.0)
# ---------------------------------------------------------------------------
Z1 = 0.25
H1 = 3.60

add_box(col_fl1_arch, "Floor1_Slab", 0.0, 0.0, 0.10, 5.0, 16.0, Z1, "Mat_FloorTileCream")
add_box(col_fl1_arch, "Floor1_Parents_WoodFloor", 0.22, 3.92, Z1, 3.72, 7.20, Z1 + 0.015, "Mat_WoodOakTable")

# SIGNATURE DOUBLE-HEIGHT VERTICAL WOOD SLAT FACADE + HIDDEN WARM LED STRIPS (Matching Reference Model!)
add_box(col_fl1_arch, "Facade_WoodBacking", 0.0, -0.10, Z1, 1.15, 0.02, 7.20, "Mat_WoodOakDark")
for sl in range(11):
    sx = 0.06 + sl * 0.10
    add_box(col_fl1_arch, f"Facade_VertSlat_{sl}", sx, -0.20, Z1, sx + 0.045, -0.05, 7.18, "Mat_WoodLouverFacade")
add_box(col_lights, "Facade_VertLED_1", 0.34, -0.18, Z1 + 0.1, 0.38, -0.12, 7.10, "Mat_WarmLED")
add_box(col_lights, "Facade_VertLED_2", 0.84, -0.18, Z1 + 0.1, 0.88, -0.12, 7.10, "Mat_WarmLED")
add_box(col_lights, "Facade_CanopyLED_Fl1", 0.10, -0.15, H1 - 0.05, 4.90, -0.08, H1, "Mat_WarmLED")

# Left Exterior Wall (cutaway base + enclosure full)
add_box(col_fl1_arch, "Floor1_LeftWall_Cutaway", 0.0, 0.0, Z1, 0.22, 16.0, Z1 + 0.42, "Mat_WallWarmWhite")
add_box(col_enclosure, "Floor1_LeftWall_Full", 0.0, 0.0, Z1 + 0.42, 0.22, 16.0, H1, "Mat_WallWarmWhite")

# Right Exterior Wall (X = 4.78..5.0)
fl1_right_openings = [
    (0.40, 1.40, 0.85, 2.65),
    (4.60, 6.40, 0.95, 2.55),
    (8.20, 9.80, 0.95, 2.55),
    (11.20, 12.80, 0.95, 2.55),
    (13.20, 14.20, Z1, 2.45),
]
add_wall_with_openings(col_fl1_arch, "Floor1_RightWall", 'Y', 4.78, 0.22, 0.0, 16.0, Z1, H1, fl1_right_openings, "Mat_WallWarmWhite")
add_framed_window(col_fl1_arch, "Win_Fl1_LivingFront", 'Y', 4.78, 0.22, 0.40, 1.40, 0.85, 2.65)
add_framed_window(col_fl1_arch, "Win_Fl1_Parents", 'Y', 4.78, 0.22, 4.60, 6.40, 0.95, 2.55)
add_framed_window(col_fl1_arch, "Win_Fl1_Study", 'Y', 4.78, 0.22, 8.20, 9.80, 0.95, 2.55)
add_framed_window(col_fl1_arch, "Win_Fl1_Kitchen", 'Y', 4.78, 0.22, 11.20, 12.80, 0.95, 2.55)
add_framed_window(col_fl1_arch, "Door_Fl1_KitchenSide", 'Y', 4.78, 0.22, 13.20, 14.20, Z1, 2.45)

# Front & Rear Facade Walls Floor 1
add_wall_with_openings(col_fl1_arch, "Floor1_FrontWall", 'X', 0.0, 0.22, 0.0, 5.0, Z1, H1, [(1.18, 4.45, Z1, 2.75)], "Mat_WallFacadeWarm")
add_framed_window(col_fl1_arch, "Entrance_4PanelDoor", 'X', 0.0, 0.22, 1.18, 4.45, Z1, 2.75)

add_wall_with_openings(col_fl1_arch, "Floor1_RearWall", 'X', 15.78, 0.22, 0.0, 5.0, Z1, H1, [(0.60, 1.40, 1.80, 2.40), (2.80, 4.20, Z1, 2.45)], "Mat_WallWarmWhite")
add_framed_window(col_fl1_arch, "Win_Fl1_RearBath", 'X', 15.78, 0.22, 0.60, 1.40, 1.80, 2.40)
add_framed_window(col_fl1_arch, "Door_Fl1_RearPatio", 'X', 15.78, 0.22, 2.80, 4.20, Z1, 2.45)

# Interior Partitions Floor 1
add_wall_with_openings(col_fl1_arch, "Part_Fl1_LivingParents", 'X', 3.80, 0.12, 0.22, 3.72, Z1, H1, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl1_arch, "Part_Fl1_ParentsHall", 'Y', 3.72, 0.12, 3.80, 7.20, Z1, H1, [(4.00, 4.90, Z1, 2.25)], "Mat_WallWarmWhite")
add_interior_door(col_fl1_arch, "Door_ParentsBed", 'Y', 3.72, 0.12, 4.00, 4.90, Z1, 2.25)
add_wall_with_openings(col_fl1_arch, "Part_Fl1_ParentsStair", 'X', 7.20, 0.12, 0.22, 3.72, Z1, H1, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl1_arch, "Part_Fl1_StudyKitchen", 'X', 10.40, 0.12, 0.22, 2.60, Z1, H1, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl1_arch, "Part_Fl1_KitchenBath", 'X', 14.20, 0.12, 0.22, 2.40, Z1, H1, [(0.60, 1.45, Z1, 2.25)], "Mat_WallWarmWhite")
add_interior_door(col_fl1_arch, "Door_Fl1_Bath", 'X', 14.20, 0.12, 0.60, 1.45, Z1, 2.25)
add_wall_with_openings(col_fl1_arch, "Part_Fl1_BathSide", 'Y', 2.40, 0.12, 14.20, 15.78, Z1, H1, [], "Mat_WallWarmWhite")

# ---------------------------------------------------------------------------
# 7. FLOOR 1 INTERIOR FURNITURE & WARM COVE LIGHTING
# ---------------------------------------------------------------------------
# A. PHÒNG KHÁCH (Y = 0.3..3.8, X = 0.3..3.2)
add_box(col_fl1_furn, "Living_Rug", 0.40, 0.50, Z1, 3.10, 3.40, Z1 + 0.015, "Mat_RugWoven", bevel=0.005)
add_box(col_fl1_furn, "Sofa_Base", 0.35, 0.60, Z1 + 0.06, 1.15, 2.50, Z1 + 0.14, "Mat_WoodOakTable", bevel=0.01)
add_box(col_fl1_furn, "Sofa_ChaiseBase", 0.35, 2.50, Z1 + 0.06, 2.05, 3.25, Z1 + 0.14, "Mat_WoodOakTable", bevel=0.01)
add_box(col_fl1_furn, "Sofa_Back", 0.35, 0.60, Z1 + 0.14, 0.55, 3.25, Z1 + 0.78, "Mat_FabricSofaWarm", bevel=0.035)
add_box(col_fl1_furn, "Sofa_Cushion1", 0.52, 0.65, Z1 + 0.14, 1.15, 1.55, Z1 + 0.42, "Mat_FabricSofaWarm", bevel=0.04)
add_box(col_fl1_furn, "Sofa_Cushion2", 0.52, 1.55, Z1 + 0.14, 1.15, 2.45, Z1 + 0.42, "Mat_FabricSofaWarm", bevel=0.04)
add_box(col_fl1_furn, "Sofa_CushionChaise", 0.52, 2.45, Z1 + 0.14, 2.00, 3.20, Z1 + 0.42, "Mat_FabricSofaWarm", bevel=0.04)
add_cyl(col_fl1_furn, "CoffeeTable_Marble", 1.95, 1.50, Z1 + 0.02, Z1 + 0.40, 0.42, 0.42, "Mat_WhiteMarble")
add_cyl(col_fl1_furn, "CoffeeTable_Oak", 2.25, 2.00, Z1 + 0.02, Z1 + 0.46, 0.30, 0.30, "Mat_WoodOakTable")

# Fluted Wood TV Wall + Backlit LED Cove + Framed Wall Art
add_box(col_fl1_furn, "Living_TVConsole", 2.85, 0.80, Z1 + 0.12, 3.18, 2.90, Z1 + 0.52, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_lights, "Living_TVConsole_UnderLED", 2.88, 0.85, Z1 + 0.08, 3.12, 2.85, Z1 + 0.12, "Mat_WarmLED")
add_box(col_fl1_furn, "Living_TVFlutedBackdrop", 3.08, 0.85, Z1 + 0.52, 3.16, 2.85, Z1 + 2.45, "Mat_WoodLouverFacade")
add_box(col_lights, "Living_TVBackdrop_TopLED", 3.04, 0.85, Z1 + 2.42, 3.10, 2.85, Z1 + 2.47, "Mat_WarmLED")
add_box(col_fl1_furn, "Living_TVBezel", 3.00, 1.05, Z1 + 0.78, 3.05, 2.65, Z1 + 1.72, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "Living_TVScreen", 2.99, 1.08, Z1 + 0.81, 3.00, 2.62, Z1 + 1.69, "Mat_TVScreenBlack")
build_framed_wall_art_with_light(col_fl1_furn, "Living_WallArt", 1.75, 3.76, Z1 + 1.85, w=0.95, h=0.68, axis='X', theme_mat="Mat_CushionMustard")
build_nightstand_with_lamp(col_fl1_furn, "Living_CornerLamp", 0.65, 3.48, Z1)

# B. GIAN THỜ BỒ TÁT QUÁN THẾ ÂM & GIA TIÊN
for slat in range(9):
    sy = 1.45 + slat * 0.25
    add_box(col_fl1_furn, f"Altar_CNC_Slat_{slat}", 3.25, sy, Z1, 3.29, sy + 0.04, 3.25, "Mat_WoodWalnutAltar")
add_box(col_fl1_furn, "Altar_CNC_TopRail", 3.24, 1.40, 3.25, 3.30, 3.70, 3.32, "Mat_WoodWalnutAltar")
add_box(col_fl1_furn, "Altar_TableLower", 3.90, 2.00, Z1 + 0.10, 4.65, 3.40, Z1 + 1.05, "Mat_WoodWalnutAltar", bevel=0.015)
add_box(col_fl1_furn, "Altar_TableUpper", 4.25, 2.20, Z1 + 1.05, 4.65, 3.20, Z1 + 1.25, "Mat_WoodWalnutAltar", bevel=0.01)
add_cyl(col_fl1_furn, "Altar_LotusPedestal", 4.45, 2.70, Z1 + 1.25, Z1 + 1.35, 0.16, 0.20, "Mat_BuddhaGold")
add_cyl(col_fl1_furn, "Altar_QuanYinRobe", 4.45, 2.70, Z1 + 1.35, Z1 + 1.78, 0.12, 0.05, "Mat_BuddhaGold")
add_sphere(col_fl1_furn, "Altar_QuanYinHead", 4.45, 2.70, Z1 + 1.84, 0.06, 0.06, 0.07, "Mat_BuddhaGold")
add_cyl(col_lights, "Altar_GoldenHalo", 4.66, 2.70, Z1 + 1.82, Z1 + 1.84, 0.40, 0.40, "Mat_WarmLED", rot=(0, math.pi / 2, 0))
add_cyl(col_fl1_furn, "Altar_IncenseBurner", 4.10, 2.70, Z1 + 1.05, Z1 + 1.18, 0.08, 0.09, "Mat_BuddhaGold")
add_cyl(col_fl1_furn, "Altar_PrayerCushion", 3.55, 2.70, Z1 + 0.01, Z1 + 0.10, 0.22, 0.22, "Mat_CushionMustard")

# C. PHÒNG NGỦ BA MẸ (Y = 3.8..7.2)
build_detailed_bed(col_fl1_furn, "Parents_Bed", 1.45, 5.50, Z1, width=1.70, length=2.0, facing="+X", duvet_mat="Mat_BeddingCream", accent_mat="Mat_CushionNavy")
build_nightstand_with_lamp(col_fl1_furn, "Parents_Nightstand_L", 0.55, 4.45, Z1)
build_nightstand_with_lamp(col_fl1_furn, "Parents_Nightstand_R", 0.55, 6.55, Z1)
build_wardrobe(col_fl1_furn, "Parents_Wardrobe", 0.35, 6.75, Z1, 2.20, 7.15, height=2.50)

# D. CẦU THANG CÓ ĐÈN LED MŨI BẬC & PHÒNG ĐỌC SÁCH GẦM THANG (Y = 7.2..10.4)
for s in range(10):
    sy = 7.25 + s * 0.20
    sz = Z1 + (s + 1) * 0.177
    add_box(col_fl1_arch, f"Stair_Tread_{s}", 0.24, sy, sz - 0.04, 1.18, sy + 0.22, sz, "Mat_WoodStairTreads", bevel=0.006)
    add_box(col_lights, f"Stair_LEDStrip_{s}", 0.26, sy, sz - 0.045, 1.15, sy + 0.02, sz - 0.035, "Mat_WarmLED")
add_box(col_fl1_arch, "Stair_Landing", 0.24, 9.25, 1.96, 2.22, 9.85, 2.04, "Mat_WoodStairTreads")
add_box(col_fl1_arch, "Stair_GlassBalustrade", 1.18, 7.25, Z1 + 0.20, 1.20, 9.25, Z1 + 1.25, "Mat_GlassClear")

# Bookshelves with Warm Shelf LEDs & Guest Daybed
add_box(col_fl1_furn, "Study_BookshelfMain", 3.45, 7.50, Z1, 3.70, 9.80, 2.65, "Mat_WoodOakCabinet", bevel=0.01)
for shelf_i in range(5):
    sh_z = Z1 + 0.45 + shelf_i * 0.44
    add_box(col_fl1_furn, f"Study_ShelfPlank_{shelf_i}", 3.46, 7.52, sh_z, 3.69, 9.78, sh_z + 0.025, "Mat_WoodOakCabinet")
    add_box(col_lights, f"Study_ShelfLED_{shelf_i}", 3.46, 7.55, sh_z + 0.41, 3.50, 9.75, sh_z + 0.43, "Mat_WarmLED")
    for b in range(7):
        by = 7.60 + b * 0.28
        b_mat = ["Mat_BookCream", "Mat_BookOchre", "Mat_CushionNavy", "Mat_CushionTerracotta"][b % 4]
        add_box(col_fl1_furn, f"Study_Book_{shelf_i}_{b}", 3.48, by, sh_z + 0.025, 3.66, by + 0.22, sh_z + 0.35, b_mat, bevel=0.005)

add_box(col_fl1_furn, "Study_DaybedFrame", 1.35, 7.60, Z1, 2.35, 9.20, Z1 + 0.35, "Mat_WoodOakTable", bevel=0.015)
add_box(col_fl1_furn, "Study_DaybedMattress", 1.40, 7.65, Z1 + 0.35, 2.30, 9.15, Z1 + 0.52, "Mat_RugWoven", bevel=0.03)

# E. BẾP MỞ, QUẦY ĐẢO LÀM BÁNH LED & PHÒNG ĂN (Y = 10.4..14.2)
add_box(col_fl1_furn, "Kitchen_CounterL", 0.35, 10.60, Z1, 1.05, 14.10, Z1 + 0.86, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl1_furn, "Kitchen_StoneTop", 0.32, 10.55, Z1 + 0.86, 1.08, 14.15, Z1 + 0.90, "Mat_WhiteMarble", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_WallCabinets", 0.35, 10.60, 2.05, 0.75, 13.30, 2.75, "Mat_WallFacadeWarm")
add_box(col_lights, "Kitchen_UnderCabinetLED", 0.65, 10.65, 2.01, 0.73, 13.25, 2.05, "Mat_WarmLED")
add_box(col_fl1_furn, "Kitchen_Fridge", 0.35, 13.35, Z1, 1.15, 14.15, Z1 + 1.95, "Mat_MetalStainless")

# Baking Island with Toe-Kick LED
add_box(col_fl1_furn, "Island_Base", 1.48, 11.85, Z1, 2.62, 13.15, Z1 + 0.86, "Mat_WoodOakCabinet", bevel=0.015)
add_box(col_fl1_furn, "Island_MarbleTop", 1.42, 11.80, Z1 + 0.86, 2.68, 13.20, Z1 + 0.90, "Mat_WhiteMarble", bevel=0.01)
add_box(col_lights, "Island_ToeKickLED", 1.46, 11.83, Z1 + 0.02, 2.64, 13.17, Z1 + 0.06, "Mat_WarmLED")
add_box(col_fl1_furn, "Mixer_Base", 1.65, 12.10, Z1 + 0.90, 1.85, 12.35, Z1 + 0.95, "Mat_TomatoRed", bevel=0.01)
add_cyl(col_fl1_furn, "Mixer_Bowl", 1.75, 12.30, Z1 + 0.95, Z1 + 1.12, 0.08, 0.07, "Mat_MetalStainless")

# Dining Table & Glowing Pendant Lamps
add_box(col_fl1_furn, "Dining_TableTop", 3.25, 11.40, Z1 + 0.72, 4.35, 13.00, Z1 + 0.76, "Mat_WoodOakTable", bevel=0.015)
for lx in [3.35, 4.25]:
    for ly in [11.50, 12.90]:
        add_cyl(col_fl1_furn, f"Dining_Leg_{lx:.1f}_{ly:.1f}", lx, ly, Z1, Z1 + 0.72, 0.035, 0.025, "Mat_WoodOakDark")
for ci, cy in enumerate([11.70, 12.20, 12.70]):
    build_dining_chair(col_fl1_furn, f"Dining_Chair_L_{ci}", 2.95, cy, Z1, rot_z=math.pi / 2)
    build_dining_chair(col_fl1_furn, f"Dining_Chair_R_{ci}", 4.65, cy, Z1, rot_z=-math.pi / 2)
for p_idx, py in enumerate([11.85, 12.55]):
    add_cyl(col_lights, f"Dining_PendantCord_{p_idx}", 3.80, py, Z1 + 2.15, H1, 0.008, 0.008, "Mat_MetalMatteBlack")
    add_cyl(col_lights, f"Dining_PendantShade_{p_idx}", 3.80, py, Z1 + 1.98, Z1 + 2.15, 0.16, 0.08, "Mat_WarmSconce")

# F. WC TẦNG 1 & SẢNH SAU
build_bathroom_fixtures(col_fl1_furn, "Fl1_Bathroom", 0.22, 14.20, Z1, 2.40, 15.78, has_bathtub=False)
build_scooter(col_site, "Scooter_RearPorch", 4.30, 14.90, Z1)

# ---------------------------------------------------------------------------
# 8. FLOOR 2 ARCHITECTURE & INTERIOR (Z2 = 3.85, H2 = 7.20)
# ---------------------------------------------------------------------------
Z2 = 3.85
H2 = 7.20

add_box(col_fl2_arch, "Floor2_Slab", 0.0, -1.6, Z2 - 0.15, 5.0, 18.0, Z2, "Mat_FloorTileCream")
add_box(col_fl2_arch, "Floor2_WoodFlooring", 0.22, 0.22, Z2, 4.76, 15.75, Z2 + 0.015, "Mat_WoodOakTable")
add_box(col_lights, "BalconyFront_UnderSlabLED", 0.10, -1.58, Z2 - 0.17, 4.90, -1.50, Z2 - 0.13, "Mat_WarmLED")

add_box(col_fl2_arch, "Floor2_LeftWall_Cutaway", 0.0, 0.0, Z2, 0.22, 16.0, Z2 + 0.42, "Mat_WallWarmWhite")
add_box(col_enclosure, "Floor2_LeftWall_Full", 0.0, 0.0, Z2 + 0.42, 0.22, 16.0, H2, "Mat_WallWarmWhite")

fl2_right_openings = [
    (0.60, 2.20, Z2 + 0.95, Z2 + 2.45),
    (4.60, 6.20, Z2 + 0.95, Z2 + 2.45),
    (7.80, 9.40, Z2 + 1.20, Z2 + 2.45),
    (11.20, 14.20, Z2 + 0.95, Z2 + 2.45),
]
add_wall_with_openings(col_fl2_arch, "Floor2_RightWall", 'Y', 4.78, 0.22, 0.0, 16.0, Z2, H2, fl2_right_openings, "Mat_WallWarmWhite")
add_framed_window(col_fl2_arch, "Win_Fl2_Youngest", 'Y', 4.78, 0.22, 0.60, 2.20, Z2 + 0.95, Z2 + 2.45)
add_framed_window(col_fl2_arch, "Win_Fl2_OlderSister", 'Y', 4.78, 0.22, 4.60, 6.20, Z2 + 0.95, Z2 + 2.45)
add_framed_window(col_fl2_arch, "Win_Fl2_Stair", 'Y', 4.78, 0.22, 7.80, 9.40, Z2 + 1.20, Z2 + 2.45)
add_framed_window(col_fl2_arch, "Win_Fl2_Master", 'Y', 4.78, 0.22, 11.20, 14.20, Z2 + 0.95, Z2 + 2.45)

add_wall_with_openings(col_fl2_arch, "Floor2_FrontWall", 'X', 0.0, 0.22, 0.0, 5.0, Z2, H2, [(1.18, 4.40, Z2, Z2 + 2.55)], "Mat_WallFacadeWarm")
add_framed_window(col_fl2_arch, "Door_Fl2_FrontBalcony", 'X', 0.0, 0.22, 1.18, 4.40, Z2, Z2 + 2.55)

add_wall_with_openings(col_fl2_arch, "Floor2_RearWall", 'X', 15.78, 0.22, 0.0, 5.0, Z2, H2, [(0.80, 4.20, Z2, Z2 + 2.55)], "Mat_WallWarmWhite")
add_framed_window(col_fl2_arch, "Door_Fl2_RearBalcony", 'X', 15.78, 0.22, 0.80, 4.20, Z2, Z2 + 2.55)

# Interior Partitions Floor 2
add_wall_with_openings(col_fl2_arch, "Part_Fl2_Sisters", 'X', 3.80, 0.12, 0.22, 3.72, Z2, H2, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl2_arch, "Part_Fl2_SisterHall1", 'Y', 3.72, 0.12, 0.0, 3.80, Z2, H2, [(0.80, 1.70, Z2, Z2 + 2.25)], "Mat_WallWarmWhite")
add_interior_door(col_fl2_arch, "Door_Fl2_Youngest", 'Y', 3.72, 0.12, 0.80, 1.70, Z2, Z2 + 2.25)

add_wall_with_openings(col_fl2_arch, "Part_Fl2_OlderSisterStair", 'X', 7.20, 0.12, 0.22, 3.72, Z2, H2, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl2_arch, "Part_Fl2_SisterHall2", 'Y', 3.72, 0.12, 3.80, 7.20, Z2, H2, [(4.20, 5.10, Z2, Z2 + 2.25)], "Mat_WallWarmWhite")
add_interior_door(col_fl2_arch, "Door_Fl2_OlderSister", 'Y', 3.72, 0.12, 4.20, 5.10, Z2, Z2 + 2.25)

add_wall_with_openings(col_fl2_arch, "Part_Fl2_SharedBathFront", 'X', 7.40, 0.12, 2.40, 4.78, Z2, H2, [(2.60, 3.45, Z2, Z2 + 2.25)], "Mat_WallWarmWhite")
add_interior_door(col_fl2_arch, "Door_Fl2_SharedBath", 'X', 7.40, 0.12, 2.60, 3.45, Z2, Z2 + 2.25)
add_wall_with_openings(col_fl2_arch, "Part_Fl2_SharedBathSide", 'Y', 2.40, 0.12, 7.40, 9.40, Z2, H2, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl2_arch, "Part_Fl2_SharedBathRear", 'X', 9.40, 0.12, 2.40, 4.78, Z2, H2, [], "Mat_WallWarmWhite")

add_wall_with_openings(col_fl2_arch, "Part_Fl2_MasterEntry", 'X', 10.40, 0.12, 0.22, 4.78, Z2, H2, [(3.60, 4.50, Z2, Z2 + 2.25)], "Mat_WallWarmWhite")
add_interior_door(col_fl2_arch, "Door_Fl2_Master", 'X', 10.40, 0.12, 3.60, 4.50, Z2, Z2 + 2.25)

add_wall_with_openings(col_fl2_arch, "Part_Fl2_MasterBathFront", 'X', 13.80, 0.12, 2.70, 4.78, Z2, H2, [(2.90, 3.75, Z2, Z2 + 2.25)], "Mat_WallWarmWhite")
add_interior_door(col_fl2_arch, "Door_Fl2_MasterBath", 'X', 13.80, 0.12, 2.90, 3.75, Z2, Z2 + 2.25)
add_wall_with_openings(col_fl2_arch, "Part_Fl2_MasterBathSide", 'Y', 2.70, 0.12, 13.80, 15.78, Z2, H2, [], "Mat_WallWarmWhite")

# Front & Rear Balconies Floor 2
add_box(col_fl2_arch, "BalconyFront_GlassRail", 0.0, -1.60, Z2, 5.0, -1.55, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyFront_TopRail", 0.0, -1.62, Z2 + 1.12, 5.0, -1.53, Z2 + 1.17, "Mat_MetalMatteBlack")
add_box(col_fl2_furn, "BalconyFront_RattanChair1", 1.20, -1.25, Z2, 1.80, -0.65, Z2 + 0.75, "Mat_RattanWeave", bevel=0.04)
add_box(col_fl2_furn, "BalconyFront_RattanChair2", 3.20, -1.25, Z2, 3.80, -0.65, Z2 + 0.75, "Mat_RattanWeave", bevel=0.04)
build_nightstand_with_lamp(col_fl2_furn, "BalconyFront_LoungeLamp", 4.35, -0.95, Z2)

# Bedrooms Floor 2
build_detailed_bed(col_fl2_furn, "Youngest_Bed", 1.45, 1.90, Z2, width=1.60, length=2.0, facing="+X", duvet_mat="Mat_BeddingWhite", accent_mat="Mat_CushionNavy")
build_nightstand_with_lamp(col_fl2_furn, "Youngest_Nightstand", 0.55, 0.85, Z2)
build_wardrobe(col_fl2_furn, "Youngest_Wardrobe", 0.35, 3.15, Z2, 2.20, 3.65, height=2.50)
build_desk_and_chair(col_fl2_furn, "Youngest_Desk", 3.10, 2.20, Z2, width=1.20, depth=0.55, facing="+X")

build_detailed_bed(col_fl2_furn, "Sister2_Bed", 1.45, 5.50, Z2, width=1.60, length=2.0, facing="+X", duvet_mat="Mat_BeddingCream", accent_mat="Mat_CushionRose")
build_nightstand_with_lamp(col_fl2_furn, "Sister2_Nightstand", 0.55, 4.45, Z2)
build_wardrobe(col_fl2_furn, "Sister2_Wardrobe", 0.35, 6.55, Z2, 2.20, 7.05, height=2.50)
build_desk_and_chair(col_fl2_furn, "Sister2_Desk", 3.10, 5.50, Z2, width=1.20, depth=0.55, facing="+X")

build_bathroom_fixtures(col_fl2_furn, "Fl2_SharedBath", 2.40, 7.40, Z2, 4.78, 9.40, has_bathtub=False)

# Master Suite
build_upright_piano(col_fl2_furn, "Master_Piano", 0.35, 11.80, Z2)
add_box(col_fl2_furn, "Yoga_Mat", 0.85, 13.20, Z2, 1.65, 15.00, Z2 + 0.012, "Mat_CushionSage", bevel=0.005)
add_cyl(col_fl2_furn, "Meditation_Zafu", 1.25, 14.70, Z2 + 0.012, Z2 + 0.12, 0.20, 0.20, "Mat_CushionTerracotta")
add_cyl(col_fl2_furn, "Tibetan_SingingBowl", 1.65, 14.70, Z2 + 0.012, Z2 + 0.10, 0.08, 0.09, "Mat_BuddhaGold")
add_box(col_fl2_furn, "Yoga_ArchedMirror", 0.36, 13.60, Z2 + 0.20, 0.38, 14.60, Z2 + 1.85, "Mat_MirrorSilver")
build_potted_plant(col_fl2_furn, "Yoga_Monstera", 0.65, 15.35, Z2, scale=1.1, style="monstera")

build_detailed_bed(col_fl2_furn, "Master_KingBed", 2.70, 12.00, Z2, width=1.80, length=2.0, facing="+X", duvet_mat="Mat_BeddingCream", accent_mat="Mat_CushionNavy")
build_nightstand_with_lamp(col_fl2_furn, "Master_Nightstand_L", 1.55, 10.95, Z2)
build_nightstand_with_lamp(col_fl2_furn, "Master_Nightstand_R", 3.85, 10.95, Z2)
build_framed_wall_art_with_light(col_fl2_furn, "Master_WallArt", 2.70, 10.55, Z2 + 1.85, w=1.0, h=0.68, axis='X', theme_mat="Mat_CushionSage")
build_wardrobe(col_fl2_furn, "Master_Wardrobe", 3.85, 11.20, Z2, 4.70, 13.50, height=2.60, glass_doors=True)
build_bathroom_fixtures(col_fl2_furn, "Master_Bathroom", 2.70, 13.80, Z2, 4.78, 15.78, has_bathtub=True)

# Rear Balcony Floor 2
add_box(col_fl2_arch, "BalconyRear_GlassRail", 0.0, 17.95, Z2, 5.0, 18.00, Z2 + 1.15, "Mat_BalconyGlassBronze")
add_box(col_fl2_furn, "Gym_TreadmillDeck", 0.55, 16.30, Z2 + 0.06, 1.35, 17.65, Z2 + 0.18, "Mat_MetalMatteBlack")
add_box(col_fl2_furn, "Gym_TreadmillConsole", 0.55, 17.45, Z2 + 1.15, 1.35, 17.70, Z2 + 1.35, "Mat_MetalMatteBlack")

# ---------------------------------------------------------------------------
# 9. ROOF SLAB, CHARCOAL ARCHITECTURAL FASCIA & SOLAR PV (ZR = 7.35)
# ---------------------------------------------------------------------------
ZR = 7.35
add_box(col_roof, "Roof_Charcoal_Fascia", -0.25, -0.35, ZR, 5.25, 16.35, ZR + 0.22, "Mat_RoofCharcoal")
add_box(col_roof, "Roof_Slab_Inner", 0.05, 0.05, ZR + 0.22, 4.95, 15.95, ZR + 0.28, "Mat_WallWarmWhite")
add_box(col_lights, "Roof_PerimeterLED_Front", -0.15, -0.34, ZR - 0.03, 5.15, -0.28, ZR + 0.01, "Mat_WarmLED")
add_box(col_roof, "Roof_Skylight_Hatch", 1.60, 7.80, ZR + 0.28, 3.40, 9.40, ZR + 0.55, "Mat_GlassClear")

add_cyl(col_roof, "Roof_WaterTank_1500L", 1.25, 13.50, ZR + 0.35, ZR + 1.75, 0.65, 0.65, "Mat_MetalStainless", rot=(math.pi / 2, 0, 0))
add_box(col_roof, "Roof_SolarHeater_Tank", 2.40, 13.20, ZR + 0.95, 3.80, 13.60, ZR + 1.35, "Mat_MetalStainless")
add_box(col_roof, "Roof_SolarHeater_Tubes", 2.45, 13.60, ZR + 0.35, 3.75, 15.00, ZR + 0.95, "Mat_SolarPVPanels", rot=(-0.35, 0, 0))
for p_i in range(3):
    py = 2.20 + p_i * 1.65
    add_box(col_roof, f"Roof_SolarPV_L_{p_i}", 0.55, py, ZR + 0.30, 2.25, py + 1.40, ZR + 0.38, "Mat_SolarPVPanels", rot=(0.12, 0, 0))
    add_box(col_roof, f"Roof_SolarPV_R_{p_i}", 2.75, py, ZR + 0.30, 4.45, py + 1.40, ZR + 0.38, "Mat_SolarPVPanels", rot=(0.12, 0, 0))

# ---------------------------------------------------------------------------
# 10. SMART HOME ECOSYSTEM: WIFI MESH, ELECTRICAL PANELS, CAMERAS & AC
# ---------------------------------------------------------------------------
# 10.1. Smart Electrical Distribution Boards & 5kW Solar Hybrid Inverter
# Main MDB & Solar Inverter at Ground Floor Stairwell/Utility Wall (X = 0.24, Y = 9.35..10.32, Z = 1.35..2.20)
add_box(col_smarthome, "Smart_Electrical_Main_MDB_Fl1", 0.22, 9.85, Z1 + 1.10, 0.38, 10.32, Z1 + 1.95, "Mat_MetalStainless", bevel=0.01)
add_box(col_smarthome, "Smart_Electrical_MDB_StatusLED", 0.38, 9.92, Z1 + 1.65, 0.40, 10.25, Z1 + 1.85, "Mat_SmartGreenLED")
add_box(col_smarthome, "Smart_Solar_Hybrid_Inverter_5kW", 0.22, 9.35, Z1 + 1.20, 0.38, 9.78, Z1 + 1.85, "Mat_CeramicWhite", bevel=0.01)
add_box(col_smarthome, "Smart_Inverter_ScreenLED", 0.38, 9.48, Z1 + 1.48, 0.40, 9.65, Z1 + 1.65, "Mat_SmartCyanLED")

# Floor 2 Sub-Distribution Board (Hành lang trung tâm Lầu 1 - X = 3.72, Y = 7.05)
add_box(col_smarthome, "Smart_Electrical_SubDB_Fl2", 3.68, 7.05, Z2 + 1.35, 3.86, 7.38, Z2 + 1.90, "Mat_MetalStainless", bevel=0.01)
add_box(col_smarthome, "Smart_SubDB_Fl2_LED", 3.86, 7.12, Z2 + 1.65, 3.88, 7.30, Z2 + 1.78, "Mat_SmartGreenLED")

# EV Wallbox Charger in Front Driveway near White SUV
add_box(col_smarthome, "Smart_EV_Wallbox_Charger", 0.01, -11.50, 1.00, 0.15, -11.10, 1.55, "Mat_MetalMatteBlack", bevel=0.015)
add_box(col_smarthome, "Smart_EV_Charger_LED", 0.15, -11.40, 1.15, 0.17, -11.20, 1.42, "Mat_SmartGreenLED")

# 10.2. Smart Home Central Touch Panel & 3 WiFi 6E Mesh Nodes (with Signal Wave Rings)
add_box(col_smarthome, "Smart_Central_Hub_10Inch", 3.35, 3.74, Z1 + 1.35, 3.68, 3.79, Z1 + 1.62, "Mat_MetalMatteBlack")
add_box(col_smarthome, "Smart_Central_Hub_Screen", 3.37, 3.73, Z1 + 1.37, 3.66, 3.74, Z1 + 1.60, "Mat_SmartCyanLED")

def build_wifi_mesh_node(name, cx, cy, cz):
    add_cyl(col_smarthome, f"{name}_Unit", cx, cy, cz, cz + 0.06, 0.14, 0.14, "Mat_CeramicWhite")
    add_cyl(col_smarthome, f"{name}_GlowRing", cx, cy, cz + 0.06, cz + 0.075, 0.14, 0.14, "Mat_SmartCyanLED")
    # 2 concentric WiFi wave rings for visual clarity
    for r_i, rad in enumerate([0.75, 1.45]):
        bm = bmesh.new()
        bmesh.ops.create_circle(bm, cap_ends=False, radius=rad, segments=32)
        me = bpy.data.meshes.new(f"{name}_Wave_{r_i}")
        bm.to_mesh(me)
        bm.free()
        obj = bpy.data.objects.new(f"{name}_Wave_{r_i}", me)
        obj.location = (cx, cy, cz + 0.04)
        col_smarthome.objects.link(obj)

build_wifi_mesh_node("Smart_WiFi_Node1_LivingRouter", 3.00, 2.20, Z1 + 0.55)
build_wifi_mesh_node("Smart_WiFi_Node2_StudyKitchen", 2.50, 10.35, Z1 + 2.35)
build_wifi_mesh_node("Smart_WiFi_Node3_Floor2Hall", 3.75, 5.80, Z2 + 2.35)

# 10.3. 6 AI Security Cameras (PoE) + 3D Field-of-View Cones
def build_security_camera(name, eye, target):
    dx = target[0] - eye[0]
    dy = target[1] - eye[1]
    dz = target[2] - eye[2]
    dist_xy = math.sqrt(dx * dx + dy * dy)
    rz = math.atan2(dx, -dy)
    rx = math.atan2(dz, dist_xy) + math.pi / 2

    add_box(col_smarthome, f"{name}_Body", eye[0] - 0.10, eye[1] - 0.14, eye[2] - 0.07, eye[0] + 0.10, eye[1] + 0.14, eye[2] + 0.07, "Mat_CeramicWhite", rot=(rx, 0, rz))
    add_sphere(col_smarthome, f"{name}_IR_LED", eye[0], eye[1], eye[2] + 0.08, 0.03, 0.03, 0.03, "Mat_SmartRedLED")
    # Semi-transparent FOV detection cone
    cone_len = 3.8
    mid = (eye[0] + dx * 0.35, eye[1] + dy * 0.35, eye[2] + dz * 0.35)
    add_cyl(col_smarthome, f"{name}_FOV_Cone", mid[0], mid[1], mid[2] - cone_len/2, mid[2] + cone_len/2, 1.25, 0.05, "Mat_CameraFOV", rot=(rx, 0, rz))

build_security_camera("Smart_Cam01_FrontGate", (2.80, -17.80, 2.55), (1.50, -12.50, 0.50))
build_security_camera("Smart_Cam02_DrivewayPorch", (4.85, -0.10, 3.35), (2.60, -6.50, 0.50))
build_security_camera("Smart_Cam03_SideCorridor2m", (5.05, 4.00, 3.25), (6.00, 10.50, 0.50))
build_security_camera("Smart_Cam04_RearGarden7m", (2.50, 16.05, 3.35), (2.50, 21.50, 0.40))
build_security_camera("Smart_Cam05_LivingIndoor", (0.35, 0.35, 3.35), (2.50, 2.80, 1.00))
build_security_camera("Smart_Cam06_BalconyFl2", (4.85, -0.10, 6.95), (2.20, -3.50, 3.85))

# 10.4. 5 Smart Inverter Air Conditioners (Dàn lạnh Inverter thông minh)
def build_smart_ac(name, x, y, z):
    add_box(col_smarthome, f"{name}_Unit", x, y - 0.48, z, x + 0.24, y + 0.48, z + 0.28, "Mat_CeramicWhite", bevel=0.015)
    add_box(col_smarthome, f"{name}_Louver", x + 0.23, y - 0.42, z + 0.04, x + 0.25, y + 0.42, z + 0.08, "Mat_MetalMatteBlack")
    add_box(col_smarthome, f"{name}_SmartLED", x + 0.24, y + 0.30, z + 0.14, x + 0.26, y + 0.40, z + 0.18, "Mat_SmartCyanLED")

build_smart_ac("Smart_AC_01_Living", 0.24, 1.80, 2.95)
build_smart_ac("Smart_AC_02_Parents", 0.24, 5.50, 2.95)
build_smart_ac("Smart_AC_03_Youngest", 0.24, 1.90, 6.50)
build_smart_ac("Smart_AC_04_OlderSister", 0.24, 5.40, 6.50)
build_smart_ac("Smart_AC_05_Master", 1.90, 10.54, 6.50)

# 10.5. Smart FaceID Door Lock at Entrance Door
add_box(col_smarthome, "Smart_Lock_MainDoor_Body", 2.75, -0.02, Z1 + 1.05, 2.84, 0.09, Z1 + 1.45, "Mat_MetalMatteBlack", bevel=0.008)
add_box(col_smarthome, "Smart_Lock_FaceID_LED", 2.77, -0.03, Z1 + 1.28, 2.82, -0.01, Z1 + 1.40, "Mat_SmartCyanLED")

# ---------------------------------------------------------------------------
# 11. 3D CALLOUT LABELS IN BLENDER (LIKE USER'S UPLOADED REFERENCE IMAGE)
# ---------------------------------------------------------------------------
def build_3d_callout_label(name, title_text, target_xyz, board_xyz):
    # Leader stem cylinder from device to floating callout board
    add_cyl(col_callouts, f"{name}_LeaderStem", target_xyz[0], target_xyz[1], target_xyz[2], board_xyz[2], 0.018, 0.018, "Mat_SmartCyanLED")
    add_sphere(col_callouts, f"{name}_TargetDot", target_xyz[0], target_xyz[1], target_xyz[2], 0.09, 0.09, 0.09, "Mat_SmartCyanLED")
    # Floating Rounded Board facing -X / Front-Left Dollhouse Camera
    bw, bh = 1.95, 0.58
    add_box(col_callouts, f"{name}_Board", board_xyz[0] - 0.04, board_xyz[1] - bw/2, board_xyz[2], board_xyz[0] + 0.04, board_xyz[1] + bw/2, board_xyz[2] + bh, "Mat_CalloutBoard", bevel=0.02)
    add_box(col_callouts, f"{name}_BorderGlow", board_xyz[0] - 0.05, board_xyz[1] - bw/2, board_xyz[2], board_xyz[0] - 0.04, board_xyz[1] + bw/2, board_xyz[2] + 0.04, "Mat_SmartCyanLED")

    # 3D Text Object on the Board
    font_curve = bpy.data.curves.new(type="FONT", name=f"{name}_TextCurve")
    font_curve.body = title_text
    font_curve.size = 0.19
    font_curve.extrude = 0.015
    font_curve.align_x = 'CENTER'
    font_curve.align_y = 'CENTER'
    text_obj = bpy.data.objects.new(f"{name}_Text", font_curve)
    text_obj.location = (board_xyz[0] - 0.06, board_xyz[1], board_xyz[2] + bh / 2.0)
    text_obj.rotation_euler = (math.pi / 2, 0, -math.pi / 2)
    text_obj.data.materials.append(bpy.data.materials["Mat_CalloutText"])
    col_callouts.objects.link(text_obj)

build_3d_callout_label("Callout_01_SmartLock", "KHOA CUA FACE-ID", (2.80, 0.0, 1.45), (2.80, 0.0, 4.25))
build_3d_callout_label("Callout_02_WiFiHub", "TRUNG TAM & WIFI MESH", (3.00, 2.20, 0.90), (3.00, 2.20, 8.35))
build_3d_callout_label("Callout_03_SmartLight", "DEN LED THONG MINH", (1.45, 5.50, 1.50), (1.45, 5.50, 8.65))
build_3d_callout_label("Callout_04_PowerMDB", "TU DIEN & INVERTER 5KW", (0.35, 9.80, 1.80), (0.35, 9.80, 8.55))
build_3d_callout_label("Callout_05_SmartAC", "DIEU HOA THONG MINH", (1.90, 10.60, 6.60), (1.90, 10.60, 9.10))
build_3d_callout_label("Callout_06_SecurityCam", "6 CAMERA AN NINH AI", (4.85, -0.10, 6.95), (4.85, -0.10, 9.10))

# ---------------------------------------------------------------------------
# 12. NIGHT ILLUMINATION POINT LIGHTS & CAMERAS
# ---------------------------------------------------------------------------
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderSettings") and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'

world = scene.world or bpy.data.worlds.new("World_Fullhouse_Night")
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs['Color'].default_value = (0.02, 0.04, 0.09, 1.0) # Deep evening twilight sky
    bg_node.inputs['Strength'].default_value = 0.35

# Subtle Cool Moonlight Directional Light
sun_data = bpy.data.lights.new(name="Moonlight_Ambient", type='SUN')
sun_data.energy = 0.65
sun_data.color = (0.55, 0.72, 1.0)
sun_obj = bpy.data.objects.new("Moonlight_Ambient", sun_data)
sun_obj.rotation_euler = (math.radians(40), math.radians(25), math.radians(-40))
col_lights.objects.link(sun_obj)

def add_warm_light(name, loc, energy=220.0, color=(1.0, 0.78, 0.45), radius=0.35):
    ld = bpy.data.lights.new(name=name, type='POINT')
    ld.energy = energy
    ld.color = color
    if hasattr(ld, 'shadow_soft_size'):
        ld.shadow_soft_size = radius
    lo = bpy.data.objects.new(name, ld)
    lo.location = loc
    col_lights.objects.link(lo)
    return lo

# Exterior Night Lights
add_warm_light("Light_Gate_Front", (1.50, -17.20, 2.80), 180.0, (1.0, 0.76, 0.40))
add_warm_light("Light_Driveway_SUV", (1.50, -10.50, 2.60), 140.0, (1.0, 0.80, 0.50))
add_warm_light("Light_Dads_TeaPorch", (3.70, -2.70, 2.65), 240.0, (1.0, 0.75, 0.38))
add_warm_light("Light_Facade_WoodLouvers", (0.55, -0.80, 3.80), 260.0, (1.0, 0.74, 0.35))
add_warm_light("Light_Rear_Garden", (2.80, 20.50, 2.50), 160.0, (1.0, 0.80, 0.48))

# Floor 1 Cozy Interior Lights
add_warm_light("Light_Fl1_Living", (1.80, 2.00, 3.15), 280.0)
add_warm_light("Light_Fl1_Altar", (4.10, 2.70, 2.95), 190.0, (1.0, 0.70, 0.28))
add_warm_light("Light_Fl1_Parents", (1.80, 5.50, 3.15), 240.0)
add_warm_light("Light_Fl1_StudyStair", (2.40, 8.60, 3.15), 220.0)
add_warm_light("Light_Fl1_KitchenIsland", (2.60, 12.40, 3.15), 300.0)

# Floor 2 Cozy Interior Lights
add_warm_light("Light_Fl2_FrontBalcony", (2.50, -0.90, 6.20), 180.0)
add_warm_light("Light_Fl2_Youngest", (1.80, 1.90, 6.75), 240.0)
add_warm_light("Light_Fl2_OlderSister", (1.80, 5.50, 6.75), 240.0)
add_warm_light("Light_Fl2_MasterSuite", (2.60, 12.50, 6.75), 320.0)
add_warm_light("Light_Fl2_PianoYoga", (1.10, 13.20, 6.75), 220.0)

def add_camera_look_at(name, eye, target, lens=30.0):
    cd = bpy.data.cameras.new(name=name)
    cd.lens = lens
    co = bpy.data.objects.new(name, cd)
    co.location = eye
    dx = target[0] - eye[0]
    dy = target[1] - eye[1]
    dz = target[2] - eye[2]
    dist_xy = math.sqrt(dx * dx + dy * dy)
    rz = math.atan2(dx, -dy)
    rx = math.atan2(dz, dist_xy) + math.pi / 2
    co.rotation_euler = (rx, 0.0, rz)
    col_lights.objects.link(co)
    return co

cam_dollhouse = add_camera_look_at("Cam_01_Night_SmartHome_Overview", (-18.5, -8.5, 11.5), (2.5, 5.5, 3.5), lens=26.0)
cam_master = add_camera_look_at("Cam_02_Master_Piano_Yoga", (2.5, 10.0, 5.5), (1.5, 12.8, 4.5), lens=22.0)
cam_living = add_camera_look_at("Cam_03_Living_SmartHub_Altar", (0.8, 1.2, 1.5), (3.8, 2.5, 1.4), lens=22.0)
cam_kitchen = add_camera_look_at("Cam_04_Kitchen_Baking_Island", (4.2, 11.0, 1.8), (2.0, 12.5, 1.1), lens=22.0)
cam_porch = add_camera_look_at("Cam_05_Dads_Tea_Porch_Night", (5.8, -5.5, 2.2), (3.7, -2.7, 0.9), lens=24.0)

scene.camera = cam_dollhouse

# ---------------------------------------------------------------------------
# 13. SAVE .BLEND & EXPORT .OBJ / .MTL IN CURRENT WORKSPACE
# ---------------------------------------------------------------------------
save_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if not os.path.exists(save_dir):
    save_dir = r"c:\Users\nconghau\Desktop\new fe\myhome\myhome"

blend_path = os.path.join(save_dir, "Fullhouse_Model.blend")
obj_path = os.path.join(save_dir, "Fullhouse_Model.obj")

bpy.ops.wm.save_as_mainfile(filepath=blend_path)
try:
    bpy.ops.wm.obj_export(filepath=obj_path, export_materials=True, forward_axis='NEGATIVE_Z', up_axis='Y')
except Exception as e:
    print("OBJ export note:", e)

print("=" * 70)
print(f"SUCCESS: Fullhouse Night & Smart Home Blender model saved to {blend_path}")
print(f"Total objects created: {len(bpy.data.objects)}")
print("=" * 70)
