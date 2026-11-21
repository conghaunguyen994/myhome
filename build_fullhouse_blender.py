"""
=============================================================================
FULLHOUSE 3D ARCHITECTURAL & SMART HOME MODEL FOR BLENDER (ENHANCED EDITION)
Phiên bản nâng cấp chi tiết Nội thất, Trang trí & Tỉ lệ phóng lớn (1.5x):
- Phóng to toàn bộ mô hình 1.5x (SCALE_FACTOR = 1.5) giúp dễ quan sát, zoom cận
  cảnh và chiêm ngưỡng từng chi tiết nội thất bên trong.
- Mở thoáng vách cắt bên trái (không bị tường rào che khuất) giúp nhìn xuyên
  vào toàn bộ các phòng Tầng 1 & Tầng 2 như mô hình nhà búp bê kiến trúc.
- Bổ sung đầy đủ đồ nội thất & đồ trang trí chi tiết:
  + Sân trước: Bộ trà cụ đầy đủ (ấm, 4 chén, khay, gối tựa, đôn gỗ), ô tô SUV
    có bánh xe/kính/đèn, cây bonsai nhiều tán, đá bước dặm & đèn nấm sân vườn.
  + Phòng khách: Sofa chữ L + gối tựa nhiều màu + thảm dệt, bàn trà + bình hoa
    + sách decor, kệ TV + loa soundbar + cây xanh, bàn thờ Quan Âm chi tiết
    (tượng, lư hương, 2 bình hoa sen, đèn nến), tranh bộ 3 treo tường, rèm cửa,
    đèn chùm hiện đại & đèn cây đứng.
  + Phòng Ba Mẹ: Giường gỗ có đầu giường + chăn gối + thảm, 2 tab đầu giường +
    đèn ngủ ấm áp, tủ áo có tay nắm, tranh nghệ thuật, cây xanh.
  + Cầu thang chữ U hoàn chỉnh 2 vế + lan can kính tay vịn gỗ + LED mũi bậc.
  + Bếp mở & Bàn ăn: Tủ bếp đầy đủ bếp từ, bồn rửa + vòi nước, máy hút mùi,
    lò vi sóng, bình siêu tốc, đĩa trái cây, tủ lạnh 2 cánh; bàn ăn tròn +
    6 ghế ăn có tựa lưng + đèn thả 3 bóng + bình hoa.
  + Tầng 2 Phòng Master Chị Ba: Giường King + đầu giường bọc nỉ + 4 gối + thảm
    + 2 tab đèn ngủ + tranh; Đàn Piano Upright chi tiết (phím trắng/đen, giá nhạc,
    pedal đồng, ghế đàn); Góc Yoga (thảm, bồ đoàn thiền, cây xanh, nến); Phòng tắm
    riêng (bồn tắm nằm, lavabo gương LED, bồn cầu, vách kính); Walk-in Closet có
    kệ quần áo & thanh treo đồ; rèm cửa sổ cao kịch trần.
  + Phòng Sếu & Phòng Chị Hai: Giường, tab đèn ngủ, bàn học + ghế + laptop/màn
    hình + đèn bàn, kệ sách nhiều màu, tủ quần áo, tranh treo tường, thảm.
  + Ban công trước & sau (5x8m): Bàn ghế chill ngoài trời, chậu cây, góc Yoga
    tắm trăng, giàn phơi có quần áo.
  + Hệ Smart Home đầy đủ: 3 Node WiFi Mesh 6E, 6 Camera AI + nón FOV, màn hình
    trung tâm 10", tủ điện MDB + Inverter 5kW, sạc EV Wallbox, 5 điều hòa.
- Tự động bật sẵn chế độ Material Preview (có màu & vật liệu ngay khi mở file)
  cùng góc Camera mặc định nhìn trực diện vào mặt cắt nội thất.
=============================================================================
"""

import bpy
import bmesh
import math
import os
import random

random.seed(42)

# Phóng to tỉ lệ toàn bộ ngôi nhà 1.5x để dễ nhìn rõ chi tiết nội thất trong Blender
SCALE_FACTOR = 1.5

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
    for block in list(bpy.data.curves):
        if block.users == 0: bpy.data.curves.remove(block)

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
    if not emission_rgba:
        return
    if 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = emission_rgba
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    elif 'Emission' in bsdf.inputs:
        bsdf.inputs['Emission'].default_value = emission_rgba
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = emission_strength

def create_mat(name, color_rgba, roughness=0.5, metallic=0.0, transmission=0.0,
               emission_rgba=None, emission_strength=1.0, alpha=1.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    # Đặt viewport diffuse color để ngay cả chế độ Solid cũng dễ phân biệt phần nào
    mat.diffuse_color = (color_rgba[0], color_rgba[1], color_rgba[2], alpha)

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
        if hasattr(mat, 'surface_render_method'):
            mat.surface_render_method = 'BLENDED'

    set_principled_emission(bsdf, emission_rgba, emission_strength)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

# Kiến trúc & Sàn
create_mat("Mat_WallWarmWhite", (0.95, 0.94, 0.91, 1.0), roughness=0.72)
create_mat("Mat_WallFacadeWarm", (0.89, 0.85, 0.79, 1.0), roughness=0.62)
create_mat("Mat_WallAccentSage", (0.72, 0.79, 0.74, 1.0), roughness=0.68)
create_mat("Mat_RoofCharcoal", (0.14, 0.17, 0.22, 1.0), roughness=0.50, metallic=0.15)
create_mat("Mat_DarkGreyStone", (0.22, 0.25, 0.30, 1.0), roughness=0.65)
create_mat("Mat_RoadAsphalt", (0.11, 0.13, 0.16, 1.0), roughness=0.88)
create_mat("Mat_FloorTileCream", (0.94, 0.92, 0.88, 1.0), roughness=0.20, metallic=0.05)
create_mat("Mat_AntiSlipWoodTile", (0.64, 0.44, 0.27, 1.0), roughness=0.38)
create_mat("Mat_AntiSlipPavers", (0.36, 0.39, 0.44, 1.0), roughness=0.78)
create_mat("Mat_StepStone", (0.75, 0.74, 0.70, 1.0), roughness=0.72)
create_mat("Mat_WhiteMarble", (0.97, 0.97, 0.98, 1.0), roughness=0.12, metallic=0.06)
create_mat("Mat_BacksplashTile", (0.86, 0.89, 0.90, 1.0), roughness=0.18)

# Gỗ
create_mat("Mat_WoodOakTable", (0.68, 0.47, 0.28, 1.0), roughness=0.30)
create_mat("Mat_WoodOakCabinet", (0.74, 0.55, 0.36, 1.0), roughness=0.34)
create_mat("Mat_WoodOakDark", (0.26, 0.15, 0.09, 1.0), roughness=0.35)
create_mat("Mat_WoodWalnutAltar", (0.22, 0.11, 0.06, 1.0), roughness=0.28)
create_mat("Mat_WoodLouverFacade", (0.70, 0.44, 0.22, 1.0), roughness=0.36)
create_mat("Mat_WoodStairTreads", (0.62, 0.41, 0.24, 1.0), roughness=0.32)
create_mat("Mat_TreeTrunk", (0.30, 0.20, 0.12, 1.0), roughness=0.85)
create_mat("Mat_SoilDark", (0.16, 0.11, 0.07, 1.0), roughness=0.95)

# Vải, Chăn gối, Thảm, Rèm
create_mat("Mat_FabricSofaWarm", (0.28, 0.32, 0.38, 1.0), roughness=0.84)
create_mat("Mat_FabricBeige", (0.82, 0.76, 0.68, 1.0), roughness=0.86)
create_mat("Mat_FabricTaupe", (0.62, 0.57, 0.52, 1.0), roughness=0.85)
create_mat("Mat_CushionMustard", (0.88, 0.64, 0.20, 1.0), roughness=0.80)
create_mat("Mat_CushionNavy", (0.15, 0.25, 0.44, 1.0), roughness=0.80)
create_mat("Mat_CushionTerracotta", (0.76, 0.35, 0.24, 1.0), roughness=0.82)
create_mat("Mat_CushionSage", (0.42, 0.58, 0.46, 1.0), roughness=0.82)
create_mat("Mat_CushionBlush", (0.84, 0.62, 0.64, 1.0), roughness=0.82)
create_mat("Mat_BeddingCream", (0.93, 0.90, 0.85, 1.0), roughness=0.85)
create_mat("Mat_BeddingWhite", (0.98, 0.98, 0.97, 1.0), roughness=0.85)
create_mat("Mat_RugWarm", (0.78, 0.73, 0.66, 1.0), roughness=0.92)
create_mat("Mat_RugPattern", (0.58, 0.62, 0.66, 1.0), roughness=0.92)
create_mat("Mat_CurtainSheer", (0.97, 0.96, 0.94, 0.65), roughness=0.75, alpha=0.68)
create_mat("Mat_CurtainLinen", (0.70, 0.66, 0.60, 1.0), roughness=0.88)

# Kính & Gương
create_mat("Mat_GlassClear", (0.84, 0.93, 0.98, 0.28), roughness=0.04, transmission=0.90, alpha=0.28)
create_mat("Mat_GlassBronze", (0.48, 0.60, 0.68, 0.40), roughness=0.08, transmission=0.78, alpha=0.40)
create_mat("Mat_BalconyGlassBronze", (0.42, 0.56, 0.64, 0.36), roughness=0.06, transmission=0.82, alpha=0.36)
create_mat("Mat_CanopyGlass", (0.38, 0.50, 0.60, 0.35), roughness=0.08, transmission=0.75, alpha=0.35)
create_mat("Mat_Mirror", (0.92, 0.95, 0.98, 1.0), roughness=0.02, metallic=0.96)

# Kim loại, Thiết bị, Nội thất đặc biệt
create_mat("Mat_PianoBlackGloss", (0.03, 0.03, 0.04, 1.0), roughness=0.05, metallic=0.25)
create_mat("Mat_TVScreenBlack", (0.05, 0.14, 0.30, 1.0), roughness=0.08, metallic=0.35,
           emission_rgba=(0.10, 0.26, 0.60, 1.0), emission_strength=1.4)
create_mat("Mat_LaptopScreen", (0.14, 0.36, 0.64, 1.0), roughness=0.10,
           emission_rgba=(0.25, 0.55, 0.95, 1.0), emission_strength=1.8)
create_mat("Mat_WarmLED", (1.0, 0.88, 0.60, 1.0), roughness=0.15,
           emission_rgba=(1.0, 0.82, 0.45, 1.0), emission_strength=6.5)
create_mat("Mat_WarmSconce", (1.0, 0.92, 0.72, 1.0), roughness=0.20,
           emission_rgba=(1.0, 0.86, 0.52, 1.0), emission_strength=7.5)
create_mat("Mat_LampShadeGlow", (0.98, 0.93, 0.80, 1.0), roughness=0.55,
           emission_rgba=(1.0, 0.84, 0.52, 1.0), emission_strength=2.8)
create_mat("Mat_SmartCyanLED", (0.22, 0.74, 0.97, 1.0), roughness=0.15,
           emission_rgba=(0.22, 0.74, 0.97, 1.0), emission_strength=5.5)
create_mat("Mat_SmartGreenLED", (0.06, 0.73, 0.50, 1.0), roughness=0.15,
           emission_rgba=(0.06, 0.73, 0.50, 1.0), emission_strength=5.0)
create_mat("Mat_SmartRedLED", (0.94, 0.26, 0.26, 1.0), roughness=0.15,
           emission_rgba=(0.94, 0.26, 0.26, 1.0), emission_strength=5.0)
create_mat("Mat_CameraFOV", (0.22, 0.74, 0.97, 0.14), roughness=0.2, transmission=0.85,
           emission_rgba=(0.22, 0.74, 0.97, 1.0), emission_strength=0.6, alpha=0.14)
create_mat("Mat_CalloutBoard", (0.06, 0.14, 0.30, 1.0), roughness=0.25, metallic=0.2,
           emission_rgba=(0.08, 0.20, 0.45, 1.0), emission_strength=1.4)
create_mat("Mat_CalloutText", (1.0, 1.0, 1.0, 1.0), roughness=0.1,
           emission_rgba=(1.0, 1.0, 1.0, 1.0), emission_strength=3.5)
create_mat("Mat_SolarPVPanels", (0.04, 0.10, 0.26, 1.0), roughness=0.14, metallic=0.65)
create_mat("Mat_CarWhite", (0.95, 0.96, 0.98, 1.0), roughness=0.14, metallic=0.70)
create_mat("Mat_TireRubber", (0.09, 0.09, 0.10, 1.0), roughness=0.88)
create_mat("Mat_MetalMatteBlack", (0.11, 0.11, 0.12, 1.0), roughness=0.35, metallic=0.75)
create_mat("Mat_MetalStainless", (0.72, 0.75, 0.78, 1.0), roughness=0.30, metallic=0.78)
create_mat("Mat_BrassGold", (0.88, 0.70, 0.28, 1.0), roughness=0.22, metallic=0.90)
create_mat("Mat_BuddhaGold", (0.96, 0.78, 0.24, 1.0), roughness=0.18, metallic=0.92)
create_mat("Mat_CeramicWhite", (0.96, 0.96, 0.97, 1.0), roughness=0.14)
create_mat("Mat_CeramicTeal", (0.18, 0.46, 0.50, 1.0), roughness=0.18)
create_mat("Mat_TerracottaPot", (0.68, 0.36, 0.22, 1.0), roughness=0.68)

# Cây xanh, Hoa, Tranh ảnh & Sách
create_mat("Mat_GrassGreen", (0.16, 0.46, 0.22, 1.0), roughness=0.86)
create_mat("Mat_FoliageGreen", (0.15, 0.50, 0.21, 1.0), roughness=0.58)
create_mat("Mat_FoliageBright", (0.24, 0.62, 0.26, 1.0), roughness=0.55)
create_mat("Mat_FlowerPink", (0.92, 0.46, 0.58, 1.0), roughness=0.45)
create_mat("Mat_FlowerYellow", (0.96, 0.80, 0.22, 1.0), roughness=0.45)
create_mat("Mat_ArtCanvasWarm", (0.88, 0.74, 0.52, 1.0), roughness=0.75)
create_mat("Mat_ArtCanvasBlue", (0.28, 0.48, 0.66, 1.0), roughness=0.75)
create_mat("Mat_ArtCanvasGreen", (0.36, 0.56, 0.42, 1.0), roughness=0.75)
create_mat("Mat_BookRed", (0.68, 0.20, 0.22, 1.0), roughness=0.65)
create_mat("Mat_BookBlue", (0.18, 0.34, 0.58, 1.0), roughness=0.65)
create_mat("Mat_BookGreen", (0.20, 0.48, 0.34, 1.0), roughness=0.65)
create_mat("Mat_BookAmber", (0.82, 0.58, 0.22, 1.0), roughness=0.65)
create_mat("Mat_WaterClear", (0.55, 0.82, 0.92, 0.45), roughness=0.05, transmission=0.85, alpha=0.45)

# ---------------------------------------------------------------------------
# 3. PRIMITIVES & COMPOSITE FURNITURE HELPERS (SCALED BY SCALE_FACTOR)
# ---------------------------------------------------------------------------
S = SCALE_FACTOR

def link_mesh_obj(collection, name, bm, mat_name, loc=(0, 0, 0), rot=(0, 0, 0), smooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    obj = bpy.data.objects.new(name, me)
    obj.location = (loc[0] * S, loc[1] * S, loc[2] * S)
    obj.rotation_euler = rot
    if mat_name and mat_name in bpy.data.materials:
        obj.data.materials.append(bpy.data.materials[mat_name])
    collection.objects.link(obj)
    return obj

def add_box(collection, name, min_x, min_y, min_z, max_x, max_y, max_z,
            mat_name=None, bevel=0.0, rot_z=0.0, rot=(0, 0, 0)):
    dx = max(max_x - min_x, 0.002) * S
    dy = max(max_y - min_y, 0.002) * S
    dz = max(max_z - min_z, 0.002) * S
    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0
    cz = (min_z + max_z) / 2.0

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(dx, dy, dz), verts=bm.verts)
    b_scaled = bevel * S
    if b_scaled > 0.001 and min(dx, dy, dz) > b_scaled * 2.1:
        bmesh.ops.bevel(
            bm, geom=bm.edges[:],
            offset=min(b_scaled, min(dx, dy, dz) * 0.42),
            segments=2, profile=0.5, affect='EDGES'
        )
    final_rot = rot if rot != (0, 0, 0) else (0, 0, rot_z)
    return link_mesh_obj(collection, name, bm, mat_name, loc=(cx, cy, cz), rot=final_rot)

def add_cyl(collection, name, cx, cy, z_bottom, z_top, r1, r2=None,
            mat_name=None, segs=20, rot=(0, 0, 0), smooth=True):
    r2 = r1 if r2 is None else r2
    dz = max(z_top - z_bottom, 0.002) * S
    cz = (z_bottom + z_top) / 2.0
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=segs,
        radius1=r1 * S, radius2=r2 * S, depth=dz
    )
    return link_mesh_obj(collection, name, bm, mat_name, loc=(cx, cy, cz), rot=rot, smooth=smooth)

def add_sphere(collection, name, cx, cy, cz, r, mat_name=None, sx=1.0, sy=1.0, sz=1.0, subdiv=2):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=r * S)
    if sx != 1.0 or sy != 1.0 or sz != 1.0:
        bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    return link_mesh_obj(collection, name, bm, mat_name, loc=(cx, cy, cz), smooth=True)

# --- Composite Decor & Furniture Builders ---

def add_potted_plant(col, prefix, cx, cy, z0, scale=1.0, pot_mat="Mat_TerracottaPot", leaf_mat="Mat_FoliageGreen"):
    r_pot = 0.16 * scale
    h_pot = 0.28 * scale
    add_cyl(col, f"{prefix}_Pot", cx, cy, z0, z0 + h_pot, r_pot * 0.78, r_pot, pot_mat, segs=16)
    add_cyl(col, f"{prefix}_Soil", cx, cy, z0 + h_pot - 0.03 * scale, z0 + h_pot + 0.005, r_pot * 0.88, r_pot * 0.88, "Mat_SoilDark", segs=12)
    add_cyl(col, f"{prefix}_Stem", cx, cy, z0 + h_pot, z0 + h_pot + 0.42 * scale, 0.022 * scale, 0.014 * scale, "Mat_TreeTrunk", segs=8)
    offsets = [
        (0.0, 0.0, 0.56, 0.20, 1.0, 1.0, 0.85),
        (0.11, 0.08, 0.42, 0.15, 1.1, 0.9, 0.8),
        (-0.10, -0.09, 0.46, 0.15, 0.9, 1.1, 0.8),
        (-0.09, 0.10, 0.36, 0.13, 1.0, 1.0, 0.8),
        (0.09, -0.10, 0.38, 0.13, 1.0, 1.0, 0.8),
    ]
    for idx, (ox, oy, oz, rad, sx, sy, sz) in enumerate(offsets):
        m = leaf_mat if idx % 2 == 0 else "Mat_FoliageBright"
        add_sphere(col, f"{prefix}_Leaf_{idx}", cx + ox * scale, cy + oy * scale, z0 + h_pot + oz * scale, rad * scale, m, sx, sy, sz)

def add_table_lamp(col, prefix, cx, cy, z0, scale=1.0):
    add_cyl(col, f"{prefix}_Base", cx, cy, z0, z0 + 0.04 * scale, 0.08 * scale, 0.06 * scale, "Mat_BrassGold", segs=14)
    add_cyl(col, f"{prefix}_Stem", cx, cy, z0 + 0.04 * scale, z0 + 0.24 * scale, 0.015 * scale, 0.012 * scale, "Mat_BrassGold", segs=10)
    add_cyl(col, f"{prefix}_Shade", cx, cy, z0 + 0.20 * scale, z0 + 0.38 * scale, 0.12 * scale, 0.085 * scale, "Mat_LampShadeGlow", segs=16)

def add_framed_art(col, prefix, x, y, z, w, h, wall_axis='X', canvas_mat="Mat_ArtCanvasWarm", frame_mat="Mat_WoodOakDark"):
    """wall_axis='X' means hanging on a wall parallel to YZ (constant X); 'Y' means constant Y."""
    t = 0.03
    if wall_axis == 'X':
        add_box(col, f"{prefix}_Frame", x - t/2, y - w/2, z - h/2, x + t/2, y + w/2, z + h/2, frame_mat, bevel=0.004)
        add_box(col, f"{prefix}_Canvas", x - t*0.65, y - w/2 + 0.04, z - h/2 + 0.04, x + t*0.65, y + w/2 - 0.04, z + h/2 - 0.04, canvas_mat)
    else:
        add_box(col, f"{prefix}_Frame", x - w/2, y - t/2, z - h/2, x + w/2, y + t/2, z + h/2, frame_mat, bevel=0.004)
        add_box(col, f"{prefix}_Canvas", x - w/2 + 0.04, y - t*0.65, z - h/2 + 0.04, x + w/2 - 0.04, y + t*0.65, z + h/2 - 0.04, canvas_mat)

def add_dining_chair(col, prefix, cx, cy, z0, angle_rad, seat_mat="Mat_FabricBeige", wood_mat="Mat_WoodOakTable"):
    # Local chair centered at (cx, cy), facing +Y when angle_rad=0
    ca, sa = math.cos(angle_rad), math.sin(angle_rad)
    def rot_pt(lx, ly):
        return cx + lx * ca - ly * sa, cy + lx * sa + ly * ca

    # 4 chân ghế
    for i, (lx, ly) in enumerate([(-0.18, -0.18), (0.18, -0.18), (-0.18, 0.18), (0.18, 0.18)]):
        px, py = rot_pt(lx, ly)
        add_cyl(col, f"{prefix}_Leg{i}", px, py, z0, z0 + 0.44, 0.020, 0.024, wood_mat, segs=8)
    # Mặt đệm ghế
    add_box(col, f"{prefix}_Seat", cx - 0.22, cy - 0.21, z0 + 0.43, cx + 0.22, cy + 0.21, z0 + 0.49, seat_mat, bevel=0.015, rot_z=angle_rad)
    # Tựa lưng (nằm ở ly = -0.19)
    bx, by = rot_pt(0.0, -0.19)
    add_box(col, f"{prefix}_Back", bx - 0.21, by - 0.025, z0 + 0.56, bx + 0.21, by + 0.025, z0 + 0.84, wood_mat, bevel=0.012, rot_z=angle_rad)
    for j, lx in enumerate([-0.17, 0.17]):
        px, py = rot_pt(lx, -0.19)
        add_cyl(col, f"{prefix}_Post{j}", px, py, z0 + 0.46, z0 + 0.82, 0.018, 0.016, wood_mat, segs=8)

def add_pendant_chandelier(col, prefix, cx, cy, z_ceil, drop=0.85, count=3):
    add_cyl(col, f"{prefix}_Canopy", cx, cy, z_ceil - 0.05, z_ceil, 0.18, 0.18, "Mat_BrassGold", segs=16)
    offsets = [(0, 0, 0)] if count == 1 else [(-0.22, -0.10, 0.0), (0.22, -0.10, -0.12), (0.0, 0.20, 0.08)]
    for i, (ox, oy, dz) in enumerate(offsets[:count]):
        bz = z_ceil - drop + dz
        add_cyl(col, f"{prefix}_Cord{i}", cx + ox, cy + oy, bz + 0.08, z_ceil - 0.05, 0.008, 0.008, "Mat_MetalMatteBlack", segs=6)
        add_sphere(col, f"{prefix}_Bulb{i}", cx + ox, cy + oy, bz, 0.10, "Mat_LampShadeGlow")

def add_books_row(col, prefix, x0, y0, z0, count=6, axis='Y'):
    mats = ["Mat_BookRed", "Mat_BookBlue", "Mat_BookGreen", "Mat_BookAmber", "Mat_CeramicWhite"]
    for i in range(count):
        h = 0.20 + (i % 3) * 0.03
        m = mats[i % len(mats)]
        if axis == 'Y':
            add_box(col, f"{prefix}_{i}", x0, y0 + i * 0.045, z0, x0 + 0.18, y0 + i * 0.045 + 0.036, z0 + h, m, bevel=0.003)
        else:
            add_box(col, f"{prefix}_{i}", x0 + i * 0.045, y0, z0, x0 + i * 0.045 + 0.036, y0 + 0.18, z0 + h, m, bevel=0.003)

def add_window_frame(col, prefix, x1, y1, z1, x2, y2, z2, glass_mat="Mat_GlassClear", frame_t=0.05):
    add_box(col, f"{prefix}_Glass", x1, y1, z1, x2, y2, z2, glass_mat)
    # Khung nhôm đen xung quanh
    add_box(col, f"{prefix}_Top", x1, y1, z2 - frame_t, x2, y2, z2 + 0.01, "Mat_MetalMatteBlack")
    add_box(col, f"{prefix}_Bot", x1, y1, z1 - 0.01, x2, y2, z1 + frame_t, "Mat_MetalMatteBlack")
    if (x2 - x1) > (y2 - y1):
        add_box(col, f"{prefix}_L", x1, y1, z1, x1 + frame_t, y2, z2, "Mat_MetalMatteBlack")
        add_box(col, f"{prefix}_R", x2 - frame_t, y1, z1, x2, y2, z2, "Mat_MetalMatteBlack")
        mx = (x1 + x2) / 2.0
        add_box(col, f"{prefix}_Mid", mx - frame_t * 0.4, y1, z1, mx + frame_t * 0.4, y2, z2, "Mat_MetalMatteBlack")
    else:
        add_box(col, f"{prefix}_L", x1, y1, z1, x2, y1 + frame_t, z2, "Mat_MetalMatteBlack")
        add_box(col, f"{prefix}_R", x1, y2 - frame_t, z1, x2, y2, z2, "Mat_MetalMatteBlack")
        my = (y1 + y2) / 2.0
        add_box(col, f"{prefix}_Mid", x1, my - frame_t * 0.4, z1, x2, my + frame_t * 0.4, z2, "Mat_MetalMatteBlack")

def add_curtain_pair(col, prefix, x1, x2, y_pos, z_bot, z_top):
    # Thanh treo rèm + 2 dải rèm bên trái/phải
    add_cyl(col, f"{prefix}_Rod", (x1 + x2) / 2, y_pos, z_top, z_top + 0.03, 0.015, 0.015, "Mat_MetalMatteBlack",
            rot=(0, math.pi / 2, 0), segs=10)
    add_box(col, f"{prefix}_RodBar", x1 - 0.15, y_pos - 0.015, z_top, x2 + 0.15, y_pos + 0.015, z_top + 0.025, "Mat_MetalMatteBlack")
    for side, sx in [("L", x1), ("R", x2 - 0.34)]:
        for f in range(4):
            fx = sx + f * 0.085
            add_box(col, f"{prefix}_{side}_{f}", fx, y_pos - 0.03 - (f % 2) * 0.03, z_bot,
                    fx + 0.07, y_pos + 0.04, z_top, "Mat_CurtainLinen", bevel=0.01)
    # Lớp rèm voan mỏng ở giữa
    add_box(col, f"{prefix}_Sheer", x1 + 0.32, y_pos - 0.01, z_bot + 0.02, x2 - 0.32, y_pos + 0.01, z_top - 0.02, "Mat_CurtainSheer")

def add_detailed_bed(col, prefix, x1, y1, z0, x2, y2, head_side='X_MAX', duvet_mat="Mat_CushionNavy", pillow_mat="Mat_BeddingWhite"):
    # Khung giường gỗ & chân
    add_box(col, f"{prefix}_Frame", x1, y1, z0 + 0.10, x2, y2, z0 + 0.28, "Mat_WoodOakTable", bevel=0.015)
    for i, (lx, ly) in enumerate([(x1 + 0.08, y1 + 0.08), (x2 - 0.08, y1 + 0.08), (x1 + 0.08, y2 - 0.08), (x2 - 0.08, y2 - 0.08)]):
        add_cyl(col, f"{prefix}_Leg{i}", lx, ly, z0, z0 + 0.11, 0.035, 0.035, "Mat_WoodOakDark", segs=10)
    # Nệm trắng kem
    add_box(col, f"{prefix}_Mattress", x1 + 0.04, y1 + 0.04, z0 + 0.28, x2 - 0.04, y2 - 0.04, z0 + 0.54, "Mat_BeddingCream", bevel=0.04)

    if head_side == 'X_MAX':
        # Đầu giường phía X_MAX
        add_box(col, f"{prefix}_Headboard", x2 - 0.08, y1 - 0.04, z0 + 0.20, x2 + 0.02, y2 + 0.04, z0 + 1.18, "Mat_FabricTaupe", bevel=0.03)
        # Chăn gấp phủ 2/3 giường phía X_MIN
        add_box(col, f"{prefix}_Duvet", x1 + 0.02, y1 + 0.02, z0 + 0.42, x1 + (x2 - x1) * 0.66, y2 - 0.02, z0 + 0.61, duvet_mat, bevel=0.035)
        # 2 gối nằm + 2 gối trang trí
        my = (y1 + y2) / 2.0
        for i, py in enumerate([my - 0.36, my + 0.36]):
            add_box(col, f"{prefix}_Pillow{i}", x2 - 0.50, py - 0.28, z0 + 0.54, x2 - 0.14, py + 0.28, z0 + 0.70, pillow_mat, bevel=0.05)
            add_box(col, f"{prefix}_AccentPillow{i}", x2 - 0.66, py - 0.18, z0 + 0.54, x2 - 0.48, py + 0.18, z0 + 0.72, "Mat_CushionMustard", bevel=0.04)
    elif head_side == 'Y_MAX':
        add_box(col, f"{prefix}_Headboard", x1 - 0.04, y2 - 0.08, z0 + 0.20, x2 + 0.04, y2 + 0.02, z0 + 1.24, "Mat_FabricTaupe", bevel=0.03)
        add_box(col, f"{prefix}_Duvet", x1 + 0.02, y1 + 0.02, z0 + 0.42, x2 - 0.02, y1 + (y2 - y1) * 0.66, z0 + 0.61, duvet_mat, bevel=0.035)
        mx = (x1 + x2) / 2.0
        for i, px in enumerate([mx - 0.42, mx + 0.42]):
            add_box(col, f"{prefix}_Pillow{i}", px - 0.30, y2 - 0.50, z0 + 0.54, px + 0.30, y2 - 0.14, z0 + 0.71, pillow_mat, bevel=0.05)
            add_box(col, f"{prefix}_AccentPillow{i}", px - 0.20, y2 - 0.66, z0 + 0.54, px + 0.20, y2 - 0.48, z0 + 0.73, "Mat_CushionTerracotta", bevel=0.04)

def add_nightstand(col, prefix, cx, cy, z0):
    add_box(col, f"{prefix}_Body", cx - 0.22, cy - 0.20, z0 + 0.08, cx + 0.22, cy + 0.20, z0 + 0.48, "Mat_WoodOakCabinet", bevel=0.012)
    add_box(col, f"{prefix}_Drawer", cx - 0.23, cy - 0.17, z0 + 0.28, cx + 0.23, cy + 0.17, z0 + 0.44, "Mat_WoodOakTable", bevel=0.008)
    for i, (ox, oy) in enumerate([(-0.18, -0.16), (0.18, -0.16), (-0.18, 0.16), (0.18, 0.16)]):
        add_cyl(col, f"{prefix}_Leg{i}", cx + ox, cy + oy, z0, z0 + 0.09, 0.018, 0.018, "Mat_MetalMatteBlack", segs=8)
    add_table_lamp(col, f"{prefix}_Lamp", cx, cy, z0 + 0.48, scale=0.9)

def add_wardrobe(col, prefix, x1, y1, z0, x2, y2, h=2.45, door_face='X_MAX'):
    add_box(col, f"{prefix}_Carcass", x1, y1, z0, x2, y2, z0 + h, "Mat_WoodOakCabinet", bevel=0.01)
    if door_face == 'X_MAX':
        n_doors = max(2, int((y2 - y1) / 0.55))
        dy = (y2 - y1) / n_doors
        for d in range(n_doors):
            dy1 = y1 + d * dy + 0.015
            dy2 = y1 + (d + 1) * dy - 0.015
            add_box(col, f"{prefix}_Door{d}", x2 - 0.01, dy1, z0 + 0.05, x2 + 0.025, dy2, z0 + h - 0.04, "Mat_WallFacadeWarm", bevel=0.006)
            hy = dy1 + 0.06 if d % 2 == 1 else dy2 - 0.06
            add_box(col, f"{prefix}_Handle{d}", x2 + 0.025, hy - 0.01, z0 + 0.95, x2 + 0.055, hy + 0.01, z0 + 1.45, "Mat_BrassGold", bevel=0.004)
    else:
        n_doors = max(2, int((x2 - x1) / 0.52))
        dx = (x2 - x1) / n_doors
        face_y = y1 - 0.015 if door_face == 'Y_MIN' else y2 + 0.015
        h_y = y1 - 0.04 if door_face == 'Y_MIN' else y2 + 0.04
        for d in range(n_doors):
            dx1 = x1 + d * dx + 0.015
            dx2 = x1 + (d + 1) * dx - 0.015
            add_box(col, f"{prefix}_Door{d}", dx1, face_y - 0.012, z0 + 0.05, dx2, face_y + 0.012, z0 + h - 0.04, "Mat_WallFacadeWarm", bevel=0.006)
            hx = dx1 + 0.06 if d % 2 == 1 else dx2 - 0.06
            add_box(col, f"{prefix}_Handle{d}", hx - 0.01, h_y - 0.012, z0 + 0.95, hx + 0.01, h_y + 0.012, z0 + 1.45, "Mat_BrassGold", bevel=0.004)

def add_study_desk_set(col, prefix, x1, y1, z0, x2, y2, chair_side='Y_MIN'):
    # Mặt bàn & 4 chân
    add_box(col, f"{prefix}_Top", x1, y1, z0 + 0.72, x2, y2, z0 + 0.76, "Mat_WoodOakTable", bevel=0.01)
    for i, (lx, ly) in enumerate([(x1 + 0.06, y1 + 0.06), (x2 - 0.06, y1 + 0.06), (x1 + 0.06, y2 - 0.06), (x2 - 0.06, y2 - 0.06)]):
        add_box(col, f"{prefix}_Leg{i}", lx - 0.025, ly - 0.025, z0, lx + 0.025, ly + 0.025, z0 + 0.72, "Mat_MetalMatteBlack")
    # Hộc tủ bàn
    add_box(col, f"{prefix}_Drawer", x1 + 0.04, y1 + 0.06, z0 + 0.12, x1 + 0.42, y2 - 0.06, z0 + 0.71, "Mat_WoodOakCabinet", bevel=0.008)
    # Laptop & đèn học & cây mini
    mx, my = (x1 + x2) / 2.0 + 0.12, (y1 + y2) / 2.0
    add_box(col, f"{prefix}_LaptopBase", mx - 0.18, my - 0.12, z0 + 0.76, mx + 0.18, my + 0.12, z0 + 0.78, "Mat_MetalStainless")
    if chair_side == 'Y_MIN':
        add_box(col, f"{prefix}_LaptopScr", mx - 0.18, my + 0.10, z0 + 0.78, mx + 0.18, my + 0.13, z0 + 1.03, "Mat_LaptopScreen")
        add_dining_chair(col, f"{prefix}_Chair", mx, y1 - 0.34, z0, 0.0, "Mat_CushionSage", "Mat_WoodOakTable")
    else:
        add_box(col, f"{prefix}_LaptopScr", mx - 0.18, my - 0.13, z0 + 0.78, mx + 0.18, my - 0.10, z0 + 1.03, "Mat_LaptopScreen")
        add_dining_chair(col, f"{prefix}_Chair", mx, y2 + 0.34, z0, math.pi, "Mat_CushionBlush", "Mat_WoodOakTable")
    add_table_lamp(col, f"{prefix}_Lamp", x1 + 0.22, my, z0 + 0.76, scale=0.72)
    add_potted_plant(col, f"{prefix}_MiniPlant", x2 - 0.14, my, z0 + 0.76, scale=0.35, pot_mat="Mat_CeramicWhite")

# ---------------------------------------------------------------------------
# 4. SITE & SÂN TRƯỚC 18M: MÁI CHE 9M, BÀN TRÀ CỦA BA, SUV & CẢNH QUAN
# ---------------------------------------------------------------------------
add_box(col_site, "Site_FrontRoad", -4.0, -24.0, -0.35, 11.0, -18.8, -0.20, "Mat_RoadAsphalt")
add_box(col_site, "Site_Sidewalk", -2.0, -18.8, -0.20, 9.0, -18.0, 0.0, "Mat_WallFacadeWarm")
add_box(col_site, "Site_ArchitecturalBasePlinth", -0.5, -18.5, -0.45, 7.5, 24.5, -0.01, "Mat_RoofCharcoal")
add_box(col_site, "Site_FrontYard_Slab", 0.0, -18.0, 0.0, 7.0, 0.0, 0.15, "Mat_AntiSlipPavers")

# Trụ cổng đá chẻ & Cổng sắt
add_box(col_site, "Gate_Pillar_L", -0.18, -18.18, 0.0, 0.35, -17.82, 2.65, "Mat_DarkGreyStone")
add_box(col_site, "Gate_Pillar_M", 3.85, -18.18, 0.0, 4.15, -17.82, 2.65, "Mat_DarkGreyStone")
add_box(col_site, "Gate_Pillar_R", 6.85, -18.18, 0.0, 7.18, -17.82, 2.65, "Mat_DarkGreyStone")
# Đèn trụ cổng
for gi, gx in enumerate([0.08, 4.0, 7.0]):
    add_box(col_lights, f"Gate_Lamp_{gi}", gx - 0.11, -18.10, 2.65, gx + 0.11, -17.90, 2.88, "Mat_WarmSconce", bevel=0.01)

add_box(col_site, "MainCarGate_3m6", 0.35, -18.0, 0.18, 3.85, -17.94, 2.25, "Mat_MetalMatteBlack")
add_box(col_site, "SideGate_2m", 4.15, -18.0, 0.18, 6.85, -17.94, 2.25, "Mat_MetalMatteBlack")

# Hàng rào: Tách tường rào trái chừa khoảng Y=0..16 để mở góc cắt nhìn rõ nội thất Tầng 1!
add_box(col_site, "Fence_Left_Front", -0.18, -18.0, 0.0, 0.0, 0.0, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Left_Rear", -0.18, 16.0, 0.0, 0.0, 24.0, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Right", 7.0, -18.0, 0.0, 7.18, 24.0, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Rear", -0.18, 24.0, 0.0, 7.18, 24.18, 2.35, "Mat_WallWarmWhite")

# Mái che sân trước Tầng 1 nối LIỀN MẠCH với mép trước Ban công Tầng 2 (Y = -9.0..-3.0, rộng trọn 7m, cùng cao độ dầm sàn Z=3.55..3.75)
for cy in [-8.94, -6.00]:
    for cx in [0.08, 6.92]:
        add_box(col_site, f"Canopy_Col_{cx:.1f}_{cy:.1f}", cx - 0.08, cy - 0.08, 0.15, cx + 0.08, cy + 0.08, 3.56, "Mat_RoofCharcoal", bevel=0.01)
# Dầm viền 2 bên & dầm mặt trước nối liền khít vào dầm Ban công Tầng 2 (BalconyFront_EdgeBeam ở Y=-3.0, Z=3.57..3.71)
add_box(col_site, "Canopy_Beam_L", 0.0, -9.02, 3.55, 0.18, -2.98, 3.72, "Mat_RoofCharcoal")
add_box(col_site, "Canopy_Beam_R", 6.82, -9.02, 3.55, 7.02, -2.98, 3.72, "Mat_RoofCharcoal")
add_box(col_site, "Canopy_Beam_Front", 0.0, -9.02, 3.55, 7.02, -8.84, 3.72, "Mat_RoofCharcoal")
for p_idx, py in enumerate([-7.5, -6.0, -4.5]):
    add_box(col_site, f"Canopy_Rafter_{p_idx}", 0.16, py - 0.05, 3.60, 6.84, py + 0.05, 3.70, "Mat_MetalMatteBlack")
    add_box(col_lights, f"Canopy_LEDStrip_{p_idx}", 0.60, py - 0.02, 3.56, 6.40, py + 0.02, 3.60, "Mat_WarmLED")
# Thanh giằng dọc chia ô kính gọn đẹp
add_box(col_site, "Canopy_MidPurlin_1", 2.30, -8.86, 3.61, 2.38, -2.98, 3.70, "Mat_MetalMatteBlack")
add_box(col_site, "Canopy_MidPurlin_2", 4.62, -8.86, 3.61, 4.70, -2.98, 3.70, "Mat_MetalMatteBlack")
# Tấm mái kính cường lực nối khít sát mép sàn Ban công Tầng 2 (Y = -8.98..-2.98, Z = 3.70..3.75)
add_box(col_site, "Canopy_GlassRoof_Flush", 0.06, -8.98, 3.70, 6.94, -2.98, 3.75, "Mat_CanopyGlass")
# Thêm dải đèn LED âm trần dưới gầm Ban công trước Tầng 2 (Y = -1.5) chiếu sáng khu bàn trà của Ba
add_box(col_lights, "BalconyUnder_LED_Mid", 0.60, -1.52, 3.66, 6.40, -1.48, 3.70, "Mat_WarmLED")

# 🍵 BÀN TRÀ CỦA BA ÁP VÁCH TƯỜNG TRÁI (CHI TIẾT ĐẦY ĐỦ)
add_box(col_site, "DadTea_Rug", 0.05, -5.0, 0.15, 2.20, -2.1, 0.17, "Mat_AntiSlipWoodTile")
add_box(col_site, "DadTea_Bench_Base", 0.08, -4.8, 0.17, 0.62, -2.3, 0.56, "Mat_WoodOakTable", bevel=0.015)
add_box(col_site, "DadTea_Bench_Back", 0.02, -4.8, 0.56, 0.12, -2.3, 1.10, "Mat_WoodLouverFacade")
add_box(col_site, "DadTea_Bench_Cushion", 0.13, -4.75, 0.56, 0.58, -2.35, 0.64, "Mat_CushionMustard", bevel=0.02)
for ti, ty in enumerate([-4.35, -3.55, -2.75]):
    add_box(col_site, f"DadTea_Pillow_{ti}", 0.13, ty - 0.22, 0.64, 0.28, ty + 0.22, 0.94,
            "Mat_CushionNavy" if ti % 2 == 0 else "Mat_BeddingCream", bevel=0.04)
add_box(col_site, "DadTea_Table_Top", 0.78, -4.45, 0.68, 1.38, -2.65, 0.74, "Mat_WhiteMarble", bevel=0.015)
for i, (lx, ly) in enumerate([(0.85, -4.35), (1.30, -4.35), (0.85, -2.75), (1.30, -2.75)]):
    add_cyl(col_site, f"DadTea_Leg_{i}", lx, ly, 0.17, 0.68, 0.03, 0.03, "Mat_MetalMatteBlack", segs=10)
# Khay trà + Ấm + 4 Chén + Chậu bonsai nhỏ
add_box(col_site, "DadTea_Tray", 0.90, -3.95, 0.74, 1.26, -3.25, 0.77, "Mat_WoodWalnutAltar", bevel=0.005)
add_sphere(col_site, "DadTea_Teapot", 1.08, -3.60, 0.83, 0.075, "Mat_CeramicTeal", sx=1.0, sy=1.0, sz=0.8)
for ci, (cx_c, cy_c) in enumerate([(0.97, -3.40), (1.18, -3.40), (0.97, -3.80), (1.18, -3.80)]):
    add_cyl(col_site, f"DadTea_Cup_{ci}", cx_c, cy_c, 0.77, 0.82, 0.025, 0.030, "Mat_CeramicWhite", segs=12)
add_potted_plant(col_site, "DadTea_MiniBonsai", 1.08, -2.95, 0.74, scale=0.38, pot_mat="Mat_CeramicTeal")
# 2 ghế đôn gỗ đối diện
for si, sy in enumerate([-4.05, -3.05]):
    add_cyl(col_site, f"DadTea_Stool_{si}", 1.72, sy, 0.17, 0.56, 0.18, 0.18, "Mat_WoodOakTable", segs=16)
    add_cyl(col_site, f"DadTea_StoolPad_{si}", 1.72, sy, 0.56, 0.61, 0.16, 0.16, "Mat_CushionMustard", segs=16)
add_box(col_lights, "DadTea_WallLamp", 0.02, -3.65, 1.70, 0.10, -3.45, 1.92, "Mat_WarmSconce")
add_potted_plant(col_site, "DadTea_CornerPlant", 0.45, -1.85, 0.15, scale=1.15, pot_mat="Mat_DarkGreyStone")

# 🚗 Xe ô tô SUV 7 chỗ chi tiết hơn (bánh xe, đèn pha/hậu, gương)
add_box(col_site, "Family_SUV_Chassis", 0.90, -14.6, 0.34, 2.80, -10.1, 0.92, "Mat_CarWhite", bevel=0.10)
add_box(col_site, "Family_SUV_Cabin", 1.02, -13.4, 0.92, 2.68, -10.7, 1.62, "Mat_CarWhite", bevel=0.10)
add_box(col_site, "Family_SUV_Windshield", 1.06, -13.45, 0.96, 2.64, -12.7, 1.56, "Mat_GlassBronze")
add_box(col_site, "Family_SUV_SideWin", 0.99, -13.1, 0.98, 2.71, -10.9, 1.52, "Mat_GlassBronze")
add_box(col_lights, "Family_SUV_Headlights", 1.02, -14.63, 0.60, 2.68, -14.57, 0.74, "Mat_WarmSconce")
add_box(col_lights, "Family_SUV_Taillights", 1.02, -10.12, 0.62, 2.68, -10.06, 0.75, "Mat_SmartRedLED")
for wi, (wx, wy) in enumerate([(0.92, -13.6), (2.78, -13.6), (0.92, -11.1), (2.78, -11.1)]):
    add_cyl(col_site, f"Family_SUV_Wheel_{wi}", wx, wy, 0.15, 0.85, 0.34, 0.34, "Mat_TireRubber",
            rot=(0, math.pi / 2, 0), segs=18)
    add_cyl(col_site, f"Family_SUV_Rim_{wi}", wx + (-0.04 if wx < 1.5 else 0.04), wy, 0.28, 0.72, 0.20, 0.20, "Mat_MetalStainless",
            rot=(0, math.pi / 2, 0), segs=14)

# 🌳 Bonsai & Cây cảnh bên phải sân + Đèn nấm lối đi
for bi, by in enumerate([-16.2, -12.5, -8.8, -5.0, -1.6]):
    add_box(col_site, f"Bonsai_Planter_{bi}", 5.55, by - 0.38, 0.15, 6.45, by + 0.38, 0.58, "Mat_DarkGreyStone", bevel=0.02)
    add_box(col_site, f"Bonsai_Soil_{bi}", 5.62, by - 0.32, 0.55, 6.38, by + 0.32, 0.60, "Mat_SoilDark")
    add_cyl(col_site, f"Bonsai_Trunk_{bi}", 6.0, by, 0.58, 1.15, 0.09, 0.06, "Mat_TreeTrunk", segs=10)
    add_sphere(col_site, f"Bonsai_Canopy1_{bi}", 6.0, by, 1.38, 0.42, "Mat_FoliageGreen", 1.2, 1.1, 0.72)
    add_sphere(col_site, f"Bonsai_Canopy2_{bi}", 5.75, by + 0.22, 1.18, 0.28, "Mat_FoliageBright", 1.1, 1.0, 0.75)
    add_sphere(col_site, f"Bonsai_Canopy3_{bi}", 6.24, by - 0.20, 1.22, 0.26, "Mat_FoliageGreen", 1.0, 1.1, 0.72)
    add_cyl(col_lights, f"Garden_Bollard_{bi}", 5.25, by, 0.15, 0.65, 0.06, 0.06, "Mat_MetalMatteBlack", segs=10)
    add_cyl(col_lights, f"Garden_BollardGlow_{bi}", 5.25, by, 0.52, 0.62, 0.065, 0.065, "Mat_WarmSconce", segs=10)

# Đường luồng 2m bên hông có đá bước dặm & cỏ xanh
add_box(col_site, "Corridor_2m_Grass", 5.0, 0.0, 0.0, 7.0, 16.0, 0.14, "Mat_GrassGreen")
for si in range(16):
    sy = 0.5 + si * 0.98
    add_box(col_site, f"StepStone_{si}", 5.45, sy - 0.26, 0.14, 6.55, sy + 0.26, 0.19, "Mat_StepStone", bevel=0.015)

# ---------------------------------------------------------------------------
# 5. TẦNG 1: PHÒNG KHÁCH, PHÒNG BA MẸ, CẦU THANG CHỮ U 2 VẾ & BẾP MỞ
# ---------------------------------------------------------------------------
Z1 = 0.25
H1 = 3.70
add_box(col_fl1_arch, "Floor1_Slab", 0.0, 0.0, 0.10, 5.0, 16.0, Z1, "Mat_FloorTileCream")

# Tường bao Tầng 1 (Tường trái cắt thấp 0.38m để nhìn xuyên toàn bộ nội thất)
add_box(col_fl1_arch, "Fl1_Wall_Left_Cutaway", 0.0, 0.0, Z1, 0.22, 16.0, Z1 + 0.38, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Right", 4.78, 0.0, Z1, 5.0, 16.0, H1, "Mat_WallWarmWhite")
# Tường mặt tiền có khung cửa chính & cửa sổ lớn
add_box(col_fl1_arch, "Fl1_Wall_Front_L", 0.0, 0.0, Z1, 0.45, 0.22, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Front_Mid", 2.25, 0.0, Z1, 2.85, 0.22, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Front_R", 4.55, 0.0, Z1, 5.0, 0.22, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Front_WinBot", 0.45, 0.0, Z1, 2.25, 0.22, 0.95, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Front_Top", 0.45, 0.0, 2.80, 4.55, 0.22, H1, "Mat_WallWarmWhite")
add_window_frame(col_fl1_arch, "Fl1_Front_MainDoor", 2.85, 0.06, Z1, 4.55, 0.18, 2.80)
add_window_frame(col_fl1_arch, "Fl1_Front_Window", 0.45, 0.06, 0.95, 2.25, 0.18, 2.80)

# Tường sau có cửa kính lớn ra sân sau
add_box(col_fl1_arch, "Fl1_Wall_Rear_L", 0.0, 15.78, Z1, 2.40, 16.0, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Rear_R", 4.20, 15.78, Z1, 5.0, 16.0, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Rear_Top", 2.40, 15.78, Z1 + 2.60, 4.20, 16.0, H1, "Mat_WallWarmWhite")
add_window_frame(col_fl1_arch, "Fl1_RearDoor", 2.40, 15.80, Z1, 4.20, 15.94, Z1 + 2.60)

# Lam gỗ mặt tiền thông tầng trang trí
for li in range(8):
    lx = 0.25 + li * 0.18
    add_box(col_fl1_arch, f"Facade_Louver_{li}", lx, -0.10, Z1 + 0.2, lx + 0.06, 0.02, 7.25, "Mat_WoodLouverFacade")
add_box(col_lights, "Facade_Louver_LED", 0.22, -0.04, Z1 + 0.3, 0.26, 0.01, 7.20, "Mat_WarmLED")

# --- A. GIAN THỜ CÚNG (1 BÊN CỬA CHÍNH, CÓ VÁCH NGĂN) & PHÒNG KHÁCH (ĐI TỪ CỬA CHÍNH VÀO) ---

# 1. VÁCH NGĂN GIAN THỜ CÚNG & PHÒNG KHÁCH (Ngăn trang nghiêm góc trái mặt tiền X=0.22..2.44, Y=0.22..2.16)
# Vách ngăn chính phía sau bàn thờ (tựa lưng bàn thờ quay mặt ra hướng Đông mặt tiền)
add_box(col_fl1_arch, "Altar_Partition_BackWall", 0.22, 2.06, Z1, 2.44, 2.16, H1, "Mat_WallWarmWhite")
add_box(col_fl1_furn, "Altar_Partition_WoodTrim", 0.35, 2.03, Z1 + 0.05, 2.32, 2.07, H1 - 0.10, "Mat_WoodWalnutAltar", bevel=0.008)
# Vách ngăn CNC lam gỗ bên cạnh cửa chính (ngăn lối vào phòng khách với gian thờ, chừa lối vào gian thờ Y=0.26..1.12)
add_box(col_fl1_furn, "Altar_CNC_FrameTop", 2.38, 1.12, H1 - 0.16, 2.48, 2.16, H1, "Mat_WoodWalnutAltar", bevel=0.006)
add_box(col_fl1_furn, "Altar_CNC_FrameBot", 2.38, 1.12, Z1, 2.48, 2.16, Z1 + 0.10, "Mat_WoodWalnutAltar", bevel=0.006)
add_box(col_fl1_furn, "Altar_CNC_PostFront", 2.38, 1.12, Z1, 2.48, 1.20, H1, "Mat_WoodWalnutAltar", bevel=0.006)
for si in range(7):
    sy_s = 1.28 + si * 0.125
    add_box(col_fl1_furn, f"Altar_CNC_Slat_{si}", 2.40, sy_s, Z1 + 0.10, 2.46, sy_s + 0.045, H1 - 0.16, "Mat_WoodLouverFacade", bevel=0.004)
add_box(col_lights, "Altar_Partition_LED", 2.37, 1.16, Z1 + 0.12, 2.40, 1.20, H1 - 0.18, "Mat_WarmLED")

# 2. GIAN THỜ BỒ TÁT QUAN ÂM & GIA TIÊN (Nằm 1 bên cửa chính: X=0.45..2.15, Y=0.30..2.03, hướng mặt ra mặt tiền -Y)
add_box(col_fl1_furn, "Altar_Table", 0.52, 1.38, Z1 + 0.98, 2.08, 2.02, Z1 + 1.08, "Mat_WoodWalnutAltar", bevel=0.015)
for i, (ax_l, ay_l) in enumerate([(0.58, 1.44), (2.02, 1.44), (0.58, 1.96), (2.02, 1.96)]):
    add_box(col_fl1_furn, f"Altar_Leg_{i}", ax_l - 0.04, ay_l - 0.04, Z1, ax_l + 0.04, ay_l + 0.04, Z1 + 0.98, "Mat_WoodWalnutAltar")
add_box(col_fl1_furn, "Altar_LowerShelf", 0.58, 1.44, Z1 + 0.28, 2.02, 1.96, Z1 + 0.35, "Mat_WoodWalnutAltar")
# Tượng Quan Âm, đế sen đồng, vòng hào quang LED hướng ra cửa mặt tiền
add_cyl(col_fl1_furn, "Altar_LotusBase", 1.30, 1.78, Z1 + 1.08, Z1 + 1.20, 0.18, 0.14, "Mat_BrassGold", segs=18)
add_cyl(col_fl1_furn, "Altar_BuddhaBody", 1.30, 1.78, Z1 + 1.20, Z1 + 1.68, 0.12, 0.05, "Mat_BuddhaGold", segs=18)
add_sphere(col_fl1_furn, "Altar_BuddhaHead", 1.30, 1.78, Z1 + 1.75, 0.075, "Mat_BuddhaGold")
add_cyl(col_lights, "Altar_HaloLED", 1.30, 1.99, Z1 + 1.68, Z1 + 1.71, 0.34, 0.34, "Mat_WarmLED", rot=(math.pi / 2, 0, 0))
# Lư hương đồng, 2 bình hoa sen, 2 đèn thờ, mâm ngũ quả & thảm lễ
add_cyl(col_fl1_furn, "Altar_IncenseBurner", 1.30, 1.55, Z1 + 1.08, Z1 + 1.24, 0.08, 0.095, "Mat_BrassGold", segs=16)
for vi, vx in enumerate([0.76, 1.84]):
    add_cyl(col_fl1_furn, f"Altar_Vase_{vi}", vx, 1.74, Z1 + 1.08, Z1 + 1.38, 0.065, 0.045, "Mat_CeramicWhite", segs=14)
    add_sphere(col_fl1_furn, f"Altar_Lotus_{vi}", vx, 1.74, Z1 + 1.46, 0.08, "Mat_FlowerPink")
    add_cyl(col_lights, f"Altar_Candle_{vi}", vx + (0.20 if vi == 0 else -0.20), 1.54, Z1 + 1.08, Z1 + 1.26, 0.032, 0.025, "Mat_WarmSconce", segs=12)
add_cyl(col_fl1_furn, "Altar_FruitPlate", 1.55, 1.66, Z1 + 1.08, Z1 + 1.15, 0.10, 0.12, "Mat_WoodOakDark", segs=14)
add_sphere(col_fl1_furn, "Altar_Fruit1", 1.55, 1.66, Z1 + 1.19, 0.042, "Mat_FlowerYellow")
add_sphere(col_fl1_furn, "Altar_Fruit2", 1.51, 1.63, Z1 + 1.18, 0.038, "Mat_CushionTerracotta")
add_box(col_fl1_furn, "Altar_PrayerMat", 0.85, 0.62, Z1, 1.75, 1.18, Z1 + 0.025, "Mat_CushionTerracotta", bevel=0.008)
add_curtain_pair(col_fl1_furn, "Altar_FrontCurtain", 0.42, 2.28, 0.26, Z1 + 0.04, H1 - 0.15)
add_pendant_chandelier(col_lights, "Altar_PendantLamp", 1.30, 1.15, H1 - 0.02, drop=0.65, count=1)

# 3. SẢNH ĐÓN TỪ CỬA CHÍNH ĐI VÀO (Bên phải cửa chính: X=2.55..4.78, Y=0.25..2.15)
add_box(col_fl1_furn, "Living_EntryConsole", 4.32, 0.55, Z1 + 0.08, 4.76, 1.65, Z1 + 0.82, "Mat_WoodOakCabinet", bevel=0.012)
add_cyl(col_fl1_furn, "Living_EntryVase", 4.54, 1.10, Z1 + 0.82, Z1 + 1.06, 0.07, 0.045, "Mat_CeramicTeal", segs=14)
add_sphere(col_fl1_furn, "Living_EntryFlowers", 4.54, 1.10, Z1 + 1.14, 0.10, "Mat_FlowerPink")
add_cyl(col_fl1_furn, "Living_EntryMirror", 4.74, 1.10, Z1 + 1.58, Z1 + 1.62, 0.36, 0.36, "Mat_Mirror", rot=(0, math.pi / 2, 0), segs=22)

# 4. KHÔNG GIAN PHÒNG KHÁCH CHÍNH (Y = 2.20..5.75 — đi thẳng từ cửa chính vào)
# Kệ TV & Vách lam gỗ thưa áp tường trái (Y = 2.75..4.78)
add_box(col_fl1_furn, "Living_TVConsole", 0.24, 2.75, Z1 + 0.08, 0.72, 4.75, Z1 + 0.50, "Mat_WoodOakCabinet", bevel=0.012)
for d in range(3):
    add_box(col_fl1_furn, f"Living_TVDrawer_{d}", 0.70, 2.81 + d * 0.63, Z1 + 0.14, 0.74, 3.38 + d * 0.63, Z1 + 0.44, "Mat_WallFacadeWarm", bevel=0.006)
for sl in range(11):
    sly = 2.78 + sl * 0.188
    add_box(col_fl1_furn, f"Living_TVLouverSlat_{sl}", 0.24, sly, Z1 + 0.50, 0.29, sly + 0.05, Z1 + 2.35, "Mat_WoodLouverFacade")
add_box(col_fl1_furn, "Living_TVFrame", 0.29, 3.10, Z1 + 0.76, 0.34, 4.40, Z1 + 1.56, "Mat_MetalMatteBlack", bevel=0.008)
add_box(col_fl1_furn, "Living_TVScreen", 0.33, 3.14, Z1 + 0.80, 0.355, 4.36, Z1 + 1.52, "Mat_TVScreenBlack")
add_box(col_fl1_furn, "Living_Soundbar", 0.44, 3.30, Z1 + 0.50, 0.56, 4.20, Z1 + 0.58, "Mat_MetalMatteBlack", bevel=0.01)
add_cyl(col_fl1_furn, "Living_ConsoleVase", 0.48, 2.95, Z1 + 0.50, Z1 + 0.72, 0.06, 0.04, "Mat_CeramicTeal")
add_books_row(col_fl1_furn, "Living_ConsoleBooks", 0.40, 4.38, Z1 + 0.50, count=4, axis='Y')
add_box(col_lights, "Living_TV_TopLED", 0.26, 2.76, Z1 + 2.32, 0.31, 4.74, Z1 + 2.36, "Mat_WarmLED")
add_potted_plant(col_fl1_furn, "Living_FicusPlant", 0.62, 5.28, Z1, scale=1.22, pot_mat="Mat_CeramicWhite")

# Thảm phòng khách + Bộ Sofa chữ L hiện đại đối diện TV (chừa lối thoáng Y=5.05..5.75 đi ra hành lang)
add_box(col_fl1_furn, "Living_AreaRug", 1.45, 2.35, Z1, 3.98, 5.15, Z1 + 0.025, "Mat_RugWarm", bevel=0.008)
add_box(col_fl1_furn, "Living_Sofa_Base", 3.72, 2.38, Z1 + 0.08, 4.66, 5.02, Z1 + 0.44, "Mat_FabricSofaWarm", bevel=0.03)
add_box(col_fl1_furn, "Living_Sofa_Chaise", 2.85, 2.38, Z1 + 0.08, 3.75, 3.22, Z1 + 0.44, "Mat_FabricSofaWarm", bevel=0.03)
add_box(col_fl1_furn, "Living_Sofa_Back", 4.32, 2.38, Z1 + 0.44, 4.68, 5.02, Z1 + 0.86, "Mat_FabricSofaWarm", bevel=0.04)
add_box(col_fl1_furn, "Living_Sofa_Arm1", 2.85, 2.32, Z1 + 0.08, 4.66, 2.50, Z1 + 0.66, "Mat_FabricSofaWarm", bevel=0.025)
add_box(col_fl1_furn, "Living_Sofa_Arm2", 3.72, 4.90, Z1 + 0.08, 4.66, 5.08, Z1 + 0.66, "Mat_FabricSofaWarm", bevel=0.025)
for si in range(3):
    sy1 = 2.52 + si * 0.79
    add_box(col_fl1_furn, f"Living_SofaSeat_{si}", 3.74, sy1, Z1 + 0.40, 4.34, sy1 + 0.76, Z1 + 0.52, "Mat_FabricBeige", bevel=0.03)
pillow_specs = [
    (4.15, 2.80, "Mat_CushionMustard"),
    (4.15, 3.45, "Mat_CushionNavy"),
    (4.15, 4.10, "Mat_CushionTerracotta"),
    (4.15, 4.68, "Mat_CushionMustard"),
]
for pi, (px, py, pm) in enumerate(pillow_specs):
    add_box(col_fl1_furn, f"Living_Pillow_{pi}", px - 0.12, py - 0.22, Z1 + 0.50, px + 0.14, py + 0.22, Z1 + 0.82, pm, bevel=0.05)

# Bàn trà tròn đá cẩm thạch + Bình hoa + Bộ sách decor đặt giữa Phòng khách
add_cyl(col_fl1_furn, "Living_CoffeeTableTop", 2.38, 3.82, Z1 + 0.40, Z1 + 0.45, 0.52, 0.52, "Mat_WhiteMarble", segs=24)
add_cyl(col_fl1_furn, "Living_CoffeeTableRim", 2.38, 3.82, Z1 + 0.37, Z1 + 0.41, 0.50, 0.50, "Mat_BrassGold", segs=24)
for i, ang in enumerate([0, 2.09, 4.18]):
    add_cyl(col_fl1_furn, f"Living_CoffeeLeg_{i}", 2.38 + 0.32 * math.cos(ang), 3.82 + 0.32 * math.sin(ang), Z1 + 0.02, Z1 + 0.38, 0.022, 0.022, "Mat_MetalMatteBlack", segs=10)
add_cyl(col_fl1_furn, "Living_FlowerVase", 2.30, 3.90, Z1 + 0.45, Z1 + 0.67, 0.07, 0.045, "Mat_CeramicWhite", segs=16)
add_sphere(col_fl1_furn, "Living_Flowers1", 2.30, 3.90, Z1 + 0.74, 0.11, "Mat_FlowerPink")
add_sphere(col_fl1_furn, "Living_Flowers2", 2.38, 3.84, Z1 + 0.72, 0.08, "Mat_FlowerYellow")
add_box(col_fl1_furn, "Living_ArtBook1", 2.39, 3.48, Z1 + 0.45, 2.67, 3.72, Z1 + 0.49, "Mat_BookBlue", bevel=0.004)
add_box(col_fl1_furn, "Living_ArtBook2", 2.42, 3.51, Z1 + 0.49, 2.64, 3.69, Z1 + 0.52, "Mat_BookAmber", bevel=0.004)

# Đèn cây đứng cạnh sofa, Tranh bộ 3 tường phải & Đèn chùm trần Phòng khách
add_cyl(col_fl1_furn, "Living_FloorLampBase", 4.35, 5.36, Z1, Z1 + 0.04, 0.18, 0.16, "Mat_BrassGold", segs=16)
add_cyl(col_fl1_furn, "Living_FloorLampPole", 4.35, 5.36, Z1 + 0.04, Z1 + 1.65, 0.018, 0.015, "Mat_BrassGold", segs=10)
add_cyl(col_fl1_furn, "Living_FloorLampShade", 4.35, 5.36, Z1 + 1.48, Z1 + 1.82, 0.22, 0.16, "Mat_LampShadeGlow", segs=18)
add_framed_art(col_fl1_furn, "Living_WallArt_1", 4.75, 2.90, Z1 + 1.80, 0.65, 0.85, wall_axis='X', canvas_mat="Mat_ArtCanvasWarm")
add_framed_art(col_fl1_furn, "Living_WallArt_2", 4.75, 3.70, Z1 + 1.80, 0.65, 0.85, wall_axis='X', canvas_mat="Mat_ArtCanvasBlue")
add_framed_art(col_fl1_furn, "Living_WallArt_3", 4.75, 4.50, Z1 + 1.80, 0.65, 0.85, wall_axis='X', canvas_mat="Mat_ArtCanvasGreen")
add_pendant_chandelier(col_lights, "Living_Chandelier", 2.45, 3.75, H1 - 0.02, drop=0.82, count=3)

# --- B. PHÒNG NGỦ BA MẸ (X = 0.22..3.95, Y = 5.85..9.0) ---
add_box(col_fl1_arch, "Wall_Living_Parents_Bot", 0.22, 5.75, Z1, 4.0, 5.85, Z1 + 1.25, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Living_Parents_Top", 0.22, 5.75, Z1 + 2.25, 4.0, 5.85, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Living_Parents_L", 0.22, 5.75, Z1 + 1.25, 1.10, 5.85, Z1 + 2.25, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Living_Parents_R", 3.20, 5.75, Z1 + 1.25, 4.0, 5.85, Z1 + 2.25, "Mat_WallWarmWhite")
add_window_frame(col_fl1_arch, "Win_Parents_3Panel", 1.10, 5.77, Z1 + 1.25, 3.20, 5.83, Z1 + 2.25)
# Vách ngăn hành lang có chừa cửa vào (Y = 8.05..8.90)
add_box(col_fl1_arch, "Wall_Parents_Hall", 3.95, 5.80, Z1, 4.05, 8.05, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Parents_HallTop", 3.95, 8.05, Z1 + 2.25, 4.05, 9.0, H1, "Mat_WallWarmWhite")

add_box(col_fl1_furn, "Parents_Rug", 1.35, 6.15, Z1, 3.85, 8.60, Z1 + 0.025, "Mat_RugWarm", bevel=0.008)
add_detailed_bed(col_fl1_furn, "Parents_Bed", 1.88, 6.50, Z1 + 0.02, 3.88, 8.20, head_side='X_MAX', duvet_mat="Mat_CushionNavy")
add_nightstand(col_fl1_furn, "Parents_Nightstand_1", 3.64, 6.15, Z1 + 0.02)
add_nightstand(col_fl1_furn, "Parents_Nightstand_2", 3.64, 8.54, Z1 + 0.02)
add_wardrobe(col_fl1_furn, "Parents_Wardrobe", 0.35, 8.36, Z1, 1.85, 8.92, h=2.45, door_face='Y_MIN')
add_framed_art(col_fl1_furn, "Parents_Art", 3.92, 7.35, Z1 + 1.85, 1.15, 0.72, wall_axis='X', canvas_mat="Mat_ArtCanvasWarm")
add_potted_plant(col_fl1_furn, "Parents_Plant", 1.20, 6.20, Z1, scale=0.85, pot_mat="Mat_CeramicWhite")
add_pendant_chandelier(col_lights, "Parents_CeilingLamp", 2.40, 7.35, H1 - 0.02, drop=0.45, count=1)

# --- C. CẦU THANG CHỮ U HOÀN CHỈNH 2 VẾ + LAN CAN KÍNH (Y = 9.0..11.2) ---
# Vế 1 (đi từ Z1=0.25 lên chiếu nghỉ Z=2.05)
for s in range(10):
    sy = 9.05 + s * 0.155
    sz = Z1 + (s + 1) * 0.18
    add_box(col_fl1_arch, f"Stair_F1_Tread_{s}", 0.24, sy, sz - 0.05, 1.88, sy + 0.20, sz, "Mat_WoodStairTreads", bevel=0.006)
    add_box(col_lights, f"Stair_F1_LED_{s}", 0.28, sy, sz - 0.055, 1.84, sy + 0.02, sz - 0.042, "Mat_WarmLED")
# Chiếu nghỉ giữa
add_box(col_fl1_arch, "Stair_Landing", 0.24, 10.55, 1.97, 3.88, 11.20, 2.06, "Mat_WoodStairTreads", bevel=0.01)
# Vế 2 (từ chiếu nghỉ đi ngược lên Tầng 2 Z2=3.85)
for s in range(10):
    sy = 10.42 - s * 0.155
    sz = 2.05 + (s + 1) * 0.18
    add_box(col_fl1_arch, f"Stair_F2_Tread_{s}", 2.16, sy - 0.18, sz - 0.05, 3.88, sy + 0.02, sz, "Mat_WoodStairTreads", bevel=0.006)
    add_box(col_lights, f"Stair_F2_LED_{s}", 2.20, sy + 0.01, sz - 0.055, 3.84, sy + 0.03, sz - 0.042, "Mat_WarmLED")
# Tay vịn & vách kính giữa 2 vế thang
add_box(col_fl1_arch, "Stair_GlassRail_Mid", 1.98, 9.05, Z1 + 0.90, 2.04, 10.60, 3.85 + 0.90, "Mat_GlassClear")
add_box(col_fl1_arch, "Stair_Handrail_Top", 1.96, 9.05, 3.85 + 0.88, 2.06, 10.60, 3.85 + 0.94, "Mat_WoodOakTable")

# --- D. BẾP MỞ & BÀN ĂN TRÒN 6 GHẾ CHI TIẾT (Y = 11.2..15.78) ---
add_box(col_fl1_furn, "Kitchen_Counter_L", 0.24, 11.50, Z1, 0.96, 14.78, Z1 + 0.86, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl1_furn, "Kitchen_StoneTop", 0.22, 11.46, Z1 + 0.86, 1.00, 14.80, Z1 + 0.91, "Mat_WhiteMarble", bevel=0.006)
add_box(col_fl1_furn, "Kitchen_Backsplash", 0.22, 11.50, Z1 + 0.91, 0.26, 14.78, Z1 + 1.18, "Mat_BacksplashTile")
add_box(col_fl1_furn, "Kitchen_UpperCabinets", 0.24, 11.60, Z1 + 1.88, 0.62, 14.70, Z1 + 2.48, "Mat_WallFacadeWarm", bevel=0.01)
add_box(col_lights, "Kitchen_UnderCabinetLED", 0.54, 11.65, Z1 + 1.85, 0.59, 14.65, Z1 + 1.88, "Mat_WarmLED")

# Bếp từ 2 vùng nấu + Máy hút mùi + Nồi nấu
add_box(col_fl1_furn, "Kitchen_Cooktop", 0.34, 12.15, Z1 + 0.91, 0.86, 12.90, Z1 + 0.935, "Mat_PianoBlackGloss")
add_cyl(col_fl1_furn, "Kitchen_Pot", 0.60, 12.40, Z1 + 0.935, Z1 + 1.08, 0.11, 0.11, "Mat_MetalStainless", segs=16)
add_box(col_fl1_furn, "Kitchen_RangeHood", 0.28, 12.10, Z1 + 1.56, 0.82, 12.95, Z1 + 1.72, "Mat_MetalStainless", bevel=0.01)
add_box(col_fl1_furn, "Kitchen_RangeDuct", 0.30, 12.38, Z1 + 1.72, 0.58, 12.68, H1 - 0.05, "Mat_MetalStainless")

# Bồn rửa chén + Vòi nước cong + Đĩa hoa quả + Bình siêu tốc
add_box(col_fl1_furn, "Kitchen_SinkBasin", 0.34, 13.45, Z1 + 0.89, 0.86, 14.15, Z1 + 0.925, "Mat_MetalStainless")
add_cyl(col_fl1_furn, "Kitchen_FaucetBase", 0.34, 13.80, Z1 + 0.91, Z1 + 1.24, 0.02, 0.016, "Mat_MetalStainless", segs=10)
add_box(col_fl1_furn, "Kitchen_FaucetSpout", 0.34, 13.78, Z1 + 1.20, 0.54, 13.82, Z1 + 1.24, "Mat_MetalStainless", bevel=0.006)
add_cyl(col_fl1_furn, "Kitchen_Kettle", 0.58, 11.78, Z1 + 0.91, Z1 + 1.12, 0.08, 0.065, "Mat_CeramicWhite", segs=14)
add_cyl(col_fl1_furn, "Kitchen_FruitBowl", 0.60, 14.45, Z1 + 0.91, Z1 + 1.00, 0.10, 0.14, "Mat_WoodOakTable", segs=16)
add_sphere(col_fl1_furn, "Kitchen_Apple1", 0.57, 14.43, Z1 + 1.03, 0.045, "Mat_CushionTerracotta")
add_sphere(col_fl1_furn, "Kitchen_Apple2", 0.63, 14.48, Z1 + 1.03, 0.042, "Mat_FlowerYellow")

# Tủ lạnh Side-by-Side 2 cánh + Tay nắm
add_box(col_fl1_furn, "Kitchen_Fridge", 0.24, 14.84, Z1, 1.04, 15.68, Z1 + 2.02, "Mat_MetalStainless", bevel=0.02)
add_box(col_fl1_furn, "Kitchen_FridgeSplit", 1.03, 15.25, Z1 + 0.06, 1.05, 15.27, Z1 + 1.98, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "Kitchen_FridgeHandle1", 1.04, 15.16, Z1 + 0.85, 1.08, 15.19, Z1 + 1.55, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "Kitchen_FridgeHandle2", 1.04, 15.33, Z1 + 0.85, 1.08, 15.36, Z1 + 1.55, "Mat_MetalMatteBlack")

# Bàn ăn tròn ấm cúng + 6 ghế ăn chi tiết + Bình hoa + Bộ bát đĩa + Đèn thả 3 bóng
dt_x, dt_y = 2.85, 13.55
add_cyl(col_fl1_furn, "Dining_RoundTableTop", dt_x, dt_y, Z1 + 0.72, Z1 + 0.77, 0.78, 0.78, "Mat_WoodOakTable", segs=28)
add_cyl(col_fl1_furn, "Dining_CenterLeg", dt_x, dt_y, Z1, Z1 + 0.72, 0.12, 0.22, "Mat_MetalMatteBlack", segs=18)
add_cyl(col_fl1_furn, "Dining_CenterVase", dt_x, dt_y, Z1 + 0.77, Z1 + 0.98, 0.065, 0.045, "Mat_CeramicTeal", segs=16)
add_sphere(col_fl1_furn, "Dining_Flowers", dt_x, dt_y, Z1 + 1.05, 0.11, "Mat_FlowerYellow")
for ci in range(6):
    ang = ci * (2 * math.pi / 6.0)
    cx_ch = dt_x + 1.06 * math.cos(ang)
    cy_ch = dt_y + 1.06 * math.sin(ang)
    # Ghế hướng mặt vào tâm bàn
    chair_rot = ang + math.pi / 2.0
    add_dining_chair(col_fl1_furn, f"Dining_Chair_{ci}", cx_ch, cy_ch, Z1, chair_rot,
                     seat_mat="Mat_FabricBeige", wood_mat="Mat_WoodOakTable")
    # Đĩa ăn trên mặt bàn tương ứng mỗi ghế
    px = dt_x + 0.54 * math.cos(ang)
    py = dt_y + 0.54 * math.sin(ang)
    add_cyl(col_fl1_furn, f"Dining_Plate_{ci}", px, py, Z1 + 0.77, Z1 + 0.79, 0.12, 0.13, "Mat_CeramicWhite", segs=16)

add_pendant_chandelier(col_lights, "Dining_Chandelier", dt_x, dt_y, H1 - 0.02, drop=1.05, count=3)
add_framed_art(col_fl1_furn, "Dining_WallArt_1", 4.75, 13.0, Z1 + 1.78, 0.75, 0.90, wall_axis='X', canvas_mat="Mat_ArtCanvasGreen")
add_framed_art(col_fl1_furn, "Dining_WallArt_2", 4.75, 14.0, Z1 + 1.78, 0.75, 0.90, wall_axis='X', canvas_mat="Mat_ArtCanvasWarm")
add_potted_plant(col_fl1_furn, "Dining_CornerPlant", 4.35, 15.20, Z1, scale=1.15, pot_mat="Mat_TerracottaPot")

# ---------------------------------------------------------------------------
# 6. SÂN SAU: DÃY PHỤ TRỢ, BÀN CHILL, XE MÁY & VƯỜN RAU HỮU CƠ XANH MƯỚT
# ---------------------------------------------------------------------------
add_box(col_site, "RearYard_Slab", 0.0, 16.0, 0.0, 7.0, 24.0, 0.15, "Mat_AntiSlipPavers")
add_box(col_site, "Rear_WC_Room", 0.1, 16.0, 0.15, 2.4, 17.6, 2.65, "Mat_WallWarmWhite")
add_box(col_site, "Rear_Bath_Room", 0.1, 17.6, 0.15, 2.4, 19.2, 2.65, "Mat_WallWarmWhite")
add_box(col_site, "Rear_Laundry_Room", 0.1, 19.2, 0.15, 2.4, 20.8, 2.65, "Mat_WallWarmWhite")
add_box(col_site, "Washer_Dryer", 0.4, 19.5, 0.15, 1.1, 20.2, 1.05, "Mat_MetalStainless", bevel=0.02)
add_cyl(col_site, "Washer_Door", 1.11, 19.85, 0.42, 0.82, 0.20, 0.20, "Mat_GlassBronze", rot=(0, math.pi / 2, 0), segs=16)
add_box(col_site, "Rear_Drying_Deck", 0.1, 20.8, 0.15, 2.4, 23.0, 0.25, "Mat_WoodOakTable")

# Bàn chill sân sau + 2 ghế + Xe tay ga chi tiết
add_cyl(col_site, "Rear_Chill_TableTop", 3.45, 17.6, 0.80, 0.85, 0.46, 0.46, "Mat_WoodOakTable", segs=20)
add_cyl(col_site, "Rear_Chill_TableLeg", 3.45, 17.6, 0.15, 0.80, 0.07, 0.12, "Mat_MetalMatteBlack", segs=14)
add_cyl(col_site, "Rear_Chill_Cup1", 3.35, 17.55, 0.85, 0.93, 0.035, 0.04, "Mat_CeramicWhite")
add_cyl(col_site, "Rear_Chill_Cup2", 3.55, 17.65, 0.85, 0.93, 0.035, 0.04, "Mat_CeramicTeal")
add_dining_chair(col_site, "Rear_Chill_Chair1", 3.45, 16.92, 0.15, 0.0, "Mat_CushionMustard", "Mat_WoodOakDark")
add_dining_chair(col_site, "Rear_Chill_Chair2", 3.45, 18.28, 0.15, math.pi, "Mat_CushionMustard", "Mat_WoodOakDark")

add_box(col_site, "Rear_Scooter_Body", 3.32, 19.4, 0.42, 3.78, 20.7, 0.95, "Mat_CeramicWhite", bevel=0.06)
add_box(col_site, "Rear_Scooter_Seat", 3.36, 19.8, 0.92, 3.74, 20.55, 1.04, "Mat_WoodOakDark", bevel=0.04)
add_box(col_site, "Rear_Scooter_Handle", 3.22, 19.45, 1.12, 3.88, 19.55, 1.20, "Mat_MetalMatteBlack")
add_cyl(col_site, "Rear_Scooter_Wheel1", 3.55, 19.45, 0.15, 0.58, 0.21, 0.21, "Mat_TireRubber", rot=(0, math.pi / 2, 0), segs=14)
add_cyl(col_site, "Rear_Scooter_Wheel2", 3.55, 20.60, 0.15, 0.58, 0.21, 0.21, "Mat_TireRubber", rot=(0, math.pi / 2, 0), segs=14)

# Vườn rau hữu cơ có luống đất & rau xanh tươi
for vr in range(4):
    vry = 20.9 + vr * 0.72
    add_box(col_site, f"VegBed_{vr}", 4.55, vry, 0.15, 6.75, vry + 0.52, 0.44, "Mat_WoodOakDark", bevel=0.01)
    add_box(col_site, f"VegSoil_{vr}", 4.62, vry + 0.05, 0.40, 6.68, vry + 0.47, 0.46, "Mat_SoilDark")
    for vc in range(5):
        vx = 4.85 + vc * 0.40
        add_sphere(col_site, f"VegLeaf_{vr}_{vc}", vx, vry + 0.26, 0.54, 0.14,
                   "Mat_FoliageBright" if (vr + vc) % 2 == 0 else "Mat_FoliageGreen", 1.1, 1.0, 0.65)

# ---------------------------------------------------------------------------
# 7. TẦNG 2 MỞ RỘNG 7M: PHÒNG MASTER, SẾU, CHỊ HAI + HÀNH LANG 2M TRÊN ĐƯỜNG LUỒNG
# ---------------------------------------------------------------------------
Z2 = 3.85
H2 = 7.35

# Sàn Tầng 2 mở rộng trọn 7m (X = 0..7), Ban công trước vươn dài 3.0m (Y = -3.0..0.0),
# chừa ô thông tầng cầu thang (X = 0.22..3.95, Y = 8.95..11.20) và chừa nắng vườn rau sau (X = 5..7, Y = 20.2..24)
add_box(col_fl2_arch, "Floor2_Slab_Front", 0.0, -3.0, Z2 - 0.15, 7.0, 8.95, Z2, "Mat_AntiSlipWoodTile")
add_box(col_fl2_arch, "Floor2_Slab_HallSide", 3.95, 8.95, Z2 - 0.15, 7.0, 11.20, Z2, "Mat_AntiSlipWoodTile")
add_box(col_fl2_arch, "Floor2_Slab_RearWide", 0.0, 11.20, Z2 - 0.15, 7.0, 20.20, Z2, "Mat_AntiSlipWoodTile")
add_box(col_fl2_arch, "Floor2_Slab_RearLaundry", 0.0, 20.20, Z2 - 0.15, 5.0, 24.0, Z2, "Mat_AntiSlipWoodTile")

# Hệ cột kết cấu đỡ hành lang Tầng 2 & góc ban công trước dọc sát tường rào phải (không cản đường luồng 2m tầng 1)
for ci, cy in enumerate([-2.88, 0.15, 4.0, 8.0, 12.0, 15.85, 19.95]):
    add_box(col_fl2_arch, f"Fl2_Corridor_Col_{ci}", 6.80, cy - 0.12, 0.15, 7.02, cy + 0.12, Z2 - 0.15, "Mat_WallWarmWhite", bevel=0.01)
add_box(col_fl2_arch, "Fl2_Corridor_EdgeBeam", 6.80, -3.0, Z2 - 0.30, 7.02, 20.20, Z2 - 0.14, "Mat_RoofCharcoal")
add_box(col_fl2_arch, "BalconyFront_EdgeBeam", 0.0, -3.02, Z2 - 0.28, 7.02, -2.86, Z2 - 0.14, "Mat_RoofCharcoal")
# Dải đèn LED hắt trần dưới hành lang Tầng 2 chiếu sáng đường luồng tầng 1
add_box(col_lights, "Fl1_Corridor_CeilingLED", 5.92, 0.30, Z2 - 0.19, 6.02, 15.70, Z2 - 0.15, "Mat_WarmLED")

# Lan can kính quanh ô cầu thang tầng 2
add_box(col_fl2_arch, "Fl2_StairGuard_Front", 0.22, 8.92, Z2, 3.95, 8.97, Z2 + 0.95, "Mat_GlassClear")
add_box(col_fl2_arch, "Fl2_StairGuard_Right", 3.92, 8.95, Z2, 3.97, 11.20, Z2 + 0.95, "Mat_GlassClear")

# Tường bao Tầng 2 (tường trái cắt thấp 0.38m)
add_box(col_fl2_arch, "Fl2_Wall_Left_Cutaway", 0.0, 0.0, Z2, 0.22, 16.0, Z2 + 0.38, "Mat_WallWarmWhite")

# Vách ngăn giữa các phòng Tầng 2 (X=0.22..4.88) và Hành lang mới 2m (X=5.0..6.84) — có cửa ra vào từng phòng
add_box(col_fl2_arch, "Fl2_InnerHallWall_Master1", 4.86, 0.0, Z2, 5.0, 2.75, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_MasterTop", 4.86, 2.75, Z2 + 2.28, 5.0, 3.65, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_Master2", 4.86, 3.65, Z2, 5.0, 7.02, H2, "Mat_WallWarmWhite")
# Y = 7.02..11.20 mở hoàn toàn nối thông sảnh cầu thang/giếng trời ra hành lang 2m!
add_box(col_fl2_arch, "Fl2_InnerHallWall_Seu1", 4.86, 11.20, Z2, 5.0, 12.60, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_SeuTop", 4.86, 12.60, Z2 + 2.28, 5.0, 13.42, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_Sis1", 4.86, 13.42, Z2, 5.0, 14.90, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_SisTop", 4.86, 14.90, Z2 + 2.28, 5.0, 15.72, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_End", 4.86, 15.72, Z2, 5.0, 16.0, H2, "Mat_WallWarmWhite")

# Vách ngoài bên phải của Hành lang Tầng 2 (X = 6.84..7.0, Y = 0..16): tường lửng + 4 khung kính lớn toàn cảnh!
add_box(col_fl2_arch, "Fl2_Corridor_OuterBot", 6.84, 0.0, Z2, 7.0, 16.0, Z2 + 0.92, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Corridor_OuterTop", 6.84, 0.0, Z2 + 2.95, 7.0, 16.0, H2, "Mat_WallWarmWhite")
for pi, py in enumerate([0.0, 4.0, 8.0, 12.0, 15.80]):
    add_box(col_fl2_arch, f"Fl2_Corridor_Pier_{pi}", 6.82, py, Z2, 7.0, py + 0.22, H2, "Mat_WallWarmWhite")
for wi, (wy1, wy2) in enumerate([(0.22, 4.0), (4.22, 8.0), (8.22, 12.0), (12.22, 15.80)]):
    add_window_frame(col_fl2_arch, f"Fl2_Corridor_Window_{wi}", 6.86, wy1, Z2 + 0.92, 6.96, wy2, Z2 + 2.95)

# Tường mặt tiền chừa cửa kính lớn Master + cửa kính lớn ở đầu Hành lang Tầng 2
add_box(col_fl2_arch, "Fl2_Wall_Front_L", 0.0, 0.0, Z2, 0.75, 0.22, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Front_Mid", 4.25, 0.0, Z2, 5.10, 0.22, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Front_R", 6.72, 0.0, Z2, 7.0, 0.22, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Front_Top", 0.75, 0.0, Z2 + 2.65, 6.72, 0.22, H2, "Mat_WallWarmWhite")
add_window_frame(col_fl2_arch, "Master_FrontGlassDoor", 0.75, 0.06, Z2, 4.25, 0.18, Z2 + 2.65)
add_window_frame(col_fl2_arch, "Fl2_Corridor_FrontDoor", 5.10, 0.06, Z2, 6.72, 0.18, Z2 + 2.65)

# Tường sau chừa cửa kính Phòng Chị Hai + cửa kính cuối Hành lang Tầng 2 mở ra Ban công sau 7m
add_box(col_fl2_arch, "Fl2_Wall_Rear_L", 0.0, 15.78, Z2, 1.35, 16.0, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Rear_Mid", 3.85, 15.78, Z2, 5.10, 16.0, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Rear_R", 6.72, 15.78, Z2, 7.0, 16.0, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Rear_Top", 1.35, 15.78, Z2 + 2.55, 6.72, 16.0, H2, "Mat_WallWarmWhite")
add_window_frame(col_fl2_arch, "Sister2_RearDoor", 1.35, 15.80, Z2, 3.85, 15.94, Z2 + 2.55)
add_window_frame(col_fl2_arch, "Fl2_Corridor_RearDoor", 5.10, 15.80, Z2, 6.72, 15.94, Z2 + 2.55)

# Nội thất & trang trí Hành lang Tầng 2 mới (X = 5.0..6.84, Y = 0..16)
add_box(col_fl2_furn, "Fl2_Corridor_RunnerRug", 5.45, 0.60, Z2, 6.30, 15.40, Z2 + 0.02, "Mat_RugWarm", bevel=0.006)
# Ghế băng đọc sách & kệ console ngắm cảnh bên khung kính hành lang
add_box(col_fl2_furn, "Fl2_Corridor_Bench", 6.26, 7.10, Z2 + 0.08, 6.78, 9.60, Z2 + 0.44, "Mat_WoodOakTable", bevel=0.015)
add_box(col_fl2_furn, "Fl2_Corridor_BenchPad", 6.30, 7.16, Z2 + 0.44, 6.76, 9.54, Z2 + 0.52, "Mat_CushionMustard", bevel=0.02)
add_box(col_fl2_furn, "Fl2_Corridor_Pillow1", 6.56, 7.35, Z2 + 0.52, 6.76, 7.75, Z2 + 0.80, "Mat_CushionNavy", bevel=0.04)
add_box(col_fl2_furn, "Fl2_Corridor_Pillow2", 6.56, 8.95, Z2 + 0.52, 6.76, 9.35, Z2 + 0.80, "Mat_CushionTerracotta", bevel=0.04)
add_box(col_fl2_furn, "Fl2_Corridor_Console", 6.34, 1.80, Z2 + 0.08, 6.78, 3.20, Z2 + 0.78, "Mat_WoodOakCabinet", bevel=0.01)
add_cyl(col_fl2_furn, "Fl2_Corridor_Vase", 6.56, 2.50, Z2 + 0.78, Z2 + 1.06, 0.08, 0.05, "Mat_CeramicTeal")
add_sphere(col_fl2_furn, "Fl2_Corridor_Flowers", 6.56, 2.50, Z2 + 1.14, 0.12, "Mat_FlowerYellow")
for pi, py in enumerate([0.85, 5.40, 10.65, 14.95]):
    add_potted_plant(col_fl2_furn, f"Fl2_Corridor_Plant_{pi}", 6.42, py, Z2, scale=0.88,
                     pot_mat="Mat_CeramicWhite" if pi % 2 == 0 else "Mat_TerracottaPot")
for li, ly in enumerate([2.2, 6.2, 10.2, 14.2]):
    add_pendant_chandelier(col_lights, f"Fl2_Corridor_Light_{li}", 5.92, ly, H2 - 0.02, drop=0.45, count=1)
add_framed_art(col_fl2_furn, "Fl2_Corridor_Art1", 5.02, 5.30, Z2 + 1.80, 0.90, 0.72, wall_axis='X', canvas_mat="Mat_ArtCanvasGreen")
add_framed_art(col_fl2_furn, "Fl2_Corridor_Art2", 5.02, 11.90, Z2 + 1.80, 0.85, 0.68, wall_axis='X', canvas_mat="Mat_ArtCanvasWarm")

# Ban công trước mở rộng dài ra 3.0m (7m x 3.0m = 21m² ngay trước Phòng Master Chị Ba!)
add_box(col_fl2_arch, "BalconyFront_Rail", 0.0, -3.00, Z2, 7.0, -2.94, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyFront_TopBar", 0.0, -3.02, Z2 + 1.10, 7.0, -2.92, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "BalconyFront_Rail_L", 0.0, -3.00, Z2, 0.05, 0.0, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyFront_TopBar_L", -0.02, -3.02, Z2 + 1.10, 0.07, 0.0, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "BalconyFront_Rail_R", 6.95, -3.00, Z2, 7.0, 0.0, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyFront_TopBar_R", 6.93, -3.02, Z2 + 1.10, 7.02, 0.0, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_lights, "BalconyFront_UnderLED", 0.1, -2.98, Z2 - 0.18, 6.9, -2.92, Z2 - 0.14, "Mat_WarmLED")
# Đèn gắn tường mặt tiền chiếu sáng ban công đêm
add_box(col_lights, "BalconyFront_Sconce1", 0.42, -0.08, Z2 + 1.85, 0.56, 0.02, Z2 + 2.15, "Mat_WarmSconce")
add_box(col_lights, "BalconyFront_Sconce2", 4.62, -0.08, Z2 + 1.85, 4.76, 0.02, Z2 + 2.15, "Mat_WarmSconce")

# Bộ bàn trà & ghế thư giãn ngắm sao ngay trước cửa kính Phòng Master
add_box(col_fl2_furn, "BalconyFront_Rug", 1.10, -2.35, Z2, 3.65, -0.75, Z2 + 0.02, "Mat_RugWarm", bevel=0.006)
add_dining_chair(col_fl2_furn, "BalconyFront_Chair1", 1.65, -1.55, Z2, -0.45, "Mat_CushionMustard", "Mat_WoodOakTable")
add_dining_chair(col_fl2_furn, "BalconyFront_Chair2", 3.10, -1.55, Z2, 0.45, "Mat_CushionMustard", "Mat_WoodOakTable")
add_cyl(col_fl2_furn, "BalconyFront_Table", 2.38, -1.62, Z2 + 0.46, Z2 + 0.51, 0.36, 0.36, "Mat_WhiteMarble", segs=22)
add_cyl(col_fl2_furn, "BalconyFront_TableLeg", 2.38, -1.62, Z2, Z2 + 0.46, 0.05, 0.09, "Mat_MetalMatteBlack")
add_cyl(col_fl2_furn, "BalconyFront_Cup1", 2.26, -1.56, Z2 + 0.51, Z2 + 0.59, 0.035, 0.04, "Mat_CeramicWhite")
add_cyl(col_fl2_furn, "BalconyFront_Cup2", 2.48, -1.68, Z2 + 0.51, Z2 + 0.59, 0.035, 0.04, "Mat_CeramicTeal")

# Ghế băng tắm nắng / chill nhạc phía phải ban công trước (X = 4.45..6.35, Y = -2.30..-1.45)
add_box(col_fl2_furn, "BalconyFront_DaybedBase", 4.45, -2.30, Z2 + 0.08, 6.35, -1.48, Z2 + 0.42, "Mat_WoodOakTable", bevel=0.02)
add_box(col_fl2_furn, "BalconyFront_DaybedPad", 4.50, -2.26, Z2 + 0.42, 6.30, -1.52, Z2 + 0.52, "Mat_BeddingCream", bevel=0.025)
add_box(col_fl2_furn, "BalconyFront_DaybedPillow1", 4.58, -2.18, Z2 + 0.52, 4.95, -1.62, Z2 + 0.78, "Mat_CushionTerracotta", bevel=0.04)
add_box(col_fl2_furn, "BalconyFront_DaybedPillow2", 5.88, -2.18, Z2 + 0.52, 6.24, -1.62, Z2 + 0.78, "Mat_CushionNavy", bevel=0.04)

# Bồn cây cảnh & chậu hoa dọc lan can ban công trước
add_box(col_fl2_furn, "BalconyFront_PlanterBox", 1.20, -2.86, Z2, 3.60, -2.52, Z2 + 0.38, "Mat_DarkGreyStone", bevel=0.015)
for fi in range(5):
    fx = 1.48 + fi * 0.46
    add_sphere(col_fl2_furn, f"BalconyFront_Bush_{fi}", fx, -2.69, Z2 + 0.48, 0.18,
               "Mat_FoliageBright" if fi % 2 == 0 else "Mat_FoliageGreen", 1.1, 0.9, 0.75)
    add_sphere(col_fl2_furn, f"BalconyFront_Flower_{fi}", fx, -2.69, Z2 + 0.60, 0.07,
               "Mat_FlowerPink" if fi % 2 == 0 else "Mat_FlowerYellow")
add_potted_plant(col_fl2_furn, "BalconyFront_Plant1", 0.48, -2.45, Z2, scale=0.95, pot_mat="Mat_CeramicWhite")
add_potted_plant(col_fl2_furn, "BalconyFront_Plant2", 0.48, -0.75, Z2, scale=0.80, pot_mat="Mat_TerracottaPot")
add_potted_plant(col_fl2_furn, "BalconyFront_Plant3", 6.45, -2.45, Z2, scale=0.95, pot_mat="Mat_CeramicWhite")

# --- A. PHÒNG NGỦ MASTER CHỊ BA (Y = 0.22..7.0, X = 0.22..4.86) ---
add_box(col_fl2_furn, "Master_AreaRug", 0.45, 1.40, Z2, 3.05, 4.05, Z2 + 0.025, "Mat_RugWarm", bevel=0.008)
add_detailed_bed(col_fl2_furn, "Master_Bed", 0.78, 1.85, Z2 + 0.02, 2.72, 4.05, head_side='Y_MAX', duvet_mat="Mat_CushionNavy")
add_nightstand(col_fl2_furn, "Master_Nightstand_L", 0.50, 3.82, Z2 + 0.02)
add_nightstand(col_fl2_furn, "Master_Nightstand_R", 3.00, 3.82, Z2 + 0.02)
add_framed_art(col_fl2_furn, "Master_HeadArt", 1.75, 4.12, Z2 + 1.85, 1.30, 0.78, wall_axis='Y', canvas_mat="Mat_ArtCanvasWarm")
add_curtain_pair(col_fl2_furn, "Master_FrontCurtain", 0.72, 4.28, 0.28, Z2 + 0.04, H2 - 0.15)
add_pendant_chandelier(col_lights, "Master_Chandelier", 2.25, 2.30, H2 - 0.02, drop=0.72, count=3)

# 🎹 ĐÀN PIANO UPRIGHT CHI TIẾT ÁP TƯỜNG PHẢI (X=4.26..4.82) + GHẾ ĐÀN + GIÁ NHẠC + PEDAL ĐỒNG
add_box(col_fl2_furn, "Master_Piano_Body", 4.26, 0.85, Z2 + 0.04, 4.82, 2.38, Z2 + 1.24, "Mat_PianoBlackGloss", bevel=0.018)
add_box(col_fl2_furn, "Master_Piano_Keybed", 4.00, 0.88, Z2 + 0.66, 4.30, 2.35, Z2 + 0.75, "Mat_PianoBlackGloss", bevel=0.01)
add_box(col_fl2_furn, "Master_Piano_WhiteKeys", 4.02, 0.94, Z2 + 0.75, 4.26, 2.29, Z2 + 0.79, "Mat_CeramicWhite")
for bk in range(18):
    if bk % 7 not in (2, 6):
        by_k = 0.99 + bk * 0.070
        add_box(col_fl2_furn, f"Master_Piano_BlackKey_{bk}", 4.10, by_k, Z2 + 0.79, 4.25, by_k + 0.028, Z2 + 0.818, "Mat_MetalMatteBlack")
add_box(col_fl2_furn, "Master_Piano_SheetMusic", 4.22, 1.40, Z2 + 0.88, 4.26, 1.85, Z2 + 1.14, "Mat_BeddingWhite")
for pd in range(3):
    add_box(col_fl2_furn, f"Master_Piano_Pedal_{pd}", 4.16, 1.52 + pd * 0.09, Z2 + 0.05, 4.26, 1.56 + pd * 0.09, Z2 + 0.09, "Mat_BrassGold")
add_box(col_fl2_furn, "Master_Piano_BenchTop", 3.46, 1.25, Z2 + 0.44, 3.86, 1.98, Z2 + 0.52, "Mat_PianoBlackGloss", bevel=0.018)
for i, (lx, ly) in enumerate([(3.51, 1.30), (3.81, 1.30), (3.51, 1.93), (3.81, 1.93)]):
    add_cyl(col_fl2_furn, f"Master_Piano_BenchLeg_{i}", lx, ly, Z2, Z2 + 0.45, 0.022, 0.022, "Mat_PianoBlackGloss", segs=8)
add_framed_art(col_fl2_furn, "Master_PianoArt", 4.83, 1.62, Z2 + 1.92, 0.92, 0.68, wall_axis='X', canvas_mat="Mat_ArtCanvasBlue")

# 🧘 Góc Yoga & Thiền Master (đặt đón nắng sáng ngay trước cửa kính ban công, hoàn toàn không chắn lối đi!)
add_box(col_fl2_furn, "Master_YogaMat", 1.00, 0.58, Z2, 2.50, 1.38, Z2 + 0.025, "Mat_CushionMustard", bevel=0.008)
add_cyl(col_fl2_furn, "Master_MeditationCushion", 1.75, 0.98, Z2 + 0.025, Z2 + 0.14, 0.22, 0.20, "Mat_CushionTerracotta", segs=18)
add_potted_plant(col_fl2_furn, "Master_YogaPlant", 0.56, 0.72, Z2, scale=1.0, pot_mat="Mat_CeramicWhite")

# Vách ngăn sau giường Master — CÓ CỬA RỘNG (X=3.25..4.20) đi thẳng vào Walk-in Closet!
add_box(col_fl2_arch, "Master_Ensuite_Wall_L", 0.22, 4.15, Z2, 3.25, 4.25, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_Ensuite_Wall_Top", 3.25, 4.15, Z2 + 2.30, 4.20, 4.25, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_Ensuite_Wall_R", 4.20, 4.15, Z2, 4.86, 4.25, H2, "Mat_WallWarmWhite")
# Khung vòm gỗ sang trọng lối vào Walk-in Closet
add_box(col_fl2_arch, "Master_ClosetPortal_L", 3.22, 4.13, Z2, 3.28, 4.27, Z2 + 2.32, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_ClosetPortal_R", 4.17, 4.13, Z2, 4.23, 4.27, Z2 + 2.32, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_ClosetPortal_Top", 3.22, 4.13, Z2 + 2.28, 4.23, 4.27, Z2 + 2.34, "Mat_WoodOakDark")

# Vách ngăn WC Riêng & Walk-in Closet — CÓ CỬA VÀO WC (Y=4.36..5.22) kèm cửa trượt gỗ kính mờ!
add_box(col_fl2_arch, "Master_WC_Div_Front", 2.25, 4.25, Z2, 2.35, 4.36, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_WC_Div_Top", 2.25, 4.36, Z2 + 2.25, 2.35, 5.22, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_WC_Div_Solid", 2.25, 5.22, Z2, 2.35, 6.95, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_BackWall", 0.22, 6.92, Z2, 4.86, 7.02, H2, "Mat_WallWarmWhite")

# Khung cửa & Cánh cửa trượt vào Phòng tắm Master (mở hờ sang phía Y=5.0..5.86 để thấy rõ lối vào thoáng)
add_box(col_fl2_arch, "Master_WCDoor_Frame1", 2.23, 4.33, Z2, 2.37, 4.39, Z2 + 2.27, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_WCDoor_Frame2", 2.23, 5.19, Z2, 2.37, 5.25, Z2 + 2.27, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_WCDoor_FrameTop", 2.23, 4.33, Z2 + 2.23, 2.37, 5.25, Z2 + 2.29, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_WCDoor_Rail", 2.35, 4.35, Z2 + 2.26, 2.41, 6.05, Z2 + 2.31, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "Master_WCDoor_Leaf", 2.36, 4.98, Z2 + 0.02, 2.41, 5.84, Z2 + 2.24, "Mat_WoodOakTable", bevel=0.008)
add_box(col_fl2_arch, "Master_WCDoor_GlassInset", 2.35, 5.12, Z2 + 0.65, 2.42, 5.70, Z2 + 2.02, "Mat_GlassBronze")
add_box(col_fl2_arch, "Master_WCDoor_Handle", 2.41, 5.04, Z2 + 0.92, 2.45, 5.07, Z2 + 1.24, "Mat_BrassGold")

# Phòng tắm riêng Master (bố trí hợp lý, chừa sảnh bước từ cửa Y=4.36..5.22 hoàn toàn thông thoáng!)
# 1. Lavabo đá cẩm thạch + Gương tròn đèn LED áp vách trước bên trái (X=0.34..1.30, Y=4.28..4.82)
add_box(col_fl2_furn, "Master_VanityCabinet", 0.36, 4.28, Z2 + 0.16, 1.30, 4.82, Z2 + 0.82, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl2_furn, "Master_VanityTop", 0.34, 4.26, Z2 + 0.82, 1.32, 4.85, Z2 + 0.86, "Mat_WhiteMarble")
add_cyl(col_fl2_furn, "Master_SinkBasin", 0.83, 4.55, Z2 + 0.86, Z2 + 0.98, 0.18, 0.22, "Mat_CeramicWhite", segs=18)
add_cyl(col_fl2_furn, "Master_SinkFaucet", 0.83, 4.36, Z2 + 0.86, Z2 + 1.08, 0.018, 0.014, "Mat_BrassGold", segs=10)
add_cyl(col_fl2_furn, "Master_Mirror", 0.83, 4.27, Z2 + 1.48, Z2 + 1.52, 0.36, 0.36, "Mat_Mirror", rot=(math.pi / 2, 0, 0), segs=22)
add_cyl(col_lights, "Master_MirrorLED", 0.83, 4.25, Z2 + 1.48, Z2 + 1.50, 0.39, 0.39, "Mat_WarmLED", rot=(math.pi / 2, 0, 0), segs=22)

# 2. Bồn cầu đặt kín đáo sau mảng tường đặc bên phải (X=1.62..2.22, Y=5.36..5.86) + Vách kính ngăn nước
add_box(col_fl2_furn, "Master_ToiletTank", 1.96, 5.42, Z2 + 0.40, 2.23, 5.82, Z2 + 0.82, "Mat_CeramicWhite", bevel=0.03)
add_cyl(col_fl2_furn, "Master_ToiletBowl", 1.76, 5.62, Z2, Z2 + 0.42, 0.18, 0.22, "Mat_CeramicWhite", segs=16)
add_box(col_fl2_furn, "Master_WC_GlassScreen", 1.48, 5.94, Z2, 2.24, 5.97, Z2 + 2.05, "Mat_GlassClear")

# 3. Bồn tắm nằm cao cấp đặt ngang sát tường sau (X=0.34..1.88, Y=6.04..6.86) + Thảm chân & Vòi đồng
add_box(col_fl2_furn, "Master_Bathtub_Outer", 0.34, 6.04, Z2, 1.88, 6.86, Z2 + 0.58, "Mat_CeramicWhite", bevel=0.10)
add_box(col_fl2_furn, "Master_Bathtub_Water", 0.46, 6.14, Z2 + 0.46, 1.76, 6.76, Z2 + 0.52, "Mat_WaterClear")
add_cyl(col_fl2_furn, "Master_TubFaucet", 1.96, 6.45, Z2, Z2 + 0.78, 0.025, 0.022, "Mat_BrassGold", segs=10)
add_box(col_fl2_furn, "Master_BathMat", 0.72, 5.54, Z2, 1.42, 5.94, Z2 + 0.02, "Mat_RugWarm", bevel=0.006)
add_pendant_chandelier(col_lights, "Master_WC_Lamp", 1.25, 5.40, H2 - 0.02, drop=0.38, count=1)

# Walk-in Closet Master (liên thông Phòng ngủ -> Phòng thay đồ -> Cửa phòng tắm cực chuẩn!)
add_box(col_fl2_furn, "Master_Closet_Left", 2.38, 5.88, Z2, 2.92, 6.88, Z2 + 2.55, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl2_furn, "Master_Closet_Right", 4.30, 4.32, Z2, 4.84, 6.88, Z2 + 2.55, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_lights, "Master_Closet_LED1", 2.90, 5.92, Z2 + 2.46, 2.94, 6.84, Z2 + 2.50, "Mat_WarmLED")
add_box(col_lights, "Master_Closet_LED2", 4.27, 4.38, Z2 + 2.46, 4.31, 6.82, Z2 + 2.50, "Mat_WarmLED")
cloth_mats = ["Mat_CushionBlush", "Mat_CushionNavy", "Mat_BeddingWhite", "Mat_CushionSage", "Mat_CushionMustard", "Mat_CushionTerracotta"]
for gi in range(8):
    gy = 4.65 + gi * 0.26
    add_box(col_fl2_furn, f"Master_Clothes_{gi}", 4.14, gy, Z2 + 1.15, 4.30, gy + 0.12, Z2 + 2.05, cloth_mats[gi % len(cloth_mats)], bevel=0.015)
add_cyl(col_fl2_furn, "Master_Closet_Ottoman", 3.60, 6.18, Z2, Z2 + 0.44, 0.34, 0.34, "Mat_CushionBlush", segs=18)

# --- B. SẢNH CẦU THANG & GIẾNG TRỜI (Y = 7.0..11.2, nối liền hành lang 2m) ---
add_potted_plant(col_fl2_furn, "Fl2_AtriumPlant", 4.45, 8.20, Z2, scale=1.10, pot_mat="Mat_CeramicWhite")

# --- C. PHÒNG SẾU — EM ÚT MỞ RỘNG 4.7M (X = 0.22..4.86, Y = 11.20..13.45) ---
add_box(col_fl2_arch, "Wall_Fl2_Seu_Front", 0.22, 11.15, Z2, 4.86, 11.25, H2, "Mat_WallWarmWhite")

add_box(col_fl2_furn, "Seu_Rug", 2.15, 11.35, Z2, 4.78, 13.25, Z2 + 0.025, "Mat_RugPattern", bevel=0.008)
add_detailed_bed(col_fl2_furn, "Seu_Bed", 2.75, 11.36, Z2 + 0.02, 4.80, 12.56, head_side='X_MAX', duvet_mat="Mat_CushionSage")
add_nightstand(col_fl2_furn, "Seu_Nightstand", 2.42, 11.55, Z2 + 0.02)
add_study_desk_set(col_fl2_furn, "Seu_Desk", 0.34, 12.76, Z2, 1.72, 13.36, chair_side='Y_MIN')
add_box(col_fl2_furn, "Seu_Shelf", 0.38, 13.22, Z2 + 1.45, 1.64, 13.42, Z2 + 1.50, "Mat_WoodOakTable")
add_books_row(col_fl2_furn, "Seu_Books", 0.46, 13.24, Z2 + 1.50, count=9, axis='X')
add_wardrobe(col_fl2_furn, "Seu_Wardrobe", 0.32, 11.28, Z2, 1.78, 11.82, h=2.40, door_face='Y_MAX')
add_framed_art(col_fl2_furn, "Seu_Art", 4.83, 11.96, Z2 + 1.85, 0.95, 0.65, wall_axis='X', canvas_mat="Mat_ArtCanvasGreen")
add_pendant_chandelier(col_lights, "Seu_Lamp", 2.55, 12.35, H2 - 0.02, drop=0.45, count=1)

# --- D. PHÒNG CHỊ HAI MỞ RỘNG 4.7M (X = 0.22..4.86, Y = 13.50..15.78) ---
add_box(col_fl2_arch, "Wall_Fl2_Sister2", 0.22, 13.45, Z2, 4.86, 13.55, H2, "Mat_WallWarmWhite")

add_box(col_fl2_furn, "Sister2_Rug", 2.15, 13.65, Z2, 4.78, 15.55, Z2 + 0.025, "Mat_RugWarm", bevel=0.008)
add_detailed_bed(col_fl2_furn, "Sister2_Bed", 2.75, 13.66, Z2 + 0.02, 4.80, 14.86, head_side='X_MAX', duvet_mat="Mat_CushionBlush")
add_nightstand(col_fl2_furn, "Sister2_Nightstand", 2.42, 13.85, Z2 + 0.02)
add_study_desk_set(col_fl2_furn, "Sister2_Desk", 0.34, 13.62, Z2, 1.72, 14.22, chair_side='Y_MAX')
add_box(col_fl2_furn, "Sister2_Shelf", 0.38, 13.58, Z2 + 1.45, 1.64, 13.78, Z2 + 1.50, "Mat_WoodOakTable")
add_books_row(col_fl2_furn, "Sister2_Books", 0.46, 13.60, Z2 + 1.50, count=9, axis='X')
add_wardrobe(col_fl2_furn, "Sister2_Wardrobe", 0.26, 15.16, Z2, 1.28, 15.72, h=2.40, door_face='Y_MIN')
add_framed_art(col_fl2_furn, "Sister2_Art", 4.83, 14.26, Z2 + 1.85, 0.95, 0.65, wall_axis='X', canvas_mat="Mat_ArtCanvasBlue")
add_pendant_chandelier(col_lights, "Sister2_Lamp", 2.55, 14.65, H2 - 0.02, drop=0.45, count=1)

# --- E. BAN CÔNG SAU CHỮ L SIÊU RỘNG (7M Ở Y=16..20.2, 5M Ở Y=20.2..24 CHỪA NẮNG VƯỜN RAU) ---
add_box(col_fl2_arch, "BalconyRear_Rail_End", 0.0, 23.94, Z2, 5.0, 24.0, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Top_End", 0.0, 23.92, Z2 + 1.10, 5.0, 24.02, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "BalconyRear_Rail_L", 0.0, 16.0, Z2, 0.06, 24.0, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Top_L", -0.02, 16.0, Z2 + 1.10, 0.08, 24.0, Z2 + 1.16, "Mat_MetalMatteBlack")
# Lan can phải chữ L: chạy X=7.0 từ Y=16..20.2, ngoặt ngang Y=20.2 từ X=5..7, rồi chạy X=5.0 từ Y=20.2..24
add_box(col_fl2_arch, "BalconyRear_Rail_R1", 6.94, 16.0, Z2, 7.0, 20.20, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Top_R1", 6.92, 16.0, Z2 + 1.10, 7.02, 20.22, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "BalconyRear_Rail_Step", 5.0, 20.14, Z2, 7.0, 20.20, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Top_Step", 4.98, 20.12, Z2 + 1.10, 7.02, 20.22, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "BalconyRear_Rail_R2", 4.94, 20.20, Z2, 5.0, 24.0, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Top_R2", 4.92, 20.20, Z2 + 1.10, 5.02, 24.0, Z2 + 1.16, "Mat_MetalMatteBlack")

# Góc Yoga ngoài trời & Khu Lounge Chill tắm trăng trên phần ban công mở rộng 7m
add_box(col_fl2_furn, "BalconyRear_YogaDeck", 0.55, 16.8, Z2, 2.35, 19.6, Z2 + 0.05, "Mat_WoodOakTable")
add_box(col_fl2_furn, "BalconyRear_YogaMat", 0.95, 17.2, Z2 + 0.05, 1.95, 19.2, Z2 + 0.08, "Mat_CushionMustard", bevel=0.01)
add_cyl(col_fl2_furn, "BalconyRear_Cushion", 1.45, 18.2, Z2 + 0.08, Z2 + 0.20, 0.22, 0.20, "Mat_CushionSage", segs=18)

add_box(col_fl2_furn, "BalconyRear_LoungeBench", 5.45, 16.9, Z2 + 0.08, 6.45, 19.6, Z2 + 0.45, "Mat_WoodOakTable", bevel=0.02)
add_box(col_fl2_furn, "BalconyRear_LoungeBack", 6.22, 16.9, Z2 + 0.45, 6.48, 19.6, Z2 + 0.88, "Mat_WoodLouverFacade")
add_box(col_fl2_furn, "BalconyRear_LoungePad", 5.50, 16.96, Z2 + 0.45, 6.22, 19.54, Z2 + 0.55, "Mat_BeddingCream", bevel=0.02)
add_box(col_fl2_furn, "BalconyRear_CoffeeTable", 4.45, 17.60, Z2 + 0.36, 5.20, 18.95, Z2 + 0.42, "Mat_WhiteMarble", bevel=0.012)
for i, (lx, ly) in enumerate([(4.52, 17.68), (5.12, 17.68), (4.52, 18.88), (5.12, 18.88)]):
    add_cyl(col_fl2_furn, f"BalconyRear_TableLeg_{i}", lx, ly, Z2, Z2 + 0.36, 0.025, 0.025, "Mat_MetalMatteBlack")
add_potted_plant(col_fl2_furn, "BalconyRear_Plant1", 0.55, 20.2, Z2, scale=1.15, pot_mat="Mat_TerracottaPot")
add_potted_plant(col_fl2_furn, "BalconyRear_Plant2", 6.45, 19.75, Z2, scale=1.10, pot_mat="Mat_CeramicWhite")
add_potted_plant(col_fl2_furn, "BalconyRear_Plant3", 0.55, 23.3, Z2, scale=1.0, pot_mat="Mat_DarkGreyStone")
add_potted_plant(col_fl2_furn, "BalconyRear_Plant4", 4.45, 23.3, Z2, scale=1.0, pot_mat="Mat_DarkGreyStone")

# Giàn phơi cuối ban công sau + quần áo phơi
for pr in range(3):
    py = 21.4 + pr * 0.65
    add_box(col_fl2_furn, f"BalconyRear_DryingRod_{pr}", 1.1, py, Z2 + 1.85, 3.9, py + 0.04, Z2 + 1.89, "Mat_MetalStainless")
    for px in [1.1, 3.9]:
        add_cyl(col_fl2_furn, f"BalconyRear_DryPost_{pr}_{px:.1f}", px, py + 0.02, Z2, Z2 + 1.88, 0.02, 0.02, "Mat_MetalStainless", segs=8)
    for cl in range(3):
        cx_c = 1.55 + cl * 0.85
        add_box(col_fl2_furn, f"BalconyRear_Cloth_{pr}_{cl}", cx_c - 0.22, py - 0.01, Z2 + 1.15, cx_c + 0.22, py + 0.05, Z2 + 1.82,
                cloth_mats[(pr * 3 + cl) % len(cloth_mats)], bevel=0.012)

# ---------------------------------------------------------------------------
# 8. TẦNG MÁI MỞ RỘNG 7M & 9 TẤM PIN SOLAR PV
# ---------------------------------------------------------------------------
ZR = 7.35
add_box(col_roof, "Roof_Fascia", -0.25, -0.35, ZR, 7.25, 16.35, ZR + 0.24, "Mat_RoofCharcoal")
add_box(col_lights, "Roof_Fascia_LED", -0.22, -0.36, ZR - 0.04, 7.22, -0.32, ZR, "Mat_WarmLED")
add_box(col_roof, "Roof_Slab", 0.05, 0.05, ZR + 0.24, 6.95, 15.95, ZR + 0.30, "Mat_WallWarmWhite")
add_box(col_roof, "Roof_SkylightFrame", 1.35, 7.15, ZR + 0.30, 3.55, 10.05, ZR + 0.62, "Mat_MetalMatteBlack")
add_box(col_roof, "Roof_SkylightGlass", 1.45, 7.25, ZR + 0.56, 3.45, 9.95, ZR + 0.66, "Mat_GlassClear")
add_cyl(col_roof, "Roof_WaterTank", 1.35, 13.8, ZR + 0.55, ZR + 1.95, 0.65, 0.65, "Mat_MetalStainless", rot=(math.pi / 2, 0, 0))
add_box(col_roof, "Roof_WaterTankStand", 0.80, 13.1, ZR + 0.30, 1.90, 14.5, ZR + 0.55, "Mat_MetalMatteBlack")
for p in range(3):
    py = 1.8 + p * 1.68
    add_box(col_roof, f"SolarPV_L_{p}", 0.55, py, ZR + 0.34, 2.30, py + 1.42, ZR + 0.42, "Mat_SolarPVPanels", rot=(0.12, 0, 0))
    add_box(col_roof, f"SolarPV_M_{p}", 2.65, py, ZR + 0.34, 4.40, py + 1.42, ZR + 0.42, "Mat_SolarPVPanels", rot=(0.12, 0, 0))
    add_box(col_roof, f"SolarPV_R_{p}", 4.75, py, ZR + 0.34, 6.50, py + 1.42, ZR + 0.42, "Mat_SolarPVPanels", rot=(0.12, 0, 0))

# ---------------------------------------------------------------------------
# 9. HỆ THỐNG SMART HOME, ĐIỆN, WIFI MESH 6E, CAMERA AI & NHÃN 3D
# ---------------------------------------------------------------------------
# Tủ điện tổng MDB + Inverter Solar 5kW gầm thang
add_box(col_smarthome, "Main_MDB_Electrical", 3.82, 9.25, Z1 + 0.90, 3.98, 9.85, Z1 + 1.85, "Mat_MetalStainless", bevel=0.01)
add_box(col_smarthome, "MDB_StatusLED", 3.98, 9.35, Z1 + 1.30, 4.00, 9.75, Z1 + 1.70, "Mat_SmartGreenLED")
add_box(col_smarthome, "Hybrid_Inverter_5kW", 3.82, 9.95, Z1 + 0.95, 3.98, 10.45, Z1 + 1.70, "Mat_CeramicWhite", bevel=0.015)
add_box(col_smarthome, "Inverter_Screen", 3.98, 10.08, Z1 + 1.35, 4.00, 10.32, Z1 + 1.55, "Mat_SmartCyanLED")

# Sạc xe điện EV Wallbox tại sân trước
add_box(col_smarthome, "EV_Wallbox_Charger", 0.02, -11.50, 1.10, 0.22, -11.10, 1.65, "Mat_CeramicWhite", bevel=0.02)
add_box(col_smarthome, "EV_Wallbox_LED", 0.22, -11.38, 1.25, 0.24, -11.22, 1.52, "Mat_SmartGreenLED")

# Màn hình Trung tâm Điều khiển Smart Home 10 inch ở Phòng khách (ngay sảnh cửa chính)
add_box(col_smarthome, "Smart_ControlPanel_10in", 4.74, 1.85, Z1 + 1.45, 4.78, 2.18, Z1 + 1.68, "Mat_MetalMatteBlack")
add_box(col_smarthome, "Smart_ControlScreen", 4.73, 1.88, Z1 + 1.48, 4.75, 2.15, Z1 + 1.65, "Mat_SmartCyanLED")

# 3 Node WiFi Mesh 6E
wifi_nodes = [
    ("WiFi_Mesh_Node1_Living", 0.50, 3.15, Z1 + 0.50),
    ("WiFi_Mesh_Node2_Kitchen", 4.66, 11.80, Z1 + 2.40),
    ("WiFi_Mesh_Node3_Fl2Hall", 5.95, 7.60, Z2 + 3.20),
]
for wname, wx, wy, wz in wifi_nodes:
    add_cyl(col_smarthome, wname, wx, wy, wz, wz + 0.20, 0.065, 0.055, "Mat_CeramicWhite", segs=16)
    add_cyl(col_smarthome, f"{wname}_LED", wx, wy, wz + 0.18, wz + 0.205, 0.058, 0.058, "Mat_SmartCyanLED", segs=16)

# 5 Điều hòa Inverter treo tường
ac_units = [
    ("AC_Living", 4.54, 3.70, Z1 + 2.75, 'X'),
    ("AC_Parents", 3.74, 7.35, Z1 + 2.75, 'X'),
    ("AC_Master", 4.62, 1.60, Z2 + 2.75, 'X'),
    ("AC_Seu", 4.62, 11.95, Z2 + 2.75, 'X'),
    ("AC_Sister2", 4.62, 14.25, Z2 + 2.75, 'X'),
]
for aname, ax, ay, az, _ in ac_units:
    add_box(col_smarthome, aname, ax, ay - 0.45, az, ax + 0.24, ay + 0.45, az + 0.30, "Mat_CeramicWhite", bevel=0.025)
    add_box(col_smarthome, f"{aname}_Vane", ax - 0.01, ay - 0.40, az + 0.03, ax + 0.04, ay + 0.40, az + 0.07, "Mat_MetalMatteBlack")

# 6 Camera An Ninh PoE AI + Nón góc quét FOV bán trong suốt
cams = [
    ("Cam1_MainGate", 0.35, -17.85, 2.55, (0.3, 0, -0.5)),
    ("Cam2_FrontYard", 4.90, -0.15, 3.15, (0.4, 0, -2.5)),
    ("Cam3_SideCorridor", 5.20, 8.0, 3.45, (0.4, 0, -0.2)),
    ("Cam4_RearGarden", 4.80, 16.10, 3.10, (0.4, 0, 0.3)),
    ("Cam5_LivingRoom", 4.65, 5.55, Z1 + 3.05, (0.4, 0, 2.6)),
    ("Cam6_BalconyFl2", 6.75, -0.15, Z2 + 2.95, (0.35, 0, -2.5)),
]
for cname, cx, cy, cz, crot in cams:
    add_box(col_smarthome, cname, cx - 0.08, cy - 0.12, cz - 0.07, cx + 0.08, cy + 0.12, cz + 0.07, "Mat_CeramicWhite", bevel=0.02, rot=crot)
    add_cyl(col_smarthome, f"{cname}_Lens", cx, cy, cz - 0.04, cz + 0.04, 0.045, 0.045, "Mat_SmartCyanLED", segs=12)

# Nhãn nổi 3D gọn đẹp, không đổ bóng lên nội thất (có thể ẩn/hiện trong Outliner)
def add_3d_label(col, name, text_str, loc, rot_z=-math.pi / 2):
    curve = bpy.data.curves.new(type="FONT", name=f"{name}_Font")
    curve.body = text_str
    curve.align_x = 'CENTER'
    curve.size = 0.24 * S
    curve.extrude = 0.012 * S
    obj = bpy.data.objects.new(name, curve)
    obj.location = (loc[0] * S, loc[1] * S, loc[2] * S)
    obj.rotation_euler = (math.pi / 2, 0, rot_z)
    obj.visible_shadow = False
    obj.data.materials.append(bpy.data.materials["Mat_CalloutText"])
    col.objects.link(obj)
    return obj

add_3d_label(col_callouts, "Label_Altar", "GIAN THO", (-0.30, 1.15, 3.25))
add_3d_label(col_callouts, "Label_Living", "PHONG KHACH", (-0.30, 4.00, 3.25))
add_3d_label(col_callouts, "Label_Parents", "PHONG BA ME", (-0.30, 7.3, 3.25))
add_3d_label(col_callouts, "Label_Kitchen", "BEP & BAN AN", (-0.30, 13.5, 3.25))
add_3d_label(col_callouts, "Label_Master", "MASTER CHI BA", (-0.30, 2.6, 6.85))
add_3d_label(col_callouts, "Label_Seu", "PHONG SEU", (-0.30, 12.2, 6.85))
add_3d_label(col_callouts, "Label_Sister2", "PHONG CHI HAI", (-0.30, 14.7, 6.85))
add_3d_label(col_callouts, "Label_Fl2_Corridor", "HANH LANG TANG 2 (2M)", (7.30, 8.0, 6.90), rot_z=math.pi / 2)

# ---------------------------------------------------------------------------
# 10. LIGHTING, WORLD, CAMERA & VIEWPORT MATERIAL PREVIEW SETUP
# ---------------------------------------------------------------------------
def add_warm_light(name, loc, energy=260.0, color=(1.0, 0.84, 0.58), radius=0.35, cast_shadow=False):
    ld = bpy.data.lights.new(name=name, type='POINT')
    ld.energy = energy * (S * S)
    ld.color = color
    ld.shadow_soft_size = radius * S
    ld.use_shadow = cast_shadow
    lo = bpy.data.objects.new(name, ld)
    lo.location = (loc[0] * S, loc[1] * S, loc[2] * S)
    col_lights.objects.link(lo)
    return lo

# Ánh sáng mặt trời nhẹ ban ngày + đèn ấm nội thất
sun_data = bpy.data.lights.new(name="Sun_Daylight", type='SUN')
sun_data.energy = 2.6
sun_data.color = (1.0, 0.96, 0.88)
sun_obj = bpy.data.objects.new("Sun_Daylight", sun_data)
sun_obj.rotation_euler = (math.radians(48), math.radians(-22), math.radians(-55))
col_lights.objects.link(sun_obj)

add_warm_light("Light_FrontCanopy", (2.5, -4.5, 3.1), 240.0)
add_warm_light("Light_DadTeaWall", (1.1, -3.5, 2.2), 180.0)
add_warm_light("Light_AltarNook", (1.3, 1.1, 3.1), 190.0, cast_shadow=True)
add_warm_light("Light_LivingNew", (2.6, 3.8, 3.1), 320.0, cast_shadow=True)
add_warm_light("Light_ParentsBed", (2.2, 7.3, 3.1), 240.0)
add_warm_light("Light_KitchenNew", (2.6, 13.5, 3.1), 340.0, cast_shadow=True)
add_warm_light("Light_Fl1_CorridorUnder", (5.95, 8.0, 3.4), 220.0)
add_warm_light("Light_MasterFront", (2.3, 2.5, 6.6), 340.0, cast_shadow=True)
add_warm_light("Light_MasterWC", (1.6, 5.5, 6.6), 200.0)
add_warm_light("Light_Seu", (2.5, 12.2, 6.6), 240.0)
add_warm_light("Light_Sister2", (2.5, 14.6, 6.6), 240.0)
add_warm_light("Light_Fl2_Corridor1", (5.95, 4.2, 6.7), 220.0)
add_warm_light("Light_Fl2_Corridor2", (5.95, 11.8, 6.7), 220.0)
add_warm_light("Light_BalconyRear8m", (3.2, 19.2, 5.6), 240.0)

# Môi trường bầu trời dịu sáng
world = bpy.context.scene.world
if not world:
    world = bpy.data.worlds.new("Fullhouse_World")
    bpy.context.scene.world = world
world.use_nodes = True
wnodes = world.node_tree.nodes
bg = wnodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.38, 0.48, 0.62, 1.0)
    bg.inputs[1].default_value = 0.75

# Camera mặc định nhìn từ góc cắt bên trái (-X) thấy rõ cả mặt tiền và toàn bộ nội thất 2 tầng
def point_at(obj, target):
    from mathutils import Vector
    direction = Vector(target) - obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()

cam_data = bpy.data.cameras.new(name="Main_Cutaway_Camera")
cam_data.lens = 32.0
cam_data.clip_end = 500.0
cam_obj = bpy.data.objects.new("Main_Cutaway_Camera", cam_data)
cam_obj.location = (-16.0 * S, -7.5 * S, 9.5 * S)
point_at(cam_obj, (2.5 * S, 7.0 * S, 3.4 * S))
col_main.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Tự động bật sẵn chế độ Material Preview (có màu sắc & vật liệu ngay khi mở file)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    space.shading.use_scene_lights = True
                    space.shading.use_scene_world = False
                    space.clip_end = 500.0
                    # Căn góc nhìn viewport sang phía mặt cắt bên trái
                    if space.region_3d:
                        space.region_3d.view_location = (2.5 * S, 6.0 * S, 3.2 * S)
                        space.region_3d.view_distance = 22.0 * S
                        space.region_3d.view_rotation = cam_obj.rotation_euler.to_quaternion()

# ---------------------------------------------------------------------------
# 11. SAVE .BLEND & EXPORT .OBJ
# ---------------------------------------------------------------------------
save_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else r"C:\Users\Administrator\.gemini\antigravity\scratch\myhome"
blend_path = os.path.join(save_dir, "Fullhouse_Model.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

obj_path = os.path.join(save_dir, "Fullhouse_Model.obj")
try:
    bpy.ops.wm.obj_export(filepath=obj_path)
    print(f"Exported OBJ to {obj_path}")
except Exception as e:
    print("Note: OBJ export skipped:", e)

print("=" * 70)
print(f"SUCCESS: Enhanced Fullhouse Model (Scale {SCALE_FACTOR}x) saved to {blend_path}")
print(f"Total objects created: {len(bpy.data.objects)}")
print("=" * 70)
