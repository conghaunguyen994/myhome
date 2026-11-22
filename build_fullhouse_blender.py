"""
=============================================================================
FULLHOUSE 3D ARCHITECTURAL & SMART HOME MODEL FOR BLENDER (ENHANCED EDITION)
Phiên bản nâng cấp chi tiết Nội thất, Trang trí & Tỉ lệ phóng lớn (1.5x)
+ Quy hoạch Đường luồng 2m & Hành lang Tầng 2 chuyển sang PHÍA NAM (bên trái
  khi nhìn từ đường Quốc lộ hướng Đông vào) để tránh gió bấc mùa đông và đón
  gió Nam/Đông Nam mát mẻ:
- Khối nhà chính 5m x 16m đặt phía Bắc (X = 2.0..7.0) đóng vai trò tường chắn
  gió bấc; Đường luồng 2m Tầng 1 & Hành lang 2m Tầng 2 đặt phía Nam (X = 0..2).
- Phóng to toàn bộ mô hình 1.5x (SCALE_FACTOR = 1.5) giúp dễ quan sát, zoom cận
  cảnh và chiêm ngưỡng từng chi tiết nội thất bên trong.
- Mở thoáng vách cắt bên phải (phía Bắc, X = 7.0, không bị tường rào che khuất)
  giúp nhìn xuyên vào toàn bộ các phòng Tầng 1 & Tầng 2 như mô hình kiến trúc.
- Bổ sung đầy đủ đồ nội thất & đồ trang trí chi tiết:
  + Sân trước: Bộ trà cụ đầy đủ của Ba áp tường rào Bắc kín gió bấc, ô tô SUV
    có bánh xe/kính/đèn phía Bắc, cây bonsai nhiều tán, đá bước dặm & đèn nấm
    dọc lối đường luồng phía Nam.
  + Phòng khách: Sofa chữ L + gối tựa nhiều màu + thảm dệt, bàn trà + bình hoa
    + sách decor, kệ TV + loa soundbar + cây xanh áp tường Bắc, bàn thờ Quan Âm
    góc Bắc mặt tiền quay hướng Đông có vách ngăn CNC trang nghiêm, tranh bộ 3,
    rèm cửa, đèn chùm hiện đại & đèn cây đứng.
  + Phòng Ba Mẹ: Giường gỗ có đầu giường + chăn gối + thảm, 2 tab đầu giường +
    đèn ngủ ấm áp, tủ áo có tay nắm, tranh nghệ thuật, cây xanh.
  + Cầu thang chữ U hoàn chỉnh 2 vế + lan can kính tay vịn gỗ + LED mũi bậc.
  + Bếp mở & Bàn ăn: Tủ bếp dọc tường Bắc đầy đủ bếp từ, bồn rửa + vòi nước,
    máy hút mùi, lò vi sóng, bình siêu tốc, đĩa trái cây, tủ lạnh 2 cánh; bàn ăn
    tròn + 6 ghế ăn có tựa lưng + đèn thả 3 bóng + bình hoa; cửa sổ mở sang
    đường luồng phía Nam đón gió mát.
  + Tầng 2 Phòng Master Chị Ba: Giường King + đầu giường bọc nỉ + 4 gối + thảm
    + 2 tab đèn ngủ + tranh; Đàn Piano Upright chi tiết (phím trắng/đen, giá nhạc,
    pedal đồng, ghế đàn); Góc Yoga (thảm, bồ đoàn thiền, cây xanh, nến); Phòng tắm
    riêng (bồn tắm nằm, lavabo gương LED, bồn cầu, vách kính); Walk-in Closet có
    kệ quần áo & thanh treo đồ; rèm cửa sổ cao kịch trần.
  + Hành lang Tầng 2 (2m phía Nam): 4 ô cửa kính toàn cảnh hướng Nam đón gió
    Nam tránh gió bấc, ghế đọc sách, console hoa, cây xanh và đèn thả ấm áp.
  + Phòng Sếu & Phòng Chị Hai: Giường, tab đèn ngủ, bàn học + ghế + laptop/màn
    hình + đèn bàn, kệ sách nhiều màu, tủ quần áo, tranh treo tường, thảm.
  + Ban công trước (7x3m) & sau chữ L: Bàn ghế chill ngoài trời, chậu cây, góc
    Yoga tắm trăng, giàn phơi có quần áo, chừa nắng phía Nam cho vườn rau T1.
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

def add_refined_interior_window(col, light_col, prefix, x1, y_center, z1, x2, z2,
                                sill_side='Y_MAX', panes=3, with_led=False, with_decor=False):
    """Cửa sổ nội thất Japandi tinh tế: khung hộp gỗ sồi bo viền + bệ cửa gỗ nhô thanh thoát
    + đố nhôm mảnh 3 ô cân đối + rèm cuốn linen gọn trên đỉnh khung."""
    casing_t = 0.036
    y_c1, y_c2 = y_center - 0.082, y_center + 0.082
    y_s1 = y_center - 0.165 if sill_side == 'Y_MIN' else y_center - 0.085
    y_s2 = y_center + 0.165 if sill_side == 'Y_MAX' else y_center + 0.085

    # 1. Khung hộp gỗ sồi ấm (bệ cửa nhô thanh lịch + viền 3 cạnh)
    add_box(col, f"{prefix}_OakSill", x1 - 0.04, y_s1, z1 - 0.015, x2 + 0.04, y_s2, z1 + 0.025, "Mat_WoodOakTable", bevel=0.008)
    add_box(col, f"{prefix}_OakTop", x1 - 0.03, y_c1, z2 - casing_t, x2 + 0.03, y_c2, z2 + 0.008, "Mat_WoodOakTable", bevel=0.006)
    add_box(col, f"{prefix}_OakL", x1 - 0.01, y_c1, z1 + 0.025, x1 + casing_t, y_c2, z2 - casing_t, "Mat_WoodOakTable", bevel=0.005)
    add_box(col, f"{prefix}_OakR", x2 - casing_t, y_c1, z1 + 0.025, x2 + 0.01, y_c2, z2 - casing_t, "Mat_WoodOakTable", bevel=0.005)

    # 2. Kính trong & hệ đố nhôm đen hệ slim chia 3 ô cân đối + nan ngang thoáng phía trên
    gx1, gx2 = x1 + casing_t, x2 - casing_t
    gz1, gz2 = z1 + 0.025, z2 - casing_t
    ft = 0.022
    add_box(col, f"{prefix}_Glass", gx1, y_center - 0.008, gz1, gx2, y_center + 0.008, gz2, "Mat_GlassClear")
    add_box(col, f"{prefix}_AluTop", gx1, y_center - 0.018, gz2 - ft, gx2, y_center + 0.018, gz2, "Mat_MetalMatteBlack")
    add_box(col, f"{prefix}_AluBot", gx1, y_center - 0.018, gz1, gx2, y_center + 0.018, gz1 + ft, "Mat_MetalMatteBlack")
    add_box(col, f"{prefix}_AluL", gx1, y_center - 0.018, gz1, gx1 + ft, y_center + 0.018, gz2, "Mat_MetalMatteBlack")
    add_box(col, f"{prefix}_AluR", gx2 - ft, y_center - 0.018, gz1, gx2, y_center + 0.018, gz2, "Mat_MetalMatteBlack")
    # Đố đứng chia 3 ô đều nhau (mảnh 2.2cm)
    span_x = gx2 - gx1
    for pi in range(1, panes):
        mx = gx1 + span_x * (pi / float(panes))
        add_box(col, f"{prefix}_Mullion_{pi}", mx - ft * 0.45, y_center - 0.018, gz1, mx + ft * 0.45, y_center + 0.018, gz2, "Mat_MetalMatteBlack")
    # Nan ngang mảnh phía trên tạo tỷ lệ kiến trúc tinh tế
    z_transom = gz2 - 0.22
    add_box(col, f"{prefix}_Transom", gx1, y_center - 0.016, z_transom - 0.009, gx2, y_center + 0.016, z_transom + 0.009, "Mat_MetalMatteBlack")

    # 3. Hộp rèm cuốn vải linen kéo gọn phía trên (kéo xuống khi Ba Mẹ cần riêng tư)
    y_sh = y_center + 0.048 if sill_side == 'Y_MAX' else y_center - 0.048
    add_box(col, f"{prefix}_ShadeValance", gx1 + 0.01, y_sh - 0.016, gz2 - 0.11, gx2 - 0.01, y_sh + 0.016, gz2 - 0.01, "Mat_CurtainLinen", bevel=0.006)
    add_box(col, f"{prefix}_ShadeBar", gx1 + 0.01, y_sh - 0.012, gz2 - 0.125, gx2 - 0.01, y_sh + 0.012, gz2 - 0.108, "Mat_BrassGold", bevel=0.003)

    # 4. Đèn LED hắt ấm âm dưới bệ cửa sổ (chiếu dịu xuống đầu giường)
    if with_led:
        y_led = y_center - 0.12 if sill_side == 'Y_MIN' else y_center + 0.12
        add_box(light_col, f"{prefix}_UnderSillLED", x1 + 0.04, y_led - 0.012, z1 - 0.025, x2 - 0.04, y_led + 0.012, z1 - 0.014, "Mat_WarmLED")

    # 5. Chậu cây mini & bình gốm nhỏ đặt tinh tế 2 góc bệ cửa sổ (giữ thoáng tầm nhìn ở giữa)
    if with_decor:
        y_dec = y_center + 0.105 if sill_side == 'Y_MAX' else y_center - 0.105
        add_cyl(col, f"{prefix}_SillVase", x1 + 0.18, y_dec, z1 + 0.025, z1 + 0.16, 0.036, 0.024, "Mat_CeramicTeal", segs=14)
        add_cyl(col, f"{prefix}_MiniPot", x2 - 0.18, y_dec, z1 + 0.025, z1 + 0.105, 0.042, 0.048, "Mat_CeramicWhite", segs=14)
        add_sphere(col, f"{prefix}_MiniPlant", x2 - 0.18, y_dec, z1 + 0.145, 0.055, "Mat_FoliageBright", sx=1.1, sy=1.1, sz=0.75)

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

def add_detailed_bed(col, prefix, x1, y1, z0, x2, y2, head_side='X_MAX', duvet_mat="Mat_CushionNavy", pillow_mat="Mat_BeddingWhite", headboard_h=1.24):
    # Khung giường gỗ & chân
    add_box(col, f"{prefix}_Frame", x1, y1, z0 + 0.10, x2, y2, z0 + 0.28, "Mat_WoodOakTable", bevel=0.015)
    for i, (lx, ly) in enumerate([(x1 + 0.08, y1 + 0.08), (x2 - 0.08, y1 + 0.08), (x1 + 0.08, y2 - 0.08), (x2 - 0.08, y2 - 0.08)]):
        add_cyl(col, f"{prefix}_Leg{i}", lx, ly, z0, z0 + 0.11, 0.035, 0.035, "Mat_WoodOakDark", segs=10)
    # Nệm trắng kem
    add_box(col, f"{prefix}_Mattress", x1 + 0.04, y1 + 0.04, z0 + 0.28, x2 - 0.04, y2 - 0.04, z0 + 0.54, "Mat_BeddingCream", bevel=0.04)

    if head_side == 'X_MAX':
        # Đầu giường phía X_MAX
        add_box(col, f"{prefix}_Headboard", x2 - 0.08, y1 - 0.04, z0 + 0.20, x2 + 0.02, y2 + 0.04, z0 + min(headboard_h, 1.18), "Mat_FabricTaupe", bevel=0.03)
        # Chăn gấp phủ 2/3 giường phía X_MIN
        add_box(col, f"{prefix}_Duvet", x1 + 0.02, y1 + 0.02, z0 + 0.42, x1 + (x2 - x1) * 0.66, y2 - 0.02, z0 + 0.61, duvet_mat, bevel=0.035)
        # 2 gối nằm + 2 gối trang trí
        my = (y1 + y2) / 2.0
        for i, py in enumerate([my - 0.36, my + 0.36]):
            add_box(col, f"{prefix}_Pillow{i}", x2 - 0.50, py - 0.28, z0 + 0.54, x2 - 0.14, py + 0.28, z0 + 0.70, pillow_mat, bevel=0.05)
            add_box(col, f"{prefix}_AccentPillow{i}", x2 - 0.66, py - 0.18, z0 + 0.54, x2 - 0.48, py + 0.18, z0 + 0.72, "Mat_CushionMustard", bevel=0.04)
    elif head_side == 'X_MIN':
        # Đầu giường phía X_MIN
        add_box(col, f"{prefix}_Headboard", x1 - 0.02, y1 - 0.04, z0 + 0.20, x1 + 0.08, y2 + 0.04, z0 + min(headboard_h, 1.18), "Mat_FabricTaupe", bevel=0.03)
        # Chăn gấp phủ 2/3 giường phía X_MAX
        add_box(col, f"{prefix}_Duvet", x2 - (x2 - x1) * 0.66, y1 + 0.02, z0 + 0.42, x2 - 0.02, y2 - 0.02, z0 + 0.61, duvet_mat, bevel=0.035)
        # 2 gối nằm + 2 gối trang trí
        my = (y1 + y2) / 2.0
        for i, py in enumerate([my - 0.36, my + 0.36]):
            add_box(col, f"{prefix}_Pillow{i}", x1 + 0.14, py - 0.28, z0 + 0.54, x1 + 0.50, py + 0.28, z0 + 0.70, pillow_mat, bevel=0.05)
            add_box(col, f"{prefix}_AccentPillow{i}", x1 + 0.48, py - 0.18, z0 + 0.54, x1 + 0.66, py + 0.18, z0 + 0.72, "Mat_CushionMustard", bevel=0.04)
    elif head_side == 'Y_MAX':
        add_box(col, f"{prefix}_Headboard", x1 - 0.04, y2 - 0.08, z0 + 0.20, x2 + 0.04, y2 + 0.02, z0 + headboard_h, "Mat_FabricTaupe", bevel=0.03)
        add_box(col, f"{prefix}_Duvet", x1 + 0.02, y1 + 0.02, z0 + 0.42, x2 - 0.02, y1 + (y2 - y1) * 0.66, z0 + 0.61, duvet_mat, bevel=0.035)
        mx = (x1 + x2) / 2.0
        poff = min(0.42, (x2 - x1) * 0.23)
        pw = min(0.30, (x2 - x1) * 0.17)
        for i, px in enumerate([mx - poff, mx + poff]):
            add_box(col, f"{prefix}_Pillow{i}", px - pw, y2 - 0.50, z0 + 0.54, px + pw, y2 - 0.14, z0 + 0.71, pillow_mat, bevel=0.05)
            add_box(col, f"{prefix}_AccentPillow{i}", px - pw * 0.68, y2 - 0.66, z0 + 0.54, px + pw * 0.68, y2 - 0.48, z0 + 0.73, "Mat_CushionTerracotta", bevel=0.04)

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
    elif door_face == 'X_MIN':
        n_doors = max(2, int((y2 - y1) / 0.55))
        dy = (y2 - y1) / n_doors
        for d in range(n_doors):
            dy1 = y1 + d * dy + 0.015
            dy2 = y1 + (d + 1) * dy - 0.015
            add_box(col, f"{prefix}_Door{d}", x1 - 0.025, dy1, z0 + 0.05, x1 + 0.01, dy2, z0 + h - 0.04, "Mat_WallFacadeWarm", bevel=0.006)
            hy = dy1 + 0.06 if d % 2 == 1 else dy2 - 0.06
            add_box(col, f"{prefix}_Handle{d}", x1 - 0.055, hy - 0.01, z0 + 0.95, x1 - 0.025, hy + 0.01, z0 + 1.45, "Mat_BrassGold", bevel=0.004)
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
# 4. SITE & SÂN TRƯỚC 18M: ĐƯỜNG LUỒNG 2M PHÍA NAM (X=0..2), BÀN TRÀ & SUV PHÍA BẮC
#    Quy ước hướng: Mặt tiền quay hướng Đông (-Y), Hậu nhà hướng Tây (+Y).
#    Nhìn từ đường Quốc lộ vào nhà: Trái (-X, X=0..2) = PHÍA NAM (đường luồng 2m
#    tránh gió bấc, đón gió Nam mát); Phải (+X, X=2..7) = PHÍA BẮC (khối nhà chính).
# ---------------------------------------------------------------------------
add_box(col_site, "Site_FrontRoad", -4.0, -24.0, -0.35, 11.0, -18.8, -0.20, "Mat_RoadAsphalt")
add_box(col_site, "Site_Sidewalk", -2.0, -18.8, -0.20, 9.0, -18.0, 0.0, "Mat_WallFacadeWarm")
add_box(col_site, "Site_ArchitecturalBasePlinth", -0.5, -18.5, -0.45, 7.5, 24.5, -0.01, "Mat_RoofCharcoal")
add_box(col_site, "Site_FrontYard_Slab", 0.0, -18.0, 0.0, 7.0, 0.0, 0.15, "Mat_AntiSlipPavers")

# Trụ cổng đá chẻ & Cổng sắt (Cổng phụ 2m phía Nam X=0.15..2.85, Cổng ô tô 3.6m phía Bắc X=3.15..6.65)
add_box(col_site, "Gate_Pillar_L", -0.18, -18.18, 0.0, 0.15, -17.82, 2.65, "Mat_DarkGreyStone")
add_box(col_site, "Gate_Pillar_M", 2.85, -18.18, 0.0, 3.15, -17.82, 2.65, "Mat_DarkGreyStone")
add_box(col_site, "Gate_Pillar_R", 6.65, -18.18, 0.0, 7.18, -17.82, 2.65, "Mat_DarkGreyStone")
# Đèn trụ cổng
for gi, gx in enumerate([0.0, 3.0, 6.92]):
    add_box(col_lights, f"Gate_Lamp_{gi}", gx - 0.11, -18.10, 2.65, gx + 0.11, -17.90, 2.88, "Mat_WarmSconce", bevel=0.01)

add_box(col_site, "SideGate_2m", 0.15, -18.0, 0.18, 2.85, -17.94, 2.25, "Mat_MetalMatteBlack")
add_box(col_site, "MainCarGate_3m6", 3.15, -18.0, 0.18, 6.65, -17.94, 2.25, "Mat_MetalMatteBlack")

# Hàng rào: Tường rào trái (phía Nam) chạy liền; Tách tường rào phải (phía Bắc) chừa Y=0..16 để mở góc cắt nội thất!
add_box(col_site, "Fence_Left", -0.18, -18.0, 0.0, 0.0, 24.0, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Right_Front", 7.0, -18.0, 0.0, 7.18, 0.0, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Right_Rear", 7.0, 16.0, 0.0, 7.18, 24.0, 2.35, "Mat_WallWarmWhite")
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

# ---------------------------------------------------------------------------
# 4B. CÁI HÈ THU HẸP GỌN (Y=-1.45..0) + BẬC THANG 3 BẬC (Y=-2.35..-1.45)
#     + 2 LAN CAN DỌC NGỒI ĐƯỢC + TỦ DÉP LAN CAN BẮC
#     + BÀN GHẾ BA CHILL Ở DƯỚI BẬC THANG (Y=-5.25..-2.70, NỀN SÂN Z=0.15)
# ---------------------------------------------------------------------------
Z1 = 0.54
H1 = 3.70

# Nền cái hè thu hẹp gọn (Y = -1.45..0.0, X = 2.0..7.0, cao độ bằng sàn nhà Z1 = 0.54)
add_box(col_site, "Porch_He_Slab", 2.0, -1.45, 0.15, 7.0, 0.0, Z1, "Mat_FloorTileCream")

# Bậc thang 3 bậc (bậc tam cấp) nối từ sân (Z=0.15) lên cái hè (Z1=0.54): Y = -2.35..-1.45
for st_i, (sy1, sy2, sz_top) in enumerate([(-2.35, -2.05, 0.28), (-2.05, -1.75, 0.41), (-1.75, -1.45, 0.54)]):
    add_box(col_site, f"Porch_Step_{st_i + 1}", 2.38, sy1, 0.15, 6.62, sy2, sz_top, "Mat_StepStone", bevel=0.008)
    add_box(col_lights, f"Porch_StepLED_{st_i + 1}", 2.50, sy1 - 0.01, sz_top - 0.03, 6.50, sy1 + 0.01, sz_top - 0.01, "Mat_WarmLED")

# Giữ nguyên 2 lan can dọc hai bên cái hè có thể ngồi được (mặt gỗ rộng ngồi thoải mái)
# 1. Lan can dọc phía Nam (X = 2.00..2.38) — nhìn qua hướng Nam là Đường luồng 2m!
add_box(col_site, "Porch_SitWall_South_Base", 2.00, -2.35, 0.15, 2.38, 0.0, Z1 + 0.42, "Mat_WallWarmWhite", bevel=0.01)
add_box(col_site, "Porch_SitWall_South_Top", 1.96, -2.38, Z1 + 0.42, 2.42, 0.0, Z1 + 0.48, "Mat_WoodOakTable", bevel=0.015)
for sci, scy in enumerate([-1.75, -0.75]):
    add_box(col_site, f"Porch_SitWall_South_Pad_{sci}", 2.00, scy - 0.32, Z1 + 0.48, 2.38, scy + 0.32, Z1 + 0.53, "Mat_CushionMustard", bevel=0.018)

# 2. Lan can dọc phía Bắc (X = 6.62..7.00) + TỦ DÉP đặt gọn trên hè sát lan can phía Bắc!
add_box(col_site, "Porch_SitWall_North_Base", 6.62, -2.35, 0.15, 7.00, 0.0, Z1 + 0.42, "Mat_WallWarmWhite", bevel=0.01)
add_box(col_site, "Porch_SitWall_North_Top", 6.58, -2.38, Z1 + 0.42, 7.00, 0.0, Z1 + 0.48, "Mat_WoodOakTable", bevel=0.015)

# 👟 TỦ DÉP GỌN ĐẸP SÁT LAN CAN PHÍA BẮC TRÊN HÈ (X = 6.18..6.60, Y = -1.35..-0.18, thấp hơn bệ cửa sổ Bắc)
add_box(col_site, "Porch_ShoeCabinet_Body", 6.20, -1.32, Z1 + 0.06, 6.60, -0.20, Z1 + 0.68, "Mat_WoodOakCabinet", bevel=0.012)
add_box(col_site, "Porch_ShoeCabinet_Top", 6.18, -1.34, Z1 + 0.68, 6.62, -0.18, Z1 + 0.72, "Mat_WoodOakTable", bevel=0.008)
for sh_d in range(2):
    sy_d1 = -1.28 + sh_d * 0.54
    add_box(col_site, f"Porch_ShoeCabinet_Door_{sh_d}", 6.18, sy_d1, Z1 + 0.10, 6.21, sy_d1 + 0.50, Z1 + 0.64, "Mat_WallFacadeWarm", bevel=0.006)
    add_box(col_site, f"Porch_ShoeCabinet_Handle_{sh_d}", 6.15, sy_d1 + 0.22, Z1 + 0.48, 6.18, sy_d1 + 0.28, Z1 + 0.58, "Mat_BrassGold", bevel=0.003)
for sl_i in range(4):
    add_cyl(col_site, f"Porch_ShoeCabinet_Leg_{sl_i}", 6.24 if sl_i % 2 == 0 else 6.56, -1.26 if sl_i < 2 else -0.26, Z1, Z1 + 0.06, 0.018, 0.018, "Mat_MetalMatteBlack", segs=8)
# Vài đôi dép/giày xếp ngay ngắn bên cạnh tủ dép
for sp_i, spy in enumerate([-1.05, -0.78, -0.52]):
    add_box(col_site, f"Porch_SlipperL_{sp_i}", 5.90, spy - 0.05, Z1, 6.12, spy + 0.03, Z1 + 0.04, "Mat_CushionNavy" if sp_i % 2 == 0 else "Mat_CushionTerracotta", bevel=0.01)
    add_box(col_site, f"Porch_SlipperR_{sp_i}", 5.90, spy + 0.05, Z1, 6.12, spy + 0.13, Z1 + 0.04, "Mat_CushionNavy" if sp_i % 2 == 0 else "Mat_CushionTerracotta", bevel=0.01)

# 🍵 BÀN GHẾ BA CHILL CHILL CÙNG ANH EM Ở DƯỚI BẬC THANG (Sân hiên hướng Bắc Z=0.15, Y=-5.25..-2.70)
# Thứ tự từ trong ra ngoài: Cửa chính -> Hè (-1.45..0) -> Bậc thang 3 bậc (-2.35..-1.45) -> Bàn Ba chill (-5.25..-2.70)
add_box(col_site, "DadTea_Rug", 4.72, -5.25, 0.15, 6.95, -2.70, 0.17, "Mat_AntiSlipWoodTile")
add_box(col_site, "DadTea_Bench_Base", 6.38, -5.05, 0.17, 6.92, -2.85, 0.56, "Mat_WoodOakTable", bevel=0.015)
add_box(col_site, "DadTea_Bench_Back", 6.88, -5.05, 0.56, 6.98, -2.85, 1.10, "Mat_WoodLouverFacade")
add_box(col_site, "DadTea_Bench_Cushion", 6.42, -5.00, 0.56, 6.87, -2.90, 0.64, "Mat_CushionMustard", bevel=0.02)
for ti, ty in enumerate([-4.62, -3.95, -3.28]):
    add_box(col_site, f"DadTea_Pillow_{ti}", 6.72, ty - 0.20, 0.64, 6.87, ty + 0.20, 0.92,
            "Mat_CushionNavy" if ti % 2 == 0 else "Mat_BeddingCream", bevel=0.04)
add_box(col_site, "DadTea_Table_Top", 5.60, -4.75, 0.68, 6.20, -3.15, 0.74, "Mat_WhiteMarble", bevel=0.015)
for i, (lx, ly) in enumerate([(5.68, -4.65), (6.12, -4.65), (5.68, -3.25), (6.12, -3.25)]):
    add_cyl(col_site, f"DadTea_Leg_{i}", lx, ly, 0.17, 0.68, 0.03, 0.03, "Mat_MetalMatteBlack", segs=10)
# Khay trà + Ấm + 4 Chén + Chậu bonsai nhỏ
add_box(col_site, "DadTea_Tray", 5.72, -4.30, 0.74, 6.08, -3.60, 0.77, "Mat_WoodWalnutAltar", bevel=0.005)
add_sphere(col_site, "DadTea_Teapot", 5.90, -3.95, 0.83, 0.075, "Mat_CeramicTeal", sx=1.0, sy=1.0, sz=0.8)
for ci, (cx_c, cy_c) in enumerate([(5.80, -3.75), (6.00, -3.75), (5.80, -4.15), (6.00, -4.15)]):
    add_cyl(col_site, f"DadTea_Cup_{ci}", cx_c, cy_c, 0.77, 0.82, 0.025, 0.030, "Mat_CeramicWhite", segs=12)
add_potted_plant(col_site, "DadTea_MiniBonsai", 5.90, -3.35, 0.74, scale=0.36, pot_mat="Mat_CeramicTeal")
# 2 ghế đôn gỗ đối diện ngồi chill cùng Ba
for si, sy in enumerate([-4.40, -3.50]):
    add_cyl(col_site, f"DadTea_Stool_{si}", 5.22, sy, 0.17, 0.56, 0.18, 0.18, "Mat_WoodOakTable", segs=16)
    add_cyl(col_site, f"DadTea_StoolPad_{si}", 5.22, sy, 0.56, 0.61, 0.16, 0.16, "Mat_CushionMustard", segs=16)
add_box(col_lights, "DadTea_WallLamp", 6.90, -4.05, 1.75, 6.98, -3.85, 1.98, "Mat_WarmSconce")
add_potted_plant(col_site, "DadTea_CornerPlant", 6.52, -5.65, 0.15, scale=1.10, pot_mat="Mat_DarkGreyStone")

# 🚗 Xe ô tô SUV 7 chỗ đỗ phía Bắc trong sân (thẳng cổng ô tô 3.6m)
add_box(col_site, "Family_SUV_Chassis", 4.20, -14.6, 0.34, 6.10, -10.1, 0.92, "Mat_CarWhite", bevel=0.10)
add_box(col_site, "Family_SUV_Cabin", 4.32, -13.4, 0.92, 5.98, -10.7, 1.62, "Mat_CarWhite", bevel=0.10)
add_box(col_site, "Family_SUV_Windshield", 4.36, -13.45, 0.96, 5.94, -12.7, 1.56, "Mat_GlassBronze")
add_box(col_site, "Family_SUV_SideWin", 4.29, -13.1, 0.98, 6.01, -10.9, 1.52, "Mat_GlassBronze")
add_box(col_lights, "Family_SUV_Headlights", 4.32, -14.63, 0.60, 5.98, -14.57, 0.74, "Mat_WarmSconce")
add_box(col_lights, "Family_SUV_Taillights", 4.32, -10.12, 0.62, 5.98, -10.06, 0.75, "Mat_SmartRedLED")
for wi, (wx, wy) in enumerate([(4.22, -13.6), (6.08, -13.6), (4.22, -11.1), (6.08, -11.1)]):
    add_cyl(col_site, f"Family_SUV_Wheel_{wi}", wx, wy, 0.15, 0.85, 0.34, 0.34, "Mat_TireRubber",
            rot=(0, math.pi / 2, 0), segs=18)
    add_cyl(col_site, f"Family_SUV_Rim_{wi}", wx + (-0.04 if wx < 5.0 else 0.04), wy, 0.28, 0.72, 0.20, 0.20, "Mat_MetalStainless",
            rot=(0, math.pi / 2, 0), segs=14)

# 🌳 Bonsai & Cây cảnh hướng phía Nam trong sân (dọc lối vào đường luồng) + Đèn nấm lối đi
for bi, by in enumerate([-16.2, -12.5, -8.8, -5.0, -1.6]):
    add_box(col_site, f"Bonsai_Planter_{bi}", 0.55, by - 0.38, 0.15, 1.45, by + 0.38, 0.58, "Mat_DarkGreyStone", bevel=0.02)
    add_box(col_site, f"Bonsai_Soil_{bi}", 0.62, by - 0.32, 0.55, 1.38, by + 0.32, 0.60, "Mat_SoilDark")
    add_cyl(col_site, f"Bonsai_Trunk_{bi}", 1.0, by, 0.58, 1.15, 0.09, 0.06, "Mat_TreeTrunk", segs=10)
    add_sphere(col_site, f"Bonsai_Canopy1_{bi}", 1.0, by, 1.38, 0.42, "Mat_FoliageGreen", 1.2, 1.1, 0.72)
    add_sphere(col_site, f"Bonsai_Canopy2_{bi}", 1.25, by + 0.22, 1.18, 0.28, "Mat_FoliageBright", 1.1, 1.0, 0.75)
    add_sphere(col_site, f"Bonsai_Canopy3_{bi}", 0.76, by - 0.20, 1.22, 0.26, "Mat_FoliageGreen", 1.0, 1.1, 0.72)
    add_cyl(col_lights, f"Garden_Bollard_{bi}", 1.75, by, 0.15, 0.65, 0.06, 0.06, "Mat_MetalMatteBlack", segs=10)
    add_cyl(col_lights, f"Garden_BollardGlow_{bi}", 1.75, by, 0.52, 0.62, 0.065, 0.065, "Mat_WarmSconce", segs=10)

# Đường luồng 2m PHÍA NAM (X = 0.0..2.0, Y = 0..16 — tránh gió bấc, nằm ngay bên hướng Nam lan can cái hè)
add_box(col_site, "Corridor_2m_Grass", 0.0, 0.0, 0.0, 2.0, 16.0, 0.14, "Mat_GrassGreen")
for si in range(16):
    sy = 0.5 + si * 0.98
    add_box(col_site, f"StepStone_{si}", 0.45, sy - 0.26, 0.14, 1.55, sy + 0.26, 0.19, "Mat_StepStone", bevel=0.015)

# ☂️ MÁI HIÊN ĐƯỜNG LUỒNG DƯỚI (X = 0.02..2.00, Y = -1.60..16.20 — mái kính khung thép đen & nẹp gỗ dốc nhẹ chắn mưa nắng!)
# Bắt sát tường nhà Nam (X=2.0, Z=3.16m trên đỉnh 2 cửa sổ đường luồng) dốc ra máng xối hàng rào Nam (X=0.04, Z=2.86m),
# chừa khe thoáng gió Nam 51cm trên tường rào 2.35m và giữ cao thông thủy 2.72m đi lại & dắt xe cực thoáng!
awn_pitch = -math.atan2(0.30, 1.96)  # +X (tường nhà) cao 3.16m -> -X (hàng rào) thấp 2.86m
add_box(col_site, "SouthAwning_WallBeam", 1.94, -1.60, 3.10, 2.02, 16.20, 3.18, "Mat_MetalMatteBlack")
add_box(col_site, "SouthAwning_Gutter", 0.00, -1.60, 2.80, 0.10, 16.20, 2.90, "Mat_RoofCharcoal")
add_box(col_site, "SouthAwning_GlassRoof", 0.02, -1.60, 3.01, 2.00, 16.20, 3.05, "Mat_CanopyGlass", rot=(0, awn_pitch, 0))
for ai, ay in enumerate([-1.50, 0.20, 2.00, 3.80, 5.60, 7.40, 9.20, 11.00, 12.80, 14.60, 16.10]):
    add_box(col_site, f"SouthAwning_Rafter_{ai}", 0.04, ay - 0.035, 2.96, 1.98, ay + 0.035, 3.02, "Mat_MetalMatteBlack", rot=(0, awn_pitch, 0))
for bi, bx in enumerate([0.52, 1.02, 1.52]):
    bz_b = 2.86 + (bx / 1.96) * 0.30 - 0.04
    add_box(col_site, f"SouthAwning_WoodPurlin_{bi}", bx - 0.025, -1.58, bz_b, bx + 0.025, 16.18, bz_b + 0.04, "Mat_WoodLouverFacade")
add_box(col_lights, "SouthAwning_WarmLED", 1.88, -1.50, 3.06, 1.93, 16.10, 3.10, "Mat_WarmLED")

# ---------------------------------------------------------------------------
# 5. TẦNG 1 (KHỐI NHÀ CHÍNH PHÍA BẮC X = 2.0..7.0, CAO ĐỘ SÀN Z1 = 0.54):
#    - Phía Nam trong nhà (X=2.22..3.15): Đường luồng trong nhà đi thẳng từ Cửa chính Nam
#    - Phía Bắc (X=3.22..6.78): Gian thờ sát vách Bắc (quay mặt hướng Bắc, lưng hướng Nam)
#      -> Vách ngăn CNC -> Sofa & TV -> Phòng Ba Mẹ (2 cửa sổ Đông/Tây, giường đầu Tây chân Đông)
#      -> Cầu thang chữ U -> Bếp mở & Bàn ăn tròn
# ---------------------------------------------------------------------------
add_box(col_fl1_arch, "Floor1_Slab", 2.0, 0.0, 0.15, 7.0, 16.0, Z1, "Mat_FloorTileCream")

# Tường bao Tầng 1:
# - Tường Bắc (X=6.78..7.0) cắt thấp 0.38m để xem nội thất
# - Tường Nam giáp đường luồng 2m ngoài (X=2.0..2.22) có ĐÚNG 2 CỬA SỔ:
#   + Cửa sổ 1 (Y=4.80..6.25): Nằm giữa khu Sofa và Phòng Ba Mẹ, lệch về phía Sofa nhiều hơn (~1.0m phía Sofa, ~0.45m phía cửa Phòng Ba Mẹ)!
#   + Cửa sổ 2 (Y=12.60..14.50): Ngay phía sau bàn ăn ở bếp để ngồi ăn có thể thấy xe ai về qua đường luồng!
add_box(col_fl1_arch, "Fl1_Wall_Right_Cutaway", 6.78, 0.0, Z1, 7.0, 16.0, Z1 + 0.38, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Left_Seg1", 2.0, 0.0, Z1, 2.22, 4.80, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Left_Win1Bot", 2.0, 4.80, Z1, 2.22, 6.25, Z1 + 0.90, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Left_Win1Top", 2.0, 4.80, Z1 + 2.35, 2.22, 6.25, H1, "Mat_WallWarmWhite")
add_window_frame(col_fl1_arch, "Fl1_Corridor_SouthWin_SofaParents", 2.05, 4.80, Z1 + 0.90, 2.17, 6.25, Z1 + 2.35)
add_box(col_fl1_arch, "Fl1_Wall_Left_Seg2", 2.0, 6.25, Z1, 2.22, 12.60, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Left_Win2Bot", 2.0, 12.60, Z1, 2.22, 14.50, Z1 + 0.90, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Left_Win2Top", 2.0, 12.60, Z1 + 2.35, 2.22, 14.50, H1, "Mat_WallWarmWhite")
add_window_frame(col_fl1_arch, "Fl1_Kitchen_SouthWin_Dining", 2.05, 12.60, Z1 + 0.90, 2.17, 14.50, Z1 + 2.35)
add_box(col_fl1_arch, "Fl1_Wall_Left_End", 2.0, 14.50, Z1, 2.22, 16.0, H1, "Mat_WallWarmWhite")

# Tường mặt tiền từ hiên vào nhà có 2 cửa: 1 Cửa chính hướng Nam (X=2.35..3.95) & 1 Cửa sổ lớn hướng Bắc (X=4.60..6.55)
add_box(col_fl1_arch, "Fl1_Wall_Front_L", 2.0, 0.0, Z1, 2.35, 0.22, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Front_Mid", 3.95, 0.0, Z1, 4.60, 0.22, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Front_R", 6.55, 0.0, Z1, 7.0, 0.22, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Front_WinBot", 4.60, 0.0, Z1, 6.55, 0.22, Z1 + 0.72, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Front_Top", 2.35, 0.0, Z1 + 2.35, 6.55, 0.22, H1, "Mat_WallWarmWhite")
add_window_frame(col_fl1_arch, "Fl1_Front_MainDoor", 2.35, 0.06, Z1, 3.95, 0.18, Z1 + 2.35)
add_window_frame(col_fl1_arch, "Fl1_Front_Window", 4.60, 0.06, Z1 + 0.72, 6.55, 0.18, Z1 + 2.35)

# Tường sau Phòng Bếp (Y = 15.78..16.0) gồm 1 Cửa chính sau + 1 Cửa sổ sau nhìn ra Nhà tắm (đã bỏ cửa sổ gần cửa sau):
# - Mảng tường đặc phía Nam (X=2.0..3.55): kín gọn, không mở cửa sổ cạnh cửa sau
# - Cửa chính sau (X=3.55..4.75): Bước xuống sân sau qua bậc tam cấp
# - Cửa sổ chỗ nấu ăn nhìn ra Nhà tắm (X=4.95..6.35): Nằm ngay bên TRÁI người nấu (khi đứng quay mặt Bắc nấu bếp hồng ngoại), thoát mùi cực thoáng!
add_box(col_fl1_arch, "Fl1_Wall_Rear_SolidS", 2.0, 15.78, Z1, 3.55, 16.0, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Rear_DoorTop", 3.55, 15.78, Z1 + 2.40, 4.75, 16.0, H1, "Mat_WallWarmWhite")
add_window_frame(col_fl1_arch, "Fl1_RearDoor", 3.55, 15.80, Z1, 4.75, 15.94, Z1 + 2.40)
add_box(col_fl1_arch, "Fl1_Wall_Rear_Pier2", 4.75, 15.78, Z1, 4.95, 16.0, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Rear_WinBathBot", 4.95, 15.78, Z1, 6.35, 16.0, Z1 + 0.95, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Fl1_Wall_Rear_WinBathTop", 4.95, 15.78, Z1 + 2.35, 6.35, 16.0, H1, "Mat_WallWarmWhite")
add_window_frame(col_fl1_arch, "Fl1_Kitchen_RearWin_Bath", 4.95, 15.82, Z1 + 0.95, 6.35, 15.94, Z1 + 2.35)
add_box(col_fl1_arch, "Fl1_Wall_Rear_EdgeR", 6.35, 15.78, Z1, 7.0, 16.0, H1, "Mat_WallWarmWhite")
# Chỉ 1 bậc thang cửa sau (nền sân sau nâng lên Z_REAR=0.34m sát cao độ bếp Z1=0.54m nên chỉ cần 1 bậc cực êm!)
add_box(col_fl1_arch, "Rear_DoorStep_1", 3.52, 16.00, 0.34, 4.78, 16.38, 0.44, "Mat_StepStone", bevel=0.008)
add_box(col_lights, "Rear_DoorStep_LED", 3.60, 16.37, 0.39, 4.70, 16.39, 0.42, "Mat_WarmLED")

# Lam gỗ mặt tiền trang trí đặt gọn tại mảng tường đặc góc Bắc (không chắn tầm nhìn cửa sổ Bắc!)
for li in range(3):
    lx = 6.62 + li * 0.13
    add_box(col_fl1_arch, f"Facade_Louver_{li}", lx, -0.10, Z1 + 0.2, lx + 0.05, 0.02, 7.25, "Mat_WoodLouverFacade")
add_box(col_lights, "Facade_Louver_LED", 6.57, -0.04, Z1 + 0.3, 6.60, 0.01, 7.20, "Mat_WarmLED")

# --- A. PHÒNG KHÁCH: GIAN THỜ SÁT VÁCH BẮC (QUAY MẶT HƯỚNG BẮC, LƯNG HƯỚNG NAM) -> VÁCH TƯỜNG Ô TRỐNG TRANG TRÍ -> SOFA & TV ---

# 1. GIAN THỜ BỒ TÁT QUAN ÂM SÁT VÁCH BẮC (X = 6.02..6.76, Y = 0.42..1.98)
# Khi thắp nhang đứng ở X ~ 5.2 quay mặt về HƯỚNG BẮC (+X), lưng hướng Nam (-X),
# nhìn qua phải (hướng Đông -Y) qua Cửa sổ Bắc thấy ngay Ba đang ngồi chill ngoài hiên!
# Vách hậu ốp lam gỗ óc chó thưa (vừa trang nghiêm khi nhìn từ trong, vừa thoáng góc cắt nhìn từ phía Bắc)
for asl in range(9):
    asly = 0.44 + asl * 0.19
    add_box(col_fl1_furn, f"Altar_BackSlat_{asl}", 6.72, asly, Z1 + 0.38, 6.77, asly + 0.055, H1 - 0.12, "Mat_WoodWalnutAltar", bevel=0.004)
add_box(col_lights, "Altar_BackTopLED", 6.71, 0.44, H1 - 0.14, 6.76, 1.98, H1 - 0.10, "Mat_WarmLED")
add_box(col_fl1_furn, "Altar_Table", 6.06, 0.48, Z1 + 0.98, 6.72, 1.92, Z1 + 1.08, "Mat_WoodWalnutAltar", bevel=0.015)
for i, (ax_l, ay_l) in enumerate([(6.12, 0.54), (6.66, 0.54), (6.12, 1.86), (6.66, 1.86)]):
    add_box(col_fl1_furn, f"Altar_Leg_{i}", ax_l - 0.04, ay_l - 0.04, Z1, ax_l + 0.04, ay_l + 0.04, Z1 + 0.98, "Mat_WoodWalnutAltar")
add_box(col_fl1_furn, "Altar_LowerShelf", 6.12, 0.54, Z1 + 0.28, 6.66, 1.86, Z1 + 0.35, "Mat_WoodWalnutAltar")
# Tượng Quan Âm, đế sen đồng, vòng hào quang LED quay mặt ra hướng Nam (-X) đối diện người thắp nhang
add_cyl(col_fl1_furn, "Altar_LotusBase", 6.48, 1.20, Z1 + 1.08, Z1 + 1.20, 0.17, 0.13, "Mat_BrassGold", segs=18)
add_cyl(col_fl1_furn, "Altar_BuddhaBody", 6.48, 1.20, Z1 + 1.20, Z1 + 1.66, 0.11, 0.05, "Mat_BuddhaGold", segs=18)
add_sphere(col_fl1_furn, "Altar_BuddhaHead", 6.48, 1.20, Z1 + 1.73, 0.072, "Mat_BuddhaGold")
add_cyl(col_lights, "Altar_HaloLED", 6.69, 1.20, Z1 + 1.66, Z1 + 1.69, 0.34, 0.34, "Mat_WarmLED", rot=(0, math.pi / 2, 0))
# Lư hương đồng, 2 bình hoa sen, 2 đèn thờ, mâm ngũ quả & thảm lễ quay mặt hướng Bắc
add_cyl(col_fl1_furn, "Altar_IncenseBurner", 6.24, 1.20, Z1 + 1.08, Z1 + 1.24, 0.08, 0.095, "Mat_BrassGold", segs=16)
for vi, vy in enumerate([0.70, 1.70]):
    add_cyl(col_fl1_furn, f"Altar_Vase_{vi}", 6.44, vy, Z1 + 1.08, Z1 + 1.38, 0.065, 0.045, "Mat_CeramicWhite", segs=14)
    add_sphere(col_fl1_furn, f"Altar_Lotus_{vi}", 6.44, vy, Z1 + 1.46, 0.08, "Mat_FlowerPink")
    add_cyl(col_lights, f"Altar_Candle_{vi}", 6.24, vy + (0.20 if vi == 0 else -0.20), Z1 + 1.08, Z1 + 1.26, 0.032, 0.025, "Mat_WarmSconce", segs=12)
add_cyl(col_fl1_furn, "Altar_FruitPlate", 6.34, 1.46, Z1 + 1.08, Z1 + 1.15, 0.10, 0.12, "Mat_WoodOakDark", segs=14)
add_sphere(col_fl1_furn, "Altar_Fruit1", 6.34, 1.46, Z1 + 1.19, 0.042, "Mat_FlowerYellow")
add_sphere(col_fl1_furn, "Altar_Fruit2", 6.31, 1.42, Z1 + 1.18, 0.038, "Mat_CushionTerracotta")
add_box(col_fl1_furn, "Altar_PrayerMat", 5.22, 0.78, Z1, 5.86, 1.62, Z1 + 0.025, "Mat_CushionTerracotta", bevel=0.008)
add_curtain_pair(col_fl1_furn, "Altar_FrontCurtain", 4.58, 6.56, 0.26, Z1 + 0.04, H1 - 0.12)
add_pendant_chandelier(col_lights, "Altar_PendantLamp", 5.80, 1.20, H1 - 0.02, drop=0.60, count=1)

# 2. VÁCH TƯỜNG XÂY CÓ 7 Ô TRỐNG TRANG TRÍ SÁCH & MÔ HÌNH NGĂN GIAN THỜ - PHÒNG KHÁCH (Y = 2.06..2.34, X = 4.26..6.78)
# Thiết kế vách xây sơn trắng ấm sâu 28cm, đục 7 ô trống xuyên sáng so le 3 tầng tạo không gian cực thoáng,
# lót đáy gỗ sồi + hắt LED ấm từng ô để bày sách, mô hình kiến trúc, tượng decor & cây xanh nhìn đẹp cả 2 mặt!
py1, py2 = 2.06, 2.34
py_mid = (py1 + py2) / 2.0
# Chân tường giật cấp gỗ sồi tối + bệ tường xây dưới + dầm tường xây trên + 2 trụ biên
add_box(col_fl1_arch, "AltarWall_KickBase", 4.28, py1 + 0.02, Z1, 6.78, py2 - 0.02, Z1 + 0.06, "Mat_WoodOakDark")
add_box(col_fl1_arch, "AltarWall_Base", 4.26, py1, Z1 + 0.06, 6.78, py2, Z1 + 0.68, "Mat_WallWarmWhite", bevel=0.008)
add_box(col_fl1_arch, "AltarWall_TopBeam", 4.26, py1, Z1 + 2.76, 6.78, py2, H1, "Mat_WallWarmWhite", bevel=0.008)
add_box(col_fl1_arch, "AltarWall_PierS", 4.26, py1, Z1 + 0.06, 4.44, py2, Z1 + 2.76, "Mat_WallWarmWhite", bevel=0.008)
add_box(col_fl1_arch, "AltarWall_PierN", 6.62, py1, Z1 + 0.06, 6.78, py2, Z1 + 2.76, "Mat_WallWarmWhite", bevel=0.008)
# 2 đợt tường xây ngang chia 3 tầng ô trống
add_box(col_fl1_arch, "AltarWall_Shelf1", 4.44, py1, Z1 + 1.32, 6.62, py2, Z1 + 1.44, "Mat_WallWarmWhite", bevel=0.006)
add_box(col_fl1_arch, "AltarWall_Shelf2", 4.44, py1, Z1 + 2.00, 6.62, py2, Z1 + 2.12, "Mat_WallWarmWhite", bevel=0.006)
# Các vách trụ đứng xây so le tạo 7 ô trống nghệ thuật thoáng khí
add_box(col_fl1_arch, "AltarWall_Div_R1", 5.66, py1, Z1 + 0.68, 5.80, py2, Z1 + 1.32, "Mat_WallWarmWhite", bevel=0.006)
add_box(col_fl1_arch, "AltarWall_Div_R2A", 5.08, py1, Z1 + 1.44, 5.22, py2, Z1 + 2.00, "Mat_WallWarmWhite", bevel=0.006)
add_box(col_fl1_arch, "AltarWall_Div_R2B", 6.02, py1, Z1 + 1.44, 6.16, py2, Z1 + 2.00, "Mat_WallWarmWhite", bevel=0.006)
add_box(col_fl1_arch, "AltarWall_Div_R3", 5.26, py1, Z1 + 2.12, 5.40, py2, Z1 + 2.76, "Mat_WallWarmWhite", bevel=0.006)

# Lót mặt gỗ sồi ấm + đèn LED âm đỉnh cho toàn bộ 7 ô trống xuyên sáng
niche_specs = [
    ("N1A", 4.44, 5.66, Z1 + 0.68, Z1 + 1.32),
    ("N1B", 5.80, 6.62, Z1 + 0.68, Z1 + 1.32),
    ("N2A", 4.44, 5.08, Z1 + 1.44, Z1 + 2.00),
    ("N2B", 5.22, 6.02, Z1 + 1.44, Z1 + 2.00),
    ("N2C", 6.16, 6.62, Z1 + 1.44, Z1 + 2.00),
    ("N3A", 4.44, 5.26, Z1 + 2.12, Z1 + 2.76),
    ("N3B", 5.40, 6.62, Z1 + 2.12, Z1 + 2.76),
]
for nid, nx1, nx2, nz1, nz2 in niche_specs:
    add_box(col_fl1_furn, f"AltarWall_OakLiner_{nid}", nx1 + 0.005, py1 + 0.005, nz1, nx2 - 0.005, py2 - 0.005, nz1 + 0.025, "Mat_WoodOakTable", bevel=0.004)
    add_box(col_lights, f"AltarWall_NicheLED_{nid}", nx1 + 0.05, py_mid - 0.014, nz2 - 0.015, nx2 - 0.05, py_mid + 0.014, nz2 - 0.002, "Mat_WarmLED")

# Trang trí sách, mô hình kiến trúc, tượng decor & cây xanh trong 7 ô trống:
# - Ô 1A (dưới trái): Hàng sách kiến trúc + bình gốm teal + khối cầu đồng decor
add_books_row(col_fl1_furn, "AltarWall_Books_1A", 4.56, py_mid - 0.09, Z1 + 0.705, count=6, axis='X')
add_cyl(col_fl1_furn, "AltarWall_Vase_1A", 5.12, py_mid, Z1 + 0.705, Z1 + 1.00, 0.055, 0.036, "Mat_CeramicTeal", segs=16)
add_box(col_fl1_furn, "AltarWall_OrbBase_1A", 5.34, py_mid - 0.06, Z1 + 0.705, 5.52, py_mid + 0.06, Z1 + 0.745, "Mat_WoodOakDark", bevel=0.004)
add_sphere(col_fl1_furn, "AltarWall_Orb_1A", 5.43, py_mid, Z1 + 0.835, 0.088, "Mat_BrassGold")
# - Ô 1B (dưới phải): Chậu cây xanh lá mềm tạo mảng xanh thoáng mắt
add_potted_plant(col_fl1_furn, "AltarWall_Plant_1B", 6.21, py_mid, Z1 + 0.705, scale=0.44, pot_mat="Mat_CeramicWhite")
# - Ô 2A (giữa trái): Mô hình tượng nghệ thuật hình học đồng - sứ trắng trên đế gỗ
add_box(col_fl1_furn, "AltarWall_SculptBase_2A", 4.60, py_mid - 0.07, Z1 + 1.465, 4.92, py_mid + 0.07, Z1 + 1.505, "Mat_WoodOakDark", bevel=0.004)
add_cyl(col_fl1_furn, "AltarWall_SculptPillar_2A", 4.70, py_mid, Z1 + 1.505, Z1 + 1.78, 0.042, 0.028, "Mat_CeramicWhite", segs=16)
add_sphere(col_fl1_furn, "AltarWall_SculptTop_2A", 4.70, py_mid, Z1 + 1.825, 0.048, "Mat_BrassGold")
add_box(col_fl1_furn, "AltarWall_SculptCube_2A", 4.78, py_mid - 0.045, Z1 + 1.505, 4.88, py_mid + 0.045, Z1 + 1.66, "Mat_BrassGold", bevel=0.006)
# - Ô 2B (giữa trung tâm — tầm mắt): MÔ HÌNH KIẾN TRÚC BIỆT THỰ MINI trưng bày nổi bật!
add_box(col_fl1_furn, "AltarWall_ModelPlinth_2B", 5.34, py_mid - 0.09, Z1 + 1.465, 5.90, py_mid + 0.09, Z1 + 1.50, "Mat_WoodOakDark", bevel=0.004)
add_box(col_fl1_furn, "AltarWall_ModelBody1_2B", 5.42, py_mid - 0.065, Z1 + 1.50, 5.76, py_mid + 0.065, Z1 + 1.63, "Mat_CeramicWhite", bevel=0.004)
add_box(col_fl1_furn, "AltarWall_ModelGlass_2B", 5.45, py_mid - 0.068, Z1 + 1.53, 5.73, py_mid + 0.068, Z1 + 1.61, "Mat_GlassBronze")
add_box(col_fl1_furn, "AltarWall_ModelBody2_2B", 5.48, py_mid - 0.055, Z1 + 1.63, 5.78, py_mid + 0.055, Z1 + 1.74, "Mat_WallFacadeWarm", bevel=0.004)
add_box(col_fl1_furn, "AltarWall_ModelRoof_2B", 5.44, py_mid - 0.07, Z1 + 1.74, 5.82, py_mid + 0.07, Z1 + 1.765, "Mat_WoodOakTable", bevel=0.003)
add_cyl(col_fl1_furn, "AltarWall_ModelTreeTrunk_2B", 5.83, py_mid, Z1 + 1.50, Z1 + 1.59, 0.010, 0.008, "Mat_TreeTrunk", segs=8)
add_sphere(col_fl1_furn, "AltarWall_ModelTreeTop_2B", 5.83, py_mid, Z1 + 1.63, 0.045, "Mat_FoliageBright")
# - Ô 2C (giữa phải): Bình gốm trắng thanh mảnh
add_cyl(col_fl1_furn, "AltarWall_Vase_2C", 6.39, py_mid, Z1 + 1.465, Z1 + 1.74, 0.052, 0.032, "Mat_CeramicWhite", segs=16)
# - Ô 3A (trên trái): Sách nghệ thuật + chậu cây mini thả rủ
add_books_row(col_fl1_furn, "AltarWall_Books_3A", 4.56, py_mid - 0.09, Z1 + 2.145, count=5, axis='X')
add_cyl(col_fl1_furn, "AltarWall_MiniPot_3A", 5.04, py_mid, Z1 + 2.145, Z1 + 2.26, 0.052, 0.058, "Mat_TerracottaPot", segs=14)
add_sphere(col_fl1_furn, "AltarWall_MiniLeaf_3A", 5.04, py_mid, Z1 + 2.33, 0.085, "Mat_FoliageGreen", sx=1.15, sy=1.1, sz=0.8)
# - Ô 3B (trên phải): Mô hình thuyền gỗ buồm trưng bày + cụm sách trang trí
add_box(col_fl1_furn, "AltarWall_BoatHull_3B", 5.56, py_mid - 0.045, Z1 + 2.145, 5.88, py_mid + 0.045, Z1 + 2.21, "Mat_WoodWalnutAltar", bevel=0.015)
add_cyl(col_fl1_furn, "AltarWall_BoatMast_3B", 5.72, py_mid, Z1 + 2.21, Z1 + 2.52, 0.009, 0.007, "Mat_BrassGold", segs=8)
add_box(col_fl1_furn, "AltarWall_BoatSail_3B", 5.60, py_mid - 0.008, Z1 + 2.24, 5.71, py_mid + 0.008, Z1 + 2.49, "Mat_BeddingCream", bevel=0.003)
add_box(col_fl1_furn, "AltarWall_BoatSail2_3B", 5.73, py_mid - 0.008, Z1 + 2.24, 5.84, py_mid + 0.008, Z1 + 2.44, "Mat_CurtainLinen", bevel=0.003)
add_books_row(col_fl1_furn, "AltarWall_Books_3B", 6.08, py_mid - 0.09, Z1 + 2.145, count=6, axis='X')

# 3. ĐƯỜNG LUỒNG TRONG NHÀ PHÍA NAM (X = 2.22..3.25 — giữ thoáng sạch tuyệt đối, bỏ tủ & gương đối diện gian thờ)

# 4. KHU GHẾ SOFA & TIVI PHÒNG KHÁCH (Phía Bắc đường luồng trong nhà: X = 3.30..6.78, Y = 2.30..5.70)
# Kệ TV & Vách lam gỗ thưa áp tường Bắc (Y = 2.80..4.90)
add_box(col_fl1_furn, "Living_TVConsole", 6.30, 2.80, Z1 + 0.08, 6.76, 4.90, Z1 + 0.50, "Mat_WoodOakCabinet", bevel=0.012)
for d in range(3):
    add_box(col_fl1_furn, f"Living_TVDrawer_{d}", 6.28, 2.86 + d * 0.66, Z1 + 0.14, 6.32, 3.46 + d * 0.66, Z1 + 0.44, "Mat_WallFacadeWarm", bevel=0.006)
for sl in range(11):
    sly = 2.84 + sl * 0.195
    add_box(col_fl1_furn, f"Living_TVLouverSlat_{sl}", 6.71, sly, Z1 + 0.50, 6.76, sly + 0.05, Z1 + 2.30, "Mat_WoodLouverFacade")
add_box(col_fl1_furn, "Living_TVFrame", 6.66, 3.18, Z1 + 0.76, 6.71, 4.52, Z1 + 1.56, "Mat_MetalMatteBlack", bevel=0.008)
add_box(col_fl1_furn, "Living_TVScreen", 6.645, 3.22, Z1 + 0.80, 6.67, 4.48, Z1 + 1.52, "Mat_TVScreenBlack")
add_box(col_fl1_furn, "Living_Soundbar", 6.46, 3.38, Z1 + 0.50, 6.58, 4.32, Z1 + 0.58, "Mat_MetalMatteBlack", bevel=0.01)
add_cyl(col_fl1_furn, "Living_ConsoleVase", 6.52, 3.00, Z1 + 0.50, Z1 + 0.72, 0.06, 0.04, "Mat_CeramicTeal")
add_books_row(col_fl1_furn, "Living_ConsoleBooks", 6.44, 4.50, Z1 + 0.50, count=4, axis='Y')
add_box(col_lights, "Living_TV_TopLED", 6.69, 2.82, Z1 + 2.27, 6.74, 4.88, Z1 + 2.31, "Mat_WarmLED")
add_potted_plant(col_fl1_furn, "Living_FicusPlant", 6.42, 5.36, Z1, scale=1.15, pot_mat="Mat_CeramicWhite")

# Thảm phòng khách + Bộ Sofa chữ L ngồi xem TV (lưng Sofa dọc X=3.32 giữ trọn đường luồng trong nhà X=2.22..3.25)
add_box(col_fl1_furn, "Living_AreaRug", 3.45, 2.45, Z1, 6.00, 5.30, Z1 + 0.025, "Mat_RugWarm", bevel=0.008)
add_box(col_fl1_furn, "Living_Sofa_Base", 3.34, 2.55, Z1 + 0.08, 4.24, 5.18, Z1 + 0.44, "Mat_FabricSofaWarm", bevel=0.03)
add_box(col_fl1_furn, "Living_Sofa_Chaise", 4.20, 2.55, Z1 + 0.08, 4.98, 3.32, Z1 + 0.44, "Mat_FabricSofaWarm", bevel=0.03)
add_box(col_fl1_furn, "Living_Sofa_Back", 3.32, 2.55, Z1 + 0.44, 3.66, 5.18, Z1 + 0.86, "Mat_FabricSofaWarm", bevel=0.04)
add_box(col_fl1_furn, "Living_Sofa_Arm1", 3.34, 2.49, Z1 + 0.08, 4.98, 2.66, Z1 + 0.66, "Mat_FabricSofaWarm", bevel=0.025)
add_box(col_fl1_furn, "Living_Sofa_Arm2", 3.34, 5.06, Z1 + 0.08, 4.24, 5.24, Z1 + 0.66, "Mat_FabricSofaWarm", bevel=0.025)
for si in range(3):
    sy1 = 2.68 + si * 0.79
    add_box(col_fl1_furn, f"Living_SofaSeat_{si}", 3.64, sy1, Z1 + 0.40, 4.22, sy1 + 0.76, Z1 + 0.52, "Mat_FabricBeige", bevel=0.03)
pillow_specs = [
    (3.82, 2.94, "Mat_CushionMustard"),
    (3.82, 3.58, "Mat_CushionNavy"),
    (3.82, 4.22, "Mat_CushionTerracotta"),
    (3.82, 4.82, "Mat_CushionMustard"),
]
for pi, (px, py, pm) in enumerate(pillow_specs):
    add_box(col_fl1_furn, f"Living_Pillow_{pi}", px - 0.14, py - 0.22, Z1 + 0.50, px + 0.12, py + 0.22, Z1 + 0.82, pm, bevel=0.05)

# Bàn trà tròn đá cẩm thạch đặt giữa Sofa và TV
add_cyl(col_fl1_furn, "Living_CoffeeTableTop", 5.18, 4.05, Z1 + 0.40, Z1 + 0.45, 0.48, 0.48, "Mat_WhiteMarble", segs=24)
add_cyl(col_fl1_furn, "Living_CoffeeTableRim", 5.18, 4.05, Z1 + 0.37, Z1 + 0.41, 0.46, 0.46, "Mat_BrassGold", segs=24)
for i, ang in enumerate([0, 2.09, 4.18]):
    add_cyl(col_fl1_furn, f"Living_CoffeeLeg_{i}", 5.18 + 0.30 * math.cos(ang), 4.05 + 0.30 * math.sin(ang), Z1 + 0.02, Z1 + 0.38, 0.022, 0.022, "Mat_MetalMatteBlack", segs=10)
add_cyl(col_fl1_furn, "Living_FlowerVase", 5.26, 4.12, Z1 + 0.45, Z1 + 0.67, 0.07, 0.045, "Mat_CeramicWhite", segs=16)
add_sphere(col_fl1_furn, "Living_Flowers1", 5.26, 4.12, Z1 + 0.74, 0.11, "Mat_FlowerPink")
add_sphere(col_fl1_furn, "Living_Flowers2", 5.18, 4.06, Z1 + 0.72, 0.08, "Mat_FlowerYellow")
add_box(col_fl1_furn, "Living_ArtBook1", 4.92, 3.74, Z1 + 0.45, 5.18, 3.96, Z1 + 0.49, "Mat_BookBlue", bevel=0.004)
add_box(col_fl1_furn, "Living_ArtBook2", 4.95, 3.77, Z1 + 0.49, 5.15, 3.93, Z1 + 0.52, "Mat_BookAmber", bevel=0.004)

# Đèn cây đứng góc Sofa & Đèn chùm trần Phòng khách (tường đường luồng phía Nam để trơn thoáng, không treo tranh)
add_cyl(col_fl1_furn, "Living_FloorLampBase", 3.60, 5.45, Z1, Z1 + 0.04, 0.17, 0.15, "Mat_BrassGold", segs=16)
add_cyl(col_fl1_furn, "Living_FloorLampPole", 3.60, 5.45, Z1 + 0.04, Z1 + 1.62, 0.018, 0.015, "Mat_BrassGold", segs=10)
add_cyl(col_fl1_furn, "Living_FloorLampShade", 3.60, 5.45, Z1 + 1.45, Z1 + 1.78, 0.20, 0.15, "Mat_LampShadeGlow", segs=18)
add_pendant_chandelier(col_lights, "Living_Chandelier", 5.05, 3.95, H1 - 0.02, drop=0.72, count=3)

# --- B. PHÒNG NGỦ BA MẸ (X = 3.22..6.78, Y = 5.85..8.95) ---
# - Cửa sổ 1 (vách Đông Y=5.80): khung hộp gỗ sồi 3 ô kính nhôm slim đồng trục giường (X=4.30..5.86), mở ra thấy Sofa
# - Cửa sổ 2 (vách Tây Y=9.00): đặt SÁT TƯỜNG PHÍA NAM (X=3.28..4.30, 2 ô kính gỗ sồi thanh thoát) lấy gió sau & nhìn thẳng ra khu Bếp!
# - Cả 2 cửa sổ căn thẳng đỉnh Z1+2.22 đồng trục với đỉnh cửa phòng Ba Mẹ, có hộp rèm cuốn linen gọn gàng
# - Cửa chính (vách Nam X=3.17, Y=5.95..6.85): mở ra đường luồng trong nhà phía Nam
# - Giường ngủ: Đầu hướng TÂY (Y=8.90, tựa mảng tường đặc vững chãi), chân hướng ĐÔNG (Y=6.92)
# - Hai bên giường: Tủ đồ SIÊU DÀI KỊCH TRẦN dọc trọn tường Bắc bên TRÁI giường (Y=5.90..8.92, dài 3.02m, 2 tầng kịch trần!),
#   Bàn ghế bên PHẢI giường (phía Nam X=3.26..3.80) & Bàn góc đầu giường (X=3.80..4.24) để sách & điện thoại

# Vách Đông ngăn Phòng khách (Cửa sổ 1 khung gỗ sồi 3 ô kính thanh thoát, cân đối trục giường X=4.30..5.86)
add_box(col_fl1_arch, "Wall_Living_Parents_Bot", 3.12, 5.75, Z1, 6.78, 5.85, Z1 + 1.12, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Living_Parents_Top", 3.12, 5.75, Z1 + 2.22, 6.78, 5.85, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Living_Parents_L", 3.12, 5.75, Z1 + 1.12, 4.30, 5.85, Z1 + 2.22, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Living_Parents_R", 5.86, 5.75, Z1 + 1.12, 6.78, 5.85, Z1 + 2.22, "Mat_WallWarmWhite")
add_refined_interior_window(col_fl1_arch, col_lights, "Win_Parents_East_Sofa",
                            4.30, 5.80, Z1 + 1.12, 5.86, Z1 + 2.22,
                            sill_side='Y_MAX', panes=3, with_led=False, with_decor=True)

# Vách Tây ngăn Cầu thang & Bếp (Cửa sổ 2 đặt SÁT TƯỜNG PHÍA NAM X=3.28..4.30, đón gió sau & nhìn ra Bếp thoáng mát!)
add_box(col_fl1_arch, "Wall_Parents_West_Bot", 3.12, 8.95, Z1, 6.78, 9.05, Z1 + 1.02, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Parents_West_Top", 3.12, 8.95, Z1 + 2.22, 6.78, 9.05, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Parents_West_L", 3.12, 8.95, Z1 + 1.02, 3.28, 9.05, Z1 + 2.22, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Parents_West_R", 4.30, 8.95, Z1 + 1.02, 6.78, 9.05, Z1 + 2.22, "Mat_WallWarmWhite")
add_refined_interior_window(col_fl1_arch, col_lights, "Win_Parents_West_Stair",
                            3.28, 9.00, Z1 + 1.02, 4.30, Z1 + 2.22,
                            sill_side='Y_MIN', panes=2, with_led=True, with_decor=True)

# Vách Nam ngăn đường luồng trong nhà (có Cửa chính phòng Ba Mẹ hướng ra đường luồng tại Y=5.95..6.85)
add_box(col_fl1_arch, "Wall_Parents_Hall_Front", 3.12, 5.80, Z1, 3.22, 5.95, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Parents_HallTop", 3.12, 5.95, Z1 + 2.20, 3.22, 6.85, H1, "Mat_WallWarmWhite")
add_box(col_fl1_arch, "Wall_Parents_Hall", 3.12, 6.85, Z1, 3.22, 9.00, H1, "Mat_WallWarmWhite")
# Khung gỗ & cánh cửa chính phòng Ba Mẹ mở nhẹ vào trong
add_box(col_fl1_arch, "Parents_DoorFrame1", 3.10, 5.93, Z1, 3.24, 5.98, Z1 + 2.22, "Mat_WoodOakDark")
add_box(col_fl1_arch, "Parents_DoorFrame2", 3.10, 6.82, Z1, 3.24, 6.87, Z1 + 2.22, "Mat_WoodOakDark")
add_box(col_fl1_arch, "Parents_DoorFrameTop", 3.10, 5.93, Z1 + 2.18, 3.24, 6.87, Z1 + 2.24, "Mat_WoodOakDark")
add_box(col_fl1_arch, "Parents_DoorLeaf", 3.24, 5.96, Z1 + 0.01, 4.02, 6.01, Z1 + 2.17, "Mat_WoodOakTable", bevel=0.008)

# Nội thất Phòng Ba Mẹ:
# 1. Thảm & Giường ngủ (đầu hướng Tây Y=8.90 tựa tường đặc, chân hướng Đông Y=6.92, X=4.34..5.80)
add_box(col_fl1_furn, "Parents_Rug", 4.00, 6.62, Z1, 6.08, 8.82, Z1 + 0.025, "Mat_RugWarm", bevel=0.008)
add_detailed_bed(col_fl1_furn, "Parents_Bed", 4.34, 6.92, Z1 + 0.02, 5.80, 8.90, head_side='Y_MAX',
                 duvet_mat="Mat_CushionNavy", headboard_h=1.02)

# 2. Bàn nhỏ góc đầu giường (X=3.80..4.24, Y=8.46..8.86 — ngay dưới cửa sổ Nam-Tây) để sách & điện thoại trước khi ngủ
add_nightstand(col_fl1_furn, "Parents_CornerBedside", 4.02, 8.66, Z1 + 0.02)
add_box(col_fl1_furn, "Parents_BedsideBook1", 3.87, 8.52, Z1 + 0.50, 4.03, 8.68, Z1 + 0.535, "Mat_BookBlue", bevel=0.003)
add_box(col_fl1_furn, "Parents_BedsideBook2", 3.89, 8.54, Z1 + 0.535, 4.01, 8.66, Z1 + 0.56, "Mat_BookAmber", bevel=0.003)
add_box(col_fl1_furn, "Parents_BedsidePhone", 4.07, 8.50, Z1 + 0.50, 4.15, 8.64, Z1 + 0.515, "Mat_MetalMatteBlack", bevel=0.003)
add_box(col_fl1_furn, "Parents_BedsidePhoneScr", 4.08, 8.51, Z1 + 0.514, 4.14, 8.63, Z1 + 0.518, "Mat_SmartCyanLED")

# 3. TỦ QUẦN ÁO SIÊU DÀI KỊCH TRẦN BÊN TRÁI GIƯỜNG (trọn tường Bắc X=6.22..6.76, Y=5.90..8.92 — dài 3.02m, cao kịch trần 3.08m!)
add_wardrobe(col_fl1_furn, "Parents_Wardrobe", 6.22, 5.90, Z1, 6.76, 8.92, h=2.26, door_face='X_MIN')
# Tầng tủ kho kịch trần phía trên để chăn màn, vali & đồ trái mùa (Z1+2.26..Z1+3.08)
add_box(col_fl1_furn, "Parents_Wardrobe_TopCarcass", 6.22, 5.90, Z1 + 2.26, 6.76, 8.92, Z1 + 3.08, "Mat_WoodOakCabinet", bevel=0.008)
for ud in range(5):
    udy1 = 5.90 + ud * (3.02 / 5.0) + 0.015
    udy2 = 5.90 + (ud + 1) * (3.02 / 5.0) - 0.015
    add_box(col_fl1_furn, f"Parents_Wardrobe_TopDoor_{ud}", 6.195, udy1, Z1 + 2.29, 6.23, udy2, Z1 + 3.04, "Mat_WallFacadeWarm", bevel=0.006)
    umy = (udy1 + udy2) / 2.0
    add_box(col_fl1_furn, f"Parents_Wardrobe_TopHandle_{ud}", 6.17, umy - 0.08, Z1 + 2.38, 6.195, umy + 0.08, Z1 + 2.41, "Mat_BrassGold", bevel=0.003)

# 4. Bàn ghế bên PHẢI giường (phía Nam X=3.26..3.80, Y=7.10..8.15 — áp vách Nam, có bàn + ghế ngồi đọc sách)
add_box(col_fl1_furn, "Parents_SideTableTop", 3.26, 7.18, Z1 + 0.72, 3.78, 8.08, Z1 + 0.76, "Mat_WoodOakTable", bevel=0.01)
for i, (lx, ly) in enumerate([(3.31, 7.24), (3.73, 7.24), (3.31, 8.02), (3.73, 8.02)]):
    add_box(col_fl1_furn, f"Parents_SideTableLeg_{i}", lx - 0.02, ly - 0.02, Z1, lx + 0.02, ly + 0.02, Z1 + 0.72, "Mat_MetalMatteBlack")
add_dining_chair(col_fl1_furn, "Parents_SideChair", 3.86, 7.63, Z1, math.pi / 2, seat_mat="Mat_CushionMustard", wood_mat="Mat_WoodOakTable")
add_books_row(col_fl1_furn, "Parents_TableBooks", 3.32, 7.72, Z1 + 0.76, count=4, axis='Y')
add_cyl(col_fl1_furn, "Parents_TableCup", 3.55, 7.42, Z1 + 0.76, Z1 + 0.85, 0.035, 0.04, "Mat_CeramicTeal", segs=12)

add_potted_plant(col_fl1_furn, "Parents_Plant", 3.48, 8.66, Z1, scale=0.62, pot_mat="Mat_CeramicWhite")
add_pendant_chandelier(col_lights, "Parents_CeilingLamp", 5.00, 7.40, H1 - 0.02, drop=0.42, count=1)

# --- C. CẦU THANG GỖ 1 VẾ THẲNG KIỂU LỬNG CỔ ĐIỂN ẤM ÁP (ĐÚNG MẪU ẢNH THAM KHẢO — KHÔNG LÀM 2 VẾ CHỮ U!) ---
# Tham khảo đúng mẫu ảnh gỗ kiểu lửng từ tubepthien.vn/cau-thang-giua-phong-khach-va-bep.html:
# - CHỈ 1 VẾ THẲNG DUY NHẤT (Y = 9.08..10.14, rộng 1.06m) đi thẳng từ hành lang Nam (X=2.72, Z1=0.54) lên Sảnh Lửng Tầng 2 phía Bắc (X=5.92..6.78, Z2=3.85)!
# - Bậc khởi đầu bo tròn rộng 2 bên + 2 TRỤ CÁI GỖ VUÔNG LỚN CÓ MŨ TRỤ hai bên chân thang!
# - 16 bậc gỗ liền khối đóng kín cổ bậc (có thảm/dải chống trượt kem sáng giữa bậc cực êm & an toàn cho Ba Mẹ) + hệ CON TIỆN GỖ DỌC 2 bên + TAY VỊN GỖ BẢN LỚN!
# - Dưới gầm thang đóng VÁCH ỐP PANO GỖ SỒI CHIA Ô DỌC sang trọng (tích hợp khoang lưu trữ kín dưới gầm)!
# - Ô thông tầng Tầng 2 ốp diềm sàn gỗ & lan can CON TIỆN GỖ đồng bộ chuẩn kiểu gác lửng!
N_MEZZ_STEPS = 16
STEP_RISE = (3.85 - Z1) / (N_MEZZ_STEPS + 1)  # 3.31 / 17 = 0.1947m
STEP_DX = (5.92 - 2.72) / N_MEZZ_STEPS        # 3.20 / 16 = 0.200m (với mũi bậc vươn 3.5cm -> mặt bậc 23.5cm êm chân!)

# 1. Bậc khởi đầu bo tròn rộng 2 bên (Starter Bullnose Step: X=2.66..2.98, Y=8.98..10.24)
add_box(col_fl1_arch, "Stair_StarterStep_Core", 2.68, 9.02, Z1, 2.98, 10.20, Z1 + STEP_RISE, "Mat_WoodOakCabinet", bevel=0.008)
add_box(col_fl1_arch, "Stair_StarterStep_Top", 2.66, 9.00, Z1 + STEP_RISE - 0.045, 2.99, 10.22, Z1 + STEP_RISE, "Mat_WoodStairTreads", bevel=0.008)
for bni, bny in enumerate([9.02, 10.20]):
    add_cyl(col_fl1_arch, f"Stair_StarterBullnose_{bni}", 2.82, bny, Z1, Z1 + STEP_RISE, 0.14, 0.14, "Mat_WoodStairTreads", segs=18)

# 2. Hai trụ cái gỗ lớn vuông có đế, thân soi rãnh & mũ trụ (2 Newel Posts tại chân cầu thang!)
def add_wood_newel_post(col, name, cx, cy, z_base, height=1.12):
    add_box(col, f"{name}_Plinth", cx - 0.08, cy - 0.08, z_base, cx + 0.08, cy + 0.08, z_base + 0.16, "Mat_WoodOakDark", bevel=0.006)
    add_box(col, f"{name}_Shaft", cx - 0.065, cy - 0.065, z_base + 0.16, cx + 0.065, cy + 0.065, z_base + height - 0.16, "Mat_WoodStairTreads", bevel=0.006)
    add_box(col, f"{name}_Neck", cx - 0.075, cy - 0.075, z_base + height - 0.18, cx + 0.075, cy + 0.075, z_base + height - 0.14, "Mat_WoodOakDark", bevel=0.004)
    add_box(col, f"{name}_Head", cx - 0.07, cy - 0.07, z_base + height - 0.14, cx + 0.07, cy + 0.07, z_base + height - 0.04, "Mat_WoodOakCabinet", bevel=0.006)
    add_box(col, f"{name}_Cap", cx - 0.09, cy - 0.09, z_base + height - 0.04, cx + 0.09, cy + 0.09, z_base + height, "Mat_WoodOakDark", bevel=0.008)

add_wood_newel_post(col_fl1_arch, "Stair_Newel_StartE", 2.82, 9.06, Z1 + STEP_RISE, height=1.08)
add_wood_newel_post(col_fl1_arch, "Stair_Newel_StartW", 2.82, 10.16, Z1 + STEP_RISE, height=1.08)

# 3. 16 bậc gỗ đóng kín cổ bậc + thảm/dải chống trượt kem sáng giữa bậc + hệ CON TIỆN GỖ 2 bên + vách ốp PANO GỖ gầm thang!
for s in range(N_MEZZ_STEPS):
    sx1 = 2.72 + s * STEP_DX
    sx2 = sx1 + 0.235
    sz = Z1 + (s + 1) * STEP_RISE
    if s > 0:
        # Mặt bậc gỗ & cổ bậc đóng kín chắc chắn
        add_box(col_fl1_arch, f"Stair_Wood_Tread_{s}", sx1, 9.08, sz - 0.048, sx2, 10.14, sz, "Mat_WoodStairTreads", bevel=0.006)
        add_box(col_fl1_arch, f"Stair_Wood_Riser_{s}", sx1 + 0.015, 9.08, sz - STEP_RISE, sx1 + 0.055, 10.14, sz - 0.045, "Mat_WoodOakCabinet")
    # Dải thảm chống trượt kem ấm giữa từng bậc (êm chân & giống mẫu ảnh!)
    add_box(col_fl1_arch, f"Stair_Runner_Tread_{s}", sx1 + 0.005, 9.24, sz - 0.004, sx2 - 0.01, 9.98, sz + 0.012, "Mat_BeddingCream", bevel=0.004)
    add_box(col_fl1_arch, f"Stair_Runner_Riser_{s}", sx1 + 0.002, 9.24, sz - STEP_RISE + 0.005, sx1 + 0.022, 9.98, sz + 0.008, "Mat_BeddingCream")
    # Vách ốp pano gỗ sồi đóng kín phần gầm tam giác bên dưới bậc (từ bậc 2 trở lên, chia ô pano dọc sang trọng!)
    if s >= 1:
        add_box(col_fl1_arch, f"Stair_Wainscot_Body_{s}", sx1 + 0.015, 9.08, Z1, sx1 + STEP_DX + 0.015, 10.14, sz - STEP_RISE + 0.01, "Mat_WoodOakCabinet")
        if s % 2 == 1 and sz - STEP_RISE > Z1 + 0.35:
            # Gờ chỉ pano dọc & khung ô pano nổi trên mặt Tây nhìn từ Bếp
            add_box(col_fl1_arch, f"Stair_PanelStile_{s}", sx1 + 0.01, 10.13, Z1 + 0.08, sx1 + 0.05, 10.16, sz - STEP_RISE - 0.02, "Mat_WoodOakDark", bevel=0.003)
    # Con tiện gỗ dọc thanh mảnh 2 bên mỗi bậc (trừ bậc đầu có trụ cái lớn)
    if s >= 1:
        for side_tag, by in [("E", 9.10), ("W", 10.12)]:
            add_cyl(col_fl1_arch, f"Stair_Baluster_{side_tag}_{s}", sx1 + 0.11, by, sz, sz + 0.90, 0.016, 0.014, "Mat_WoodStairTreads", segs=10)

# Nẹp chân tường gỗ & má thang nghiêng gỗ sồi mặt Tây (hướng ra Bếp) + 2 tay vịn gỗ bản lớn chạy nghiêng 2 bên!
add_box(col_fl1_arch, "Stair_Wainscot_Baseboard", 2.94, 10.13, Z1, 5.92, 10.17, Z1 + 0.10, "Mat_WoodOakDark", bevel=0.004)
str_dx = 5.92 - 2.72
str_dz = 3.85 - (Z1 + STEP_RISE)
str_len = math.hypot(str_dx, str_dz)
str_ang = math.atan2(str_dz, str_dx)
str_cx = (2.72 + 5.92) / 2.0
str_cz = (Z1 + STEP_RISE + 3.85) / 2.0 - 0.10
add_box(col_fl1_arch, "Stair_WoodStringer_W",
        str_cx - str_len / 2.0, 10.11, str_cz - 0.10,
        str_cx + str_len / 2.0, 10.17, str_cz + 0.10,
        "Mat_WoodOakDark", bevel=0.006, rot=(0, -str_ang, 0))
hr_z1 = Z1 + STEP_RISE + 0.92
hr_z2 = 3.85 + 0.92
hr_dx = 5.94 - 2.80
hr_dz = hr_z2 - hr_z1
hr_len = math.hypot(hr_dx, hr_dz)
hr_ang = math.atan2(hr_dz, hr_dx)
hr_cx = (2.80 + 5.94) / 2.0
hr_cz = (hr_z1 + hr_z2) / 2.0
for side_tag, hy in [("E", 9.10), ("W", 10.12)]:
    add_box(col_fl1_arch, f"Stair_WoodHandrail_{side_tag}",
            hr_cx - hr_len / 2.0, hy - 0.04, hr_cz - 0.035,
            hr_cx + hr_len / 2.0, hy + 0.04, hr_cz + 0.035,
            "Mat_WoodOakDark", bevel=0.008, rot=(0, -hr_ang, 0))

# 4. Chiếu tới Sảnh Lửng phía Bắc (X=5.92..6.78, Y=8.95..10.14, Z=3.70..3.85) + Trụ cái gỗ đỉnh & con tiện gỗ đồng bộ!
add_box(col_fl1_arch, "Stair_Mezz_TopLanding", 5.92, 8.95, 3.85 - 0.15, 6.78, 10.14, 3.85, "Mat_WoodStairTreads", bevel=0.008)
add_box(col_fl1_arch, "Stair_Mezz_TopFascia", 5.92, 10.12, 3.85 - 0.20, 6.78, 10.18, 3.85 + 0.03, "Mat_WoodOakDark", bevel=0.006)
add_wood_newel_post(col_fl1_arch, "Stair_Newel_TopW", 5.94, 10.12, 3.85, height=1.02)
add_box(col_fl1_arch, "Stair_Mezz_TopGuardRail", 5.94, 10.08, 3.85 + 0.90, 6.78, 10.16, 3.85 + 0.97, "Mat_WoodOakDark", bevel=0.006)
for bi in range(5):
    bx = 6.08 + bi * 0.14
    add_cyl(col_fl1_arch, f"Stair_Mezz_TopBaluster_{bi}", bx, 10.12, 3.85, 3.85 + 0.90, 0.016, 0.014, "Mat_WoodStairTreads", segs=10)

# --- D. PHÒNG BẾP CHỮ L (BẮC + TÂY): 1 TỦ SÁT BẾP HƯỚNG NAM + 1 TỦ XOONG CAO NGANG BẰNG TỦ LẠNH + MÁY LỌC NƯỚC ---
# Tất cả đồng cao độ đỉnh Z_CAB_TOP = Z1 + 1.86 = 2.40m (tủ kính + tủ xoong + tủ lạnh thẳng tắp 1 đường ngang cực đẹp!)
Z_CAB_TOP = Z1 + 1.86

# 1. TỦ CHÉN BÁT CÚNG GIỖ KÍNH MÀU ĐỒNG — ĐẶT SÁT LIỀN VÀO TỦ BẾP BẮC, MẶT TỦ HƯỚNG VÀO PHÍA NAM (-X)!
add_box(col_fl1_furn, "Kitchen_FeastDishCab_Back", 6.71, 11.18, Z1, 6.76, 12.22, Z_CAB_TOP, "Mat_WoodOakCabinet")
add_box(col_fl1_furn, "Kitchen_FeastDishCab_Top", 6.08, 11.18, Z_CAB_TOP - 0.05, 6.76, 12.22, Z_CAB_TOP, "Mat_WoodOakTable", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_FeastDishCab_Bot", 6.08, 11.18, Z1, 6.76, 12.22, Z1 + 0.08, "Mat_WoodOakCabinet")
add_box(col_fl1_furn, "Kitchen_FeastDishCab_SideE", 6.08, 11.18, Z1, 6.76, 11.23, Z_CAB_TOP, "Mat_WoodOakCabinet")
add_box(col_fl1_furn, "Kitchen_FeastDishCab_SideW", 6.08, 12.17, Z1, 6.76, 12.22, Z_CAB_TOP, "Mat_WoodOakCabinet")
for sh_i, sh_z in enumerate([Z1 + 0.46, Z1 + 0.90, Z1 + 1.34]):
    add_box(col_fl1_furn, f"UnderStair_DishShelf_{sh_i}", 6.14, 11.23, sh_z, 6.71, 12.17, sh_z + 0.032, "Mat_WoodOakTable")
    add_box(col_lights, f"UnderStair_DishLED_{sh_i}", 6.16, 11.28, sh_z - 0.02, 6.20, 12.12, sh_z, "Mat_WarmLED")
add_box(col_lights, "UnderStair_DishLED_Top", 6.16, 11.28, Z_CAB_TOP - 0.09, 6.20, 12.12, Z_CAB_TOP - 0.05, "Mat_WarmLED")
for col_i, by in enumerate([11.42, 11.70, 11.98]):
    for st in range(5):
        add_cyl(col_fl1_furn, f"Feast_PlateStack_{col_i}_{st}", 6.42, by, Z1 + 0.08 + st * 0.032, Z1 + 0.106 + st * 0.032, 0.095, 0.115, "Mat_CeramicWhite", segs=16)
    for st in range(3):
        add_cyl(col_fl1_furn, f"Feast_BigBowl_{col_i}_{st}", 6.42, by, Z1 + 0.495 + st * 0.075, Z1 + 0.565 + st * 0.075, 0.062, 0.10, "Mat_CeramicWhite", segs=16)
    for st in range(4):
        add_cyl(col_fl1_furn, f"Feast_RiceBowl_{col_i}_{st}", 6.42, by, Z1 + 0.935 + st * 0.055, Z1 + 0.985 + st * 0.055, 0.046, 0.072, "Mat_CeramicWhite", segs=14)
    add_cyl(col_fl1_furn, f"Feast_CupSet_{col_i}", 6.42, by, Z1 + 1.375, Z1 + 1.52, 0.052, 0.052, "Mat_CeramicTeal" if col_i == 1 else "Mat_CeramicWhite", segs=14)
for di, (dy1, dy2) in enumerate([(11.23, 11.69), (11.71, 12.17)]):
    add_box(col_fl1_furn, f"UnderStair_GlassDoor_{di}", 6.08, dy1 + 0.04, Z1 + 0.14, 6.12, dy2 - 0.04, Z_CAB_TOP - 0.11, "Mat_GlassBronze")
    add_box(col_fl1_furn, f"UnderStair_DoorFrameL_{di}", 6.07, dy1, Z1 + 0.08, 6.13, dy1 + 0.042, Z_CAB_TOP - 0.05, "Mat_WoodOakDark")
    add_box(col_fl1_furn, f"UnderStair_DoorFrameR_{di}", 6.07, dy2 - 0.042, Z1 + 0.08, 6.13, dy2, Z_CAB_TOP - 0.05, "Mat_WoodOakDark")
    add_box(col_fl1_furn, f"UnderStair_DoorFrameT_{di}", 6.07, dy1, Z_CAB_TOP - 0.11, 6.13, dy2, Z_CAB_TOP - 0.05, "Mat_WoodOakDark")
    add_box(col_fl1_furn, f"UnderStair_DoorFrameB_{di}", 6.07, dy1, Z1 + 0.08, 6.13, dy2, Z1 + 0.14, "Mat_WoodOakDark")
    hy = dy2 - 0.055 if di == 0 else dy1 + 0.055
    add_box(col_fl1_furn, f"UnderStair_GlassHandle_{di}", 6.04, hy - 0.011, Z1 + 0.85, 6.07, hy + 0.011, Z1 + 1.25, "Mat_BrassGold", bevel=0.003)

# 2. TỦ XOONG NỒI TO CÚNG GIỖ — CHIỀU CAO NGANG BẰNG TỦ LẠNH (Z_CAB_TOP = 2.40m = 1.86m) XỊT GỌN DƯỚI GẦM THANG!
add_box(col_fl1_furn, "UnderStair_PotCab_Back", 5.04, 10.22, Z1, 6.04, 10.28, Z_CAB_TOP, "Mat_WoodOakCabinet")
add_box(col_fl1_furn, "UnderStair_PotCab_Top", 5.04, 10.22, Z_CAB_TOP - 0.05, 6.04, 11.14, Z_CAB_TOP, "Mat_WoodOakTable", bevel=0.008)
add_box(col_fl1_furn, "UnderStair_PotCab_Bot", 5.04, 10.22, Z1, 6.04, 11.14, Z1 + 0.08, "Mat_WoodOakCabinet")
add_box(col_fl1_furn, "UnderStair_PotCab_SideL", 5.04, 10.22, Z1, 5.09, 11.14, Z_CAB_TOP, "Mat_WoodOakCabinet")
add_box(col_fl1_furn, "UnderStair_PotCab_SideR", 5.99, 10.22, Z1, 6.04, 11.14, Z_CAB_TOP, "Mat_WoodOakCabinet")
add_box(col_fl1_furn, "UnderStair_PotShelf_Mid", 5.09, 10.28, Z1 + 0.88, 5.99, 11.06, Z1 + 0.92, "Mat_WoodOakTable")
add_box(col_lights, "UnderStair_PotLED", 5.14, 10.96, Z_CAB_TOP - 0.09, 5.94, 11.00, Z_CAB_TOP - 0.05, "Mat_WarmLED")
add_cyl(col_fl1_furn, "Feast_BigPot_1", 5.34, 10.68, Z1 + 0.08, Z1 + 0.44, 0.21, 0.21, "Mat_MetalStainless", segs=20)
add_cyl(col_fl1_furn, "Feast_BigPotLid_1", 5.34, 10.68, Z1 + 0.44, Z1 + 0.48, 0.22, 0.14, "Mat_MetalStainless", segs=20)
add_cyl(col_fl1_furn, "Feast_BigPot_2", 5.74, 10.68, Z1 + 0.08, Z1 + 0.36, 0.16, 0.16, "Mat_MetalStainless", segs=18)
add_cyl(col_fl1_furn, "Feast_BigPotLid_2", 5.74, 10.68, Z1 + 0.36, Z1 + 0.39, 0.17, 0.11, "Mat_MetalStainless", segs=18)
for tr_i in range(4):
    add_cyl(col_fl1_furn, f"Feast_Tray_{tr_i}", 5.54, 10.68, Z1 + 0.50 + tr_i * 0.032, Z1 + 0.525 + tr_i * 0.032, 0.28, 0.30, "Mat_MetalStainless", segs=22)
add_cyl(col_fl1_furn, "Feast_MidPot_1", 5.34, 10.68, Z1 + 0.92, Z1 + 1.24, 0.17, 0.17, "Mat_MetalStainless", segs=18)
add_cyl(col_fl1_furn, "Feast_MidPot_2", 5.74, 10.68, Z1 + 0.92, Z1 + 1.18, 0.15, 0.15, "Mat_CeramicTeal", segs=18)
add_box(col_fl1_furn, "UnderStair_PotDoor_L", 5.09, 11.10, Z1 + 0.08, 5.53, 11.14, Z_CAB_TOP - 0.05, "Mat_WallFacadeWarm", bevel=0.006)
add_box(col_fl1_furn, "UnderStair_PotDoor_R", 5.55, 11.10, Z1 + 0.08, 5.99, 11.14, Z_CAB_TOP - 0.05, "Mat_WallFacadeWarm", bevel=0.006)
add_box(col_fl1_furn, "UnderStair_PotHandle_L", 5.47, 11.14, Z1 + 0.85, 5.50, 11.17, Z1 + 1.25, "Mat_BrassGold", bevel=0.003)
add_box(col_fl1_furn, "UnderStair_PotHandle_R", 5.58, 11.14, Z1 + 0.85, 5.61, 11.17, Z1 + 1.25, "Mat_BrassGold", bevel=0.003)

# 3. 🧊 TỦ LẠNH 2 CÁNH (CAO ĐÚNG BẰNG TỦ XOONG 1.86m -> Z_CAB_TOP = 2.40m!) & 💧 MÁY LỌC NƯỚC RO DƯỚI GẦM THANG
add_box(col_fl1_furn, "Kitchen_Fridge", 4.16, 10.32, Z1, 4.96, 11.12, Z_CAB_TOP, "Mat_MetalStainless", bevel=0.02)
add_box(col_fl1_furn, "Kitchen_FridgeSplit", 4.55, 11.11, Z1 + 0.06, 4.57, 11.14, Z_CAB_TOP - 0.04, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "Kitchen_FridgeHandle1", 4.47, 11.12, Z1 + 0.85, 4.50, 11.16, Z1 + 1.48, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "Kitchen_FridgeHandle2", 4.62, 11.12, Z1 + 0.85, 4.65, 11.16, Z1 + 1.48, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "Kitchen_WaterPurifier_Body", 3.64, 10.68, Z1, 4.08, 11.10, Z1 + 1.14, "Mat_CeramicWhite", bevel=0.015)
add_box(col_fl1_furn, "Kitchen_WaterPurifier_Front", 3.66, 11.08, Z1 + 0.06, 4.06, 11.12, Z1 + 1.10, "Mat_PianoBlackGloss", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_WaterPurifier_Niche", 3.72, 11.00, Z1 + 0.64, 4.00, 11.13, Z1 + 0.90, "Mat_MetalStainless")
add_cyl(col_fl1_furn, "Kitchen_WaterPurifier_Tap1", 3.81, 11.07, Z1 + 0.82, Z1 + 0.89, 0.012, 0.012, "Mat_MetalStainless", segs=8)
add_cyl(col_fl1_furn, "Kitchen_WaterPurifier_Tap2", 3.91, 11.07, Z1 + 0.82, Z1 + 0.89, 0.012, 0.012, "Mat_MetalStainless", segs=8)
add_box(col_fl1_furn, "Kitchen_WaterPurifier_LED", 3.76, 11.11, Z1 + 0.96, 3.96, 11.13, Z1 + 1.02, "Mat_SmartCyanLED")
add_cyl(col_fl1_furn, "Kitchen_WaterPurifier_Glass", 3.86, 11.07, Z1 + 0.64, Z1 + 0.74, 0.032, 0.036, "Mat_GlassClear", segs=12)

# 3. BẾP CHỮ L KÉO DÀI TỪ HƯỚNG BẮC BẾP (X=6.08..6.76) NGOẶT SANG HƯỚNG TÂY BẾP (Y=15.08..15.76)
# Nhánh hướng Bắc: Bồn rửa chén -> Máy rửa chén âm tủ chuẩn 60cm -> BẾP HỒNG NGOẠI ĐÔI SÁT TƯỜNG BẮC!
# (Người nấu hướng mặt về PHÍA BẮC +X, nhìn sang BÊN TRÁI +Y thấy ngay cửa sổ hướng ra Phòng tắm!)
add_box(col_fl1_furn, "Kitchen_L_NorthBase", 6.08, 12.22, Z1, 6.76, 15.76, Z1 + 0.86, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl1_furn, "Kitchen_L_NorthTop", 6.04, 12.20, Z1 + 0.86, 6.78, 15.78, Z1 + 0.91, "Mat_WhiteMarble", bevel=0.006)
add_box(col_fl1_furn, "Kitchen_Backsplash_N", 6.74, 12.22, Z1 + 0.91, 6.78, 15.76, Z1 + 1.20, "Mat_BacksplashTile")
add_box(col_fl1_furn, "Kitchen_UpperCabinets", 6.38, 12.26, Z1 + 1.88, 6.76, 14.02, Z1 + 2.48, "Mat_WallFacadeWarm", bevel=0.01)
add_box(col_lights, "Kitchen_UnderCabinetLED", 6.41, 12.30, Z1 + 1.85, 6.46, 13.98, Z1 + 1.88, "Mat_WarmLED")

# Nhánh hướng Tây (dưới Cửa sổ nhìn ra Phòng tắm, thoáng sáng làm bàn soạn/để gia vị & ra đồ!): X = 4.86..6.08, Y = 15.08..15.76
add_box(col_fl1_furn, "Kitchen_L_WestBase", 4.86, 15.08, Z1, 6.08, 15.76, Z1 + 0.86, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl1_furn, "Kitchen_L_WestTop", 4.84, 15.04, Z1 + 0.86, 6.08, 15.78, Z1 + 0.91, "Mat_WhiteMarble", bevel=0.006)
for wdi in range(2):
    wx1 = 4.90 + wdi * 0.56
    add_box(col_fl1_furn, f"Kitchen_L_WestDoor_{wdi}", wx1, 15.05, Z1 + 0.08, wx1 + 0.52, 15.09, Z1 + 0.82, "Mat_WallFacadeWarm", bevel=0.006)
    add_box(col_fl1_furn, f"Kitchen_L_WestHandle_{wdi}", wx1 + 0.20, 15.03, Z1 + 0.72, wx1 + 0.34, 15.06, Z1 + 0.75, "Mat_BrassGold", bevel=0.003)

# Bồn rửa chén + Vòi cong trên nhánh Bắc gần Tủ lạnh (Y = 12.36..13.06)
add_box(col_fl1_furn, "Kitchen_SinkBasin", 6.16, 12.36, Z1 + 0.89, 6.66, 13.06, Z1 + 0.925, "Mat_MetalStainless")
add_cyl(col_fl1_furn, "Kitchen_FaucetBase", 6.66, 12.71, Z1 + 0.91, Z1 + 1.24, 0.02, 0.016, "Mat_MetalStainless", segs=10)
add_box(col_fl1_furn, "Kitchen_FaucetSpout", 6.46, 12.69, Z1 + 1.20, 6.66, 12.73, Z1 + 1.24, "Mat_MetalStainless", bevel=0.006)

# 🍽️ MÁY RỬA CHÉN ÂM TỦ CHUẨN 60CM NGAY CẠNH BỒN RỬA (X = 6.06..6.74, Y = 13.14..13.76)
add_box(col_fl1_furn, "Kitchen_Dishwasher_Body", 6.06, 13.14, Z1 + 0.04, 6.74, 13.76, Z1 + 0.84, "Mat_MetalStainless", bevel=0.01)
add_box(col_fl1_furn, "Kitchen_Dishwasher_Panel", 6.04, 13.16, Z1 + 0.68, 6.08, 13.74, Z1 + 0.82, "Mat_PianoBlackGloss", bevel=0.006)
add_box(col_fl1_furn, "Kitchen_Dishwasher_Handle", 6.01, 13.30, Z1 + 0.62, 6.05, 13.60, Z1 + 0.66, "Mat_MetalStainless", bevel=0.004)
add_box(col_fl1_furn, "Kitchen_Dishwasher_LED", 6.03, 13.38, Z1 + 0.73, 6.05, 13.52, Z1 + 0.77, "Mat_SmartCyanLED")

# 🔥 BẾP HỒNG NGOẠI ĐÔI ĐẶT SÁT TƯỜNG PHÍA BẮC (X = 6.14..6.66, Y = 14.12..14.96)
# Đứng nấu quay mặt về HƯỚNG BẮC (+X), nhìn sang BÊN TRÁI (+Y) là Cửa sổ thoáng nhìn ra Phòng tắm!
add_box(col_fl1_furn, "Kitchen_InfraredCooktop", 6.14, 14.12, Z1 + 0.91, 6.66, 14.96, Z1 + 0.94, "Mat_PianoBlackGloss", bevel=0.005)
add_cyl(col_lights, "Kitchen_InfraredRing_1", 6.40, 14.36, Z1 + 0.935, Z1 + 0.946, 0.12, 0.12, "Mat_SmartRedLED", segs=20)
add_cyl(col_lights, "Kitchen_InfraredRing_2", 6.40, 14.72, Z1 + 0.935, Z1 + 0.946, 0.10, 0.10, "Mat_SmartRedLED", segs=20)
add_cyl(col_fl1_furn, "Kitchen_Pot", 6.40, 14.36, Z1 + 0.945, Z1 + 1.10, 0.115, 0.115, "Mat_MetalStainless", segs=18)
# Máy hút mùi áp tường phía Bắc gọn gàng ngay phía trên bếp hồng ngoại
add_box(col_fl1_furn, "Kitchen_RangeHood_North", 6.14, 14.10, Z1 + 1.68, 6.76, 14.98, Z1 + 1.82, "Mat_MetalStainless", bevel=0.01)
add_box(col_fl1_furn, "Kitchen_RangeDuct_North", 6.42, 14.38, Z1 + 1.82, 6.74, 14.70, H1 - 0.04, "Mat_MetalStainless")

# Bàn soạn & bày hoa quả, ấm siêu tốc, lọ gia vị trên nhánh Tây dưới cửa sổ thoáng sáng
add_cyl(col_fl1_furn, "Kitchen_FruitBowl", 5.38, 15.42, Z1 + 0.91, Z1 + 1.00, 0.10, 0.14, "Mat_WoodOakTable", segs=16)
add_sphere(col_fl1_furn, "Kitchen_Apple1", 5.41, 15.40, Z1 + 1.03, 0.045, "Mat_CushionTerracotta")
add_sphere(col_fl1_furn, "Kitchen_Apple2", 5.35, 15.45, Z1 + 1.03, 0.042, "Mat_FlowerYellow")
add_cyl(col_fl1_furn, "Kitchen_Kettle", 5.84, 15.42, Z1 + 0.91, Z1 + 1.12, 0.08, 0.065, "Mat_CeramicWhite", segs=14)
add_box(col_fl1_furn, "Kitchen_CuttingBoard", 4.96, 15.22, Z1 + 0.91, 5.20, 15.56, Z1 + 0.935, "Mat_WoodOakTable", bevel=0.004)

# 4. BÀN ĂN TRÒN 6 GHẾ NGAY CẠNH CỬA SỔ ĐƯỜNG LUỒNG PHÍA NAM (Y = 12.60..14.50) ĐỂ NGỒI ĂN THẤY XE AI VỀ!
dt_x, dt_y = 4.10, 13.22
add_cyl(col_fl1_furn, "Dining_RoundTableTop", dt_x, dt_y, Z1 + 0.72, Z1 + 0.77, 0.78, 0.78, "Mat_WoodOakTable", segs=28)
add_cyl(col_fl1_furn, "Dining_CenterLeg", dt_x, dt_y, Z1, Z1 + 0.72, 0.12, 0.22, "Mat_MetalMatteBlack", segs=18)
add_cyl(col_fl1_furn, "Dining_CenterVase", dt_x, dt_y, Z1 + 0.77, Z1 + 0.98, 0.065, 0.045, "Mat_CeramicTeal", segs=16)
add_sphere(col_fl1_furn, "Dining_Flowers", dt_x, dt_y, Z1 + 1.05, 0.11, "Mat_FlowerYellow")
for ci in range(6):
    ang = ci * (2 * math.pi / 6.0)
    cx_ch = dt_x + 1.04 * math.cos(ang)
    cy_ch = dt_y + 1.04 * math.sin(ang)
    chair_rot = ang + math.pi / 2.0
    add_dining_chair(col_fl1_furn, f"Dining_Chair_{ci}", cx_ch, cy_ch, Z1, chair_rot,
                     seat_mat="Mat_FabricBeige", wood_mat="Mat_WoodOakTable")
    px = dt_x + 0.54 * math.cos(ang)
    py = dt_y + 0.54 * math.sin(ang)
    add_cyl(col_fl1_furn, f"Dining_Plate_{ci}", px, py, Z1 + 0.77, Z1 + 0.79, 0.12, 0.13, "Mat_CeramicWhite", segs=16)

add_pendant_chandelier(col_lights, "Dining_Chandelier", dt_x, dt_y, H1 - 0.02, drop=0.95, count=3)
add_potted_plant(col_fl1_furn, "Dining_CornerPlant", 2.50, 11.35, Z1, scale=0.88, pot_mat="Mat_TerracottaPot")

# 🛋️ 5. GHẾ BĂNG CHỮ L TRẢI THẢM & GỐI NẰM CHILL SAU KHI ĂN XONG!
# Tận dụng trọn góc trống hướng Nam cửa chính hiên sau (X=2.22..3.48, Y=15.06..15.76) & hướng Tây cửa sổ đường luồng (X=2.22..2.94, Y=14.05..15.76)!
# Xây bệ bê tông sơn trắng + mặt gỗ sồi ấm + LED hắt chân + trải thảm dày êm & gối nằm chill đón gió cửa sổ Nam!
add_box(col_fl1_furn, "Dining_LBench_KickS", 2.24, 14.08, Z1, 2.88, 15.74, Z1 + 0.06, "Mat_WoodOakDark")
add_box(col_fl1_furn, "Dining_LBench_KickW", 2.88, 15.10, Z1, 3.45, 15.74, Z1 + 0.06, "Mat_WoodOakDark")
add_box(col_lights, "Dining_LBench_ToeLED_S", 2.88, 14.12, Z1 + 0.02, 2.91, 15.10, Z1 + 0.05, "Mat_WarmLED")
add_box(col_lights, "Dining_LBench_ToeLED_W", 2.90, 15.07, Z1 + 0.02, 3.44, 15.10, Z1 + 0.05, "Mat_WarmLED")
add_box(col_fl1_furn, "Dining_LBench_BaseS", 2.22, 14.05, Z1 + 0.06, 2.94, 15.76, Z1 + 0.36, "Mat_WallWarmWhite", bevel=0.01)
add_box(col_fl1_furn, "Dining_LBench_BaseW", 2.94, 15.06, Z1 + 0.06, 3.48, 15.76, Z1 + 0.36, "Mat_WallWarmWhite", bevel=0.01)
add_box(col_fl1_furn, "Dining_LBench_TopS", 2.22, 14.03, Z1 + 0.36, 2.96, 15.76, Z1 + 0.40, "Mat_WoodOakTable", bevel=0.008)
add_box(col_fl1_furn, "Dining_LBench_TopW", 2.94, 15.04, Z1 + 0.36, 3.50, 15.76, Z1 + 0.40, "Mat_WoodOakTable", bevel=0.008)
# Trải thảm nệm dệt êm chữ L phủ trọn mặt ghế để nằm nghỉ thư giãn
add_box(col_fl1_furn, "Dining_LBench_MatS", 2.25, 14.08, Z1 + 0.40, 2.92, 15.72, Z1 + 0.46, "Mat_RugWarm", bevel=0.02)
add_box(col_fl1_furn, "Dining_LBench_MatW", 2.90, 15.08, Z1 + 0.40, 3.46, 15.72, Z1 + 0.46, "Mat_RugWarm", bevel=0.02)
# Gối nằm & gối tựa lưng + chăn mỏng gấp gọn trên ghế chữ L
add_box(col_fl1_furn, "Dining_LBench_NapPillow", 2.34, 14.18, Z1 + 0.46, 2.82, 14.54, Z1 + 0.60, "Mat_BeddingWhite", bevel=0.05)
add_box(col_fl1_furn, "Dining_LBench_Blanket", 2.32, 14.66, Z1 + 0.46, 2.86, 15.10, Z1 + 0.54, "Mat_CushionNavy", bevel=0.025)
add_box(col_fl1_furn, "Dining_LBench_BackPillow1", 2.36, 15.54, Z1 + 0.46, 2.82, 15.72, Z1 + 0.80, "Mat_CushionSage", bevel=0.045)
add_box(col_fl1_furn, "Dining_LBench_BackPillow2", 2.92, 15.54, Z1 + 0.46, 3.38, 15.72, Z1 + 0.80, "Mat_CushionMustard", bevel=0.045)
add_box(col_fl1_furn, "Dining_LBench_AccentPillow", 2.26, 15.16, Z1 + 0.46, 2.44, 15.52, Z1 + 0.74, "Mat_CushionTerracotta", bevel=0.04)
add_box(col_lights, "Dining_LBench_WallSconce", 2.76, 15.72, Z1 + 1.48, 2.96, 15.77, Z1 + 1.66, "Mat_WarmSconce", bevel=0.01)

# ---------------------------------------------------------------------------
# 6. SÂN SAU (NỀN NÂNG Z_REAR = 0.34m -> CHỈ 1 BẬC THANG CỬA SAU):
#    - Máy giặt đặt SÁT TƯỜNG NGAY DƯỚI CỬA SỔ BẾP & GẦN SÁT PHÒNG TẮM (X=5.75..6.45, Y=16.04..16.68)!
#    - Phòng tắm (1.75m x 1.40m) & Phòng WC (1.75m x 1.20m) thu nhỏ gọn gàng áp tường Bắc (X=5.20..6.95, Y=17.45..20.05)
#    - Xe máy đi từ đường luồng chạy xuống dựng GẦN NHÀ TẮM (X=3.35..4.65, Y=18.65..19.12): ĐẦU hướng BẮC (+X), BÁNH SAU hướng NAM (-X)!
#    - Hệ dây phơi đồ inox 3 dây thoáng rộng phía Tây Bắc sau WC (X=3.95..6.80, Y=20.60..23.60) đón gió nắng
#    - Bàn ghế chill (1 ghế dài + 1 bàn tròn) phía Nam bậc thang cửa sau tựa tường Đông ngắm Vườn rau phía Tây
# ---------------------------------------------------------------------------
Z_REAR = 0.34
# Nền lát gạch/đá chỉ làm gọn trong phần Hiên sau & rãnh thoát nước sau nhà tắm (Y=16.0..20.52)
add_box(col_site, "RearYard_Slab", 0.0, 16.0, 0.0, 7.0, 20.52, Z_REAR, "Mat_AntiSlipPavers")
# Toàn bộ khu phía sau Y=20.52..24.00 (cả Vườn rau Nam lẫn DƯỚI CHỖ PHƠI ĐỒ Bắc) là ĐẤT TỰ NHIÊN trồng rau, KHÔNG xây bê tông!
add_box(col_site, "RearYard_NaturalSoil", 0.0, 20.52, 0.0, 7.0, 24.0, Z_REAR - 0.04, "Mat_SoilDark")
# 5 viên đá bước dặm rời giữa 2 khu vườn rau (X=3.18..3.72) để đi phơi đồ & hái rau sạch chân mà không đổ bê tông
for sti, sty in enumerate([20.85, 21.48, 22.10, 22.72, 23.35]):
    add_box(col_site, f"RearYard_StepStone_{sti}", 3.18, sty - 0.18, Z_REAR - 0.04, 3.72, sty + 0.18, Z_REAR + 0.01, "Mat_StepStone", bevel=0.015)
# 1 bậc chuyển tiếp êm từ đường luồng Nam (0.14m) lên nền sân sau (0.34m)
add_box(col_site, "Corridor_ToRear_Step", 0.05, 15.66, 0.14, 1.98, 16.00, 0.24, "Mat_StepStone", bevel=0.008)

# 🚿🚽🧺 PHÒNG TẮM + NHÀ VỆ SINH + MÁY GIẶT GỘP CHUNG 1 PHÒNG RỘNG RÃI TRONG HIÊN SAU (X = 4.95..6.95, Y = 16.65..20.25 -> 7.20m²!)
# Thiết kế lại nội thất bên trong phòng (giữ nguyên vị trí X=4.95..6.95, Y=16.65..20.25 -> 7.20m²):
# - Cửa vào phía Nam (X=4.95, Y=16.92..17.68): Mặt ngoài hướng Nam, mặt trong hướng Bắc — nhìn vô thấy ngay Gương & Chỗ rửa tay!
# - Dọc tường Bắc từ Đông -> Tây:
#   + Phía Đông gương (Y=16.77..17.37): Bức tường xây 2 ngăn (ngăn trên đựng đồ linh tinh, ngăn dưới để thùng lau nhà!)
#   + Chính diện (Y=17.38..18.17): Gương tròn LED + Chỗ rửa tay Lavabo mặt đá + kệ trên gương
#   + Phía Tây gương (Y=18.17..18.98): Bồn cầu (mặt hướng Nam) + bức tường ngang nhô ra 1 chút phía trên để giấy vệ sinh & chai Vim!
# - Tường Nam đối diện Gương & Bồn cầu (Y=17.74..19.22): Thiết kế CÂY TREO ĐỒ DÀI RA để thành viên treo đồ khô mỗi khi tắm!
# - Bên phải Bồn cầu & chỗ treo đồ khô là HƯỚNG TÂY (Y=19.00..20.13): NGĂN TẮM ƯỚT (Bắc-Tây) + CHỖ ĐỂ MÁY GIẶT (Nam-Tây) — CẢ 2 HƯỚNG MẶT RA HƯỚNG ĐÔNG (-Y)!
#   + Ngăn tắm ướt: Vòi tắm nóng lạnh bắt trên tường phía Bắc + xây 2 khung kiểu ô trên tường phía Bắc để tiện tay lấy sữa tắm, dầu gội!
RB_H = Z_REAR + 2.52
# Sàn lát gạch chống trơn toàn phòng
add_box(col_site, "RearBath_Floor", 4.95, 16.65, Z_REAR, 6.95, 20.25, Z_REAR + 0.04, "Mat_FloorTileCream")
# Tường bao 4 mặt (tường Nam chừa cửa Y=17.14..17.88; đầu Đông tường Nam đỡ nhánh chữ L; phần Y=17.88..20.25 đối diện Gương & Bồn cầu!)
add_box(col_site, "RearBath_Wall_East", 4.95, 16.65, Z_REAR, 6.95, 16.77, RB_H, "Mat_WallWarmWhite")
add_box(col_site, "RearBath_Wall_West", 4.95, 20.13, Z_REAR, 6.95, 20.25, RB_H, "Mat_WallWarmWhite")
add_box(col_site, "RearBath_Wall_North", 6.83, 16.65, Z_REAR, 6.95, 20.25, RB_H, "Mat_WallWarmWhite")
add_box(col_site, "RearBath_Wall_South1", 4.95, 16.65, Z_REAR, 5.07, 17.14, RB_H, "Mat_WallWarmWhite")
add_box(col_site, "RearBath_Wall_SouthTop", 4.95, 17.14, Z_REAR + 2.14, 5.07, 17.88, RB_H, "Mat_WallWarmWhite")
add_box(col_site, "RearBath_Wall_South2", 4.95, 17.88, Z_REAR, 5.07, 20.25, RB_H, "Mat_WallWarmWhite")
# Khung & cánh cửa kính mờ (mặt ngoài hướng Nam, mặt trong hướng Bắc — mở gọn ra ngoài sát mép Đông không cấn kệ chữ L bên trong!)
add_box(col_site, "RearBath_DoorFrame1", 4.93, 17.12, Z_REAR, 5.09, 17.17, Z_REAR + 2.16, "Mat_WoodOakDark")
add_box(col_site, "RearBath_DoorFrame2", 4.93, 17.85, Z_REAR, 5.09, 17.90, Z_REAR + 2.16, "Mat_WoodOakDark")
add_box(col_site, "RearBath_DoorFrameTop", 4.93, 17.12, Z_REAR + 2.12, 5.09, 17.90, Z_REAR + 2.18, "Mat_WoodOakDark")
add_box(col_site, "RearBath_DoorLeaf", 4.25, 17.13, Z_REAR + 0.04, 4.95, 17.17, Z_REAR + 2.12, "Mat_GlassBronze")

# 1. CHỖ RỬA TAY LAVABO & GƯƠNG LED TRÊN TƯỜNG BẮC (X=6.28..6.83, Y=17.38..18.17)
add_box(col_site, "RearBath_VanityCab", 6.32, 17.40, Z_REAR + 0.16, 6.82, 18.15, Z_REAR + 0.78, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_site, "RearBath_VanityTop", 6.28, 17.38, Z_REAR + 0.78, 6.83, 18.17, Z_REAR + 0.84, "Mat_WhiteMarble", bevel=0.008)
add_cyl(col_site, "RearBath_Basin", 6.54, 17.78, Z_REAR + 0.84, Z_REAR + 0.96, 0.17, 0.21, "Mat_CeramicWhite", segs=20)
add_cyl(col_site, "RearBath_Faucet", 6.72, 17.78, Z_REAR + 0.84, Z_REAR + 1.06, 0.016, 0.014, "Mat_MetalMatteBlack", segs=10)
add_box(col_site, "RearBath_FaucetSpout", 6.58, 17.765, Z_REAR + 1.03, 6.72, 17.795, Z_REAR + 1.06, "Mat_MetalMatteBlack")
# Gương soi tròn lớn viền đèn LED ấm
add_cyl(col_site, "RearBath_Mirror", 6.80, 17.78, Z_REAR + 1.44, Z_REAR + 1.48, 0.34, 0.34, "Mat_Mirror", rot=(0, math.pi / 2, 0), segs=24)
add_cyl(col_lights, "RearBath_MirrorLED", 6.82, 17.78, Z_REAR + 1.44, Z_REAR + 1.47, 0.36, 0.36, "Mat_WarmLED", rot=(0, math.pi / 2, 0), segs=24)
# Kệ hốc phía trên gương (Y=17.39..18.16, Z=Z_REAR+1.90..2.32)
add_box(col_site, "RearBath_TopNicheFrameB", 6.64, 17.39, Z_REAR + 1.90, 6.83, 18.16, Z_REAR + 1.95, "Mat_WallWarmWhite", bevel=0.004)
add_box(col_site, "RearBath_TopNicheFrameT", 6.64, 17.39, Z_REAR + 2.26, 6.83, 18.16, Z_REAR + 2.32, "Mat_WallWarmWhite", bevel=0.004)
add_box(col_site, "RearBath_TopNicheOak", 6.65, 17.41, Z_REAR + 1.95, 6.82, 18.14, Z_REAR + 1.97, "Mat_WoodOakTable")
add_box(col_lights, "RearBath_TopNicheLED", 6.67, 17.44, Z_REAR + 2.24, 6.71, 18.10, Z_REAR + 2.26, "Mat_WarmLED")

# 2. PHÍA ĐÔNG GƯƠNG — KỆ TƯỜNG XÂY CHỮ L DÀI TỚI TƯỜNG NAM (NGĂN TRÊN CHỮ L ĐỰNG ĐỒ LINH TINH, BÊN DƯỚI VẪN ĐỂ THÙNG & CÂY LAU NHÀ!)
# Nhánh Bắc-Đông (từ gương sang tường Đông: X=6.35..6.83, Y=16.77..17.38) + Nhánh Đông-Nam (kéo dài dọc tường Đông sát tường Nam: X=5.07..6.35, Y=16.77..17.10)!
add_box(col_site, "RearBath_EastWall_DivW", 6.35, 17.31, Z_REAR + 0.04, 6.83, 17.38, Z_REAR + 2.32, "Mat_WallWarmWhite", bevel=0.006)
# Đợt tường ngang chữ L chia ngăn trên & không gian dưới (Z=Z_REAR+1.08..1.16)
add_box(col_site, "RearBath_EastWall_MidShelf", 6.35, 16.77, Z_REAR + 1.08, 6.83, 17.31, Z_REAR + 1.16, "Mat_WallWarmWhite", bevel=0.006)
add_box(col_site, "RearBath_EastWall_MidShelf_S", 5.07, 16.77, Z_REAR + 1.08, 6.35, 17.10, Z_REAR + 1.16, "Mat_WallWarmWhite", bevel=0.006)
# Đỉnh tường chữ L đồng bộ (Z=Z_REAR+2.24..2.32)
add_box(col_site, "RearBath_EastWall_TopCap", 6.35, 16.77, Z_REAR + 2.24, 6.83, 17.38, Z_REAR + 2.32, "Mat_WallWarmWhite", bevel=0.006)
add_box(col_site, "RearBath_EastWall_TopCap_S", 5.07, 16.77, Z_REAR + 2.24, 6.35, 17.10, Z_REAR + 2.32, "Mat_WallWarmWhite", bevel=0.006)
# + NGĂN TRÊN CHỮ L (Z=Z_REAR+1.16..2.24): Lót gỗ sồi + LED ấm chạy dọc chữ L đựng đồ linh tinh cực rộng!
add_box(col_site, "RearBath_EastUpperOak", 6.35, 16.78, Z_REAR + 1.16, 6.82, 17.30, Z_REAR + 1.185, "Mat_WoodOakTable")
add_box(col_site, "RearBath_EastUpperOak_S", 5.08, 16.78, Z_REAR + 1.16, 6.35, 17.09, Z_REAR + 1.185, "Mat_WoodOakTable")
add_box(col_lights, "RearBath_EastUpperLED", 6.39, 16.82, Z_REAR + 2.21, 6.43, 17.26, Z_REAR + 2.24, "Mat_WarmLED")
add_box(col_lights, "RearBath_EastUpperLED_S", 5.14, 17.04, Z_REAR + 2.21, 6.35, 17.08, Z_REAR + 2.24, "Mat_WarmLED")
# Đồ linh tinh xếp gọn suốt 2 nhánh chữ L (giỏ đồ, khăn gấp, hộp giấy, chai lọ chăm sóc)
add_box(col_site, "RearBath_EastMiscBasket", 6.44, 16.82, Z_REAR + 1.185, 6.76, 17.08, Z_REAR + 1.42, "Mat_WoodOakTable", bevel=0.015)
add_box(col_site, "RearBath_EastMiscTowel1", 6.46, 17.11, Z_REAR + 1.185, 6.74, 17.28, Z_REAR + 1.255, "Mat_BeddingWhite", bevel=0.015)
add_box(col_site, "RearBath_EastMiscTowel2", 6.47, 17.12, Z_REAR + 1.255, 6.73, 17.27, Z_REAR + 1.32, "Mat_CushionSage", bevel=0.015)
# Nhánh chữ L kéo về hướng Nam (X=5.08..6.35, Y=16.78..17.09)
add_box(col_site, "RearBath_EastSouthBasket", 5.92, 16.81, Z_REAR + 1.185, 6.28, 17.05, Z_REAR + 1.40, "Mat_WoodOakTable", bevel=0.015)
add_box(col_site, "RearBath_EastSouthTowel1", 5.56, 16.82, Z_REAR + 1.185, 5.84, 17.04, Z_REAR + 1.26, "Mat_BeddingCream", bevel=0.015)
add_box(col_site, "RearBath_EastSouthTowel2", 5.57, 16.83, Z_REAR + 1.26, 5.83, 17.03, Z_REAR + 1.33, "Mat_CushionBlush", bevel=0.015)
add_box(col_site, "RearBath_EastSouthTissueBox", 5.20, 16.83, Z_REAR + 1.185, 5.44, 17.02, Z_REAR + 1.30, "Mat_CeramicWhite", bevel=0.01)
bottle_specs = [
    (6.48, 17.14, Z_REAR + 1.32, 0.19, "Mat_CeramicTeal"),
    (6.58, 17.22, Z_REAR + 1.32, 0.16, "Mat_CeramicWhite"),
    (6.66, 16.92, Z_REAR + 1.42, 0.18, "Mat_CushionMustard"),
    (5.16, 16.94, Z_REAR + 1.185, 0.21, "Mat_CeramicTeal"),
    (5.50, 16.94, Z_REAR + 1.185, 0.18, "Mat_CushionMustard"),
    (6.73, 17.56, Z_REAR + 1.97, 0.18, "Mat_CeramicWhite"),
    (6.73, 17.78, Z_REAR + 1.97, 0.15, "Mat_CeramicTeal"),
    (6.73, 17.98, Z_REAR + 1.97, 0.17, "Mat_CushionSage"),
]
for bi, (bx, by, bz, bh, bmat) in enumerate(bottle_specs):
    add_cyl(col_site, f"RearBath_Skincare_{bi}", bx, by, bz, bz + bh, 0.030, 0.024, bmat, segs=12)
# + NGĂN DƯỚI (Z=Z_REAR+0.04..1.08): VẪN ĐỂ THÙNG LAU NHÀ & CÂY LAU NHÀ gọn gàng ngay trên nền gạch như cũ!
add_box(col_site, "RearBath_MopBucket", 6.42, 16.84, Z_REAR + 0.04, 6.76, 17.22, Z_REAR + 0.34, "Mat_CeramicTeal", bevel=0.025)
add_box(col_site, "RearBath_MopWringer", 6.45, 16.86, Z_REAR + 0.30, 6.73, 17.02, Z_REAR + 0.38, "Mat_MetalStainless", bevel=0.01)
add_box(col_site, "RearBath_MopWater", 6.45, 17.02, Z_REAR + 0.24, 6.73, 17.20, Z_REAR + 0.28, "Mat_WaterClear")
add_cyl(col_site, "RearBath_MopHead", 6.59, 16.94, Z_REAR + 0.34, Z_REAR + 0.42, 0.080, 0.060, "Mat_BeddingWhite", segs=14)
add_cyl(col_site, "RearBath_MopPole", 6.59, 16.94, Z_REAR + 0.42, Z_REAR + 1.04, 0.014, 0.014, "Mat_MetalStainless", segs=10)
add_cyl(col_site, "RearBath_FloorCleaner", 6.58, 17.26, Z_REAR + 0.04, Z_REAR + 0.30, 0.038, 0.028, "Mat_CushionMustard", segs=12)

# 3. PHÍA TÂY GƯƠNG — BỒN CẦU (LƯNG ÁP TƯỜNG BẮC, MẶT HƯỚNG NAM) + BỨC TƯỜNG NGANG NHÔ RA 1 CHÚT PHÍA TRÊN ĐỂ GIẤY & CHAI VIM!
# (Y = 18.17..18.98, tâm bồn cầu Y=18.58, khoảng trống phía trước rộng 1.08m!)
add_box(col_site, "RearBath_ToiletTank", 6.56, 18.37, Z_REAR + 0.40, 6.81, 18.79, Z_REAR + 0.84, "Mat_CeramicWhite", bevel=0.03)
add_cyl(col_site, "RearBath_ToiletBowl", 6.38, 18.58, Z_REAR + 0.04, Z_REAR + 0.44, 0.17, 0.20, "Mat_CeramicWhite", segs=16)
add_box(col_site, "RearBath_ToiletSeat", 6.18, 18.39, Z_REAR + 0.44, 6.56, 18.77, Z_REAR + 0.48, "Mat_BeddingWhite", bevel=0.02)
# Bức tường xây ngang nhô ra 1 chút trên bồn cầu 1 khoảng vừa đủ (Z=Z_REAR+1.18..1.25, sâu 19cm từ tường Bắc) để giấy vệ sinh & chai Vim!
add_box(col_site, "RearBath_ToiletWallLedge", 6.64, 18.24, Z_REAR + 1.18, 6.83, 18.94, Z_REAR + 1.25, "Mat_WallWarmWhite", bevel=0.006)
add_box(col_site, "RearBath_ToiletLedgeTop", 6.65, 18.25, Z_REAR + 1.25, 6.82, 18.93, Z_REAR + 1.27, "Mat_WoodOakTable")
# 2 cuộn giấy vệ sinh + chai Vim tẩy rửa (thân xanh đậm cổ nghiêng) + bình xịt phòng
add_cyl(col_site, "RearBath_ToiletPaper_0", 6.73, 18.36, Z_REAR + 1.27, Z_REAR + 1.39, 0.055, 0.055, "Mat_BeddingWhite", segs=14)
add_cyl(col_site, "RearBath_ToiletPaper_1", 6.73, 18.50, Z_REAR + 1.27, Z_REAR + 1.39, 0.055, 0.055, "Mat_BeddingWhite", segs=14)
add_cyl(col_site, "RearBath_VimBottle", 6.73, 18.74, Z_REAR + 1.27, Z_REAR + 1.50, 0.044, 0.032, "Mat_CushionNavy", segs=14)
add_cyl(col_site, "RearBath_VimCap", 6.73, 18.74, Z_REAR + 1.50, Z_REAR + 1.56, 0.018, 0.012, "Mat_CushionMustard", segs=10)
add_cyl(col_site, "RearBath_AirSpray", 6.73, 18.87, Z_REAR + 1.27, Z_REAR + 1.44, 0.028, 0.025, "Mat_CushionSage", segs=12)

# 4. ĐỐI DIỆN GƯƠNG & BỒN CẦU (TƯỜNG PHÍA NAM X=5.07, Y=17.94..19.26) — CÂY TREO ĐỒ DÀI RA ĐỂ TREO ĐỒ KHÔ MỖI KHI TẮM!
add_box(col_site, "RearBath_DryWallBar", 5.07, 17.94, Z_REAR + 1.56, 5.10, 19.26, Z_REAR + 1.68, "Mat_WoodOakTable", bevel=0.006)
for bki, bky in enumerate([18.00, 18.60, 19.20]):
    add_box(col_site, f"RearBath_DryRodBracket_{bki}", 5.09, bky - 0.018, Z_REAR + 1.60, 5.26, bky + 0.018, Z_REAR + 1.64, "Mat_BrassGold")
# Thanh cây treo đồ inox dài 1.28m dọc tường Nam (X=5.24, Y=17.96..19.24, Z=Z_REAR+1.62)
add_cyl(col_site, "RearBath_LongClothesRod", 5.245, 18.60, Z_REAR + 1.61, Z_REAR + 1.64, 0.014, 0.014, "Mat_MetalStainless",
        rot=(math.pi / 2, 0, 0), segs=12)
add_box(col_site, "RearBath_LongClothesRodBar", 5.23, 17.96, Z_REAR + 1.61, 5.26, 19.24, Z_REAR + 1.64, "Mat_MetalStainless")
# Các móc áo & bộ đồ khô + khăn tắm treo gọn dọc cây treo đồ dài
for dci, (dcy, dch, dcmat) in enumerate([
    (18.12, 0.56, "Mat_CushionNavy"),
    (18.42, 0.52, "Mat_BeddingCream"),
    (18.72, 0.58, "Mat_CushionSage"),
    (19.04, 0.50, "Mat_CushionBlush"),
]):
    add_cyl(col_site, f"RearBath_HangerHook_{dci}", 5.245, dcy, Z_REAR + 1.56, Z_REAR + 1.63, 0.008, 0.008, "Mat_BrassGold", segs=8)
    add_box(col_site, f"RearBath_DryClothes_{dci}", 5.21, dcy - 0.11, Z_REAR + 1.56 - dch, 5.27, dcy + 0.11, Z_REAR + 1.56, dcmat, bevel=0.015)

# 5. BÊN PHẢI BỒN CẦU & CHỖ TREO ĐỒ KHÔ LÀ HƯỚNG TÂY (Y=19.00..20.13) — KHU ƯỚT (NGĂN TẮM + MÁY GIẶT) XÂY NỀN CAO HƠN NỀN KHÔ (LAVABO/BỒN CẦU) + THOÁT NƯỚC DỐC RA THẲNG SÂN SAU!
# Nền khu ướt chung cho CẢ NGĂN TẮM & MÁY GIẶT (X=5.07..6.83, Y=19.00..20.13) xây CAO HƠN nền Lavabo/Bồn cầu (+9cm: Z_REAR+0.04 -> +0.13) + gờ đá chống trơn ngăn khu ướt & khô!
add_box(col_site, "RearBath_WetZoneFloor", 5.07, 19.00, Z_REAR + 0.04, 6.83, 20.13, Z_REAR + 0.13, "Mat_StepStone", bevel=0.008)
add_box(col_site, "RearBath_WetDryCurb", 5.07, 18.96, Z_REAR + 0.04, 6.83, 19.04, Z_REAR + 0.135, "Mat_DarkGreyStone", bevel=0.006)
# Phễu thoát sàn khu khô (Lavabo + Bồn cầu) đặt sát mép Tây nền khô (X=6.06, Y=18.80) thoát dốc ngầm ra thẳng phía sau!
add_cyl(col_site, "RearBath_DryFloorDrain", 6.06, 18.80, Z_REAR + 0.038, Z_REAR + 0.046, 0.052, 0.052, "Mat_MetalStainless", segs=14)
add_box(col_site, "RearBath_DryDrainGrate", 6.02, 18.76, Z_REAR + 0.045, 6.10, 18.84, Z_REAR + 0.048, "Mat_MetalMatteBlack")

# Vách tường xây ngăn nước tách biệt Ngăn tắm ướt (Bắc-Tây) & Máy giặt (Nam-Tây): X=5.78..5.88, Y=19.00..20.13
add_box(col_site, "RearBath_ShowerDivWall", 5.78, 19.00, Z_REAR + 0.13, 5.88, 20.13, Z_REAR + 2.18, "Mat_WallWarmWhite", bevel=0.006)

# 5.1 NGĂN TẮM ƯỚT (Bắc-Tây: X=5.88..6.83, Y=19.00..20.13 -> 0.95m x 1.13m, lối vào hướng ĐÔNG -Y!)
# Phễu thoát sàn ngăn tắm đặt sát mép Tây dốc thẳng ra sau (X=6.36, Y=19.95, Z=Z_REAR+0.13)
add_cyl(col_site, "RearBath_ShowerDrain", 6.36, 19.95, Z_REAR + 0.128, Z_REAR + 0.136, 0.058, 0.058, "Mat_MetalStainless", segs=14)
add_box(col_site, "RearBath_ShowerDrainSlot", 6.24, 19.93, Z_REAR + 0.132, 6.48, 19.97, Z_REAR + 0.137, "Mat_MetalStainless")
# Vách kính chắn nước nửa Bắc của mặt Đông (ngăn bắn sang Bồn cầu, chừa lối bước rộng 50cm ở X=5.88..6.38 hướng Đông!)
add_box(col_site, "RearBath_ShowerGlassScreen", 6.38, 18.98, Z_REAR + 0.135, 6.83, 19.02, Z_REAR + 2.14, "Mat_GlassClear")
# VÒI TẮM NÓNG LẠNH BẮT TRÊN TƯỜNG PHÍA BẮC (X=6.76, Y=19.76 — bộ trộn nóng/lạnh + sen cây + sen cầm tay!)
add_box(col_site, "RearBath_MixerBody", 6.72, 19.65, Z_REAR + 1.00, 6.83, 19.87, Z_REAR + 1.07, "Mat_MetalStainless", bevel=0.008)
add_box(col_site, "RearBath_MixerHotDot", 6.71, 19.67, Z_REAR + 1.02, 6.73, 19.70, Z_REAR + 1.05, "Mat_CushionBlush")
add_box(col_site, "RearBath_MixerColdDot", 6.71, 19.82, Z_REAR + 1.02, 6.73, 19.85, Z_REAR + 1.05, "Mat_SmartCyanLED")
add_box(col_site, "RearBath_MixerLever", 6.66, 19.74, Z_REAR + 1.05, 6.74, 19.78, Z_REAR + 1.09, "Mat_MetalStainless")
add_cyl(col_site, "RearBath_ShowerPipe", 6.76, 19.76, Z_REAR + 1.06, Z_REAR + 2.14, 0.015, 0.015, "Mat_MetalStainless", segs=10)
add_box(col_site, "RearBath_ShowerArm", 6.42, 19.74, Z_REAR + 2.11, 6.77, 19.78, Z_REAR + 2.15, "Mat_MetalStainless")
add_cyl(col_site, "RearBath_RainHead", 6.42, 19.76, Z_REAR + 2.06, Z_REAR + 2.11, 0.12, 0.12, "Mat_MetalStainless", segs=18)
add_cyl(col_site, "RearBath_HandShower", 6.72, 19.90, Z_REAR + 1.38, Z_REAR + 1.54, 0.022, 0.038, "Mat_MetalStainless", segs=12)
# 2 KHUNG Ô XÂY TRÊN TƯỜNG PHÍA BẮC NGAY CẠNH VÒI TẮM (X=6.67..6.83, Y=19.10..19.58) ĐỂ TIỆN TAY LẤY SỮA TẮM, DẦU GỘI!
add_box(col_site, "RearBath_ShowerFrameL", 6.67, 19.10, Z_REAR + 0.94, 6.83, 19.15, Z_REAR + 1.78, "Mat_WallWarmWhite", bevel=0.004)
add_box(col_site, "RearBath_ShowerFrameR", 6.67, 19.53, Z_REAR + 0.94, 6.83, 19.58, Z_REAR + 1.78, "Mat_WallWarmWhite", bevel=0.004)
add_box(col_site, "RearBath_ShowerNicheBot", 6.67, 19.10, Z_REAR + 0.94, 6.83, 19.58, Z_REAR + 0.99, "Mat_WallWarmWhite", bevel=0.004)
add_box(col_site, "RearBath_ShowerNicheMid", 6.67, 19.10, Z_REAR + 1.33, 6.83, 19.58, Z_REAR + 1.38, "Mat_WallWarmWhite", bevel=0.004)
add_box(col_site, "RearBath_ShowerNicheTop", 6.67, 19.10, Z_REAR + 1.73, 6.83, 19.58, Z_REAR + 1.78, "Mat_WallWarmWhite", bevel=0.004)
add_box(col_site, "RearBath_ShowerNicheOak1", 6.68, 19.15, Z_REAR + 0.99, 6.82, 19.53, Z_REAR + 1.01, "Mat_WoodOakTable")
add_box(col_site, "RearBath_ShowerNicheOak2", 6.68, 19.15, Z_REAR + 1.38, 6.82, 19.53, Z_REAR + 1.40, "Mat_WoodOakTable")
add_box(col_lights, "RearBath_ShowerNicheLED1", 6.70, 19.17, Z_REAR + 1.31, 6.73, 19.51, Z_REAR + 1.33, "Mat_WarmLED")
add_box(col_lights, "RearBath_ShowerNicheLED2", 6.70, 19.17, Z_REAR + 1.71, 6.73, 19.51, Z_REAR + 1.73, "Mat_WarmLED")
for si, (sy, sz_b, sh_b, smat) in enumerate([
    (19.22, Z_REAR + 1.01, 0.21, "Mat_CeramicTeal"),
    (19.34, Z_REAR + 1.01, 0.18, "Mat_CeramicWhite"),
    (19.46, Z_REAR + 1.01, 0.20, "Mat_CushionMustard"),
    (19.25, Z_REAR + 1.40, 0.19, "Mat_CushionSage"),
    (19.43, Z_REAR + 1.40, 0.17, "Mat_CushionBlush"),
]):
    add_cyl(col_site, f"RearBath_Shampoo_{si}", 6.75, sy, sz_b, sz_b + sh_b, 0.032, 0.025, smat, segs=12)

# 5.2 CHỖ ĐỂ MÁY GIẶT (Nam-Tây: X=5.07..5.78, Y=19.40..20.13 — ĐẶT TRÊN NỀN KHU ƯỚT CAO +9CM, MẶT LỒNG GIẶT HƯỚNG ĐÔNG -Y!)
add_box(col_site, "Washer_Dryer", 5.10, 19.42, Z_REAR + 0.13, 5.74, 20.06, Z_REAR + 0.98, "Mat_MetalStainless", bevel=0.02)
add_cyl(col_site, "Washer_Door", 5.42, 19.41, Z_REAR + 0.36, Z_REAR + 0.76, 0.20, 0.20, "Mat_GlassBronze", rot=(math.pi / 2, 0, 0), segs=18)
add_box(col_site, "Washer_Panel", 5.14, 19.40, Z_REAR + 0.84, 5.70, 19.43, Z_REAR + 0.95, "Mat_PianoBlackGloss", bevel=0.004)
add_box(col_site, "Washer_LED", 5.46, 19.39, Z_REAR + 0.87, 5.62, 19.41, Z_REAR + 0.92, "Mat_SmartCyanLED")
# Phễu & ống xả nước máy giặt sau/cạnh máy nối xuyên tường Tây thoát thẳng ra sân sau!
add_cyl(col_site, "RearBath_WasherFloorDrain", 5.22, 19.22, Z_REAR + 0.128, Z_REAR + 0.136, 0.048, 0.048, "Mat_MetalStainless", segs=14)
add_cyl(col_site, "RearBath_WasherDrainStandpipe", 5.16, 20.09, Z_REAR + 0.13, Z_REAR + 0.42, 0.022, 0.022, "Mat_DarkGreyStone", segs=10)
# 2 đợt kệ gọn trên tường Tây phía trên máy giặt đựng nước giặt, nước xả & khăn sạch
for wn_i, wn_z in enumerate([Z_REAR + 1.22, Z_REAR + 1.68]):
    add_box(col_site, f"Washer_WallShelf_{wn_i}", 5.08, 19.80, wn_z, 5.77, 20.13, wn_z + 0.05, "Mat_WallWarmWhite", bevel=0.004)
    add_box(col_site, f"Washer_WallOak_{wn_i}", 5.10, 19.81, wn_z + 0.05, 5.75, 20.12, wn_z + 0.07, "Mat_WoodOakTable")
add_box(col_site, "Washer_DetergentBox", 5.16, 19.86, Z_REAR + 1.29, 5.42, 20.06, Z_REAR + 1.52, "Mat_CeramicTeal", bevel=0.01)
add_box(col_site, "Washer_SoftenerBox", 5.48, 19.88, Z_REAR + 1.29, 5.68, 20.04, Z_REAR + 1.50, "Mat_CushionMustard", bevel=0.01)
add_box(col_site, "Washer_TowelStack1", 5.18, 19.84, Z_REAR + 1.75, 5.56, 20.06, Z_REAR + 1.86, "Mat_BeddingCream", bevel=0.015)
add_box(col_site, "Washer_TowelStack2", 5.20, 19.86, Z_REAR + 1.86, 5.54, 20.04, Z_REAR + 1.96, "Mat_CushionSage", bevel=0.015)

# 5.3 HỆ THỐNG ỐNG & RÃNH THOÁT NƯỚC DỐC THẢI THẲNG RA PHÍA SAU TỪ CẢ 3 KHU (TẮM + MÁY GIẶT + SÀN LAVABO/BỒN CẦU)!
# Rãnh thu nước dốc có lưới inox chạy dọc chân tường Tây ngoài nhà tắm (X=4.95..6.95, Y=20.25..20.52)
add_box(col_site, "RearBath_RearDrainTrough", 4.95, 20.25, Z_REAR - 0.06, 6.95, 20.52, Z_REAR + 0.005, "Mat_DarkGreyStone")
add_box(col_site, "RearBath_RearDrainGrate", 5.02, 20.29, Z_REAR + 0.003, 6.88, 20.48, Z_REAR + 0.014, "Mat_MetalStainless")
# 3 ống thoát nước PVC/xám đi dốc xuyên tường Tây (Y=20.13..20.42) thải trực tiếp vào rãnh thoát phía sau:
# (1) Ống thoát Ngăn tắm (X=6.36), (2) Ống thoát sàn khô Lavabo/Bồn cầu (X=6.06), (3) Ống thoát Máy giặt (X=5.32)
for op_name, op_x, op_z in [
    ("RearBath_OutPipe_Shower", 6.36, Z_REAR + 0.06),
    ("RearBath_OutPipe_DryFloor", 6.06, Z_REAR + 0.025),
    ("RearBath_OutPipe_Washer", 5.32, Z_REAR + 0.065),
]:
    add_cyl(col_site, op_name, op_x, 20.28, op_z - 0.18, op_z + 0.18, 0.030, 0.030, "Mat_DarkGreyStone",
            rot=(math.pi / 2, 0, 0), segs=12)
# Ống dẫn thoát tổng từ rãnh ra sau vườn/cống biên phía Tây
add_cyl(col_site, "RearBath_MainOutfallPipe", 5.02, 20.68, Z_REAR - 0.215, Z_REAR + 0.185, 0.042, 0.042, "Mat_DarkGreyStone",
        rot=(math.pi / 2, 0, 0), segs=12)

add_pendant_chandelier(col_lights, "RearBath_CeilingLight", 5.95, 18.30, RB_H - 0.04, drop=0.18, count=1)

# 👕🥬 CHỖ PHƠI ĐỒ BÊN TRÊN — BÊN DƯỚI LÀ ĐẤT LÀM RAU KHÔNG XÂY BÊ TÔNG (X = 3.95..6.80, Y = 20.65..23.70)!
# Khung trụ inox 4 góc cắm gọn trực tiếp xuống nền đất vườn (KHÔNG đổ bê tông nền!), bên trên treo 3 dây phơi thoáng gió nắng
for px in [4.05, 6.70]:
    for py in [20.78, 23.52]:
        add_cyl(col_site, f"DryRack_Footing_{px:.1f}_{py:.1f}", px, py, Z_REAR - 0.04, Z_REAR + 0.02, 0.065, 0.055, "Mat_DarkGreyStone", segs=12)
        add_cyl(col_site, f"DryRack_Post_{px:.1f}_{py:.1f}", px, py, Z_REAR - 0.02, Z_REAR + 1.96, 0.024, 0.024, "Mat_MetalStainless", segs=12)
for py in [20.78, 23.52]:
    add_box(col_site, f"DryRack_CrossBar_{py:.1f}", 4.02, py - 0.022, Z_REAR + 1.88, 6.74, py + 0.022, Z_REAR + 1.94, "Mat_MetalStainless", bevel=0.005)
cloth_mats_rear = ["Mat_BeddingWhite", "Mat_CushionSage", "Mat_CushionNavy", "Mat_CushionBlush", "Mat_CushionMustard", "Mat_WallFacadeWarm"]
for li, lx in enumerate([4.55, 5.38, 6.20]):
    add_cyl(col_site, f"DryRack_Wire_{li}", lx, 22.15, Z_REAR + 1.85, Z_REAR + 1.87, 0.009, 0.009, "Mat_MetalStainless",
            rot=(math.pi / 2, 0, 0), segs=8)
    add_box(col_site, f"DryRack_LineBar_{li}", lx - 0.010, 20.78, Z_REAR + 1.84, lx + 0.010, 23.52, Z_REAR + 1.87, "Mat_MetalStainless")
    for ci, cy in enumerate([21.30, 22.15, 22.98]):
        add_box(col_site, f"DryRack_Cloth_{li}_{ci}", lx - 0.02, cy - 0.22, Z_REAR + 1.18, lx + 0.02, cy + 0.22, Z_REAR + 1.82,
                cloth_mats_rear[(li * 3 + ci) % len(cloth_mats_rear)], bevel=0.012)
# 3 luống ĐẤT TRỒNG RAU XANH trực tiếp ngay dưới dây phơi đồ (KHÔNG bê tông — thoáng ẩm, nước phơi nhỏ xuống tưới rau luôn!)
for dv_i, dv_y in enumerate([21.05, 21.95, 22.85]):
    add_box(col_site, f"DryVeg_SoilRidge_{dv_i}", 4.22, dv_y, Z_REAR - 0.04, 6.56, dv_y + 0.56, Z_REAR + 0.08, "Mat_SoilDark", bevel=0.04)
    for dvc in range(6):
        dvx = 4.44 + dvc * 0.38
        add_sphere(col_site, f"DryVeg_Leaf_{dv_i}_{dvc}", dvx, dv_y + 0.28, Z_REAR + 0.16, 0.135,
                   "Mat_FoliageBright" if (dv_i + dvc) % 2 == 0 else "Mat_FoliageGreen", 1.1, 1.0, 0.65)
add_cyl(col_site, "Rear_LaundryBasket", 3.45, 20.85, Z_REAR + 0.01, Z_REAR + 0.39, 0.18, 0.22, "Mat_WoodOakTable", segs=16)

# ☕ BÀN GHẾ NGỒI CHILL PHÍA SAU (CHỈ 1 GHẾ DÀI + 1 BÀN TRÒN) — PHÍA NAM BẬC THANG CỬA SAU (X=1.94..3.44, Y=16.0..17.85)
# Ngồi tựa đầu vào tường hậu nhà phía Đông (Y=16.0), lưng về phía Đông (-Y), mặt hướng về phía Tây (+Y) ngắm trọn Vườn rau!
add_box(col_site, "Rear_Chill_Deck", 1.85, 16.00, Z_REAR, 3.48, 17.90, Z_REAR + 0.02, "Mat_AntiSlipWoodTile")
add_box(col_site, "Rear_Chill_BenchBase", 1.94, 16.08, Z_REAR + 0.02, 3.44, 16.64, Z_REAR + 0.38, "Mat_WoodOakTable", bevel=0.015)
add_box(col_site, "Rear_Chill_BenchBack", 1.94, 16.00, Z_REAR + 0.38, 3.44, 16.09, Z_REAR + 0.98, "Mat_WoodLouverFacade", bevel=0.008)
add_box(col_site, "Rear_Chill_BenchPad", 1.98, 16.10, Z_REAR + 0.38, 3.40, 16.60, Z_REAR + 0.46, "Mat_CushionMustard", bevel=0.02)
for rci, rcx in enumerate([2.24, 2.69, 3.14]):
    add_box(col_site, f"Rear_Chill_Pillow_{rci}", rcx - 0.19, 16.11, Z_REAR + 0.46, rcx + 0.19, 16.26, Z_REAR + 0.74,
            "Mat_CushionSage" if rci % 2 == 0 else "Mat_BeddingCream", bevel=0.035)
add_cyl(col_site, "Rear_Chill_RoundTableTop", 2.69, 17.28, Z_REAR + 0.46, Z_REAR + 0.51, 0.42, 0.42, "Mat_WhiteMarble", segs=24)
add_cyl(col_site, "Rear_Chill_RoundTableLeg", 2.69, 17.28, Z_REAR + 0.02, Z_REAR + 0.46, 0.06, 0.12, "Mat_MetalMatteBlack", segs=16)
add_cyl(col_site, "Rear_Chill_Cup1", 2.57, 17.24, Z_REAR + 0.51, Z_REAR + 0.59, 0.035, 0.04, "Mat_CeramicWhite")
add_cyl(col_site, "Rear_Chill_Cup2", 2.81, 17.32, Z_REAR + 0.51, Z_REAR + 0.59, 0.035, 0.04, "Mat_CeramicTeal")
add_potted_plant(col_site, "Rear_Chill_Plant", 1.62, 16.32, Z_REAR, scale=0.82, pot_mat="Mat_TerracottaPot")

# 🛵 XE MÁY DỰNG GẦN NHÀ TẮM (từ đường luồng chạy xuống tới Y=18.9 rẽ Bắc): ĐẦU HƯỚNG BẮC (+X), BÁNH SAU HƯỚNG NAM (-X)!
add_box(col_site, "Rear_Scooter_Body", 3.18, 18.70, Z_REAR + 0.27, 4.46, 19.16, Z_REAR + 0.80, "Mat_CeramicWhite", bevel=0.06)
add_box(col_site, "Rear_Scooter_Seat", 3.30, 18.74, Z_REAR + 0.77, 4.06, 19.12, Z_REAR + 0.89, "Mat_WoodOakDark", bevel=0.04)
add_box(col_site, "Rear_Scooter_FrontShield", 4.22, 18.72, Z_REAR + 0.60, 4.44, 19.14, Z_REAR + 1.04, "Mat_CeramicWhite", bevel=0.04)
add_box(col_site, "Rear_Scooter_Handle", 4.32, 18.60, Z_REAR + 1.02, 4.42, 19.26, Z_REAR + 1.10, "Mat_MetalMatteBlack")
add_box(col_lights, "Rear_Scooter_Headlight", 4.43, 18.85, Z_REAR + 0.86, 4.47, 19.01, Z_REAR + 0.96, "Mat_WarmSconce")
add_cyl(col_site, "Rear_Scooter_WheelFront_N", 4.34, 18.93, Z_REAR, Z_REAR + 0.43, 0.21, 0.21, "Mat_TireRubber", rot=(math.pi / 2, 0, 0), segs=16)
add_cyl(col_site, "Rear_Scooter_WheelRear_S", 3.30, 18.93, Z_REAR, Z_REAR + 0.43, 0.21, 0.21, "Mat_TireRubber", rot=(math.pi / 2, 0, 0), segs=16)

# 🫧 NƠI RỬA CHÉN NGOÀI TRỜI PHÍA SAU (CÚNG GIỖ — NẰM TRỌN TRONG HIÊN SAU Y<=20.30, PHÍA TRƯỚC LÀ ĐÔNG, PHÍA SAU LÀ RAU!)
# Sàn rửa chén chống trơn rộng rãi (X=0.30..2.85, Y=18.40..20.20 -> 2.55m x 1.80m ngồi 2-3 người rửa cỗ cực thoải mái!)
# Mưa nắng ngồi rửa mát mẻ như trong nhà; trụ vòi nước đôi quay mặt Đông (-Y), phía sau (+Y) có rãnh thoát nước tưới thẳng ra Vườn rau!
add_box(col_site, "RearWash_Pad", 0.30, 18.40, Z_REAR, 2.85, 20.22, Z_REAR + 0.03, "Mat_StepStone", bevel=0.008)
# Gờ chắn nước thấp & rãnh thu nước có lưới lọc rác dẫn thẳng ra luống rau phía Tây (+Y)
add_box(col_site, "RearWash_DrainChannel", 0.35, 20.12, Z_REAR + 0.01, 2.80, 20.26, Z_REAR + 0.045, "Mat_DarkGreyStone")
add_box(col_site, "RearWash_DrainGrate", 0.42, 20.15, Z_REAR + 0.042, 2.73, 20.23, Z_REAR + 0.052, "Mat_MetalStainless")
for dr_i, dr_x in enumerate([0.95, 2.15]):
    add_cyl(col_site, f"RearWash_DrainPipe_{dr_i}", dr_x, 20.48, Z_REAR + 0.03, Z_REAR + 0.07, 0.032, 0.032, "Mat_DarkGreyStone",
            rot=(math.pi / 2, 0, 0), segs=10)
# Trụ vòi nước đôi ốp đá thấp ở mép Tây khu rửa (Y=19.95..20.14): phía trước là Đông (-Y, sân ngồi rửa), phía sau là Vườn rau (+Y)!
add_box(col_site, "RearWash_TapWall", 1.05, 19.96, Z_REAR + 0.03, 2.10, 20.14, Z_REAR + 0.68, "Mat_WallWarmWhite", bevel=0.01)
add_box(col_site, "RearWash_TapWallCap", 1.03, 19.94, Z_REAR + 0.68, 2.12, 20.16, Z_REAR + 0.72, "Mat_DarkGreyStone", bevel=0.008)
# 2 vòi nước inox tầm thấp (cao 0.44m vừa tầm ngồi ghế đẩu rửa chén cúng giỗ) hướng ra phía Đông (-Y)
for ti, tx in enumerate([1.32, 1.84]):
    add_cyl(col_site, f"RearWash_FaucetPipe_{ti}", tx, 19.89, Z_REAR + 0.42, Z_REAR + 0.45, 0.016, 0.016, "Mat_MetalStainless",
            rot=(math.pi / 2, 0, 0), segs=10)
    add_cyl(col_site, f"RearWash_FaucetSpout_{ti}", tx, 19.82, Z_REAR + 0.36, Z_REAR + 0.44, 0.014, 0.014, "Mat_MetalStainless", segs=10)
    add_box(col_site, f"RearWash_FaucetHandle_{ti}", tx - 0.035, 19.90, Z_REAR + 0.46, tx + 0.035, 19.93, Z_REAR + 0.48, "Mat_MetalMatteBlack")
# 2 thau inox rửa chén lớn dưới 2 vòi nước + 2 ghế đẩu thấp ngồi rửa cực thoải mái + rổ úp chén
add_cyl(col_site, "RearWash_Basin1", 1.32, 19.55, Z_REAR + 0.03, Z_REAR + 0.22, 0.22, 0.27, "Mat_MetalStainless", segs=20)
add_cyl(col_site, "RearWash_Water1", 1.32, 19.55, Z_REAR + 0.16, Z_REAR + 0.19, 0.24, 0.24, "Mat_WaterClear", segs=18)
add_cyl(col_site, "RearWash_Basin2", 1.92, 19.55, Z_REAR + 0.03, Z_REAR + 0.22, 0.22, 0.27, "Mat_MetalStainless", segs=20)
add_cyl(col_site, "RearWash_Water2", 1.92, 19.55, Z_REAR + 0.16, Z_REAR + 0.19, 0.24, 0.24, "Mat_WaterClear", segs=18)
add_box(col_site, "RearWash_DishRack", 0.56, 19.42, Z_REAR + 0.03, 0.96, 19.84, Z_REAR + 0.24, "Mat_WoodOakTable", bevel=0.01)
for wsi, wsx in enumerate([1.25, 1.95]):
    add_cyl(col_site, f"RearWash_LowStool_{wsi}", wsx, 18.92, Z_REAR + 0.03, Z_REAR + 0.28, 0.14, 0.16, "Mat_WoodOakTable", segs=14)

# Vườn rau hữu cơ PHÍA NAM (X = 0.25..2.95, Y = 20.75..23.60 — HOÀN TOÀN NGOÀI HIÊN SAU để hứng trọn nắng mưa tự nhiên!)
for vr in range(4):
    vry = 20.75 + vr * 0.72
    add_box(col_site, f"VegBed_{vr}", 0.25, vry, Z_REAR, 2.95, vry + 0.52, Z_REAR + 0.29, "Mat_WoodOakDark", bevel=0.01)
    add_box(col_site, f"VegSoil_{vr}", 0.32, vry + 0.05, Z_REAR + 0.25, 2.88, vry + 0.47, Z_REAR + 0.31, "Mat_SoilDark")
    for vc in range(6):
        vx = 0.55 + vc * 0.42
        add_sphere(col_site, f"VegLeaf_{vr}_{vc}", vx, vry + 0.26, Z_REAR + 0.39, 0.14,
                   "Mat_FoliageBright" if (vr + vc) % 2 == 0 else "Mat_FoliageGreen", 1.1, 1.0, 0.65)

# ---------------------------------------------------------------------------
# 7. TẦNG 2 MỞ RỘNG 7M: HÀNH LANG 2M PHÍA NAM (X=0..2) + CÁC PHÒNG PHÍA BẮC (X=2.14..6.78)
# ---------------------------------------------------------------------------
Z2 = 3.85
H2 = 7.35

# Sàn Tầng 2 mở rộng trọn 7m (X = 0..7):
# - Ban công trước vươn dài 3.0m (Y = -3.0..0.0)
# - Hiên sau / Ban công sau che phủ trọn đến hết Nhà vệ sinh & Nơi rửa chén ngoài trời (Y = 16.0..20.30, rộng 7m!)
# - Từ Y = 20.30..24.00 ĐỂ TRỐNG TRỜI HOÀN TOÀN cho Vườn rau hứng mưa nắng tươi tốt & Dây phơi đón nắng!
add_box(col_fl2_arch, "Floor2_Slab_Front", 0.0, -3.0, Z2 - 0.15, 7.0, 8.95, Z2, "Mat_AntiSlipWoodTile")
add_box(col_fl2_arch, "Floor2_Slab_HallSide", 0.0, 8.95, Z2 - 0.15, 3.05, 11.20, Z2, "Mat_AntiSlipWoodTile")
add_box(col_fl2_arch, "Floor2_Slab_RearWide", 0.0, 11.20, Z2 - 0.15, 7.0, 20.30, Z2, "Mat_AntiSlipWoodTile")
add_box(col_lights, "RearPorch_EdgeLED", 0.20, 20.22, Z2 - 0.19, 6.80, 20.26, Z2 - 0.15, "Mat_WarmLED")

# Hệ cột kết cấu đỡ hành lang Tầng 2 & góc hiên sau dọc sát tường rào Nam (không cản đường luồng 2m) + cột góc Tây Bắc hiên sau
for ci, cy in enumerate([-2.88, 0.15, 4.0, 8.0, 12.0, 15.85, 20.15]):
    add_box(col_fl2_arch, f"Fl2_Corridor_Col_{ci}", -0.02, cy - 0.12, 0.15, 0.20, cy + 0.12, Z2 - 0.15, "Mat_WallWarmWhite", bevel=0.01)
add_box(col_fl2_arch, "Fl2_RearPorch_Col_NW", 6.78, 20.03, Z_REAR, 7.00, 20.27, Z2 - 0.15, "Mat_WallWarmWhite", bevel=0.01)
add_box(col_fl2_arch, "Fl2_Corridor_EdgeBeam", -0.02, -3.0, Z2 - 0.30, 0.20, 20.30, Z2 - 0.14, "Mat_RoofCharcoal")
add_box(col_fl2_arch, "BalconyFront_EdgeBeam", -0.02, -3.02, Z2 - 0.28, 7.0, -2.86, Z2 - 0.14, "Mat_RoofCharcoal")
# Dải đèn LED hắt trần dưới hành lang Tầng 2 chiếu sáng đường luồng 2m phía Nam tầng 1
add_box(col_lights, "Fl1_Corridor_CeilingLED", 0.98, 0.30, Z2 - 0.19, 1.08, 15.70, Z2 - 0.15, "Mat_WarmLED")

# Lan can CON TIỆN GỖ & diềm sàn ốp gỗ sồi kiểu gác lửng quanh ô thông tầng Tầng 2 (đồng bộ tuyệt đối với mẫu ảnh cầu thang gỗ!)
# Chừa mở X=5.92..6.78 tại Y=8.95 để từ cầu thang gỗ 1 vế bước thẳng vào Sảnh Tầng 2!
add_box(col_fl2_arch, "Fl2_StairFascia_Front", 3.05, 8.91, Z2 - 0.20, 5.92, 8.98, Z2 + 0.03, "Mat_WoodOakDark", bevel=0.006)
add_box(col_fl2_arch, "Fl2_StairGuard_FrontRail", 3.03, 8.90, Z2 + 0.90, 5.94, 8.98, Z2 + 0.97, "Mat_WoodOakDark", bevel=0.006)
add_wood_newel_post(col_fl2_arch, "Fl2_StairNewel_Corner", 3.06, 8.94, Z2, height=1.02)
add_wood_newel_post(col_fl2_arch, "Fl2_StairNewel_TopE", 5.92, 8.94, Z2, height=1.02)
for fbi in range(18):
    fbx = 3.22 + fbi * 0.145
    add_cyl(col_fl2_arch, f"Fl2_StairBaluster_Front_{fbi}", fbx, 8.94, Z2, Z2 + 0.90, 0.016, 0.014, "Mat_WoodStairTreads", segs=10)

add_box(col_fl2_arch, "Fl2_StairFascia_Left", 3.02, 8.95, Z2 - 0.20, 3.09, 11.20, Z2 + 0.03, "Mat_WoodOakDark", bevel=0.006)
add_box(col_fl2_arch, "Fl2_StairGuard_LeftRail", 3.02, 8.94, Z2 + 0.90, 3.10, 11.20, Z2 + 0.97, "Mat_WoodOakDark", bevel=0.006)
for lbi in range(14):
    lby = 9.12 + lbi * 0.148
    add_cyl(col_fl2_arch, f"Fl2_StairBaluster_Left_{lbi}", 3.06, lby, Z2, Z2 + 0.90, 0.016, 0.014, "Mat_WoodStairTreads", segs=10)

# Tường bao Tầng 2 (tường phải phía Bắc cắt thấp 0.38m để xem xuyên nội thất)
add_box(col_fl2_arch, "Fl2_Wall_Right_Cutaway", 6.78, 0.0, Z2, 7.0, 16.0, Z2 + 0.38, "Mat_WallWarmWhite")

# Vách ngăn giữa Hành lang mới 2m phía Nam (X=0.16..2.0) và các phòng Tầng 2 phía Bắc (X=2.14..6.78) — có cửa ra vào từng phòng
add_box(col_fl2_arch, "Fl2_InnerHallWall_Master1", 2.0, 0.0, Z2, 2.14, 2.75, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_MasterTop", 2.0, 2.75, Z2 + 2.28, 2.14, 3.65, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_Master2", 2.0, 3.65, Z2, 2.14, 7.02, H2, "Mat_WallWarmWhite")
# Y = 7.02..11.20 mở hoàn toàn nối thông sảnh cầu thang/giếng trời ra hành lang 2m phía Nam!
add_box(col_fl2_arch, "Fl2_InnerHallWall_Seu1", 2.0, 11.20, Z2, 2.14, 12.60, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_SeuTop", 2.0, 12.60, Z2 + 2.28, 2.14, 13.42, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_Sis1", 2.0, 13.42, Z2, 2.14, 14.90, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_SisTop", 2.0, 14.90, Z2 + 2.28, 2.14, 15.72, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_InnerHallWall_End", 2.0, 15.72, Z2, 2.14, 16.0, H2, "Mat_WallWarmWhite")

# Vách ngoài bên trái (PHÍA NAM) của Hành lang Tầng 2 (X = 0.0..0.16, Y = 0..16): 4 khung kính lớn toàn cảnh đón gió Nam!
add_box(col_fl2_arch, "Fl2_Corridor_OuterBot", 0.0, 0.0, Z2, 0.16, 16.0, Z2 + 0.92, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Corridor_OuterTop", 0.0, 0.0, Z2 + 2.95, 0.16, 16.0, H2, "Mat_WallWarmWhite")
for pi, py in enumerate([0.0, 4.0, 8.0, 12.0, 15.80]):
    add_box(col_fl2_arch, f"Fl2_Corridor_Pier_{pi}", 0.0, py, Z2, 0.18, py + 0.22, H2, "Mat_WallWarmWhite")
for wi, (wy1, wy2) in enumerate([(0.22, 4.0), (4.22, 8.0), (8.22, 12.0), (12.22, 15.80)]):
    add_window_frame(col_fl2_arch, f"Fl2_Corridor_Window_{wi}", 0.04, wy1, Z2 + 0.92, 0.14, wy2, Z2 + 2.95)

# Tường mặt tiền chừa cửa kính lớn đầu Hành lang phía Nam + cửa kính lớn Phòng Master phía Bắc
add_box(col_fl2_arch, "Fl2_Wall_Front_L", 0.0, 0.0, Z2, 0.28, 0.22, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Front_Mid", 1.90, 0.0, Z2, 2.75, 0.22, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Front_R", 6.25, 0.0, Z2, 7.0, 0.22, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Front_Top", 0.28, 0.0, Z2 + 2.65, 6.25, 0.22, H2, "Mat_WallWarmWhite")
add_window_frame(col_fl2_arch, "Fl2_Corridor_FrontDoor", 0.28, 0.06, Z2, 1.90, 0.18, Z2 + 2.65)
add_window_frame(col_fl2_arch, "Master_FrontGlassDoor", 2.75, 0.06, Z2, 6.25, 0.18, Z2 + 2.65)

# Tường sau chừa cửa kính cuối Hành lang phía Nam + cửa kính Phòng Chị Hai mở ra Ban công sau 7m
add_box(col_fl2_arch, "Fl2_Wall_Rear_L", 0.0, 15.78, Z2, 0.28, 16.0, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Rear_Mid", 1.90, 15.78, Z2, 3.15, 16.0, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Rear_R", 5.65, 15.78, Z2, 7.0, 16.0, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Fl2_Wall_Rear_Top", 0.28, 15.78, Z2 + 2.55, 5.65, 16.0, H2, "Mat_WallWarmWhite")
add_window_frame(col_fl2_arch, "Fl2_Corridor_RearDoor", 0.28, 15.80, Z2, 1.90, 15.94, Z2 + 2.55)
add_window_frame(col_fl2_arch, "Sister2_RearDoor", 3.15, 15.80, Z2, 5.65, 15.94, Z2 + 2.55)

# Nội thất & trang trí Hành lang Tầng 2 PHÍA NAM (X = 0.16..2.0, Y = 0..16)
add_box(col_fl2_furn, "Fl2_Corridor_RunnerRug", 0.70, 0.60, Z2, 1.55, 15.40, Z2 + 0.02, "Mat_RugWarm", bevel=0.006)
# Ghế băng đọc sách & kệ console ngắm cảnh bên khung kính hướng Nam
add_box(col_fl2_furn, "Fl2_Corridor_Bench", 0.22, 7.10, Z2 + 0.08, 0.74, 9.60, Z2 + 0.44, "Mat_WoodOakTable", bevel=0.015)
add_box(col_fl2_furn, "Fl2_Corridor_BenchPad", 0.24, 7.16, Z2 + 0.44, 0.70, 9.54, Z2 + 0.52, "Mat_CushionMustard", bevel=0.02)
add_box(col_fl2_furn, "Fl2_Corridor_Pillow1", 0.24, 7.35, Z2 + 0.52, 0.44, 7.75, Z2 + 0.80, "Mat_CushionNavy", bevel=0.04)
add_box(col_fl2_furn, "Fl2_Corridor_Pillow2", 0.24, 8.95, Z2 + 0.52, 0.44, 9.35, Z2 + 0.80, "Mat_CushionTerracotta", bevel=0.04)
add_box(col_fl2_furn, "Fl2_Corridor_Console", 0.22, 1.80, Z2 + 0.08, 0.66, 3.20, Z2 + 0.78, "Mat_WoodOakCabinet", bevel=0.01)
add_cyl(col_fl2_furn, "Fl2_Corridor_Vase", 0.44, 2.50, Z2 + 0.78, Z2 + 1.06, 0.08, 0.05, "Mat_CeramicTeal")
add_sphere(col_fl2_furn, "Fl2_Corridor_Flowers", 0.44, 2.50, Z2 + 1.14, 0.12, "Mat_FlowerYellow")
for pi, py in enumerate([0.85, 5.40, 10.65, 14.95]):
    add_potted_plant(col_fl2_furn, f"Fl2_Corridor_Plant_{pi}", 0.58, py, Z2, scale=0.88,
                     pot_mat="Mat_CeramicWhite" if pi % 2 == 0 else "Mat_TerracottaPot")
for li, ly in enumerate([2.2, 6.2, 10.2, 14.2]):
    add_pendant_chandelier(col_lights, f"Fl2_Corridor_Light_{li}", 1.08, ly, H2 - 0.02, drop=0.45, count=1)
add_framed_art(col_fl2_furn, "Fl2_Corridor_Art1", 1.98, 5.30, Z2 + 1.80, 0.90, 0.72, wall_axis='X', canvas_mat="Mat_ArtCanvasGreen")
add_framed_art(col_fl2_furn, "Fl2_Corridor_Art2", 1.98, 11.90, Z2 + 1.80, 0.85, 0.68, wall_axis='X', canvas_mat="Mat_ArtCanvasWarm")

# Ban công trước mở rộng dài ra 3.0m (7m x 3.0m = 21m² ngay trước Phòng Master Chị Ba & đầu Hành lang Nam!)
add_box(col_fl2_arch, "BalconyFront_Rail", 0.0, -3.00, Z2, 7.0, -2.94, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyFront_TopBar", 0.0, -3.02, Z2 + 1.10, 7.0, -2.92, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "BalconyFront_Rail_L", 0.0, -3.00, Z2, 0.05, 0.0, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyFront_TopBar_L", -0.02, -3.02, Z2 + 1.10, 0.07, 0.0, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "BalconyFront_Rail_R", 6.95, -3.00, Z2, 7.0, 0.0, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyFront_TopBar_R", 6.93, -3.02, Z2 + 1.10, 7.02, 0.0, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_lights, "BalconyFront_UnderLED", 0.1, -2.98, Z2 - 0.18, 6.9, -2.92, Z2 - 0.14, "Mat_WarmLED")
# Đèn gắn tường mặt tiền chiếu sáng ban công đêm
add_box(col_lights, "BalconyFront_Sconce1", 6.44, -0.08, Z2 + 1.85, 6.58, 0.02, Z2 + 2.15, "Mat_WarmSconce")
add_box(col_lights, "BalconyFront_Sconce2", 2.24, -0.08, Z2 + 1.85, 2.38, 0.02, Z2 + 2.15, "Mat_WarmSconce")

# Bộ bàn trà & ghế thư giãn ngắm sao ngay trước cửa kính Phòng Master (phía Bắc)
add_box(col_fl2_furn, "BalconyFront_Rug", 3.35, -2.35, Z2, 5.90, -0.75, Z2 + 0.02, "Mat_RugWarm", bevel=0.006)
add_dining_chair(col_fl2_furn, "BalconyFront_Chair1", 5.35, -1.55, Z2, 0.45, "Mat_CushionMustard", "Mat_WoodOakTable")
add_dining_chair(col_fl2_furn, "BalconyFront_Chair2", 3.90, -1.55, Z2, -0.45, "Mat_CushionMustard", "Mat_WoodOakTable")
add_cyl(col_fl2_furn, "BalconyFront_Table", 4.62, -1.62, Z2 + 0.46, Z2 + 0.51, 0.36, 0.36, "Mat_WhiteMarble", segs=22)
add_cyl(col_fl2_furn, "BalconyFront_TableLeg", 4.62, -1.62, Z2, Z2 + 0.46, 0.05, 0.09, "Mat_MetalMatteBlack")
add_cyl(col_fl2_furn, "BalconyFront_Cup1", 4.74, -1.56, Z2 + 0.51, Z2 + 0.59, 0.035, 0.04, "Mat_CeramicWhite")
add_cyl(col_fl2_furn, "BalconyFront_Cup2", 4.52, -1.68, Z2 + 0.51, Z2 + 0.59, 0.035, 0.04, "Mat_CeramicTeal")

# Ghế băng tắm nắng / chill nhạc phía Nam ban công trước (X = 0.65..2.55, Y = -2.30..-1.45)
add_box(col_fl2_furn, "BalconyFront_DaybedBase", 0.65, -2.30, Z2 + 0.08, 2.55, -1.48, Z2 + 0.42, "Mat_WoodOakTable", bevel=0.02)
add_box(col_fl2_furn, "BalconyFront_DaybedPad", 0.70, -2.26, Z2 + 0.42, 2.50, -1.52, Z2 + 0.52, "Mat_BeddingCream", bevel=0.025)
add_box(col_fl2_furn, "BalconyFront_DaybedPillow1", 2.05, -2.18, Z2 + 0.52, 2.42, -1.62, Z2 + 0.78, "Mat_CushionTerracotta", bevel=0.04)
add_box(col_fl2_furn, "BalconyFront_DaybedPillow2", 0.76, -2.18, Z2 + 0.52, 1.12, -1.62, Z2 + 0.78, "Mat_CushionNavy", bevel=0.04)

# Bồn cây cảnh & chậu hoa dọc lan can ban công trước
add_box(col_fl2_furn, "BalconyFront_PlanterBox", 3.40, -2.86, Z2, 5.80, -2.52, Z2 + 0.38, "Mat_DarkGreyStone", bevel=0.015)
for fi in range(5):
    fx = 3.68 + fi * 0.46
    add_sphere(col_fl2_furn, f"BalconyFront_Bush_{fi}", fx, -2.69, Z2 + 0.48, 0.18,
               "Mat_FoliageBright" if fi % 2 == 0 else "Mat_FoliageGreen", 1.1, 0.9, 0.75)
    add_sphere(col_fl2_furn, f"BalconyFront_Flower_{fi}", fx, -2.69, Z2 + 0.60, 0.07,
               "Mat_FlowerPink" if fi % 2 == 0 else "Mat_FlowerYellow")
add_potted_plant(col_fl2_furn, "BalconyFront_Plant1", 6.52, -2.45, Z2, scale=0.95, pot_mat="Mat_CeramicWhite")
add_potted_plant(col_fl2_furn, "BalconyFront_Plant2", 6.52, -0.75, Z2, scale=0.80, pot_mat="Mat_TerracottaPot")
add_potted_plant(col_fl2_furn, "BalconyFront_Plant3", 0.55, -2.45, Z2, scale=0.95, pot_mat="Mat_CeramicWhite")

# --- A. PHÒNG NGỦ MASTER CHỊ BA (Y = 0.22..7.0, X = 2.14..6.78) ---
add_box(col_fl2_furn, "Master_AreaRug", 3.95, 1.40, Z2, 6.55, 4.05, Z2 + 0.025, "Mat_RugWarm", bevel=0.008)
add_detailed_bed(col_fl2_furn, "Master_Bed", 4.28, 1.85, Z2 + 0.02, 6.22, 4.05, head_side='Y_MAX', duvet_mat="Mat_CushionNavy")
add_nightstand(col_fl2_furn, "Master_Nightstand_R", 6.50, 3.82, Z2 + 0.02)
add_nightstand(col_fl2_furn, "Master_Nightstand_L", 4.00, 3.82, Z2 + 0.02)
add_framed_art(col_fl2_furn, "Master_HeadArt", 5.25, 4.12, Z2 + 1.85, 1.30, 0.78, wall_axis='Y', canvas_mat="Mat_ArtCanvasWarm")
add_curtain_pair(col_fl2_furn, "Master_FrontCurtain", 2.72, 6.28, 0.28, Z2 + 0.04, H2 - 0.15)
add_pendant_chandelier(col_lights, "Master_Chandelier", 4.75, 2.30, H2 - 0.02, drop=0.72, count=3)

# 🎹 ĐÀN PIANO UPRIGHT CHI TIẾT ÁP TƯỜNG TRÁI (GIÁP HÀNH LANG NAM, X=2.18..2.74) + GHẾ ĐÀN + GIÁ NHẠC + PEDAL ĐỒNG
add_box(col_fl2_furn, "Master_Piano_Body", 2.18, 0.85, Z2 + 0.04, 2.74, 2.38, Z2 + 1.24, "Mat_PianoBlackGloss", bevel=0.018)
add_box(col_fl2_furn, "Master_Piano_Keybed", 2.70, 0.88, Z2 + 0.66, 3.00, 2.35, Z2 + 0.75, "Mat_PianoBlackGloss", bevel=0.01)
add_box(col_fl2_furn, "Master_Piano_WhiteKeys", 2.74, 0.94, Z2 + 0.75, 2.98, 2.29, Z2 + 0.79, "Mat_CeramicWhite")
for bk in range(18):
    if bk % 7 not in (2, 6):
        by_k = 0.99 + bk * 0.070
        add_box(col_fl2_furn, f"Master_Piano_BlackKey_{bk}", 2.75, by_k, Z2 + 0.79, 2.90, by_k + 0.028, Z2 + 0.818, "Mat_MetalMatteBlack")
add_box(col_fl2_furn, "Master_Piano_SheetMusic", 2.74, 1.40, Z2 + 0.88, 2.78, 1.85, Z2 + 1.14, "Mat_BeddingWhite")
for pd in range(3):
    add_box(col_fl2_furn, f"Master_Piano_Pedal_{pd}", 2.74, 1.52 + pd * 0.09, Z2 + 0.05, 2.84, 1.56 + pd * 0.09, Z2 + 0.09, "Mat_BrassGold")
add_box(col_fl2_furn, "Master_Piano_BenchTop", 3.14, 1.25, Z2 + 0.44, 3.54, 1.98, Z2 + 0.52, "Mat_PianoBlackGloss", bevel=0.018)
for i, (lx, ly) in enumerate([(3.19, 1.30), (3.49, 1.30), (3.19, 1.93), (3.49, 1.93)]):
    add_cyl(col_fl2_furn, f"Master_Piano_BenchLeg_{i}", lx, ly, Z2, Z2 + 0.45, 0.022, 0.022, "Mat_PianoBlackGloss", segs=8)
add_framed_art(col_fl2_furn, "Master_PianoArt", 2.17, 1.62, Z2 + 1.92, 0.92, 0.68, wall_axis='X', canvas_mat="Mat_ArtCanvasBlue")

# 🧘 Góc Yoga & Thiền Master (đặt đón nắng sáng ngay trước cửa kính ban công, hoàn toàn không chắn lối đi!)
add_box(col_fl2_furn, "Master_YogaMat", 4.50, 0.58, Z2, 6.00, 1.38, Z2 + 0.025, "Mat_CushionMustard", bevel=0.008)
add_cyl(col_fl2_furn, "Master_MeditationCushion", 5.25, 0.98, Z2 + 0.025, Z2 + 0.14, 0.22, 0.20, "Mat_CushionTerracotta", segs=18)
add_potted_plant(col_fl2_furn, "Master_YogaPlant", 6.44, 0.72, Z2, scale=1.0, pot_mat="Mat_CeramicWhite")

# Vách ngăn sau giường Master — CÓ CỬA RỘNG (X=2.80..3.75) đi thẳng vào Walk-in Closet!
add_box(col_fl2_arch, "Master_Ensuite_Wall_L", 2.14, 4.15, Z2, 2.80, 4.25, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_Ensuite_Wall_Top", 2.80, 4.15, Z2 + 2.30, 3.75, 4.25, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_Ensuite_Wall_R", 3.75, 4.15, Z2, 6.78, 4.25, H2, "Mat_WallWarmWhite")
# Khung vòm gỗ sang trọng lối vào Walk-in Closet
add_box(col_fl2_arch, "Master_ClosetPortal_L", 2.77, 4.13, Z2, 2.83, 4.27, Z2 + 2.32, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_ClosetPortal_R", 3.72, 4.13, Z2, 3.78, 4.27, Z2 + 2.32, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_ClosetPortal_Top", 2.77, 4.13, Z2 + 2.28, 3.78, 4.27, Z2 + 2.34, "Mat_WoodOakDark")

# Vách ngăn WC Riêng & Walk-in Closet — CÓ CỬA VÀO WC (Y=4.36..5.22) kèm cửa trượt gỗ kính mờ!
add_box(col_fl2_arch, "Master_WC_Div_Front", 4.65, 4.25, Z2, 4.75, 4.36, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_WC_Div_Top", 4.65, 4.36, Z2 + 2.25, 4.75, 5.22, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_WC_Div_Solid", 4.65, 5.22, Z2, 4.75, 6.95, H2, "Mat_WallWarmWhite")
add_box(col_fl2_arch, "Master_BackWall", 2.14, 6.92, Z2, 6.78, 7.02, H2, "Mat_WallWarmWhite")

# Khung cửa & Cánh cửa trượt vào Phòng tắm Master (mở hờ sang phía Y=5.0..5.86 để thấy rõ lối vào thoáng)
add_box(col_fl2_arch, "Master_WCDoor_Frame1", 4.63, 4.33, Z2, 4.77, 4.39, Z2 + 2.27, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_WCDoor_Frame2", 4.63, 5.19, Z2, 4.77, 5.25, Z2 + 2.27, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_WCDoor_FrameTop", 4.63, 4.33, Z2 + 2.23, 4.77, 5.25, Z2 + 2.29, "Mat_WoodOakDark")
add_box(col_fl2_arch, "Master_WCDoor_Rail", 4.59, 4.35, Z2 + 2.26, 4.65, 6.05, Z2 + 2.31, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "Master_WCDoor_Leaf", 4.59, 4.98, Z2 + 0.02, 4.64, 5.84, Z2 + 2.24, "Mat_WoodOakTable", bevel=0.008)
add_box(col_fl2_arch, "Master_WCDoor_GlassInset", 4.58, 5.12, Z2 + 0.65, 4.65, 5.70, Z2 + 2.02, "Mat_GlassBronze")
add_box(col_fl2_arch, "Master_WCDoor_Handle", 4.55, 5.04, Z2 + 0.92, 4.59, 5.07, Z2 + 1.24, "Mat_BrassGold")

# Phòng tắm riêng Master (X=4.75..6.78, chừa sảnh bước từ cửa Y=4.36..5.22 hoàn toàn thông thoáng!)
# 1. Lavabo đá cẩm thạch + Gương tròn đèn LED áp vách trước bên phải (X=5.70..6.66, Y=4.28..4.82)
add_box(col_fl2_furn, "Master_VanityCabinet", 5.70, 4.28, Z2 + 0.16, 6.64, 4.82, Z2 + 0.82, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl2_furn, "Master_VanityTop", 5.68, 4.26, Z2 + 0.82, 6.66, 4.85, Z2 + 0.86, "Mat_WhiteMarble")
add_cyl(col_fl2_furn, "Master_SinkBasin", 6.17, 4.55, Z2 + 0.86, Z2 + 0.98, 0.18, 0.22, "Mat_CeramicWhite", segs=18)
add_cyl(col_fl2_furn, "Master_SinkFaucet", 6.17, 4.36, Z2 + 0.86, Z2 + 1.08, 0.018, 0.014, "Mat_BrassGold", segs=10)
add_cyl(col_fl2_furn, "Master_Mirror", 6.17, 4.27, Z2 + 1.48, Z2 + 1.52, 0.36, 0.36, "Mat_Mirror", rot=(math.pi / 2, 0, 0), segs=22)
add_cyl(col_lights, "Master_MirrorLED", 6.17, 4.25, Z2 + 1.48, Z2 + 1.50, 0.39, 0.39, "Mat_WarmLED", rot=(math.pi / 2, 0, 0), segs=22)

# 2. Bồn cầu đặt kín đáo sau mảng tường đặc bên trái (X=4.77..5.38, Y=5.36..5.86) + Vách kính ngăn nước
add_box(col_fl2_furn, "Master_ToiletTank", 4.77, 5.42, Z2 + 0.40, 5.04, 5.82, Z2 + 0.82, "Mat_CeramicWhite", bevel=0.03)
add_cyl(col_fl2_furn, "Master_ToiletBowl", 5.24, 5.62, Z2, Z2 + 0.42, 0.18, 0.22, "Mat_CeramicWhite", segs=16)
add_box(col_fl2_furn, "Master_WC_GlassScreen", 4.76, 5.94, Z2, 5.52, 5.97, Z2 + 2.05, "Mat_GlassClear")

# 3. Bồn tắm nằm cao cấp đặt ngang sát tường sau (X=5.12..6.66, Y=6.04..6.86) + Thảm chân & Vòi đồng
add_box(col_fl2_furn, "Master_Bathtub_Outer", 5.12, 6.04, Z2, 6.66, 6.86, Z2 + 0.58, "Mat_CeramicWhite", bevel=0.10)
add_box(col_fl2_furn, "Master_Bathtub_Water", 5.24, 6.14, Z2 + 0.46, 6.54, 6.76, Z2 + 0.52, "Mat_WaterClear")
add_cyl(col_fl2_furn, "Master_TubFaucet", 5.04, 6.45, Z2, Z2 + 0.78, 0.025, 0.022, "Mat_BrassGold", segs=10)
add_box(col_fl2_furn, "Master_BathMat", 5.58, 5.54, Z2, 6.28, 5.94, Z2 + 0.02, "Mat_RugWarm", bevel=0.006)
add_pendant_chandelier(col_lights, "Master_WC_Lamp", 5.75, 5.40, H2 - 0.02, drop=0.38, count=1)

# Walk-in Closet Master (liên thông Phòng ngủ -> Phòng thay đồ -> Cửa phòng tắm cực chuẩn!)
add_box(col_fl2_furn, "Master_Closet_Right", 4.08, 5.88, Z2, 4.62, 6.88, Z2 + 2.55, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl2_furn, "Master_Closet_Left", 2.16, 4.32, Z2, 2.70, 6.88, Z2 + 2.55, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_lights, "Master_Closet_LED1", 4.06, 5.92, Z2 + 2.46, 4.10, 6.84, Z2 + 2.50, "Mat_WarmLED")
add_box(col_lights, "Master_Closet_LED2", 2.69, 4.38, Z2 + 2.46, 2.73, 6.82, Z2 + 2.50, "Mat_WarmLED")
cloth_mats = ["Mat_CushionBlush", "Mat_CushionNavy", "Mat_BeddingWhite", "Mat_CushionSage", "Mat_CushionMustard", "Mat_CushionTerracotta"]
for gi in range(8):
    gy = 4.65 + gi * 0.26
    add_box(col_fl2_furn, f"Master_Clothes_{gi}", 2.70, gy, Z2 + 1.15, 2.86, gy + 0.12, Z2 + 2.05, cloth_mats[gi % len(cloth_mats)], bevel=0.015)
add_cyl(col_fl2_furn, "Master_Closet_Ottoman", 3.40, 6.18, Z2, Z2 + 0.44, 0.34, 0.34, "Mat_CushionBlush", segs=18)

# --- B. SẢNH CẦU THANG & GIẾNG TRỜI (Y = 7.0..11.2, nối liền hành lang 2m phía Nam) ---
add_potted_plant(col_fl2_furn, "Fl2_AtriumPlant", 2.55, 8.20, Z2, scale=1.10, pot_mat="Mat_CeramicWhite")

# --- C. PHÒNG SẾU — EM ÚT MỞ RỘNG 4.7M (X = 2.14..6.78, Y = 11.20..13.45) ---
add_box(col_fl2_arch, "Wall_Fl2_Seu_Front", 2.14, 11.15, Z2, 6.78, 11.25, H2, "Mat_WallWarmWhite")

add_box(col_fl2_furn, "Seu_Rug", 2.22, 11.35, Z2, 4.85, 13.25, Z2 + 0.025, "Mat_RugPattern", bevel=0.008)
add_detailed_bed(col_fl2_furn, "Seu_Bed", 2.20, 11.36, Z2 + 0.02, 4.25, 12.56, head_side='X_MIN', duvet_mat="Mat_CushionSage")
add_nightstand(col_fl2_furn, "Seu_Nightstand", 4.58, 11.55, Z2 + 0.02)
add_study_desk_set(col_fl2_furn, "Seu_Desk", 5.28, 12.76, Z2, 6.66, 13.36, chair_side='Y_MIN')
add_box(col_fl2_furn, "Seu_Shelf", 5.36, 13.22, Z2 + 1.45, 6.62, 13.42, Z2 + 1.50, "Mat_WoodOakTable")
add_books_row(col_fl2_furn, "Seu_Books", 5.44, 13.24, Z2 + 1.50, count=9, axis='X')
add_wardrobe(col_fl2_furn, "Seu_Wardrobe", 5.22, 11.28, Z2, 6.68, 11.82, h=2.40, door_face='Y_MAX')
add_framed_art(col_fl2_furn, "Seu_Art", 2.17, 11.96, Z2 + 1.85, 0.95, 0.65, wall_axis='X', canvas_mat="Mat_ArtCanvasGreen")
add_pendant_chandelier(col_lights, "Seu_Lamp", 4.45, 12.35, H2 - 0.02, drop=0.45, count=1)

# --- D. PHÒNG CHỊ HAI MỞ RỘNG 4.7M (X = 2.14..6.78, Y = 13.50..15.78) ---
add_box(col_fl2_arch, "Wall_Fl2_Sister2", 2.14, 13.45, Z2, 6.78, 13.55, H2, "Mat_WallWarmWhite")

add_box(col_fl2_furn, "Sister2_Rug", 2.22, 13.65, Z2, 4.85, 15.55, Z2 + 0.025, "Mat_RugWarm", bevel=0.008)
add_detailed_bed(col_fl2_furn, "Sister2_Bed", 2.20, 13.66, Z2 + 0.02, 4.25, 14.86, head_side='X_MIN', duvet_mat="Mat_CushionBlush")
add_nightstand(col_fl2_furn, "Sister2_Nightstand", 4.58, 13.85, Z2 + 0.02)
add_study_desk_set(col_fl2_furn, "Sister2_Desk", 5.28, 13.62, Z2, 6.66, 14.22, chair_side='Y_MAX')
add_box(col_fl2_furn, "Sister2_Shelf", 5.36, 13.58, Z2 + 1.45, 6.62, 13.78, Z2 + 1.50, "Mat_WoodOakTable")
add_books_row(col_fl2_furn, "Sister2_Books", 5.44, 13.60, Z2 + 1.50, count=9, axis='X')
add_wardrobe(col_fl2_furn, "Sister2_Wardrobe", 5.72, 15.16, Z2, 6.74, 15.72, h=2.40, door_face='Y_MIN')
add_framed_art(col_fl2_furn, "Sister2_Art", 2.17, 14.26, Z2 + 1.85, 0.95, 0.65, wall_axis='X', canvas_mat="Mat_ArtCanvasBlue")
add_pendant_chandelier(col_lights, "Sister2_Lamp", 4.45, 14.65, H2 - 0.02, drop=0.45, count=1)

# --- E. BAN CÔNG SAU / HIÊN SAU RỘNG 7M x 4.3M (Y = 16.0..20.30 — CHE PHỦ ĐẾN HẾT NHÀ VỆ SINH, CHỪA TRỐNG TRỜI CHO VƯỜN RAU TỪ Y>20.30!) ---
add_box(col_fl2_arch, "BalconyRear_Rail_End", 0.0, 20.24, Z2, 7.0, 20.30, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Top_End", -0.02, 20.22, Z2 + 1.10, 7.02, 20.32, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "BalconyRear_Rail_R", 6.94, 16.0, Z2, 7.0, 20.30, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Top_R", 6.92, 16.0, Z2 + 1.10, 7.02, 20.32, Z2 + 1.16, "Mat_MetalMatteBlack")
add_box(col_fl2_arch, "BalconyRear_Rail_L1", 0.0, 16.0, Z2, 0.06, 20.30, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyRear_Top_L1", -0.02, 16.0, Z2 + 1.10, 0.08, 20.32, Z2 + 1.16, "Mat_MetalMatteBlack")

# Góc Yoga ngoài trời & Khu Lounge Chill tắm trăng trên ban công sau 7m x 4.3m
add_box(col_fl2_furn, "BalconyRear_YogaDeck", 4.65, 16.8, Z2, 6.45, 19.6, Z2 + 0.05, "Mat_WoodOakTable")
add_box(col_fl2_furn, "BalconyRear_YogaMat", 5.05, 17.2, Z2 + 0.05, 6.05, 19.2, Z2 + 0.08, "Mat_CushionMustard", bevel=0.01)
add_cyl(col_fl2_furn, "BalconyRear_Cushion", 5.55, 18.2, Z2 + 0.08, Z2 + 0.20, 0.22, 0.20, "Mat_CushionSage", segs=18)

add_box(col_fl2_furn, "BalconyRear_LoungeBench", 0.55, 16.9, Z2 + 0.08, 1.55, 19.6, Z2 + 0.45, "Mat_WoodOakTable", bevel=0.02)
add_box(col_fl2_furn, "BalconyRear_LoungeBack", 0.52, 16.9, Z2 + 0.45, 0.78, 19.6, Z2 + 0.88, "Mat_WoodLouverFacade")
add_box(col_fl2_furn, "BalconyRear_LoungePad", 0.78, 16.96, Z2 + 0.45, 1.50, 19.54, Z2 + 0.55, "Mat_BeddingCream", bevel=0.02)
add_box(col_fl2_furn, "BalconyRear_CoffeeTable", 1.80, 17.60, Z2 + 0.36, 2.55, 18.95, Z2 + 0.42, "Mat_WhiteMarble", bevel=0.012)
for i, (lx, ly) in enumerate([(1.88, 17.68), (2.48, 17.68), (1.88, 18.88), (2.48, 18.88)]):
    add_cyl(col_fl2_furn, f"BalconyRear_TableLeg_{i}", lx, ly, Z2, Z2 + 0.36, 0.025, 0.025, "Mat_MetalMatteBlack")
add_potted_plant(col_fl2_furn, "BalconyRear_Plant1", 6.45, 19.75, Z2, scale=1.10, pot_mat="Mat_TerracottaPot")
add_potted_plant(col_fl2_furn, "BalconyRear_Plant2", 0.55, 19.75, Z2, scale=1.10, pot_mat="Mat_CeramicWhite")

# ---------------------------------------------------------------------------
# 8. TẦNG MÁI MỞ RỘNG 7M & 9 TẤM PIN SOLAR PV
# ---------------------------------------------------------------------------
ZR = 7.35
add_box(col_roof, "Roof_Fascia", -0.25, -0.35, ZR, 7.25, 16.35, ZR + 0.24, "Mat_RoofCharcoal")
add_box(col_lights, "Roof_Fascia_LED", -0.22, -0.36, ZR - 0.04, 7.22, -0.32, ZR, "Mat_WarmLED")
add_box(col_roof, "Roof_Slab", 0.05, 0.05, ZR + 0.24, 6.95, 15.95, ZR + 0.30, "Mat_WallWarmWhite")
add_box(col_roof, "Roof_SkylightFrame", 3.45, 7.15, ZR + 0.30, 5.65, 10.05, ZR + 0.62, "Mat_MetalMatteBlack")
add_box(col_roof, "Roof_SkylightGlass", 3.55, 7.25, ZR + 0.56, 5.55, 9.95, ZR + 0.66, "Mat_GlassClear")
add_cyl(col_roof, "Roof_WaterTank", 5.65, 13.8, ZR + 0.55, ZR + 1.95, 0.65, 0.65, "Mat_MetalStainless", rot=(math.pi / 2, 0, 0))
add_box(col_roof, "Roof_WaterTankStand", 5.10, 13.1, ZR + 0.30, 6.20, 14.5, ZR + 0.55, "Mat_MetalMatteBlack")
for p in range(3):
    py = 1.8 + p * 1.68
    add_box(col_roof, f"SolarPV_L_{p}", 0.50, py, ZR + 0.34, 2.25, py + 1.42, ZR + 0.42, "Mat_SolarPVPanels", rot=(0.12, 0, 0))
    add_box(col_roof, f"SolarPV_M_{p}", 2.60, py, ZR + 0.34, 4.35, py + 1.42, ZR + 0.42, "Mat_SolarPVPanels", rot=(0.12, 0, 0))
    add_box(col_roof, f"SolarPV_R_{p}", 4.70, py, ZR + 0.34, 6.45, py + 1.42, ZR + 0.42, "Mat_SolarPVPanels", rot=(0.12, 0, 0))

# ---------------------------------------------------------------------------
# 9. HỆ THỐNG SMART HOME, ĐIỆN, WIFI MESH 6E, CAMERA AI & NHÃN 3D
# ---------------------------------------------------------------------------
# Tủ điện tổng MDB + Inverter Solar 5kW gắn gọn tường kỹ thuật đường luồng phía Nam (tránh vướng bậc 1 cầu thang!)
add_box(col_smarthome, "Main_MDB_Electrical", 2.22, 9.25, Z1 + 0.90, 2.36, 9.85, Z1 + 1.65, "Mat_MetalStainless", bevel=0.01)
add_box(col_smarthome, "MDB_StatusLED", 2.35, 9.35, Z1 + 1.20, 2.37, 9.75, Z1 + 1.55, "Mat_SmartGreenLED")
add_box(col_smarthome, "Hybrid_Inverter_5kW", 2.22, 9.95, Z1 + 0.95, 2.36, 10.45, Z1 + 1.60, "Mat_CeramicWhite", bevel=0.015)
add_box(col_smarthome, "Inverter_Screen", 2.35, 10.08, Z1 + 1.25, 2.37, 10.32, Z1 + 1.45, "Mat_SmartCyanLED")

# Sạc xe điện EV Wallbox gắn tường rào Bắc cạnh ô tô SUV
add_box(col_smarthome, "EV_Wallbox_Charger", 6.78, -11.50, 1.10, 6.98, -11.10, 1.65, "Mat_CeramicWhite", bevel=0.02)
add_box(col_smarthome, "EV_Wallbox_LED", 6.76, -11.38, 1.25, 6.78, -11.22, 1.52, "Mat_SmartGreenLED")

# Màn hình Trung tâm Điều khiển Smart Home 10 inch ở Phòng khách (ngay sảnh cửa chính phía Nam)
add_box(col_smarthome, "Smart_ControlPanel_10in", 2.22, 1.85, Z1 + 1.38, 2.26, 2.18, Z1 + 1.61, "Mat_MetalMatteBlack")
add_box(col_smarthome, "Smart_ControlScreen", 2.25, 1.88, Z1 + 1.41, 2.27, 2.15, Z1 + 1.58, "Mat_SmartCyanLED")

# 3 Node WiFi Mesh 6E
wifi_nodes = [
    ("WiFi_Mesh_Node1_Living", 6.50, 3.15, Z1 + 0.50),
    ("WiFi_Mesh_Node2_Kitchen", 2.34, 11.80, Z1 + 2.30),
    ("WiFi_Mesh_Node3_Fl2Hall", 1.05, 7.60, Z2 + 3.20),
]
for wname, wx, wy, wz in wifi_nodes:
    add_cyl(col_smarthome, wname, wx, wy, wz, wz + 0.20, 0.065, 0.055, "Mat_CeramicWhite", segs=16)
    add_cyl(col_smarthome, f"{wname}_LED", wx, wy, wz + 0.18, wz + 0.205, 0.058, 0.058, "Mat_SmartCyanLED", segs=16)

# 5 Điều hòa Inverter treo tường
ac_units = [
    ("AC_Living", 2.22, 3.70, Z1 + 2.65, 'X'),
    ("AC_Parents", 3.22, 7.60, Z1 + 2.65, 'X'),
    ("AC_Master", 2.14, 1.60, Z2 + 2.75, 'X'),
    ("AC_Seu", 2.14, 11.95, Z2 + 2.75, 'X'),
    ("AC_Sister2", 2.14, 14.25, Z2 + 2.75, 'X'),
]
for aname, ax, ay, az, _ in ac_units:
    add_box(col_smarthome, aname, ax, ay - 0.45, az, ax + 0.24, ay + 0.45, az + 0.30, "Mat_CeramicWhite", bevel=0.025)
    add_box(col_smarthome, f"{aname}_Vane", ax + 0.20, ay - 0.40, az + 0.03, ax + 0.25, ay + 0.40, az + 0.07, "Mat_MetalMatteBlack")

# 6 Camera An Ninh PoE AI
cams = [
    ("Cam1_MainGate", 6.65, -17.85, 2.55, (0.3, 0, 0.5)),
    ("Cam2_FrontYard", 2.10, -0.15, 3.15, (0.4, 0, 2.5)),
    ("Cam3_SideCorridor", 1.80, 8.0, 2.90, (0.35, 0, 0.2)),
    ("Cam4_RearGarden", 2.20, 16.10, 3.10, (0.4, 0, -0.3)),
    ("Cam5_LivingRoom", 2.35, 5.55, Z1 + 2.85, (0.4, 0, -2.6)),
    ("Cam6_BalconyFl2", 0.25, -0.15, Z2 + 2.95, (0.35, 0, 2.5)),
]
for cname, cx, cy, cz, crot in cams:
    add_box(col_smarthome, cname, cx - 0.08, cy - 0.12, cz - 0.07, cx + 0.08, cy + 0.12, cz + 0.07, "Mat_CeramicWhite", bevel=0.02, rot=crot)
    add_cyl(col_smarthome, f"{cname}_Lens", cx, cy, cz - 0.04, cz + 0.04, 0.045, 0.045, "Mat_SmartCyanLED", segs=12)

# Nhãn nổi 3D gọn đẹp, không đổ bóng lên nội thất (có thể ẩn/hiện trong Outliner)
def add_3d_label(col, name, text_str, loc, rot_z=math.pi / 2):
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

add_3d_label(col_callouts, "Label_Altar", "GIAN THO", (7.30, 1.15, 3.25))
add_3d_label(col_callouts, "Label_Living", "PHONG KHACH", (7.30, 4.00, 3.25))
add_3d_label(col_callouts, "Label_Parents", "PHONG BA ME", (7.30, 7.3, 3.25))
add_3d_label(col_callouts, "Label_Kitchen", "BEP & BAN AN", (7.30, 13.5, 3.25))
add_3d_label(col_callouts, "Label_Master", "MASTER CHI BA", (7.30, 2.6, 6.85))
add_3d_label(col_callouts, "Label_Seu", "PHONG SEU", (7.30, 12.2, 6.85))
add_3d_label(col_callouts, "Label_Sister2", "PHONG CHI HAI", (7.30, 14.7, 6.85))
add_3d_label(col_callouts, "Label_Fl1_SouthCorridor", "DUONG LUONG NAM (2M)", (-0.30, 8.0, 2.15), rot_z=-math.pi / 2)
add_3d_label(col_callouts, "Label_Fl2_Corridor", "HANH LANG NAM TANG 2 (2M)", (-0.30, 8.0, 6.90), rot_z=-math.pi / 2)

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

# Ánh sáng mặt trời nhẹ ban ngày từ hướng Đông Nam + đèn ấm nội thất
sun_data = bpy.data.lights.new(name="Sun_Daylight", type='SUN')
sun_data.energy = 2.6
sun_data.color = (1.0, 0.96, 0.88)
sun_obj = bpy.data.objects.new("Sun_Daylight", sun_data)
sun_obj.rotation_euler = (math.radians(48), math.radians(-22), math.radians(-55))
col_lights.objects.link(sun_obj)

add_warm_light("Light_FrontCanopy", (4.5, -5.0, 3.1), 240.0)
add_warm_light("Light_DadTeaWall", (5.9, -3.95, 2.3), 190.0)
add_warm_light("Light_AltarNook", (5.8, 1.2, 3.2), 190.0, cast_shadow=True)
add_warm_light("Light_LivingNew", (4.9, 3.9, 3.2), 320.0, cast_shadow=True)
add_warm_light("Light_ParentsBed", (4.9, 7.4, 3.2), 240.0)
add_warm_light("Light_KitchenNew", (4.4, 13.5, 3.1), 340.0, cast_shadow=True)
add_warm_light("Light_Fl1_CorridorUnder", (1.05, 8.0, 3.4), 220.0)
add_warm_light("Light_MasterFront", (4.7, 2.5, 6.6), 340.0, cast_shadow=True)
add_warm_light("Light_MasterWC", (5.4, 5.5, 6.6), 200.0)
add_warm_light("Light_Seu", (4.5, 12.2, 6.6), 240.0)
add_warm_light("Light_Sister2", (4.5, 14.6, 6.6), 240.0)
add_warm_light("Light_Fl2_Corridor1", (1.05, 4.2, 6.7), 220.0)
add_warm_light("Light_Fl2_Corridor2", (1.05, 11.8, 6.7), 220.0)
add_warm_light("Light_BalconyRear8m", (3.8, 19.2, 5.6), 240.0)

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

# Camera mặc định nhìn từ góc cắt bên phải (+X, phía Bắc) thấy rõ cả mặt tiền và toàn bộ nội thất 2 tầng
def point_at(obj, target):
    from mathutils import Vector
    direction = Vector(target) - obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()

cam_data = bpy.data.cameras.new(name="Main_Cutaway_Camera")
cam_data.lens = 32.0
cam_data.clip_end = 500.0
cam_obj = bpy.data.objects.new("Main_Cutaway_Camera", cam_data)
cam_obj.location = (23.0 * S, -7.5 * S, 9.5 * S)
point_at(cam_obj, (4.5 * S, 7.0 * S, 3.4 * S))
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
                    # Căn góc nhìn viewport sang phía mặt cắt bên phải (phía Bắc)
                    if space.region_3d:
                        space.region_3d.view_location = (4.5 * S, 6.0 * S, 3.2 * S)
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
