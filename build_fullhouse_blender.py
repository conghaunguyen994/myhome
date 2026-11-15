"""
=============================================================================
FULLHOUSE 3D ARCHITECTURAL & ULTRA-DETAILED INTERIOR MODEL FOR BLENDER
Dự án: Nhà phố 2 tầng hiện đại (5m × 18m trên lô đất 7m × 22.8m)
Phong cách: Nhiệt đới Tối giản Ấm cúng (Japandi Tropical)
=============================================================================
Đặc điểm nổi bật (Bản Vẽ Chi Tiết Nội Thất Như Đời Thật):
1. Tầng 1 (Trệt):
   - Sân trước: Ô tô SUV chi tiết (bánh xe, mâm, kính, đèn, gương), Hiên trà của Ba
     (pergola gỗ, bàn đá nguyên khối, 4 ghế gỗ tựa lưng, bộ ấm chén trà, đèn lồng).
   - Hành lang 2m bên hông: Xe tay ga dựng gọn gàng, đá bước dạo, khóm trúc & hoa.
   - Phòng khách: Sofa chữ L bọc nỉ bouclé có đệm rời, 6 gối tựa, thảm dệt, bàn trà đôi
     mặt đá cẩm thạch + gỗ sồi, bình hoa, sách, vách tivi lam gỗ sóng + đá marble hắt LED,
     kệ tivi, màn hình OLED 65", loa soundbar, đèn chùm vòng LED, cây Bàng Singapore.
   - Gian thờ Phật Quan Âm & Gia tiên: Vách ngăn CNC hoa sen, bàn thờ gỗ óc chó 2 cấp
     chạm khắc, tượng Quan Âm trên đài sen vàng có hào quang, đèn sen, bình hoa sen,
     bài vị, bát hương đồng, chân nến, mâm ngũ quả, bồ đoàn tụng kinh.
   - Cầu thang & Giếng trời: 19 bậc gỗ sồi, lan can kính tay vịn gỗ, tiểu cảnh khô gầm
     cầu thang (sỏi trắng, đá bước dạo, bonsai, đèn đá Nhật, tủ âm gầm thang).
   - Phòng ngủ Ba Mẹ: Giường Queen bọc đầu giường êm ái, chăn ga gối đa lớp, 2 tab đầu
     giường + đèn ngủ, tủ quần áo kịch trần 3 cánh, ghế bành đọc sách cạnh cửa sổ lớn.
   - Phòng Đọc sách, Kỷ vật & Tiếp khách: Hệ kệ sách kịch trần 5 khoang với hơn 60 cuốn
     sách đủ màu & kỷ vật trưng bày, giường daybed có gối ôm, bàn làm việc, laptop, đèn bàn.
   - Bếp mở & Quầy đảo làm bánh: Tủ bếp chữ L trên/dưới, bếp từ, nồi chảo, máy hút mùi,
     chậu rửa 2 hố + vòi cổ ngỗng, tủ lạnh 2 cánh lớn, lò nướng âm tủ. Quầy đảo đá trắng
     có máy nhào bột KitchenAid, thớt gỗ, cây lăn bột, khay bánh croissant, lồng kính bánh kem,
     2 ghế bar. Bàn ăn gỗ sồi 6 ghế tựa + bộ bát đĩa & đèn thả trần.
   - Sân sau: WC tầng trệt (vách tắm kính, sen cây, bồn cầu, lavabo, gương LED), khu giặt
     phơi mái kính (máy giặt cửa trước), vườn rau hữu cơ 3 luống (bắp cải, cà chua, rau thơm)
     và cây ăn quả trĩu quả.
2. Tầng 2 (Lầu 1):
   - Ban công ngắm sao: Lan can kính đồng, hệ lam gỗ chắn nắng hướng Tây, 2 ghế mây thư
     giãn, bàn trà, đàn Guitar Acoustic trên giá đỡ, bồn hoa dạ yến thảo.
   - Phòng Master: Đàn Piano Upright đen bóng (đầy đủ 52 phím trắng, 36 phím đen, 3 pedal
     đồng, giá nhạc & bản nhạc, ghế đàn), góc tập Yoga & Thiền định (thảm yoga, đệm thiền
     Zafu, chuông xoay Tây Tạng, gương vòm toàn thân, cây Monstera), giường King size sang
     trọng, tủ áo cánh kính đèn LED có quần áo treo bên trong, bàn trang điểm gương LED,
     WC khép kín có bồn tắm nằm độc lập, buồng tắm kính, lavabo, gương LED.
   - Phòng ngủ Chị Hai & Phòng ngủ Em Út: Đầy đủ giường, chăn ga gối, tủ áo kịch trần,
     bàn học/trang điểm, kệ sách, ghế, rèm cửa sổ mở ra đường luồng 2m.
   - Ban công sau: Khu tập Gym (máy chạy bộ, ghế tập tạ, kệ tạ tay) & Giàn phơi thông minh
     nâng hạ có quần áo treo, hệ khung lưới an toàn cáp inox.
3. Tầng Mái:
   - Tum kính giếng trời thông gió, bồn nước Inox 1500L trên giá đỡ, máy nước nóng năng
     lượng mặt trời Thái Dương Năng 16 ống chân không, 6 tấm pin mặt trời Solar PV.
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

clear_scene()

def get_or_create_col(name, parent=None):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
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
col_enclosure = get_or_create_col("08_Left_Cutaway_Walls_Full", col_main)

# ---------------------------------------------------------------------------
# 2. PBR MATERIALS (WORKS IN BOTH SOLID MODE AND MATERIAL PREVIEW / RENDERED)
# ---------------------------------------------------------------------------
materials = {}

def create_mat(name, color_rgba, roughness=0.5, metallic=0.0, transmission=0.0, emission_rgba=None, emission_strength=1.0):
    mat = bpy.data.materials.new(name=name)
    # Set viewport solid-mode display properties so even Solid mode shows rich colors!
    mat.diffuse_color = color_rgba
    mat.roughness = roughness
    mat.metallic = metallic

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
        if emission_rgba:
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = emission_rgba
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = emission_rgba
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
    if transmission > 0.1:
        alpha = max(0.15, 1.0 - transmission * 0.88)
        mat.diffuse_color = (color_rgba[0], color_rgba[1], color_rgba[2], alpha)
        if bsdf and "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        if hasattr(mat, "surface_render_method"):
            try:
                mat.surface_render_method = 'BLENDED'
            except Exception:
                pass
        if hasattr(mat, "blend_method"):
            try:
                mat.blend_method = 'BLEND'
            except Exception:
                pass
    materials[name] = mat
    return mat

# Architectural & Surface Materials
create_mat("Mat_WallWarmWhite", (0.96, 0.94, 0.90, 1.0), roughness=0.75)
create_mat("Mat_WallFacadeWarm", (0.86, 0.82, 0.76, 1.0), roughness=0.6)
create_mat("Mat_DarkGreyStone", (0.20, 0.22, 0.25, 1.0), roughness=0.45, metallic=0.05)
create_mat("Mat_RoadAsphalt", (0.14, 0.15, 0.17, 1.0), roughness=0.85)
create_mat("Mat_FloorTileCream", (0.93, 0.90, 0.85, 1.0), roughness=0.22)
create_mat("Mat_AntiSlipWoodTile", (0.68, 0.50, 0.34, 1.0), roughness=0.38)
create_mat("Mat_AntiSlipTileGrey", (0.38, 0.40, 0.43, 1.0), roughness=0.65)
create_mat("Mat_AntiSlipPavers", (0.52, 0.50, 0.48, 1.0), roughness=0.8)
create_mat("Mat_WhitePebbles", (0.90, 0.89, 0.86, 1.0), roughness=0.7)
create_mat("Mat_SoilDark", (0.24, 0.16, 0.11, 1.0), roughness=0.95)

# Nature & Landscape Materials
create_mat("Mat_GrassGreen", (0.20, 0.52, 0.22, 1.0), roughness=0.88)
create_mat("Mat_FoliageGreen", (0.16, 0.58, 0.20, 1.0), roughness=0.6)
create_mat("Mat_FoliageDark", (0.09, 0.40, 0.14, 1.0), roughness=0.65)
create_mat("Mat_FoliageLime", (0.32, 0.68, 0.22, 1.0), roughness=0.55)
create_mat("Mat_TreeTrunk", (0.35, 0.23, 0.15, 1.0), roughness=0.85)
create_mat("Mat_FlowerPink", (0.92, 0.26, 0.48, 1.0), roughness=0.5)
create_mat("Mat_FlowerYellow", (0.96, 0.76, 0.15, 1.0), roughness=0.5)
create_mat("Mat_FruitOrange", (0.95, 0.45, 0.10, 1.0), roughness=0.35)
create_mat("Mat_TomatoRed", (0.88, 0.15, 0.15, 1.0), roughness=0.3)

# Wood & Stone Furniture Materials
create_mat("Mat_WhiteMarble", (0.96, 0.97, 0.98, 1.0), roughness=0.12)
create_mat("Mat_BlackGranite", (0.08, 0.09, 0.10, 1.0), roughness=0.15)
create_mat("Mat_WoodOakTable", (0.68, 0.47, 0.29, 1.0), roughness=0.32)
create_mat("Mat_WoodOakCabinet", (0.73, 0.53, 0.35, 1.0), roughness=0.36)
create_mat("Mat_WoodOakDark", (0.28, 0.17, 0.10, 1.0), roughness=0.35)
create_mat("Mat_WoodWalnutAltar", (0.24, 0.13, 0.08, 1.0), roughness=0.3)
create_mat("Mat_WoodLouverFacade", (0.64, 0.43, 0.25, 1.0), roughness=0.38)
create_mat("Mat_WoodStairTreads", (0.62, 0.42, 0.25, 1.0), roughness=0.32)
create_mat("Mat_RattanWeave", (0.76, 0.60, 0.40, 1.0), roughness=0.65)
create_mat("Mat_PlanterWood", (0.46, 0.30, 0.18, 1.0), roughness=0.55)

# Fabrics, Cushions & Soft Furnishings
create_mat("Mat_FabricSofaWarm", (0.84, 0.80, 0.74, 1.0), roughness=0.85)
create_mat("Mat_FabricTaupe", (0.62, 0.57, 0.52, 1.0), roughness=0.85)
create_mat("Mat_CushionMustard", (0.88, 0.64, 0.20, 1.0), roughness=0.8)
create_mat("Mat_CushionTerracotta", (0.78, 0.36, 0.26, 1.0), roughness=0.8)
create_mat("Mat_CushionSage", (0.48, 0.62, 0.52, 1.0), roughness=0.8)
create_mat("Mat_CushionNavy", (0.16, 0.26, 0.42, 1.0), roughness=0.8)
create_mat("Mat_CushionRose", (0.82, 0.52, 0.56, 1.0), roughness=0.8)
create_mat("Mat_BeddingWhite", (0.96, 0.95, 0.93, 1.0), roughness=0.78)
create_mat("Mat_BeddingCream", (0.90, 0.86, 0.79, 1.0), roughness=0.82)
create_mat("Mat_RugWoven", (0.78, 0.73, 0.65, 1.0), roughness=0.92)
create_mat("Mat_CurtainSheer", (0.96, 0.95, 0.92, 0.65), roughness=0.6, transmission=0.45)
create_mat("Mat_CurtainDrape", (0.72, 0.66, 0.58, 1.0), roughness=0.85)
create_mat("Mat_YogaMatPastel", (0.68, 0.54, 0.82, 1.0), roughness=0.75)

# Metals, Glass, Electronics & Accents
create_mat("Mat_BuddhaGold", (0.96, 0.78, 0.20, 1.0), roughness=0.18, metallic=0.92)
create_mat("Mat_BrassWarm", (0.85, 0.68, 0.32, 1.0), roughness=0.25, metallic=0.88)
create_mat("Mat_BronzeGateMetal", (0.32, 0.24, 0.18, 1.0), roughness=0.3, metallic=0.82)
create_mat("Mat_MetalMatteBlack", (0.10, 0.11, 0.13, 1.0), roughness=0.35, metallic=0.75)
create_mat("Mat_MetalStainless", (0.88, 0.90, 0.93, 1.0), roughness=0.22, metallic=0.45)
create_mat("Mat_CeramicWhite", (0.97, 0.98, 0.99, 1.0), roughness=0.08)
create_mat("Mat_GlassClear", (0.82, 0.92, 0.97, 0.32), roughness=0.04, transmission=0.88)
create_mat("Mat_BalconyGlassBronze", (0.55, 0.68, 0.74, 0.45), roughness=0.08, transmission=0.78)
create_mat("Mat_MirrorSilver", (0.92, 0.95, 0.97, 1.0), roughness=0.02, metallic=0.98)
create_mat("Mat_PianoBlackGloss", (0.02, 0.02, 0.03, 1.0), roughness=0.04, metallic=0.25)
create_mat("Mat_TVScreenBlack", (0.04, 0.05, 0.08, 1.0), roughness=0.08, metallic=0.4)
create_mat("Mat_WarmLED", (1.0, 0.88, 0.62, 1.0), roughness=0.2, emission_rgba=(1.0, 0.85, 0.55, 1.0), emission_strength=3.5)
create_mat("Mat_SolarPVPanels", (0.08, 0.14, 0.28, 1.0), roughness=0.18, metallic=0.75)
create_mat("Mat_CarBlue", (0.14, 0.34, 0.72, 1.0), roughness=0.18, metallic=0.85)
create_mat("Mat_TireRubber", (0.12, 0.12, 0.13, 1.0), roughness=0.85)
create_mat("Mat_CroissantGold", (0.82, 0.54, 0.22, 1.0), roughness=0.55)
create_mat("Mat_MixerPastelPink", (0.92, 0.68, 0.72, 1.0), roughness=0.2, metallic=0.3)

# Book colors for libraries
book_mats = [
    create_mat("Mat_BookRed", (0.72, 0.20, 0.18, 1.0), roughness=0.6),
    create_mat("Mat_BookBlue", (0.18, 0.36, 0.62, 1.0), roughness=0.6),
    create_mat("Mat_BookGreen", (0.18, 0.46, 0.32, 1.0), roughness=0.6),
    create_mat("Mat_BookOchre", (0.82, 0.58, 0.20, 1.0), roughness=0.6),
    create_mat("Mat_BookCream", (0.88, 0.84, 0.76, 1.0), roughness=0.6),
    create_mat("Mat_BookPlum", (0.45, 0.22, 0.42, 1.0), roughness=0.6),
]

# ---------------------------------------------------------------------------
# 3. FAST BMesh GEOMETRY BUILDERS (NO SLOW OPS CALLS!)
# ---------------------------------------------------------------------------
def link_mesh_obj(collection, name, bm, mat_name, loc=(0, 0, 0), rot=(0, 0, 0), smooth=False):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    if smooth:
        for poly in mesh.polygons:
            poly.use_smooth = True
    obj = bpy.data.objects.new(name, mesh)
    obj.location = loc
    obj.rotation_euler = rot
    collection.objects.link(obj)
    if mat_name and mat_name in materials:
        mesh.materials.append(materials[mat_name])
    return obj

def add_box(collection, name, min_x, min_y, min_z, max_x, max_y, max_z, mat_name=None, bevel=0.0, rot_z=0.0):
    dx = max(0.002, abs(max_x - min_x))
    dy = max(0.002, abs(max_y - min_y))
    dz = max(0.002, abs(max_z - min_z))
    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0
    cz = (min_z + max_z) / 2.0

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(dx, dy, dz), verts=bm.verts)
    if bevel > 0.0:
        b = min(bevel, min(dx, dy, dz) * 0.35)
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=b, segments=2, profile=0.5, affect='EDGES')
    return link_mesh_obj(collection, name, bm, mat_name, loc=(cx, cy, cz), rot=(0, 0, rot_z), smooth=(bevel > 0.0))

def add_cyl(collection, name, cx, cy, z_bottom, z_top, r1, r2=None, mat_name=None, segs=20, rot=(0, 0, 0), smooth=True):
    if r2 is None:
        r2 = r1
    dz = abs(z_top - z_bottom)
    cz = (z_bottom + z_top) / 2.0
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r1, radius2=r2, depth=dz)
    return link_mesh_obj(collection, name, bm, mat_name, loc=(cx, cy, cz), rot=rot, smooth=smooth)

def add_sphere(collection, name, cx, cy, cz, rx, ry=None, rz=None, mat_name=None, subdiv=2, smooth=True):
    if ry is None:
        ry = rx
    if rz is None:
        rz = rx
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    bmesh.ops.scale(bm, vec=(rx, ry, rz), verts=bm.verts)
    return link_mesh_obj(collection, name, bm, mat_name, loc=(cx, cy, cz), smooth=smooth)

# Wall with rectangular cutouts (doors / windows)
def add_wall_with_openings(collection, name, axis, fixed_coord, thickness, start_u, end_u, z_bot, z_top, openings, mat_name="Mat_WallWarmWhite"):
    """
    axis='X': wall runs along X from start_u..end_u at Y = fixed_coord..fixed_coord+thickness
    axis='Y': wall runs along Y from start_u..end_u at X = fixed_coord..fixed_coord+thickness
    openings: list of (u1, u2, oz1, oz2) sorted by u1
    """
    if not openings:
        if axis == 'X':
            add_box(collection, name, start_u, fixed_coord, z_bot, end_u, fixed_coord + thickness, z_top, mat_name)
        else:
            add_box(collection, name, fixed_coord, start_u, z_bot, fixed_coord + thickness, end_u, z_top, mat_name)
        return

    openings_sorted = sorted(openings, key=lambda o: o[0])
    cur_u = start_u
    idx = 0
    for (u1, u2, oz1, oz2) in openings_sorted:
        if u1 > cur_u + 0.01:
            if axis == 'X':
                add_box(collection, f"{name}_seg_{idx}", cur_u, fixed_coord, z_bot, u1, fixed_coord + thickness, z_top, mat_name)
            else:
                add_box(collection, f"{name}_seg_{idx}", fixed_coord, cur_u, z_bot, fixed_coord + thickness, u1, z_top, mat_name)
            idx += 1
        # Sill below opening
        if oz1 > z_bot + 0.01:
            if axis == 'X':
                add_box(collection, f"{name}_sill_{idx}", u1, fixed_coord, z_bot, u2, fixed_coord + thickness, oz1, mat_name)
            else:
                add_box(collection, f"{name}_sill_{idx}", fixed_coord, u1, z_bot, fixed_coord + thickness, u2, oz1, mat_name)
        # Header above opening
        if oz2 < z_top - 0.01:
            if axis == 'X':
                add_box(collection, f"{name}_head_{idx}", u1, fixed_coord, oz2, u2, fixed_coord + thickness, z_top, mat_name)
            else:
                add_box(collection, f"{name}_head_{idx}", fixed_coord, u1, oz2, fixed_coord + thickness, u2, z_top, mat_name)
        cur_u = u2
        idx += 1

    if cur_u < end_u - 0.01:
        if axis == 'X':
            add_box(collection, f"{name}_seg_{idx}", cur_u, fixed_coord, z_bot, end_u, fixed_coord + thickness, z_top, mat_name)
        else:
            add_box(collection, f"{name}_seg_{idx}", fixed_coord, cur_u, z_bot, fixed_coord + thickness, end_u, z_top, mat_name)

def add_framed_window(collection, name, axis, fixed_coord, thickness, u1, u2, z1, z2, with_curtains=False, curtain_side=-1):
    """Creates aluminum window frame, mullions, glass panes, and optional interior curtains."""
    ft = 0.045
    mid_u = (u1 + u2) / 2.0
    if axis == 'Y':
        # Window on a Y-running wall (at X = fixed_coord..fixed_coord+thickness)
        cx = fixed_coord + thickness / 2.0
        add_box(collection, f"{name}_FrameBot", fixed_coord - 0.01, u1, z1, fixed_coord + thickness + 0.01, u2, z1 + ft, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameTop", fixed_coord - 0.01, u1, z2 - ft, fixed_coord + thickness + 0.01, u2, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameL", fixed_coord - 0.01, u1, z1, fixed_coord + thickness + 0.01, u1 + ft, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameR", fixed_coord - 0.01, u2 - ft, z1, fixed_coord + thickness + 0.01, u2, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_Mullion", cx - 0.015, mid_u - 0.02, z1 + ft, cx + 0.015, mid_u + 0.02, z2 - ft, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_Glass", cx - 0.008, u1 + ft, z1 + ft, cx + 0.008, u2 - ft, z2 - ft, "Mat_GlassClear")
        if with_curtains:
            cur_x = fixed_coord - 0.08 if curtain_side < 0 else fixed_coord + thickness + 0.08
            # Curtain rod
            add_cyl(collection, f"{name}_Rod", cur_x, (u1 + u2) / 2.0, z2 + 0.08, z2 + 0.10, 0.015, mat_name="Mat_MetalMatteBlack", rot=(math.pi / 2, 0, 0))
            # Left & Right pleated drapes
            for side_i, sy in enumerate([u1 + 0.18, u2 - 0.18]):
                for p in range(5):
                    py = sy + (p - 2) * 0.055
                    add_box(collection, f"{name}_Drape_{side_i}_{p}", cur_x - 0.04, py - 0.022, z1 - 0.25, cur_x + 0.04, py + 0.022, z2 + 0.07, "Mat_CurtainDrape", bevel=0.01)
            add_box(collection, f"{name}_Sheer", cur_x - 0.01, u1 + 0.32, z1 - 0.15, cur_x + 0.01, u2 - 0.32, z2 + 0.05, "Mat_CurtainSheer")
    else:
        # Window on an X-running wall (at Y = fixed_coord..fixed_coord+thickness)
        cy = fixed_coord + thickness / 2.0
        add_box(collection, f"{name}_FrameBot", u1, fixed_coord - 0.01, z1, u2, fixed_coord + thickness + 0.01, z1 + ft, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameTop", u1, fixed_coord - 0.01, z2 - ft, u2, fixed_coord + thickness + 0.01, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameL", u1, fixed_coord - 0.01, z1, u1 + ft, fixed_coord + thickness + 0.01, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_FrameR", u2 - ft, fixed_coord - 0.01, z1, u2, fixed_coord + thickness + 0.01, z2, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_Mullion", mid_u - 0.02, cy - 0.015, z1 + ft, mid_u + 0.02, cy + 0.015, z2 - ft, "Mat_MetalMatteBlack")
        add_box(collection, f"{name}_Glass", u1 + ft, cy - 0.008, z1 + ft, u2 - ft, cy + 0.008, z2 - ft, "Mat_GlassClear")

def add_interior_door(collection, name, axis, fixed_coord, thickness, u1, u2, z1, z2, open_angle=0.35):
    """Adds wooden door frame, paneled door leaf (slightly ajar), and brass lever handles."""
    ft = 0.04
    if axis == 'Y':
        add_box(collection, f"{name}_JambL", fixed_coord - 0.01, u1, z1, fixed_coord + thickness + 0.01, u1 + ft, z2, "Mat_WoodOakDark")
        add_box(collection, f"{name}_JambR", fixed_coord - 0.01, u2 - ft, z1, fixed_coord + thickness + 0.01, u2, z2, "Mat_WoodOakDark")
        add_box(collection, f"{name}_Header", fixed_coord - 0.01, u1, z2 - ft, fixed_coord + thickness + 0.01, u2, z2, "Mat_WoodOakDark")
        dw = (u2 - u1) - 2 * ft
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
# 4. REUSABLE ULTRA-DETAILED FURNITURE & LANDSCAPE BUILDERS
# ---------------------------------------------------------------------------
def build_tree(collection, name, x, y, z, scale=1.0, with_fruit=False):
    # Main trunk + 3 organic branches
    add_cyl(collection, f"{name}_Trunk", x, y, z, z + 1.8 * scale, 0.14 * scale, 0.09 * scale, "Mat_TreeTrunk")
    branches = [
        (0.25 * scale, 0.15 * scale, 0.35, -0.2),
        (-0.22 * scale, 0.18 * scale, -0.3, 0.25),
        (0.05 * scale, -0.25 * scale, 0.1, 0.35),
    ]
    for idx, (bx, by, rx, ry) in enumerate(branches):
        add_cyl(collection, f"{name}_Branch_{idx}", x + bx * 0.5, y + by * 0.5, z + 1.5 * scale, z + 2.5 * scale, 0.07 * scale, 0.03 * scale, "Mat_TreeTrunk", rot=(rx, ry, 0))

    # Multi-layered foliage canopy
    canopy_blobs = [
        (0.0, 0.0, 2.7, 1.05, 1.0, 0.85, "Mat_FoliageGreen"),
        (0.55, 0.35, 2.5, 0.80, 0.75, 0.68, "Mat_FoliageDark"),
        (-0.50, 0.30, 2.6, 0.82, 0.78, 0.70, "Mat_FoliageLime"),
        (0.20, -0.50, 2.5, 0.78, 0.80, 0.65, "Mat_FoliageGreen"),
        (-0.25, -0.35, 3.1, 0.75, 0.72, 0.65, "Mat_FoliageDark"),
        (0.30, 0.15, 3.25, 0.68, 0.65, 0.60, "Mat_FoliageLime"),
    ]
    for i, (ox, oy, oz, rx, ry, rz, m) in enumerate(canopy_blobs):
        add_sphere(collection, f"{name}_Canopy_{i}", x + ox * scale, y + oy * scale, z + oz * scale, rx * scale, ry * scale, rz * scale, m, subdiv=2)

    if with_fruit:
        fruits = [(0.5, 0.4, 2.3), (-0.45, 0.25, 2.35), (0.2, -0.5, 2.25), (-0.3, -0.35, 2.5), (0.6, -0.1, 2.4), (0.0, 0.6, 2.4)]
        for fi, (fx, fy, fz) in enumerate(fruits):
            add_sphere(collection, f"{name}_Fruit_{fi}", x + fx * scale, y + fy * scale, z + fz * scale, 0.08 * scale, 0.08 * scale, 0.09 * scale, "Mat_FruitOrange", subdiv=1)

def build_potted_plant(collection, name, x, y, z, scale=1.0, style="monstera"):
    # Ceramic pot with rim & soil
    add_cyl(collection, f"{name}_Pot", x, y, z, z + 0.36 * scale, 0.15 * scale, 0.19 * scale, "Mat_CeramicWhite")
    add_cyl(collection, f"{name}_Soil", x, y, z + 0.33 * scale, z + 0.35 * scale, 0.17 * scale, 0.17 * scale, "Mat_SoilDark")
    # Stems & leaves fanning out
    angles = [0, 1.05, 2.1, 3.15, 4.2, 5.25]
    for i, ang in enumerate(angles):
        lx = x + math.cos(ang) * 0.16 * scale
        ly = y + math.sin(ang) * 0.16 * scale
        lz = z + (0.55 + (i % 3) * 0.12) * scale
        add_cyl(collection, f"{name}_Stem_{i}", (x + lx) / 2, (y + ly) / 2, z + 0.34 * scale, lz, 0.012 * scale, 0.008 * scale, "Mat_FoliageDark")
        add_sphere(collection, f"{name}_Leaf_{i}", lx, ly, lz, 0.14 * scale, 0.09 * scale, 0.03 * scale, "Mat_FoliageGreen" if i % 2 == 0 else "Mat_FoliageLime", subdiv=1)

def build_detailed_bed(collection, name, cx, cy, z, width=1.8, length=2.0, facing="+X", duvet_mat="Mat_BeddingCream", accent_mat="Mat_CushionNavy"):
    """
    Builds a realistic luxury bed: wooden platform frame, legs, upholstered channel headboard,
    thick beveled mattress, fitted sheet, folded duvet, textured throw blanket, and 4 pillows + 2 accent cushions.
    facing="+X" means headboard is at min_x and bed extends toward +X.
    facing="-Y" means headboard is at max_y and bed extends toward -Y.
    """
    if facing == "+X":
        x0 = cx - length / 2.0
        x1 = cx + length / 2.0
        y0 = cy - width / 2.0
        y1 = cy + width / 2.0
        # Wooden bed base & 4 solid legs
        add_box(collection, f"{name}_Frame", x0, y0, z + 0.08, x1, y1, z + 0.28, "Mat_WoodOakTable", bevel=0.015)
        for lx in [x0 + 0.08, x1 - 0.08]:
            for ly in [y0 + 0.08, y1 - 0.08]:
                add_cyl(collection, f"{name}_Leg_{lx:.1f}_{ly:.1f}", lx, ly, z, z + 0.08, 0.03, 0.02, "Mat_WoodOakDark")
        # Channel-tufted Headboard
        add_box(collection, f"{name}_HeadboardBoard", x0 - 0.02, y0 - 0.08, z, x0 + 0.06, y1 + 0.08, z + 1.18, "Mat_WoodOakTable", bevel=0.015)
        num_channels = 6
        ch_w = (width - 0.08) / num_channels
        for c in range(num_channels):
            cy_c = y0 + 0.04 + c * ch_w
            add_box(collection, f"{name}_HeadPad_{c}", x0 + 0.05, cy_c + 0.005, z + 0.30, x0 + 0.13, cy_c + ch_w - 0.005, z + 1.10, "Mat_FabricSofaWarm", bevel=0.025)
        # Beveled Mattress
        add_box(collection, f"{name}_Mattress", x0 + 0.10, y0 + 0.04, z + 0.28, x1 - 0.04, y1 - 0.04, z + 0.54, "Mat_BeddingWhite", bevel=0.04)
        # Fluffy Duvet Cover
        add_box(collection, f"{name}_Duvet", x0 + 0.52, y0 + 0.02, z + 0.32, x1 - 0.02, y1 - 0.02, z + 0.58, duvet_mat, bevel=0.05)
        # Folded Top Sheet Edge
        add_box(collection, f"{name}_SheetFold", x0 + 0.44, y0 + 0.03, z + 0.54, x0 + 0.62, y1 - 0.03, z + 0.59, "Mat_BeddingWhite", bevel=0.02)
        # Accent Throw Runner at foot of bed
        add_box(collection, f"{name}_Runner", x1 - 0.52, y0 + 0.01, z + 0.34, x1 - 0.08, y1 - 0.01, z + 0.60, accent_mat, bevel=0.025)
        # 4 Sleeping Pillows + 2 Accent Cushions
        pw = (width - 0.24) / 2.0
        for pi in range(2):
            py_center = y0 + 0.12 + pw / 2.0 + pi * (pw + 0.04)
            add_box(collection, f"{name}_PillowBack_{pi}", x0 + 0.14, py_center - pw * 0.44, z + 0.54, x0 + 0.36, py_center + pw * 0.44, z + 0.72, "Mat_BeddingWhite", bevel=0.05)
            add_box(collection, f"{name}_PillowFront_{pi}", x0 + 0.28, py_center - pw * 0.40, z + 0.54, x0 + 0.48, py_center + pw * 0.40, z + 0.70, duvet_mat, bevel=0.05)
            add_box(collection, f"{name}_AccentCush_{pi}", x0 + 0.42, py_center - 0.18, z + 0.55, x0 + 0.56, py_center + 0.18, z + 0.74, accent_mat, bevel=0.04)
    else:
        # Bed oriented along Y (headboard at y0, foot at y1)
        x0 = cx - width / 2.0
        x1 = cx + width / 2.0
        y0 = cy - length / 2.0
        y1 = cy + length / 2.0
        add_box(collection, f"{name}_Frame", x0, y0, z + 0.08, x1, y1, z + 0.28, "Mat_WoodOakTable", bevel=0.015)
        add_box(collection, f"{name}_HeadboardBoard", x0 - 0.06, y0 - 0.02, z, x1 + 0.06, y0 + 0.06, z + 1.15, "Mat_WoodOakTable", bevel=0.015)
        num_channels = 6
        ch_w = (width - 0.08) / num_channels
        for c in range(num_channels):
            cx_c = x0 + 0.04 + c * ch_w
            add_box(collection, f"{name}_HeadPad_{c}", cx_c + 0.005, y0 + 0.05, z + 0.30, cx_c + ch_w - 0.005, y0 + 0.13, z + 1.08, "Mat_FabricSofaWarm", bevel=0.025)
        add_box(collection, f"{name}_Mattress", x0 + 0.04, y0 + 0.10, z + 0.28, x1 - 0.04, y1 - 0.04, z + 0.54, "Mat_BeddingWhite", bevel=0.04)
        add_box(collection, f"{name}_Duvet", x0 + 0.02, y0 + 0.52, z + 0.32, x1 - 0.02, y1 - 0.02, z + 0.58, duvet_mat, bevel=0.05)
        add_box(collection, f"{name}_Runner", x0 + 0.01, y1 - 0.52, z + 0.34, x1 - 0.01, y1 - 0.08, z + 0.60, accent_mat, bevel=0.025)
        pw = (width - 0.24) / 2.0
        for pi in range(2):
            px_center = x0 + 0.12 + pw / 2.0 + pi * (pw + 0.04)
            add_box(collection, f"{name}_PillowBack_{pi}", px_center - pw * 0.44, y0 + 0.14, z + 0.54, px_center + pw * 0.44, y0 + 0.36, z + 0.72, "Mat_BeddingWhite", bevel=0.05)
            add_box(collection, f"{name}_PillowFront_{pi}", px_center - pw * 0.40, y0 + 0.28, z + 0.54, px_center + pw * 0.40, y0 + 0.48, z + 0.70, duvet_mat, bevel=0.05)
            add_box(collection, f"{name}_AccentCush_{pi}", px_center - 0.18, y0 + 0.42, z + 0.55, px_center + 0.18, y0 + 0.56, z + 0.74, accent_mat, bevel=0.04)

def build_nightstand_with_lamp(collection, name, cx, cy, z):
    add_box(collection, f"{name}_Body", cx - 0.24, cy - 0.22, z + 0.12, cx + 0.24, cy + 0.22, z + 0.52, "Mat_WoodOakCabinet", bevel=0.01)
    add_box(collection, f"{name}_Drawer1", cx - 0.22, cy - 0.23, z + 0.33, cx + 0.22, cy + 0.23, z + 0.50, "Mat_WoodOakTable", bevel=0.008)
    add_box(collection, f"{name}_Drawer2", cx - 0.22, cy - 0.23, z + 0.14, cx + 0.22, cy + 0.23, z + 0.31, "Mat_WoodOakTable", bevel=0.008)
    for lx in [cx - 0.19, cx + 0.19]:
        for ly in [cy - 0.17, cy + 0.17]:
            add_cyl(collection, f"{name}_Leg_{lx:.2f}_{ly:.2f}", lx, ly, z, z + 0.12, 0.018, 0.012, "Mat_MetalMatteBlack")
    # Warm Table Lamp
    add_cyl(collection, f"{name}_LampBase", cx, cy, z + 0.52, z + 0.66, 0.07, 0.04, "Mat_CeramicWhite")
    add_cyl(collection, f"{name}_LampStem", cx, cy, z + 0.66, z + 0.76, 0.012, 0.012, "Mat_BrassWarm")
    add_cyl(collection, f"{name}_LampShade", cx, cy, z + 0.72, z + 0.90, 0.13, 0.09, "Mat_WarmLED")

def build_wardrobe(collection, name, min_x, min_y, z, max_x, max_y, height=2.55, glass_doors=False):
    # Main carcass
    add_box(collection, f"{name}_Carcass", min_x, min_y, z, max_x, max_y, z + height, "Mat_WoodOakCabinet", bevel=0.01)
    dx = max_x - min_x
    dy = max_y - min_y
    along_y = dy > dx
    num_doors = max(2, int(round((dy if along_y else dx) / 0.55)))
    if along_y:
        dw = (dy - 0.04) / num_doors
        front_x = max_x if min_x < 2.5 else min_x
        dir_x = 1 if min_x < 2.5 else -1
        for d in range(num_doors):
            y1 = min_y + 0.02 + d * dw
            y2 = y1 + dw - 0.012
            d_mat = "Mat_BalconyGlassBronze" if glass_doors else "Mat_WoodOakTable"
            add_box(collection, f"{name}_Door_{d}", front_x, y1, z + 0.06, front_x + dir_x * 0.025, y2, z + height - 0.04, d_mat, bevel=0.006)
            hy = y2 - 0.05 if d % 2 == 0 else y1 + 0.05
            add_box(collection, f"{name}_Handle_{d}", front_x + dir_x * 0.025, hy - 0.008, z + 0.85, front_x + dir_x * 0.045, hy + 0.008, z + 1.45, "Mat_MetalMatteBlack")
    else:
        dw = (dx - 0.04) / num_doors
        front_y = min_y
        for d in range(num_doors):
            x1 = min_x + 0.02 + d * dw
            x2 = x1 + dw - 0.012
            d_mat = "Mat_BalconyGlassBronze" if glass_doors else "Mat_WoodOakTable"
            add_box(collection, f"{name}_Door_{d}", x1, front_y - 0.025, z + 0.06, x2, front_y, z + height - 0.04, d_mat, bevel=0.006)
            hx = x2 - 0.05 if d % 2 == 0 else x1 + 0.05
            add_box(collection, f"{name}_Handle_{d}", hx - 0.008, front_y - 0.045, z + 0.85, hx + 0.008, front_y - 0.025, z + 1.45, "Mat_MetalMatteBlack")
            if glass_doors:
                # Hanging clothes & LED strip inside glass wardrobe
                add_box(collection, f"{name}_LED_{d}", x1 + 0.02, min_y + 0.05, z + 0.1, x1 + 0.04, min_y + 0.07, z + height - 0.1, "Mat_WarmLED")
                for c in range(4):
                    cx_g = x1 + 0.08 + c * ((dw - 0.16) / 4.0)
                    g_mat = ["Mat_CushionNavy", "Mat_BeddingCream", "Mat_CushionTerracotta", "Mat_CushionSage"][c % 4]
                    add_box(collection, f"{name}_Garment_{d}_{c}", cx_g, min_y + 0.12, z + 0.95, cx_g + 0.045, max_y - 0.12, z + 1.75, g_mat, bevel=0.015)

def build_dining_chair(collection, name, cx, cy, z, rot_z=0.0, seat_mat="Mat_FabricSofaWarm"):
    # Seat cushion & wooden frame
    add_box(collection, f"{name}_SeatFrame", cx - 0.22, cy - 0.22, z + 0.41, cx + 0.22, cy + 0.22, z + 0.45, "Mat_WoodOakTable", bevel=0.01, rot_z=rot_z)
    add_box(collection, f"{name}_SeatPad", cx - 0.20, cy - 0.20, z + 0.45, cx + 0.20, cy + 0.20, z + 0.49, seat_mat, bevel=0.02, rot_z=rot_z)
    # 4 legs
    for dx in [-0.18, 0.18]:
        for dy in [-0.18, 0.18]:
            rx = cx + dx * math.cos(rot_z) - dy * math.sin(rot_z)
            ry = cy + dx * math.sin(rot_z) + dy * math.cos(rot_z)
            add_cyl(collection, f"{name}_Leg_{dx:.2f}_{dy:.2f}", rx, ry, z, z + 0.43, 0.018, 0.013, "Mat_WoodOakTable")
    # Backrest posts & curved top rail (at local -Y)
    for dx in [-0.18, 0.18]:
        dy = -0.19
        rx = cx + dx * math.cos(rot_z) - dy * math.sin(rot_z)
        ry = cy + dx * math.sin(rot_z) + dy * math.cos(rot_z)
        add_cyl(collection, f"{name}_Post_{dx:.2f}", rx, ry, z + 0.43, z + 0.84, 0.016, 0.014, "Mat_WoodOakTable")
    bx = cx - (-0.19) * math.sin(rot_z)
    by = cy + (-0.19) * math.cos(rot_z)
    add_box(collection, f"{name}_BackRail", bx - 0.21, by - 0.025, z + 0.72, bx + 0.21, by + 0.025, z + 0.85, "Mat_WoodOakTable", bevel=0.012, rot_z=rot_z)

def build_desk_and_chair(collection, name, cx, cy, z, width=1.25, depth=0.58, facing="+X"):
    if facing == "+X":
        x0, x1 = cx - depth / 2.0, cx + depth / 2.0
        y0, y1 = cy - width / 2.0, cy + width / 2.0
        add_box(collection, f"{name}_Top", x0, y0, z + 0.72, x1, y1, z + 0.76, "Mat_WoodOakTable", bevel=0.01)
        add_box(collection, f"{name}_DrawerUnit", x0 + 0.03, y0 + 0.03, z + 0.15, x1 - 0.03, y0 + 0.38, z + 0.72, "Mat_WoodOakCabinet", bevel=0.008)
        for ly in [y0 + 0.04, y1 - 0.04]:
            for lx in [x0 + 0.04, x1 - 0.04]:
                add_cyl(collection, f"{name}_Leg_{lx:.2f}_{ly:.2f}", lx, ly, z, z + 0.72, 0.018, 0.014, "Mat_MetalMatteBlack")
        # Laptop on desk
        add_box(collection, f"{name}_LaptopBase", cx - 0.08, cy + 0.05, z + 0.76, cx + 0.14, cy + 0.37, z + 0.775, "Mat_MetalStainless", bevel=0.004)
        add_box(collection, f"{name}_LaptopScreen", cx + 0.12, cy + 0.05, z + 0.775, cx + 0.14, cy + 0.37, z + 0.99, "Mat_TVScreenBlack", bevel=0.004)
        # Desk Lamp
        add_cyl(collection, f"{name}_LampBase", cx + 0.12, y0 + 0.18, z + 0.76, z + 0.78, 0.07, 0.07, "Mat_BrassWarm")
        add_cyl(collection, f"{name}_LampArm", cx + 0.12, y0 + 0.18, z + 0.78, z + 1.12, 0.01, 0.01, "Mat_BrassWarm")
        add_cyl(collection, f"{name}_LampHead", cx + 0.05, y0 + 0.18, z + 1.06, z + 1.15, 0.06, 0.03, "Mat_BrassWarm")
        # Chair tucked in front of desk
        build_dining_chair(collection, f"{name}_Chair", cx - 0.38, cy + 0.15, z, rot_z=-math.pi / 2.0, seat_mat="Mat_CushionSage")

def build_bathroom_fixtures(collection, name, min_x, min_y, z, max_x, max_y, has_bathtub=False):
    # Anti-slip grey floor
    add_box(collection, f"{name}_Floor", min_x, min_y, z, max_x, max_y, z + 0.02, "Mat_AntiSlipTileGrey")
    # 1. Modern One-Piece Ceramic Toilet (at min_x + 0.35, min_y + 0.45)
    tx, ty = min_x + 0.38, min_y + 0.42
    add_cyl(collection, f"{name}_ToiletBase", tx, ty + 0.12, z + 0.02, z + 0.40, 0.17, 0.21, "Mat_CeramicWhite")
    add_box(collection, f"{name}_ToiletSeat", tx - 0.20, ty - 0.05, z + 0.40, tx + 0.20, ty + 0.36, z + 0.45, "Mat_CeramicWhite", bevel=0.04)
    add_box(collection, f"{name}_ToiletTank", tx - 0.20, min_y + 0.04, z + 0.40, tx + 0.20, min_y + 0.22, z + 0.78, "Mat_CeramicWhite", bevel=0.02)
    add_cyl(collection, f"{name}_FlushBtn", tx, min_y + 0.13, z + 0.78, z + 0.795, 0.03, 0.03, "Mat_MetalStainless")

    # 2. Floating Vanity Cabinet, Ceramic Vessel Sink, Faucet & Backlit LED Mirror
    vx0, vx1 = max_x - 0.55, max_x - 0.04
    vy0, vy1 = min_y + 0.15, min_y + 0.85
    add_box(collection, f"{name}_VanityCab", vx0, vy0, z + 0.35, vx1, vy1, z + 0.82, "Mat_WoodOakCabinet", bevel=0.01)
    add_box(collection, f"{name}_VanityTop", vx0 - 0.02, vy0 - 0.02, z + 0.82, vx1 + 0.01, vy1 + 0.02, z + 0.86, "Mat_WhiteMarble", bevel=0.008)
    sx, sy = (vx0 + vx1) / 2.0, (vy0 + vy1) / 2.0
    add_cyl(collection, f"{name}_BasinOuter", sx, sy, z + 0.86, z + 0.98, 0.18, 0.20, "Mat_CeramicWhite")
    add_cyl(collection, f"{name}_FaucetStem", sx + 0.15, sy, z + 0.86, z + 1.06, 0.016, 0.016, "Mat_BrassWarm")
    add_box(collection, f"{name}_FaucetSpout", sx + 0.04, sy - 0.015, z + 1.03, sx + 0.16, sy + 0.015, z + 1.06, "Mat_BrassWarm", bevel=0.005)
    # Glowing LED Mirror
    add_cyl(collection, f"{name}_MirrorGlow", vx1 - 0.02, sy, z + 1.42, z + 1.44, 0.34, 0.34, "Mat_WarmLED", rot=(0, math.pi / 2, 0))
    add_cyl(collection, f"{name}_MirrorGlass", vx1 - 0.03, sy, z + 1.42, z + 1.44, 0.31, 0.31, "Mat_MirrorSilver", rot=(0, math.pi / 2, 0))

    # 3. Walk-in Glass Rain Shower
    sh_x0, sh_x1 = min_x + 0.05, min_x + 0.95
    sh_y0, sh_y1 = max_y - 0.95, max_y - 0.05
    add_box(collection, f"{name}_ShowerGlass", sh_x1 - 0.015, sh_y0, z + 0.02, sh_x1 + 0.015, sh_y1, z + 2.05, "Mat_GlassClear")
    add_box(collection, f"{name}_ShowerFrame", sh_x1 - 0.02, sh_y0, z + 2.03, sh_x1 + 0.02, sh_y1, z + 2.07, "Mat_MetalMatteBlack")
    add_cyl(collection, f"{name}_ShowerPipe", min_x + 0.08, (sh_y0 + sh_y1) / 2.0, z + 1.05, z + 2.10, 0.012, 0.012, "Mat_BrassWarm")
    add_cyl(collection, f"{name}_RainHead", min_x + 0.32, (sh_y0 + sh_y1) / 2.0, z + 2.06, z + 2.08, 0.13, 0.13, "Mat_BrassWarm")

    # 4. Optional Freestanding Sculpted Bathtub (for Master Bathroom)
    if has_bathtub:
        bx, by = (min_x + max_x) / 2.0 + 0.15, max_y - 0.48
        add_box(collection, f"{name}_BathtubOuter", bx - 0.72, by - 0.36, z + 0.02, bx + 0.72, by + 0.36, z + 0.58, "Mat_CeramicWhite", bevel=0.16)
        add_box(collection, f"{name}_BathtubTray", bx - 0.12, by - 0.38, z + 0.57, bx + 0.12, by + 0.38, z + 0.60, "Mat_WoodOakTable", bevel=0.008)
        add_cyl(collection, f"{name}_TubFiller", bx + 0.65, by + 0.32, z + 0.02, z + 0.72, 0.02, 0.02, "Mat_BrassWarm")

def build_upright_piano(collection, name, x, y, z):
    """
    Ultra-detailed Upright Acoustic Piano facing +X (against the wall at x):
    - High-gloss ebony cabinet, toe blocks, front relief panels, top lid
    - Keybed with fallboard
    - 52 individual White Ivory Keys + 36 raised Black Ebony Keys
    - Slanted music stand with sheet music book
    - 3 Gold Pedals
    - Tufted leather Piano Bench + Brass Floor Lamp
    """
    # Main Cabinet Body (x..x+0.42, y-0.74..y+0.74, z..z+1.22)
    add_box(collection, f"{name}_MainCase", x, y - 0.74, z + 0.04, x + 0.38, y + 0.74, z + 1.20, "Mat_PianoBlackGloss", bevel=0.015)
    add_box(collection, f"{name}_TopLid", x - 0.01, y - 0.76, z + 1.20, x + 0.42, y + 0.76, z + 1.24, "Mat_PianoBlackGloss", bevel=0.012)
    # Front Decorative Panel & Brass Trim
    add_box(collection, f"{name}_UpperPanel", x + 0.38, y - 0.66, z + 0.80, x + 0.40, y + 0.66, z + 1.15, "Mat_PianoBlackGloss", bevel=0.008)
    add_box(collection, f"{name}_BrassTrim", x + 0.40, y - 0.62, z + 0.82, x + 0.408, y + 0.62, z + 0.835, "Mat_BuddhaGold")
    # Toe blocks & front support columns
    for side_y in [y - 0.70, y + 0.70]:
        add_box(collection, f"{name}_Toe_{side_y:.2f}", x, side_y - 0.04, z, x + 0.62, side_y + 0.04, z + 0.08, "Mat_PianoBlackGloss", bevel=0.01)
        add_box(collection, f"{name}_LegCol_{side_y:.2f}", x + 0.52, side_y - 0.035, z + 0.08, x + 0.60, side_y + 0.035, z + 0.68, "Mat_PianoBlackGloss", bevel=0.01)
    # Keybed Shelf
    add_box(collection, f"{name}_Keybed", x + 0.36, y - 0.74, z + 0.66, x + 0.64, y + 0.74, z + 0.73, "Mat_PianoBlackGloss", bevel=0.01)
    # 52 White Keys
    key_span = 1.32
    wk_w = key_span / 52.0
    start_ky = y - key_span / 2.0
    for k in range(52):
        ky = start_ky + k * wk_w
        add_box(collection, f"{name}_WKey_{k}", x + 0.41, ky + 0.001, z + 0.73, x + 0.62, ky + wk_w - 0.001, z + 0.755, "Mat_CeramicWhite", bevel=0.002)
    # 36 Black Keys (grouped in 2s and 3s per octave)
    black_pattern = [0, 1, 3, 4, 5]
    bk_idx = 0
    for oct_i in range(7):
        for bp in black_pattern:
            w_idx = oct_i * 7 + bp
            if w_idx < 51:
                ky = start_ky + (w_idx + 0.65) * wk_w
                add_box(collection, f"{name}_BKey_{bk_idx}", x + 0.41, ky, z + 0.75, x + 0.53, ky + wk_w * 0.65, z + 0.775, "Mat_PianoBlackGloss", bevel=0.002)
                bk_idx += 1
    # Music Stand & Sheet Music
    add_box(collection, f"{name}_MusicStand", x + 0.41, y - 0.32, z + 0.83, x + 0.43, y + 0.32, z + 1.04, "Mat_PianoBlackGloss", bevel=0.005)
    add_box(collection, f"{name}_SheetBookL", x + 0.43, y - 0.24, z + 0.84, x + 0.445, y - 0.005, z + 1.02, "Mat_BeddingWhite", bevel=0.003)
    add_box(collection, f"{name}_SheetBookR", x + 0.43, y + 0.005, z + 0.84, x + 0.445, y + 0.24, z + 1.02, "Mat_BeddingWhite", bevel=0.003)
    # 3 Brass Pedals
    for pi, py in enumerate([y - 0.12, y, y + 0.12]):
        add_box(collection, f"{name}_Pedal_{pi}", x + 0.36, py - 0.018, z + 0.04, x + 0.48, py + 0.018, z + 0.07, "Mat_BuddhaGold", bevel=0.005)
    # Tufted Piano Bench
    bx = x + 0.84
    add_box(collection, f"{name}_BenchFrame", bx - 0.18, y - 0.38, z + 0.38, bx + 0.18, y + 0.38, z + 0.44, "Mat_PianoBlackGloss", bevel=0.008)
    add_box(collection, f"{name}_BenchCushion", bx - 0.17, y - 0.37, z + 0.44, bx + 0.17, y + 0.37, z + 0.49, "Mat_WoodOakDark", bevel=0.018)
    for lx in [bx - 0.14, bx + 0.14]:
        for ly in [y - 0.33, y + 0.33]:
            add_cyl(collection, f"{name}_BenchLeg_{lx:.2f}_{ly:.2f}", lx, ly, z, z + 0.38, 0.022, 0.015, "Mat_PianoBlackGloss")

def build_detailed_car(collection, name, cx, cy, z):
    """Builds a sculpted SUV/Crossover with chassis, cabin, hood, 4 wheels + alloy rims, headlights, taillights, mirrors."""
    # Lower Body Chassis
    add_box(collection, f"{name}_LowerBody", cx - 0.88, cy - 2.15, z + 0.28, cx + 0.88, cy + 2.15, z + 0.88, "Mat_CarBlue", bevel=0.08)
    # Upper Greenhouse Cabin
    add_box(collection, f"{name}_Cabin", cx - 0.76, cy - 1.05, z + 0.85, cx + 0.76, cy + 1.45, z + 1.48, "Mat_CarBlue", bevel=0.10)
    # Windshield, Rear Window & Side Windows
    add_box(collection, f"{name}_Windshield", cx - 0.70, cy - 1.07, z + 0.88, cx + 0.70, cy - 0.92, z + 1.42, "Mat_BalconyGlassBronze", bevel=0.02)
    add_box(collection, f"{name}_RearWin", cx - 0.68, cy + 1.35, z + 0.90, cx + 0.68, cy + 1.47, z + 1.40, "Mat_BalconyGlassBronze", bevel=0.02)
    add_box(collection, f"{name}_SideWin", cx - 0.78, cy - 0.85, z + 0.92, cx + 0.78, cy + 1.25, z + 1.38, "Mat_BalconyGlassBronze", bevel=0.02)
    # Front Grille, Bumpers, LED Headlights & Taillights
    add_box(collection, f"{name}_FrontGrille", cx - 0.52, cy - 2.17, z + 0.42, cx + 0.52, cy - 2.12, z + 0.72, "Mat_MetalMatteBlack", bevel=0.02)
    for sx in [cx - 0.68, cx + 0.68]:
        add_box(collection, f"{name}_Headlight_{sx:.2f}", sx - 0.14, cy - 2.17, z + 0.65, sx + 0.14, cy - 2.10, z + 0.78, "Mat_WarmLED", bevel=0.015)
        add_box(collection, f"{name}_Taillight_{sx:.2f}", sx - 0.16, cy + 2.10, z + 0.68, sx + 0.16, cy + 2.17, z + 0.80, "Mat_TomatoRed", bevel=0.015)
        add_box(collection, f"{name}_Mirror_{sx:.2f}", sx + (-0.22 if sx < cx else 0.04), cy - 0.85, z + 0.92, sx + (-0.04 if sx < cx else 0.22), cy - 0.72, z + 1.02, "Mat_CarBlue", bevel=0.02)
    # 4 Wheels with Rubber Tires & Silver Alloy Rims
    for wx in [cx - 0.86, cx + 0.86]:
        for wy in [cy - 1.32, cy + 1.32]:
            add_cyl(collection, f"{name}_Tire_{wx:.2f}_{wy:.2f}", wx, wy, z + 0.34, z + 0.36, 0.34, 0.34, "Mat_TireRubber", rot=(0, math.pi / 2, 0))
            add_BoxWheel(collection, f"{name}_Wheel_{wx:.2f}_{wy:.2f}", wx, wy, z + 0.34)

def add_BoxWheel(collection, name, wx, wy, wz):
    add_cyl(collection, f"{name}_Rubber", wx, wy, wz - 0.11, wz + 0.11, 0.34, 0.34, "Mat_TireRubber", rot=(0, math.pi / 2, 0))
    add_cyl(collection, f"{name}_AlloyRim", wx + (-0.02 if wx < 3.8 else 0.02), wy, wz - 0.115, wz + 0.115, 0.21, 0.21, "Mat_MetalStainless", rot=(0, math.pi / 2, 0))

def build_scooter(collection, name, cx, cy, z):
    """Builds a stylish Vespa-like scooter in the 2m Side Corridor."""
    add_cyl(collection, f"{name}_WheelF", cx, cy - 0.62, z + 0.22, z + 0.24, 0.22, 0.22, "Mat_TireRubber", rot=(0, math.pi / 2, 0))
    add_cyl(collection, f"{name}_WheelR", cx, cy + 0.58, z + 0.22, z + 0.24, 0.22, 0.22, "Mat_TireRubber", rot=(0, math.pi / 2, 0))
    add_box(collection, f"{name}_Floorboard", cx - 0.18, cy - 0.45, z + 0.22, cx + 0.18, cy + 0.25, z + 0.30, "Mat_BeddingCream", bevel=0.03)
    add_box(collection, f"{name}_FrontShield", cx - 0.20, cy - 0.52, z + 0.28, cx + 0.20, cy - 0.36, z + 0.92, "Mat_BeddingCream", bevel=0.04)
    add_box(collection, f"{name}_RearCowls", cx - 0.22, cy + 0.05, z + 0.30, cx + 0.22, cy + 0.68, z + 0.68, "Mat_BeddingCream", bevel=0.08)
    add_box(collection, f"{name}_Seat", cx - 0.16, cy - 0.02, z + 0.66, cx + 0.16, cy + 0.58, z + 0.78, "Mat_WoodOakDark", bevel=0.04)
    add_cyl(collection, f"{name}_Handlebar", cx, cy - 0.44, z + 0.94, z + 0.96, 0.02, 0.02, "Mat_MetalStainless", rot=(0, math.pi / 2, 0))
    add_sphere(collection, f"{name}_Headlamp", cx, cy - 0.48, z + 0.95, 0.07, 0.06, 0.07, "Mat_WarmLED")

# ---------------------------------------------------------------------------
# 5. BUILD SITE, LANDSCAPE, CAR, SCOOTER, PORCH & VEGGIE GARDEN
# ---------------------------------------------------------------------------
# Road, dashed white road stripes & sidewalk
add_box(col_site, "Site_FrontRoad", -4.0, -12.0, -0.35, 11.0, -5.8, -0.20, "Mat_RoadAsphalt")
for stripe in range(5):
    sx = -2.5 + stripe * 3.0
    add_box(col_site, f"Road_Stripe_{stripe}", sx, -9.0, -0.195, sx + 1.4, -8.82, -0.19, "Mat_CeramicWhite")
add_box(col_site, "Site_Sidewalk", -3.0, -5.8, -0.20, 10.0, -5.0, 0.0, "Mat_WallFacadeWarm")

# Yards & Side Corridor (Z = 0.0..0.15)
add_box(col_site, "Site_FrontYard", 0.0, -5.0, 0.0, 7.0, 0.0, 0.15, "Mat_AntiSlipPavers")
# Lawn & Tea Porch moved to Right (X = 2.55..4.95), Car Driveway moved to Left (X = 0.20..2.50)
add_box(col_site, "Site_FrontLawn", 2.55, -4.75, 0.15, 4.95, -0.25, 0.17, "Mat_GrassGreen")
add_box(col_site, "Site_SideCorridor", 5.0, 0.0, 0.0, 7.0, 18.0, 0.15, "Mat_AntiSlipPavers")
add_box(col_site, "Site_SideLawn", 6.35, 0.2, 0.15, 6.92, 17.8, 0.17, "Mat_GrassGreen")
for step_i in range(14):
    sy = 0.6 + step_i * 1.22
    add_box(col_site, f"Side_SteppingStone_{step_i}", 5.35, sy, 0.15, 6.10, sy + 0.65, 0.175, "Mat_WallFacadeWarm", bevel=0.01)
add_box(col_site, "Site_RearPatio", 0.0, 18.0, 0.0, 7.0, 20.0, 0.15, "Mat_AntiSlipPavers")
add_box(col_site, "Site_RearVegGarden", 0.0, 20.0, 0.0, 7.0, 22.8, 0.15, "Mat_GrassGreen")

# Boundary Fences & Gate Pillars
add_box(col_site, "Fence_Left_Base", -0.18, -5.0, 0.0, 0.0, 22.8, 0.55, "Mat_WallWarmWhite")
add_box(col_enclosure, "Fence_Left_Full", -0.18, -5.0, 0.55, 0.0, 22.8, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Right", 7.0, -5.0, 0.0, 7.18, 22.8, 2.35, "Mat_WallWarmWhite")
add_box(col_site, "Fence_Rear", -0.18, 22.8, 0.0, 7.18, 22.98, 2.40, "Mat_WallWarmWhite")

# Gate Pillars & Slatted Bronze Gates (Left: Car Gate, Middle: Porch Fence/Gate, Right: Corridor Gate)
for px1, px2 in [(-0.18, 0.32), (2.42, 2.78), (4.72, 5.06), (6.72, 7.18)]:
    add_box(col_site, f"Gate_Pillar_{px1:.1f}", px1, -5.12, 0.0, px2, -4.82, 2.65, "Mat_DarkGreyStone", bevel=0.01)
    add_box(col_site, f"Gate_Cap_{px1:.1f}", px1 - 0.04, -5.16, 2.65, px2 + 0.04, -4.78, 2.74, "Mat_WallFacadeWarm", bevel=0.01)
    add_sphere(col_site, f"Gate_Lamp_{px1:.1f}", (px1 + px2) / 2.0, -4.97, 2.86, 0.12, 0.12, 0.12, "Mat_WarmLED")

for gx0, gx1, gname in [(0.34, 2.40, "MainCarGate"), (2.80, 4.70, "PorchFrontFence"), (5.08, 6.70, "SideGate")]:
    add_box(col_site, f"{gname}_BotRail", gx0, -5.0, 0.18, gx1, -4.94, 0.26, "Mat_BronzeGateMetal")
    add_box(col_site, f"{gname}_TopRail", gx0, -5.0, 2.22, gx1, -4.94, 2.30, "Mat_BronzeGateMetal")
    num_slats = int((gx1 - gx0) / 0.14)
    for s in range(num_slats):
        sx = gx0 + 0.04 + s * 0.14
        add_box(col_site, f"{gname}_Slat_{s}", sx, -4.99, 0.24, sx + 0.06, -4.95, 2.24, "Mat_BronzeGateMetal")

# Dad's Outdoor Tea & Beer Porch on the RIGHT (X = 2.65..4.88, Y = -3.95..-0.65)
# Sitting on the Living Room Sofa looks straight out through the glass door to this Tea Table!
add_box(col_site, "Porch_Deck", 2.65, -3.95, 0.15, 4.88, -0.65, 0.22, "Mat_AntiSlipWoodTile", bevel=0.01)
for px in [2.72, 4.80]:
    for py in [-3.85, -0.75]:
        add_box(col_site, f"Porch_Post_{px:.1f}_{py:.1f}", px - 0.05, py - 0.05, 0.22, px + 0.05, py + 0.05, 2.75, "Mat_MetalMatteBlack")
for r in range(9):
    ry = -4.0 + r * 0.42
    add_box(col_site, f"Porch_Rafter_{r}", 2.60, ry, 2.75, 4.92, ry + 0.12, 2.85, "Mat_WoodLouverFacade")
add_box(col_site, "Porch_GlassRoof", 2.60, -4.05, 2.85, 4.92, -0.55, 2.89, "Mat_BalconyGlassBronze")
# Granite & Oak Tea Table + 4 Detailed Chairs + Tea Set + Beer Mugs (Centered at X = 3.75, Y = -2.35)
add_box(col_site, "Porch_TableTop", 3.25, -2.95, 0.90, 4.25, -1.75, 0.96, "Mat_WhiteMarble", bevel=0.015)
add_box(col_site, "Porch_TableBase", 3.45, -2.65, 0.22, 4.05, -2.05, 0.90, "Mat_WoodOakDark", bevel=0.01)
build_dining_chair(col_site, "Porch_Chair_L", 2.92, -2.35, 0.22, rot_z=-math.pi / 2.0, seat_mat="Mat_CushionMustard")
build_dining_chair(col_site, "Porch_Chair_R", 4.58, -2.35, 0.22, rot_z=math.pi / 2.0, seat_mat="Mat_CushionMustard")
build_dining_chair(col_site, "Porch_Chair_F", 3.75, -3.32, 0.22, rot_z=math.pi, seat_mat="Mat_CushionMustard")
build_dining_chair(col_site, "Porch_Chair_B", 3.75, -1.38, 0.22, rot_z=0.0, seat_mat="Mat_CushionMustard")
# Tea Tray, Teapot, 4 Teacups & 2 Beer Mugs on Porch Table
add_box(col_site, "Porch_TeaTray", 3.52, -2.55, 0.96, 3.98, -2.15, 0.98, "Mat_WoodOakDark", bevel=0.005)
add_sphere(col_site, "Porch_Teapot", 3.70, -2.35, 1.04, 0.07, 0.07, 0.06, "Mat_CeramicWhite")
for ci, (cx_c, cy_c) in enumerate([(3.58, -2.22), (3.85, -2.22), (3.58, -2.48), (3.85, -2.48)]):
    add_cyl(col_site, f"Porch_Teacup_{ci}", cx_c, cy_c, 0.98, 1.03, 0.025, 0.03, "Mat_CeramicWhite")
add_cyl(col_site, "Porch_Beer1", 3.42, -1.95, 0.96, 1.08, 0.035, 0.038, "Mat_CushionMustard")
add_cyl(col_site, "Porch_Beer2", 4.08, -1.95, 0.96, 1.08, 0.035, 0.038, "Mat_CushionMustard")

# Family Car in LEFT Front Driveway (X = 1.35, Y = -2.55) & Scooter in Side Corridor
build_detailed_car(col_site, "Family_SUV", 1.35, -2.55, 0.15)
build_scooter(col_site, "Corridor_Scooter", 5.75, 2.20, 0.15)

# Rear Organic Vegetable Garden (3 Raised Beds with Cabbages, Tomatoes on Stakes, Herbs)
for r in range(3):
    vy = 20.25 + r * 0.82
    add_box(col_site, f"VegBox_Frame_{r}", 0.45, vy, 0.15, 4.65, vy + 0.58, 0.42, "Mat_PlanterWood", bevel=0.01)
    add_box(col_site, f"VegBox_Soil_{r}", 0.52, vy + 0.06, 0.16, 4.58, vy + 0.52, 0.39, "Mat_SoilDark")
    for vx_i in range(10):
        vx = 0.72 + vx_i * 0.40
        if r == 0:
            # Round green cabbages / lettuce
            add_sphere(col_site, f"Veg_Cabbage_{vx_i}", vx, vy + 0.29, 0.45, 0.13, 0.13, 0.10, "Mat_FoliageLime" if vx_i % 2 == 0 else "Mat_FoliageGreen", subdiv=1)
        elif r == 1:
            # Staked tomato bushes with red tomatoes
            add_cyl(col_site, f"Tomato_Stake_{vx_i}", vx, vy + 0.29, 0.38, 0.85, 0.01, 0.01, "Mat_PlanterWood")
            add_sphere(col_site, f"Tomato_Bush_{vx_i}", vx, vy + 0.29, 0.58, 0.14, 0.14, 0.18, "Mat_FoliageDark", subdiv=1)
            add_sphere(col_site, f"Tomato_FruitA_{vx_i}", vx + 0.08, vy + 0.22, 0.55, 0.035, 0.035, 0.035, "Mat_TomatoRed", subdiv=1)
            add_sphere(col_site, f"Tomato_FruitB_{vx_i}", vx - 0.06, vy + 0.35, 0.64, 0.032, 0.032, 0.032, "Mat_TomatoRed", subdiv=1)
        else:
            # Lush herbs & greens
            add_sphere(col_site, f"Veg_Herb_{vx_i}", vx, vy + 0.20, 0.44, 0.10, 0.10, 0.09, "Mat_FoliageGreen", subdiv=1)
            add_sphere(col_site, f"Veg_Herb2_{vx_i}", vx, vy + 0.38, 0.44, 0.10, 0.10, 0.09, "Mat_FoliageLime", subdiv=1)

# Trees & Flowering Borders
build_tree(col_site, "Tree_FrontShade", 4.55, -4.15, 0.15, scale=1.25, with_fruit=False)
build_tree(col_site, "Tree_RearFruit_Mango", 6.15, 19.3, 0.15, scale=1.15, with_fruit=True)
build_tree(col_site, "Tree_RearFruit_Orange", 6.15, 21.8, 0.15, scale=1.05, with_fruit=True)
for fb_i in range(16):
    fy = 1.0 + fb_i * 1.02
    add_sphere(col_site, f"Corridor_Shrub_{fb_i}", 6.65, fy, 0.32, 0.24, 0.28, 0.20, "Mat_FoliageDark" if fb_i % 2 == 0 else "Mat_FoliageGreen", subdiv=1)
    add_sphere(col_site, f"Corridor_Flower_{fb_i}", 6.58, fy + 0.1, 0.46, 0.07, 0.07, 0.07, "Mat_FlowerPink" if fb_i % 2 == 0 else "Mat_FlowerYellow", subdiv=1)

# ---------------------------------------------------------------------------
# 6. FLOOR 1 ARCHITECTURE (WALLS WITH REAL WINDOW/DOOR OPENINGS)
# ---------------------------------------------------------------------------
Z1 = 0.25  # Floor 1 finished floor level
H1 = 3.60  # Floor 1 ceiling / Floor 2 slab bottom

add_box(col_fl1_arch, "Floor1_Slab", 0.0, 0.0, 0.10, 5.0, 18.0, Z1, "Mat_FloorTileCream")

# Left Wall (Cutaway base at Z1..0.70m in main view so interior is visible + full height in col_enclosure)
add_box(col_fl1_arch, "Floor1_LeftWall_CutawayBase", 0.0, 0.0, Z1, 0.22, 18.0, Z1 + 0.45, "Mat_WallWarmWhite")
add_box(col_enclosure, "Floor1_LeftWall_Full", 0.0, 0.0, Z1 + 0.45, 0.22, 18.0, H1, "Mat_WallWarmWhite")

# Right Exterior Wall (X = 4.78..5.0) with Windows & Side Kitchen Door opening to 2m Corridor
# Note: Y = 3.35..5.00 is solid wall so the Sacred Altar Sanctuary has a solid feng-shui backing ("tọa sơn")!
fl1_right_openings = [
    (0.35, 1.35, 0.85, 2.65),   # Front-right Living Room window looking out to Porch & Corridor
    (8.20, 10.60, 0.95, 2.55),  # Parents' bedroom window
    (11.80, 13.90, 0.95, 2.55), # Reading room window
    (15.20, 16.40, Z1, 2.45),   # Side kitchen glass door to 2m corridor
]
add_wall_with_openings(col_fl1_arch, "Floor1_RightWall", 'Y', 4.78, 0.22, 0.0, 18.0, Z1, H1, fl1_right_openings, "Mat_WallWarmWhite")
add_framed_window(col_fl1_arch, "Win_Fl1_LivingFront", 'Y', 4.78, 0.22, 0.35, 1.35, 0.85, 2.65, with_curtains=False)
add_framed_window(col_fl1_arch, "Win_Fl1_Parents", 'Y', 4.78, 0.22, 8.20, 10.60, 0.95, 2.55, with_curtains=True, curtain_side=-1)
add_framed_window(col_fl1_arch, "Win_Fl1_Reading", 'Y', 4.78, 0.22, 11.80, 13.90, 0.95, 2.55, with_curtains=True, curtain_side=-1)
add_framed_window(col_fl1_arch, "Door_Fl1_KitchenSide", 'Y', 4.78, 0.22, 15.20, 16.40, Z1, 2.45, with_curtains=False)

# Front Facade Wall (Y = 0.0..0.22) with Wide 4-panel Acoustic Entrance Door
add_wall_with_openings(col_fl1_arch, "Floor1_FrontWall", 'X', 0.0, 0.22, 0.0, 5.0, Z1, H1, [(0.65, 4.45, Z1, 2.75)], "Mat_WallFacadeWarm")
add_framed_window(col_fl1_arch, "Entrance_4PanelDoor", 'X', 0.0, 0.22, 0.65, 4.45, Z1, 2.75)
for m_x in [1.60, 2.55, 3.50]:
    add_box(col_fl1_arch, f"Entrance_Mullion_{m_x:.2f}", m_x - 0.02, 0.06, Z1 + 0.04, m_x + 0.02, 0.16, 2.71, "Mat_MetalMatteBlack")
for h_x in [2.47, 2.63]:
    add_box(col_fl1_arch, f"Entrance_Handle_{h_x:.2f}", h_x - 0.01, 0.02, 1.05, h_x + 0.01, 0.20, 1.55, "Mat_BrassWarm")

# Rear Wall (Y = 17.78..18.0) with Kitchen Window & Patio Glass Door
add_wall_with_openings(col_fl1_arch, "Floor1_RearWall", 'X', 17.78, 0.22, 0.0, 5.0, Z1, H1, [(1.40, 2.70, 1.10, 2.40), (3.10, 4.50, Z1, 2.45)], "Mat_WallWarmWhite")
add_framed_window(col_fl1_arch, "Win_Fl1_KitchenRear", 'X', 17.78, 0.22, 1.40, 2.70, 1.10, 2.40)
add_framed_window(col_fl1_arch, "Door_Fl1_PatioRear", 'X', 17.78, 0.22, 3.10, 4.50, Z1, 2.45)

# Interior Partition Walls on Floor 1:
# Bedrooms on Left (X = 0.22..3.72), Internal Hallway on Right (X = 3.72..4.78) so Cutaway View shows 100% of every room!
add_wall_with_openings(col_fl1_arch, "Part_Fl1_ParentsFront", 'X', 7.55, 0.12, 0.22, 3.72, Z1, H1, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl1_arch, "Part_Fl1_ParentsHall", 'Y', 3.72, 0.12, 7.55, 11.35, Z1, H1, [(7.80, 8.65, Z1, 2.25), (9.00, 10.80, 1.05, 2.45)], "Mat_WallWarmWhite")
add_interior_door(col_fl1_arch, "Door_ParentsBed", 'Y', 3.72, 0.12, 7.80, 8.65, Z1, 2.25, open_angle=-0.35)
add_framed_window(col_fl1_arch, "Win_ParentsHall", 'Y', 3.72, 0.12, 9.00, 10.80, 1.05, 2.45)

add_wall_with_openings(col_fl1_arch, "Part_Fl1_ParentsReading", 'X', 11.35, 0.12, 0.22, 3.72, Z1, H1, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl1_arch, "Part_Fl1_ReadingHall", 'Y', 3.72, 0.12, 11.35, 14.35, Z1, H1, [(11.60, 12.45, Z1, 2.25), (12.70, 14.05, 1.05, 2.45)], "Mat_WallWarmWhite")
add_interior_door(col_fl1_arch, "Door_ReadingRoom", 'Y', 3.72, 0.12, 11.60, 12.45, Z1, 2.25, open_angle=-0.35)
add_framed_window(col_fl1_arch, "Win_ReadingHall", 'Y', 3.72, 0.12, 12.70, 14.05, 1.05, 2.45)
add_wall_with_openings(col_fl1_arch, "Part_Fl1_ReadingKitchen", 'X', 14.35, 0.12, 0.22, 3.72, Z1, H1, [], "Mat_WallWarmWhite")

# ---------------------------------------------------------------------------
# 7. FLOOR 1 ULTRA-DETAILED INTERIOR FURNITURE
# ---------------------------------------------------------------------------
# A. LIVING ROOM AT FRONT (Y = 0.45..3.30) — Sitting on Sofa looks straight out to Dad's Tea Table!
# Large Woven Area Rug
add_box(col_fl1_furn, "Living_AreaRug", 0.45, 0.55, Z1, 3.45, 3.30, Z1 + 0.018, "Mat_RugWoven", bevel=0.005)

# Luxury L-Shaped Sectional Sofa (along X = 0.32..1.26, Y = 0.55..3.25 + Chaise X = 0.32..2.15, Y = 2.45..3.25)
add_box(col_fl1_furn, "Sofa_WoodPlinthMain", 0.32, 0.55, Z1 + 0.06, 1.26, 2.45, Z1 + 0.14, "Mat_WoodOakTable", bevel=0.01)
add_box(col_fl1_furn, "Sofa_WoodPlinthChaise", 0.32, 2.45, Z1 + 0.06, 2.15, 3.25, Z1 + 0.14, "Mat_WoodOakTable", bevel=0.01)
add_box(col_fl1_furn, "Sofa_BackStructure", 0.32, 0.55, Z1 + 0.14, 0.52, 3.25, Z1 + 0.78, "Mat_FabricSofaWarm", bevel=0.035)
add_box(col_fl1_furn, "Sofa_ArmLeft", 0.32, 0.50, Z1 + 0.14, 1.26, 0.70, Z1 + 0.62, "Mat_FabricSofaWarm", bevel=0.035)
add_box(col_fl1_furn, "Sofa_ArmChaise", 0.32, 3.08, Z1 + 0.14, 1.55, 3.28, Z1 + 0.62, "Mat_FabricSofaWarm", bevel=0.035)
# 3 Seat Cushions + 1 Long Chaise Cushion + 4 Back Cushions + 6 Throw Pillows
for sc in range(3):
    sy0 = 0.70 + sc * 0.58
    add_box(col_fl1_furn, f"Sofa_SeatCush_{sc}", 0.50, sy0 + 0.01, Z1 + 0.14, 1.25, sy0 + 0.57, Z1 + 0.42, "Mat_FabricSofaWarm", bevel=0.045)
    add_box(col_fl1_furn, f"Sofa_BackCush_{sc}", 0.50, sy0 + 0.02, Z1 + 0.40, 0.72, sy0 + 0.56, Z1 + 0.84, "Mat_FabricSofaWarm", bevel=0.045)
add_box(col_fl1_furn, "Sofa_ChaiseCush", 0.50, 2.46, Z1 + 0.14, 2.12, 3.08, Z1 + 0.42, "Mat_FabricSofaWarm", bevel=0.045)
add_box(col_fl1_furn, "Sofa_BackCush_3", 0.50, 2.48, Z1 + 0.40, 0.72, 3.06, Z1 + 0.84, "Mat_FabricSofaWarm", bevel=0.045)
pillow_specs = [
    (0.74, 0.88, "Mat_CushionMustard", 0.25),
    (0.76, 1.12, "Mat_CushionTerracotta", -0.15),
    (0.74, 1.78, "Mat_CushionSage", 0.10),
    (0.74, 2.60, "Mat_CushionMustard", -0.20),
    (0.78, 2.86, "Mat_CushionNavy", 0.18),
    (1.25, 2.90, "Mat_CushionTerracotta", 0.40),
]
for pi, (px, py, pmat, prot) in enumerate(pillow_specs):
    add_box(col_fl1_furn, f"Sofa_ThrowPillow_{pi}", px - 0.08, py - 0.18, Z1 + 0.42, px + 0.08, py + 0.18, Z1 + 0.72, pmat, bevel=0.04, rot_z=prot)

# Dual Nested Round Coffee Tables + Art Books + Ikebana Vase
add_cyl(col_fl1_furn, "CoffeeTable_MarbleTop", 2.10, 1.55, Z1 + 0.36, Z1 + 0.40, 0.45, 0.45, "Mat_WhiteMarble")
add_cyl(col_fl1_furn, "CoffeeTable_MarbleBase", 2.10, 1.55, Z1 + 0.02, Z1 + 0.36, 0.39, 0.39, "Mat_MetalMatteBlack")
add_cyl(col_fl1_furn, "CoffeeTable_OakTop", 2.42, 2.08, Z1 + 0.43, Z1 + 0.47, 0.31, 0.31, "Mat_WoodOakTable")
add_cyl(col_fl1_furn, "CoffeeTable_OakBase", 2.42, 2.08, Z1 + 0.02, Z1 + 0.43, 0.25, 0.25, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "CoffeeTable_ArtBook1", 1.92, 1.38, Z1 + 0.40, 2.18, 1.66, Z1 + 0.43, "Mat_BookCream", bevel=0.005)
add_box(col_fl1_furn, "CoffeeTable_ArtBook2", 1.95, 1.41, Z1 + 0.43, 2.16, 1.63, Z1 + 0.455, "Mat_BookOchre", bevel=0.005)
add_cyl(col_fl1_furn, "CoffeeTable_Vase", 2.42, 2.08, Z1 + 0.47, Z1 + 0.68, 0.06, 0.04, "Mat_CeramicWhite")
add_sphere(col_fl1_furn, "CoffeeTable_Flowers", 2.42, 2.08, Z1 + 0.74, 0.11, 0.11, 0.09, "Mat_FlowerPink", subdiv=1)

# TV Media Wall, Fluted Wood Backdrop & Console (at X = 4.05..4.76, Y = 1.40..3.28, facing -X toward Sofa)
add_box(col_fl1_furn, "Living_TVFlutedBackdrop", 4.66, 1.38, Z1, 4.76, 3.30, 3.25, "Mat_WoodLouverFacade")
add_box(col_fl1_furn, "Living_TVMarbleSlab", 4.60, 1.55, Z1 + 0.58, 4.66, 3.12, 2.75, "Mat_WhiteMarble")
add_box(col_fl1_furn, "Living_TVBacklightLED", 4.64, 1.58, Z1 + 0.60, 4.66, 3.09, 2.72, "Mat_WarmLED")
add_box(col_fl1_furn, "Living_TVConsole", 4.10, 1.42, Z1 + 0.18, 4.65, 3.26, Z1 + 0.56, "Mat_WoodOakCabinet", bevel=0.015)
add_box(col_fl1_furn, "Living_TVConsoleMarble", 4.08, 1.40, Z1 + 0.56, 4.66, 3.28, Z1 + 0.59, "Mat_WhiteMarble", bevel=0.008)
for dr in range(4):
    dy0 = 1.45 + dr * 0.44
    add_box(col_fl1_furn, f"Living_TVDrawer_{dr}", 4.08, dy0, Z1 + 0.20, 4.10, dy0 + 0.42, Z1 + 0.54, "Mat_WoodOakTable", bevel=0.006)
# 65-inch OLED TV + Soundbar
add_box(col_fl1_furn, "Living_TVStandBase", 4.28, 2.15, Z1 + 0.59, 4.48, 2.55, Z1 + 0.61, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "Living_TVStandNeck", 4.36, 2.30, Z1 + 0.61, 4.40, 2.40, Z1 + 0.82, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "Living_TVBezel", 4.35, 1.62, Z1 + 0.78, 4.40, 3.06, Z1 + 1.68, "Mat_MetalMatteBlack", bevel=0.006)
add_box(col_fl1_furn, "Living_TVScreen", 4.34, 1.65, Z1 + 0.81, 4.35, 3.03, Z1 + 1.65, "Mat_TVScreenBlack")
add_box(col_fl1_furn, "Living_Soundbar", 4.16, 1.90, Z1 + 0.59, 4.24, 2.78, Z1 + 0.65, "Mat_MetalMatteBlack", bevel=0.01)
build_potted_plant(col_fl1_furn, "Living_FrontPlant", 4.35, 0.55, Z1, scale=0.95)

# B. SACRED QUAN YIN & ANCESTRAL ALTAR SANCTUARY (PARALLEL TO TV: X = 3.28..4.76, Y = 3.36..4.98, facing -X)
# 1. Warm Walnut Sanctuary Back Wall, Golden Lotus Mandala Halo & Warm LED Cove Lighting
add_box(col_fl1_furn, "Altar_BackPanelWalnut", 4.68, 3.38, Z1, 4.76, 4.96, 3.30, "Mat_WoodWalnutAltar")
add_box(col_fl1_furn, "Altar_LED_TopCove", 3.32, 3.38, 3.22, 4.72, 4.96, 3.28, "Mat_WarmLED")
add_box(col_fl1_furn, "Altar_LED_BackLeft", 4.66, 3.42, Z1 + 0.20, 4.69, 3.46, 3.20, "Mat_WarmLED")
add_box(col_fl1_furn, "Altar_LED_BackRight", 4.66, 4.90, Z1 + 0.20, 4.69, 4.94, 3.20, "Mat_WarmLED")
# Glowing Golden Mandala Halo on the back wall behind Quan Yin Statue
add_cyl(col_fl1_furn, "Altar_SacredHaloOuter", 4.66, 4.18, Z1 + 1.88, Z1 + 1.90, 0.42, 0.42, "Mat_WarmLED", rot=(0, math.pi / 2, 0))
add_cyl(col_fl1_furn, "Altar_SacredHaloInner", 4.65, 4.18, Z1 + 1.88, Z1 + 1.90, 0.34, 0.34, "Mat_WoodWalnutAltar", rot=(0, math.pi / 2, 0))

# 2. Two CNC Wooden Lattice Wing Screens (at Y = 3.35 separating from TV, and Y = 4.97 separating from Hallway)
for side_idx, wy in enumerate([3.35, 4.96]):
    add_box(col_fl1_furn, f"Altar_CNC_PostFront_{side_idx}", 3.28, wy - 0.03, Z1, 3.36, wy + 0.03, 3.30, "Mat_WoodWalnutAltar", bevel=0.008)
    add_box(col_fl1_furn, f"Altar_CNC_PostBack_{side_idx}", 4.66, wy - 0.03, Z1, 4.76, wy + 0.03, 3.30, "Mat_WoodWalnutAltar", bevel=0.008)
    add_box(col_fl1_furn, f"Altar_CNC_RailBot_{side_idx}", 3.28, wy - 0.03, Z1, 4.76, wy + 0.03, Z1 + 0.12, "Mat_WoodWalnutAltar", bevel=0.008)
    add_box(col_fl1_furn, f"Altar_CNC_RailTop_{side_idx}", 3.28, wy - 0.03, 3.18, 4.76, wy + 0.03, 3.30, "Mat_WoodWalnutAltar", bevel=0.008)
    for slat in range(11):
        sx = 3.42 + slat * 0.115
        add_box(col_fl1_furn, f"Altar_CNC_VBar_{side_idx}_{slat}", sx, wy - 0.015, Z1 + 0.12, sx + 0.025, wy + 0.015, 3.18, "Mat_WoodLouverFacade")
    for hbar in range(7):
        hz = Z1 + 0.45 + hbar * 0.40
        add_box(col_fl1_furn, f"Altar_CNC_HBar_{side_idx}_{hbar}", 3.34, wy - 0.018, hz, 4.68, wy + 0.018, hz + 0.022, "Mat_WoodLouverFacade")

# 3. SACRED HANGING CURTAIN / VEIL SCREEN (Màn ngăn phòng thờ ấm cúng thiêng liêng tại X = 3.32, Y = 3.38..4.96)
# Carved overhead wooden valance & golden curtain rod
add_box(col_fl1_furn, "Altar_FrontValance", 3.28, 3.35, 2.55, 3.36, 4.99, 3.30, "Mat_WoodWalnutAltar", bevel=0.01)
add_box(col_fl1_furn, "Altar_ValanceGoldTrim", 3.27, 3.40, 2.58, 3.29, 4.94, 2.61, "Mat_BuddhaGold")
add_cyl(col_fl1_furn, "Altar_CurtainRod", 3.32, 4.18, 2.50, 2.52, 0.016, 0.016, "Mat_BuddhaGold", rot=(math.pi / 2, 0, 0))
# Upper Semi-Sheer Bamboo/Silk Sanctuary Veil (Màn sáo lụa phía trên)
add_box(col_fl1_furn, "Altar_UpperBambooVeil", 3.31, 3.42, 2.22, 3.33, 4.92, 2.54, "Mat_CurtainSheer")
for b_slat in range(7):
    bz = 2.24 + b_slat * 0.042
    add_box(col_fl1_furn, f"Altar_VeilStrip_{b_slat}", 3.305, 3.44, bz, 3.335, 4.90, bz + 0.012, "Mat_WoodLouverFacade")
# Left & Right Draped Warm Amber-Gold Sanctuary Curtains (Màn lụa vàng ấm vén 2 bên có đai cột vàng)
for side_c, cy_base in enumerate([3.58, 4.78]):
    for pleat in range(6):
        py = cy_base + (pleat - 2.5) * 0.055
        add_box(col_fl1_furn, f"Altar_SanctuaryCurtain_{side_c}_{pleat}", 3.28, py - 0.022, Z1 + 0.02, 3.36, py + 0.022, 2.54, "Mat_CushionMustard" if pleat % 2 == 0 else "Mat_BeddingCream", bevel=0.012)
    # Golden Tassel Tie-Back
    add_box(col_fl1_furn, f"Altar_CurtainTie_{side_c}", 3.26, cy_base - 0.16, Z1 + 1.05, 3.38, cy_base + 0.16, Z1 + 1.10, "Mat_BuddhaGold", bevel=0.01)
# Pair of Glowing Hanging Traditional Lotus Lanterns (Đèn lồng hoa sen thả trần)
for lan_y in [3.78, 4.58]:
    add_cyl(col_fl1_furn, f"Altar_LanternCord_{lan_y:.2f}", 3.38, lan_y, 2.22, 3.25, 0.005, 0.005, "Mat_BuddhaGold")
    add_sphere(col_fl1_furn, f"Altar_LanternGlow_{lan_y:.2f}", 3.38, lan_y, 2.15, 0.09, 0.09, 0.12, "Mat_WarmLED", subdiv=2)
    add_cyl(col_fl1_furn, f"Altar_LanternCap_{lan_y:.2f}", 3.38, lan_y, 2.25, 2.28, 0.10, 0.04, "Mat_BuddhaGold")

# 4. Two-Tier Carved Walnut Altar Table Inside Sanctuary (facing -X, parallel to TV!)
add_box(col_fl1_furn, "Altar_MainTop", 3.92, 3.56, Z1 + 1.05, 4.65, 4.80, Z1 + 1.12, "Mat_WoodWalnutAltar", bevel=0.012)
add_box(col_fl1_furn, "Altar_UpperTier", 4.30, 3.68, Z1 + 1.12, 4.66, 4.68, Z1 + 1.28, "Mat_WoodWalnutAltar", bevel=0.01)
add_box(col_fl1_furn, "Altar_LowerCabinet", 4.02, 3.66, Z1 + 0.12, 4.62, 4.70, Z1 + 0.80, "Mat_WoodOakDark", bevel=0.01)
for lx in [3.96, 4.60]:
    for ly in [3.62, 4.74]:
        add_box(col_fl1_furn, f"Altar_Leg_{lx:.2f}_{ly:.2f}", lx - 0.035, ly - 0.035, Z1, lx + 0.035, ly + 0.035, Z1 + 1.05, "Mat_WoodWalnutAltar", bevel=0.008)

# Quan Yin Bodhisattva Statue on Golden Lotus Pedestal (at X = 4.48, Y = 4.18, facing -X)
add_cyl(col_fl1_furn, "Altar_LotusBase", 4.48, 4.18, Z1 + 1.28, Z1 + 1.38, 0.14, 0.18, "Mat_BuddhaGold")
add_cyl(col_fl1_furn, "Altar_QuanYinRobe", 4.48, 4.18, Z1 + 1.38, Z1 + 1.82, 0.11, 0.05, "Mat_BuddhaGold")
add_sphere(col_fl1_furn, "Altar_QuanYinHead", 4.48, 4.18, Z1 + 1.88, 0.055, 0.055, 0.065, "Mat_BuddhaGold")
# 2 Lotus Lamps & 2 Lotus Flower Vases
for side_y in [3.82, 4.54]:
    add_cyl(col_fl1_furn, f"Altar_Vase_{side_y:.2f}", 4.48, side_y, Z1 + 1.28, Z1 + 1.54, 0.055, 0.075, "Mat_CeramicWhite")
    add_sphere(col_fl1_furn, f"Altar_LotusBloom_{side_y:.2f}", 4.48, side_y, Z1 + 1.62, 0.08, 0.08, 0.09, "Mat_FlowerPink")
    add_cyl(col_fl1_furn, f"Altar_LampStem_{side_y:.2f}", 4.15, side_y + (0.10 if side_y < 4.18 else -0.10), Z1 + 1.12, Z1 + 1.34, 0.03, 0.02, "Mat_BuddhaGold")
    add_sphere(col_fl1_furn, f"Altar_LampBulb_{side_y:.2f}", 4.15, side_y + (0.10 if side_y < 4.18 else -0.10), Z1 + 1.37, 0.045, 0.045, 0.055, "Mat_WarmLED")
# Brass Incense Burner (Bát hương), 3 Ritual Cups & 5-Fruit Platter (Mâm ngũ quả)
add_cyl(col_fl1_furn, "Altar_IncenseBurner", 4.12, 4.18, Z1 + 1.12, Z1 + 1.25, 0.08, 0.09, "Mat_BuddhaGold")
for inc_i in range(3):
    add_cyl(col_fl1_furn, f"Altar_IncenseStick_{inc_i}", 4.12, 4.16 + inc_i * 0.02, Z1 + 1.25, Z1 + 1.42, 0.003, 0.003, "Mat_TomatoRed")
add_cyl(col_fl1_furn, "Altar_FruitPlatter", 4.12, 4.42, Z1 + 1.12, Z1 + 1.17, 0.09, 0.14, "Mat_WoodOakDark")
for fi, (ox, oy, m_col) in enumerate([(0, 0, "Mat_FoliageLime"), (0.04, 0.06, "Mat_FruitOrange"), (-0.04, -0.05, "Mat_FlowerPink"), (0.05, -0.04, "Mat_FlowerYellow")]):
    add_sphere(col_fl1_furn, f"Altar_Fruit_{fi}", 4.12 + ox, 4.42 + oy, Z1 + 1.21, 0.045, 0.045, 0.045, m_col, subdiv=1)
# Kneeling Prayer Mat & Round Cushion (Bồ đoàn tụng kinh)
add_box(col_fl1_furn, "Altar_SacredRug", 2.85, 3.65, Z1, 3.85, 4.70, Z1 + 0.015, "Mat_CushionTerracotta", bevel=0.005)
add_cyl(col_fl1_furn, "Altar_PrayerMat", 3.12, 4.18, Z1 + 0.015, Z1 + 0.10, 0.24, 0.22, "Mat_CushionMustard")

# C. CENTRAL STAIRCASE, GLASS BALUSTRADE & UNDER-STAIR ZEN GARDEN (Y = 5.0..7.55)
# 19 Solid Oak Treads rising along Left & Center (U-turn with landing)
# Flight 1: Y = 5.05..7.25 at X = 0.24..1.18 (10 steps, Z = 0.25..2.02)
for s in range(10):
    sy = 5.05 + s * 0.22
    sz = Z1 + (s + 1) * 0.177
    add_box(col_fl1_arch, f"Stair_F1_Tread_{s}", 0.24, sy, sz - 0.04, 1.18, sy + 0.24, sz, "Mat_WoodStairTreads", bevel=0.006)
    add_box(col_fl1_arch, f"Stair_F1_Riser_{s}", 0.24, sy, sz - 0.177, 1.16, sy + 0.02, sz - 0.04, "Mat_WallWarmWhite")
# Mid Landing: X = 0.24..2.22, Y = 7.25..7.52, Z = 2.02
add_box(col_fl1_arch, "Stair_Landing", 0.24, 7.05, 1.96, 2.22, 7.52, 2.04, "Mat_WoodStairTreads", bevel=0.008)
# Flight 2: Y = 7.05 down to 5.05 at X = 1.28..2.22 (9 steps, Z = 2.04..3.80)
for s in range(9):
    sy = 6.83 - s * 0.22
    sz = 2.04 + (s + 1) * 0.195
    add_box(col_fl1_arch, f"Stair_F2_Tread_{s}", 1.28, sy, sz - 0.04, 2.22, sy + 0.24, sz, "Mat_WoodStairTreads", bevel=0.006)
# Tempered Glass Balustrade & Oak Handrail
add_box(col_fl1_arch, "Stair_GlassRail1", 1.18, 5.05, Z1 + 0.35, 1.21, 7.05, 2.85, "Mat_GlassClear")
add_box(col_fl1_arch, "Stair_GlassRail2", 2.20, 5.05, 2.15, 2.23, 7.52, 4.65, "Mat_GlassClear")
add_box(col_fl1_arch, "Stair_Handrail", 2.18, 5.05, 4.62, 2.25, 7.52, 4.68, "Mat_WoodOakTable", bevel=0.01)

# Under-Stair Zen Dry Garden (Tiểu cảnh khô gầm cầu thang)
add_box(col_fl1_furn, "Zen_Border", 0.24, 5.05, Z1, 2.25, 7.45, Z1 + 0.12, "Mat_WoodOakDark", bevel=0.01)
add_box(col_fl1_furn, "Zen_Pebbles", 0.30, 5.11, Z1, 2.19, 7.39, Z1 + 0.09, "Mat_WhitePebbles")
for st_i, (sx, sy) in enumerate([(1.55, 5.45), (1.75, 5.95), (1.60, 6.45), (1.80, 6.95)]):
    add_cyl(col_fl1_furn, f"Zen_StepStone_{st_i}", sx, sy, Z1 + 0.08, Z1 + 0.12, 0.18, 0.20, "Mat_DarkGreyStone")
add_sphere(col_fl1_furn, "Zen_Boulder1", 0.75, 6.65, Z1 + 0.18, 0.24, 0.18, 0.16, "Mat_DarkGreyStone", subdiv=1)
add_sphere(col_fl1_furn, "Zen_Boulder2", 0.95, 6.85, Z1 + 0.14, 0.16, 0.15, 0.12, "Mat_DarkGreyStone", subdiv=1)
build_potted_plant(col_fl1_furn, "Zen_Bonsai", 1.55, 6.20, Z1 + 0.09, scale=0.85)

# D. PARENTS' BEDROOM (Phòng ngủ Ba Mẹ - X = 0.22..3.72, Y = 7.67..11.35)
build_detailed_bed(col_fl1_furn, "Parents_QueenBed", 1.35, 9.45, Z1, width=1.65, length=2.0, facing="+X", duvet_mat="Mat_BeddingCream", accent_mat="Mat_CushionTerracotta")
build_nightstand_with_lamp(col_fl1_furn, "Parents_Nightstand_L", 0.55, 8.35, Z1)
build_nightstand_with_lamp(col_fl1_furn, "Parents_Nightstand_R", 0.55, 10.55, Z1)
build_wardrobe(col_fl1_furn, "Parents_Wardrobe", 0.35, 10.75, Z1, 2.55, 11.33, height=2.60, glass_doors=False)
# Dresser & Armchair by Window
add_box(col_fl1_furn, "Parents_Dresser", 1.85, 7.70, Z1, 3.25, 8.15, Z1 + 0.82, "Mat_WoodOakCabinet", bevel=0.01)
build_dining_chair(col_fl1_furn, "Parents_Armchair", 3.15, 9.85, Z1, rot_z=0.4, seat_mat="Mat_CushionMustard")
build_potted_plant(col_fl1_furn, "Parents_Plant", 3.35, 10.90, Z1, scale=0.75)

# E. READING, KEEPSAKE & GUEST ROOM (Phòng Đọc sách & Kỷ vật - X = 0.22..3.72, Y = 11.47..14.35)
# Full-Wall Floor-to-Ceiling Bookcase & Keepsake Cabinet (along Y = 11.48..11.88, X = 0.35..3.15)
add_box(col_fl1_furn, "Reading_BookcaseBack", 0.35, 11.48, Z1, 3.15, 11.54, Z1 + 2.65, "Mat_WoodOakCabinet")
num_bays = 5
bay_w = (3.15 - 0.35) / num_bays
for b in range(num_bays + 1):
    bx = 0.35 + b * bay_w
    add_box(col_fl1_furn, f"Reading_VSide_{b}", bx - 0.018, 11.48, Z1, bx + 0.018, 11.88, Z1 + 2.65, "Mat_WoodOakTable")
for sh in range(7):
    sz = Z1 + sh * 0.43
    add_box(col_fl1_furn, f"Reading_Shelf_{sh}", 0.35, 11.48, sz, 3.15, 11.88, sz + 0.03, "Mat_WoodOakTable")
    if 0 < sh < 6:
        for b in range(num_bays):
            bx0 = 0.38 + b * bay_w
            if (b + sh) % 3 == 0:
                # Keepsake trophy / vase / globe
                add_cyl(col_fl1_furn, f"Keepsake_Vase_{sh}_{b}", bx0 + bay_w * 0.5, 11.68, sz + 0.03, sz + 0.28, 0.06, 0.04, "Mat_BuddhaGold" if b % 2 == 0 else "Mat_CeramicWhite")
            else:
                # Row of individual colorful books!
                cur_bk_x = bx0 + 0.02
                bk_i = 0
                while cur_bk_x < bx0 + bay_w - 0.08:
                    bw = 0.032 + (bk_i % 3) * 0.012
                    bh = 0.24 + (bk_i % 4) * 0.03
                    bmat = book_mats[(b * 7 + sh * 3 + bk_i) % len(book_mats)].name
                    add_box(col_fl1_furn, f"Book_{sh}_{b}_{bk_i}", cur_bk_x, 11.56, sz + 0.03, cur_bk_x + bw, 11.82, sz + 0.03 + bh, bmat, bevel=0.003)
                    cur_bk_x += bw + 0.004
                    bk_i += 1

# Cozy Guest Daybed / Sofa Bed (along Y = 13.38..14.28, X = 0.35..2.25)
add_box(col_fl1_furn, "Reading_DaybedFrame", 0.35, 13.38, Z1 + 0.06, 2.25, 14.28, Z1 + 0.28, "Mat_WoodOakTable", bevel=0.012)
add_box(col_fl1_furn, "Reading_DaybedBack", 0.35, 14.16, Z1 + 0.28, 2.25, 14.30, Z1 + 0.78, "Mat_WoodOakTable", bevel=0.012)
add_box(col_fl1_furn, "Reading_DaybedMattress", 0.40, 13.42, Z1 + 0.28, 2.20, 14.16, Z1 + 0.48, "Mat_FabricSofaWarm", bevel=0.035)
for dp in range(3):
    px = 0.55 + dp * 0.55
    add_box(col_fl1_furn, f"Reading_DaybedCush_{dp}", px, 13.95, Z1 + 0.48, px + 0.45, 14.15, Z1 + 0.76, "Mat_CushionSage" if dp % 2 == 0 else "Mat_CushionMustard", bevel=0.035)

# Study Desk & Ergonomic Chair by Corridor Window
build_desk_and_chair(col_fl1_furn, "Reading_StudyDesk", 3.15, 13.10, Z1, width=1.25, depth=0.58, facing="+X")

# F. OPEN KITCHEN, PASTRY ISLAND & DINING ROOM (X = 0.22..4.78, Y = 14.47..17.78)
# 1. Tall Refrigerator & Built-in Oven/Microwave Tower (X = 0.24..1.02, Y = 14.52..15.95)
add_box(col_fl1_furn, "Kitchen_FridgeBody", 0.24, 14.55, Z1, 0.98, 15.38, Z1 + 1.85, "Mat_MetalStainless", bevel=0.015)
add_box(col_fl1_furn, "Kitchen_FridgeDoorL", 0.98, 14.56, Z1 + 0.05, 1.02, 14.96, Z1 + 1.83, "Mat_MetalStainless", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_FridgeDoorR", 0.98, 14.97, Z1 + 0.05, 1.02, 15.37, Z1 + 1.83, "Mat_MetalStainless", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_OvenTower", 0.24, 15.40, Z1, 0.88, 16.05, Z1 + 2.35, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl1_furn, "Kitchen_OvenDoor", 0.88, 15.44, Z1 + 0.65, 0.91, 16.01, Z1 + 1.25, "Mat_TVScreenBlack", bevel=0.006)
add_box(col_fl1_furn, "Kitchen_OvenHandle", 0.91, 15.50, Z1 + 1.18, 0.94, 15.95, Z1 + 1.21, "Mat_MetalStainless")
add_box(col_fl1_furn, "Kitchen_MicroDoor", 0.88, 15.44, Z1 + 1.30, 0.91, 16.01, Z1 + 1.68, "Mat_TVScreenBlack", bevel=0.006)

# 2. L-Shaped Lower & Upper Kitchen Counter + Double Sink + Induction Hob + Range Hood
add_box(col_fl1_furn, "Kitchen_LowerCab_Left", 0.24, 16.05, Z1, 0.88, 17.75, Z1 + 0.86, "Mat_WoodOakCabinet", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_Counter_Left", 0.24, 16.05, Z1 + 0.86, 0.92, 17.75, Z1 + 0.90, "Mat_WhiteMarble", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_LowerCab_Rear", 0.88, 17.12, Z1, 2.95, 17.75, Z1 + 0.86, "Mat_WoodOakCabinet", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_Counter_Rear", 0.88, 17.08, Z1 + 0.86, 2.95, 17.75, Z1 + 0.90, "Mat_WhiteMarble", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_UpperCab_Left", 0.24, 16.05, Z1 + 1.55, 0.62, 17.75, Z1 + 2.35, "Mat_WallWarmWhite", bevel=0.008)
add_box(col_fl1_furn, "Kitchen_UnderCabLED", 0.55, 16.08, Z1 + 1.53, 0.58, 17.70, Z1 + 1.55, "Mat_WarmLED")

# Induction Hob, Stainless Pot & Range Hood (at X = 0.58, Y = 16.65)
add_box(col_fl1_furn, "Kitchen_InductionHob", 0.35, 16.35, Z1 + 0.90, 0.82, 17.05, Z1 + 0.915, "Mat_TVScreenBlack", bevel=0.004)
add_cyl(col_fl1_furn, "Kitchen_SoupPot", 0.58, 16.55, Z1 + 0.915, Z1 + 1.08, 0.11, 0.12, "Mat_MetalStainless")
add_cyl(col_fl1_furn, "Kitchen_FryPan", 0.58, 16.85, Z1 + 0.915, Z1 + 0.97, 0.13, 0.14, "Mat_MetalMatteBlack")
add_box(col_fl1_furn, "Kitchen_RangeHood", 0.24, 16.30, Z1 + 1.60, 0.78, 17.10, Z1 + 1.72, "Mat_MetalStainless", bevel=0.01)

# Double Sink & Gooseneck Faucet (under rear window at X = 1.95, Y = 17.42)
add_box(col_fl1_furn, "Kitchen_SinkBasin1", 1.62, 17.22, Z1 + 0.88, 1.98, 17.62, Z1 + 0.905, "Mat_MetalStainless", bevel=0.005)
add_box(col_fl1_furn, "Kitchen_SinkBasin2", 2.02, 17.22, Z1 + 0.88, 2.38, 17.62, Z1 + 0.905, "Mat_MetalStainless", bevel=0.005)
add_cyl(col_fl1_furn, "Kitchen_SinkFaucet", 2.00, 17.66, Z1 + 0.90, Z1 + 1.22, 0.015, 0.015, "Mat_MetalStainless")
add_box(col_fl1_furn, "Kitchen_SinkSpout", 2.00 - 0.015, 17.48, Z1 + 1.19, 2.00 + 0.015, 17.66, Z1 + 1.22, "Mat_MetalStainless", bevel=0.004)

# 3. SIGNATURE PASTRY & BAKING ISLAND (Quầy Đảo Làm Bánh Đá Trắng - X = 1.55..3.35, Y = 14.80..15.58)
add_box(col_fl1_furn, "Island_Cabinet", 1.60, 14.84, Z1, 3.30, 15.50, Z1 + 0.88, "Mat_WoodOakCabinet", bevel=0.01)
add_box(col_fl1_furn, "Island_MarbleTop", 1.54, 14.78, Z1 + 0.88, 3.36, 15.62, Z1 + 0.93, "Mat_WhiteMarble", bevel=0.01)
add_box(col_fl1_furn, "Island_WaterfallL", 1.54, 14.78, Z1, 1.59, 15.62, Z1 + 0.93, "Mat_WhiteMarble", bevel=0.008)
add_box(col_fl1_furn, "Island_WaterfallR", 3.31, 14.78, Z1, 3.36, 15.62, Z1 + 0.93, "Mat_WhiteMarble", bevel=0.008)
# KitchenAid Stand Mixer
add_box(col_fl1_furn, "Baking_MixerBase", 1.78, 15.05, Z1 + 0.93, 2.08, 15.28, Z1 + 0.96, "Mat_MixerPastelPink", bevel=0.01)
add_cyl(col_fl1_furn, "Baking_MixerNeck", 1.84, 15.16, Z1 + 0.96, Z1 + 1.24, 0.055, 0.05, "Mat_MixerPastelPink")
add_box(col_fl1_furn, "Baking_MixerHead", 1.80, 15.08, Z1 + 1.20, 2.10, 15.24, Z1 + 1.32, "Mat_MixerPastelPink", bevel=0.03)
add_cyl(col_fl1_furn, "Baking_MixerBowl", 1.99, 15.16, Z1 + 0.96, Z1 + 1.15, 0.08, 0.11, "Mat_MetalStainless")
# Wooden Pastry Board, Rolling Pin & Croissant Baking Tray
add_box(col_fl1_furn, "Baking_PastryBoard", 2.25, 14.95, Z1 + 0.93, 2.72, 15.35, Z1 + 0.95, "Mat_WoodOakTable", bevel=0.005)
add_cyl(col_fl1_furn, "Baking_RollingPin", 2.48, 15.12, Z1 + 0.97, Z1 + 0.99, 0.022, 0.022, "Mat_WoodOakDark", rot=(0, math.pi / 2, 0.3))
add_box(col_fl1_furn, "Baking_SheetTray", 2.80, 14.92, Z1 + 0.93, 3.22, 15.26, Z1 + 0.945, "Mat_MetalMatteBlack", bevel=0.004)
for cr_i in range(6):
    cx_cr = 2.88 + (cr_i % 3) * 0.11
    cy_cr = 15.02 + (cr_i // 3) * 0.13
    add_sphere(col_fl1_furn, f"Baking_Croissant_{cr_i}", cx_cr, cy_cr, Z1 + 0.965, 0.042, 0.026, 0.022, "Mat_CroissantGold", subdiv=1)
# Glass-Domed Cake Stand with 2-Tier Berry Cake
add_cyl(col_fl1_furn, "Baking_CakeStand", 2.48, 15.46, Z1 + 0.93, Z1 + 1.01, 0.05, 0.13, "Mat_CeramicWhite")
add_cyl(col_fl1_furn, "Baking_CakeTier1", 2.48, 15.46, Z1 + 1.01, Z1 + 1.10, 0.10, 0.10, "Mat_BeddingCream")
add_cyl(col_fl1_furn, "Baking_CakeTier2", 2.48, 15.46, Z1 + 1.10, Z1 + 1.17, 0.07, 0.07, "Mat_FlowerPink")
add_sphere(col_fl1_furn, "Baking_CakeDome", 2.48, 15.46, Z1 + 1.10, 0.125, 0.125, 0.14, "Mat_GlassClear", subdiv=2)
# 2 Bar Stools at Island
for bs_i, b_x in enumerate([2.05, 2.85]):
    add_cyl(col_fl1_furn, f"Island_StoolSeat_{bs_i}", b_x, 14.62, Z1 + 0.62, Z1 + 0.67, 0.17, 0.17, "Mat_WoodOakTable")
    for sl_x, sl_y in [(-0.12, -0.12), (0.12, -0.12), (-0.12, 0.12), (0.12, 0.12)]:
        add_cyl(col_fl1_furn, f"Island_StoolLeg_{bs_i}_{sl_x:.2f}_{sl_y:.2f}", b_x + sl_x, 14.62 + sl_y, Z1, Z1 + 0.62, 0.014, 0.010, "Mat_MetalMatteBlack")

# 4. 6-SEAT SOLID OAK DINING TABLE & PENDANT CHANDELIER (X = 2.65..4.45, Y = 15.95..16.85)
add_box(col_fl1_furn, "Dining_TableTop", 2.65, 15.95, Z1 + 0.72, 4.45, 16.85, Z1 + 0.76, "Mat_WoodOakTable", bevel=0.015)
for dl_x in [2.78, 4.32]:
    for dl_y in [16.05, 16.75]:
        add_cyl(col_fl1_furn, f"Dining_Leg_{dl_x:.2f}_{dl_y:.2f}", dl_x, dl_y, Z1, Z1 + 0.72, 0.028, 0.020, "Mat_WoodOakTable")
for ch_i, ch_x in enumerate([2.98, 3.55, 4.12]):
    build_dining_chair(col_fl1_furn, f"Dining_Chair_Front_{ch_i}", ch_x, 15.72, Z1, rot_z=math.pi, seat_mat="Mat_FabricSofaWarm")
    build_dining_chair(col_fl1_furn, f"Dining_Chair_Back_{ch_i}", ch_x, 17.08, Z1, rot_z=0.0, seat_mat="Mat_FabricSofaWarm")
    # Dinner Plates & Bowls
    add_cyl(col_fl1_furn, f"Dining_PlateF_{ch_i}", ch_x, 16.14, Z1 + 0.76, Z1 + 0.775, 0.12, 0.13, "Mat_CeramicWhite")
    add_cyl(col_fl1_furn, f"Dining_PlateB_{ch_i}", ch_x, 16.66, Z1 + 0.76, Z1 + 0.775, 0.12, 0.13, "Mat_CeramicWhite")
    # 3 Warm Pendant Lights Above Dining Table
    add_cyl(col_fl1_furn, f"Dining_PendantWire_{ch_i}", ch_x, 16.40, Z1 + 1.85, H1, 0.004, 0.004, "Mat_MetalMatteBlack")
    add_sphere(col_fl1_furn, f"Dining_PendantBulb_{ch_i}", ch_x, 16.40, Z1 + 1.80, 0.11, 0.11, 0.11, "Mat_WarmLED", subdiv=2)

# G. REAR YARD GROUND FLOOR WC & COVERED LAUNDRY (Y = 18.0..20.0)
add_wall_with_openings(col_fl1_arch, "WC1_RightWall", 'Y', 2.15, 0.12, 18.0, 19.95, 0.15, 2.75, [(18.25, 19.00, 0.15, 2.15)], "Mat_WallWarmWhite")
add_interior_door(col_fl1_arch, "Door_WC1", 'Y', 2.15, 0.12, 18.25, 19.00, 0.15, 2.15)
add_wall_with_openings(col_fl1_arch, "WC1_RearWall", 'X', 19.83, 0.12, 0.0, 2.27, 0.15, 2.75, [], "Mat_WallWarmWhite")
build_bathroom_fixtures(col_fl1_furn, "WC1_Fixtures", 0.18, 18.05, 0.15, 2.12, 19.80, has_bathtub=False)
# Covered Laundry Canopy & Front-Load Washing Machine
add_box(col_fl1_arch, "Laundry_GlassCanopy", 0.0, 18.0, 2.75, 5.0, 20.0, 2.82, "Mat_BalconyGlassBronze")
add_box(col_fl1_furn, "Laundry_WasherBody", 2.35, 18.12, 0.15, 2.98, 18.72, 1.00, "Mat_CeramicWhite", bevel=0.015)
add_cyl(col_fl1_furn, "Laundry_WasherDoor", 2.66, 18.73, 0.56, 0.58, 0.21, 0.21, "Mat_TVScreenBlack", rot=(math.pi / 2, 0, 0))

# ---------------------------------------------------------------------------
# 8. FLOOR 2 ARCHITECTURE (SLAB WITH STAIR OPENING, WALLS, WINDOWS, BALCONIES)
# ---------------------------------------------------------------------------
Z2 = 3.80  # Floor 2 finished floor level
H2 = 7.20  # Floor 2 ceiling / Roof slab bottom

# Floor 2 Slab (with cutout for Central Staircase & Skylight Atrium X = 0.22..2.25, Y = 5.05..7.52)
add_box(col_fl2_arch, "Floor2_Slab_Front", 0.0, -1.60, H1, 5.0, 5.05, Z2, "Mat_AntiSlipWoodTile")
add_box(col_fl2_arch, "Floor2_Slab_MidRight", 2.25, 5.05, H1, 5.0, 7.52, Z2, "Mat_AntiSlipWoodTile")
add_box(col_fl2_arch, "Floor2_Slab_Rear", 0.0, 7.52, H1, 5.0, 18.0, Z2, "Mat_AntiSlipWoodTile")

# Floor 2 Left Wall (Cutaway base at Z2..Z2+0.45 in main view + full height in col_enclosure)
add_box(col_fl2_arch, "Floor2_LeftWall_CutawayBase", 0.0, 0.0, Z2, 0.22, 15.0, Z2 + 0.45, "Mat_WallWarmWhite")
add_box(col_enclosure, "Floor2_LeftWall_Full", 0.0, 0.0, Z2 + 0.45, 0.22, 15.0, H2, "Mat_WallWarmWhite")

# Floor 2 Right Wall (X = 4.78..5.0) with Bedroom & Bathroom Windows to 2m Corridor
fl2_right_openings = [
    (0.85, 2.85, Z2 + 0.85, Z2 + 2.45),  # Master Bedroom window
    (3.65, 4.75, Z2 + 1.45, Z2 + 2.35),  # Master Bathroom window
    (8.15, 10.45, Z2 + 0.85, Z2 + 2.45), # Sister 2 Bedroom window
    (11.85, 14.15, Z2 + 0.85, Z2 + 2.45) # Youngest Sister Bedroom window
]
add_wall_with_openings(col_fl2_arch, "Floor2_RightWall", 'Y', 4.78, 0.22, 0.0, 15.0, Z2, H2, fl2_right_openings, "Mat_WallWarmWhite")
add_framed_window(col_fl2_arch, "Win_Fl2_Master", 'Y', 4.78, 0.22, 0.85, 2.85, Z2 + 0.85, Z2 + 2.45, with_curtains=True, curtain_side=-1)
add_framed_window(col_fl2_arch, "Win_Fl2_MasterBath", 'Y', 4.78, 0.22, 3.65, 4.75, Z2 + 1.45, Z2 + 2.35, with_curtains=False)
add_framed_window(col_fl2_arch, "Win_Fl2_Sister2", 'Y', 4.78, 0.22, 8.15, 10.45, Z2 + 0.85, Z2 + 2.45, with_curtains=True, curtain_side=-1)
add_framed_window(col_fl2_arch, "Win_Fl2_Youngest", 'Y', 4.78, 0.22, 11.85, 14.15, Z2 + 0.85, Z2 + 2.45, with_curtains=True, curtain_side=-1)

# Master Suite Front Wall (Y = 0.0..0.22) with Wide Sliding Glass Door to Star-Gazing Balcony
add_wall_with_openings(col_fl2_arch, "Floor2_FrontWall", 'X', 0.0, 0.22, 0.0, 5.0, Z2, H2, [(0.75, 4.25, Z2, Z2 + 2.65)], "Mat_WallFacadeWarm")
add_framed_window(col_fl2_arch, "Door_Fl2_MasterBalcony", 'X', 0.0, 0.22, 0.75, 4.25, Z2, Z2 + 2.65, with_curtains=True, curtain_side=1)

# Floor 2 Interior Partition Walls:
# 1. Master Suite Rear Wall (Y = 5.15) & Master En-Suite Bathroom (X = 3.05..4.78, Y = 3.20..5.15)
add_wall_with_openings(col_fl2_arch, "Part_Fl2_MasterRear", 'X', 5.15, 0.12, 0.22, 4.78, Z2, H2, [(2.30, 3.00, Z2, Z2 + 2.25)], "Mat_WallWarmWhite")
add_interior_door(col_fl2_arch, "Door_MasterSuite", 'X', 5.15, 0.12, 2.30, 3.00, Z2, Z2 + 2.25)
add_wall_with_openings(col_fl2_arch, "Part_Fl2_MasterBathFront", 'X', 3.20, 0.12, 3.05, 4.78, Z2, H2, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl2_arch, "Part_Fl2_MasterBathLeft", 'Y', 3.05, 0.12, 3.20, 5.15, Z2, H2, [(3.40, 4.15, Z2, Z2 + 2.20)], "Mat_WallWarmWhite")
add_interior_door(col_fl2_arch, "Door_MasterBath", 'Y', 3.05, 0.12, 3.40, 4.15, Z2, Z2 + 2.20)

# 2. Sister 2 Bedroom (X = 0.22..3.72, Y = 7.55..11.20) & Youngest Sister Bedroom (X = 0.22..3.72, Y = 11.20..14.85)
add_wall_with_openings(col_fl2_arch, "Part_Fl2_Sis2Front", 'X', 7.55, 0.12, 0.22, 3.72, Z2, H2, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl2_arch, "Part_Fl2_Sis2Hall", 'Y', 3.72, 0.12, 7.55, 11.20, Z2, H2, [(7.80, 8.65, Z2, Z2 + 2.25), (8.95, 10.65, Z2 + 0.95, Z2 + 2.40)], "Mat_WallWarmWhite")
add_interior_door(col_fl2_arch, "Door_Sister2", 'Y', 3.72, 0.12, 7.80, 8.65, Z2, Z2 + 2.25, open_angle=-0.35)
add_framed_window(col_fl2_arch, "Win_Sister2Hall", 'Y', 3.72, 0.12, 8.95, 10.65, Z2 + 0.95, Z2 + 2.40)

add_wall_with_openings(col_fl2_arch, "Part_Fl2_SisDivide", 'X', 11.20, 0.12, 0.22, 3.72, Z2, H2, [], "Mat_WallWarmWhite")
add_wall_with_openings(col_fl2_arch, "Part_Fl2_YoungestHall", 'Y', 3.72, 0.12, 11.20, 14.85, Z2, H2, [(11.45, 12.30, Z2, Z2 + 2.25), (12.60, 14.25, Z2 + 0.95, Z2 + 2.40)], "Mat_WallWarmWhite")
add_interior_door(col_fl2_arch, "Door_Youngest", 'Y', 3.72, 0.12, 11.45, 12.30, Z2, Z2 + 2.25, open_angle=-0.35)
add_framed_window(col_fl2_arch, "Win_YoungestHall", 'Y', 3.72, 0.12, 12.60, 14.25, Z2 + 0.95, Z2 + 2.40)

# Rear Wall separating Floor 2 Interior from Rear Gym/Laundry Balcony (Y = 14.85)
add_wall_with_openings(col_fl2_arch, "Floor2_RearWall", 'X', 14.85, 0.20, 0.0, 5.0, Z2, H2, [(3.85, 4.70, Z2, Z2 + 2.35), (1.40, 2.80, Z2 + 0.95, Z2 + 2.35)], "Mat_WallWarmWhite")
add_framed_window(col_fl2_arch, "Door_Fl2_RearBalcony", 'X', 14.85, 0.20, 3.85, 4.70, Z2, Z2 + 2.35)
add_framed_window(col_fl2_arch, "Win_Fl2_YoungestRear", 'X', 14.85, 0.20, 1.40, 2.80, Z2 + 0.95, Z2 + 2.35)

# Front & Rear Balcony Glass Railings & West Sun-Louvers
add_box(col_fl2_arch, "BalconyFront_GlassRail", 0.0, -1.60, Z2, 5.0, -1.55, Z2 + 1.12, "Mat_BalconyGlassBronze")
add_box(col_fl2_arch, "BalconyFront_Handrail", 0.0, -1.62, Z2 + 1.10, 5.0, -1.53, Z2 + 1.16, "Mat_BronzeGateMetal", bevel=0.01)
# Architectural West-Facing Wooden Sunshade Louvers (rotating 45 deg louvers on right/front of balcony)
for lv in range(12):
    lx = 3.20 + lv * 0.14
    add_box(col_fl2_arch, f"Facade_WestLouver_{lv}", lx, -1.58, Z2 + 1.16, lx + 0.08, -1.46, H2, "Mat_WoodLouverFacade", rot_z=0.55)

# ---------------------------------------------------------------------------
# 9. FLOOR 2 ULTRA-DETAILED INTERIOR FURNITURE (MASTER, SISTERS, BALCONIES)
# ---------------------------------------------------------------------------
# A. FRONT STAR-GAZING BALCONY (Ban công ngắm sao, tắm trăng & Guitar Acoustic)
for lc_i, lx in enumerate([0.95, 2.25]):
    # Woven Rattan Lounge Chair with Cream Cushions
    add_box(col_fl2_furn, f"Balcony_LoungeBase_{lc_i}", lx - 0.38, -1.25, Z2 + 0.08, lx + 0.38, -0.45, Z2 + 0.32, "Mat_RattanWeave", bevel=0.025)
    add_box(col_fl2_furn, f"Balcony_LoungeBack_{lc_i}", lx - 0.38, -0.55, Z2 + 0.32, lx + 0.38, -0.38, Z2 + 0.78, "Mat_RattanWeave", bevel=0.025)
    add_box(col_fl2_furn, f"Balcony_LoungePad_{lc_i}", lx - 0.34, -1.22, Z2 + 0.32, lx + 0.34, -0.52, Z2 + 0.42, "Mat_BeddingCream", bevel=0.03)
    add_box(col_fl2_furn, f"Balcony_LoungePillow_{lc_i}", lx - 0.25, -0.62, Z2 + 0.42, lx + 0.25, -0.48, Z2 + 0.68, "Mat_CushionTerracotta" if lc_i == 0 else "Mat_CushionSage", bevel=0.03)
add_cyl(col_fl2_furn, "Balcony_TeaTable", 1.60, -0.92, Z2, Z2 + 0.42, 0.24, 0.26, "Mat_RattanWeave")
add_cyl(col_fl2_furn, "Balcony_Lantern", 1.60, -0.92, Z2 + 0.42, Z2 + 0.58, 0.07, 0.06, "Mat_WarmLED")
# Acoustic Guitar on Stand (at X = 2.95, Y = -0.85)
add_cyl(col_fl2_furn, "Guitar_BodyBot", 2.95, -0.85, Z2 + 0.15, Z2 + 0.25, 0.19, 0.19, "Mat_WoodOakTable", rot=(math.pi / 2.2, 0, -0.4))
add_cyl(col_fl2_furn, "Guitar_BodyTop", 2.95, -0.82, Z2 + 0.35, Z2 + 0.44, 0.14, 0.14, "Mat_WoodOakTable", rot=(math.pi / 2.2, 0, -0.4))
add_box(col_fl2_furn, "Guitar_Neck", 2.92, -0.83, Z2 + 0.42, 2.98, -0.79, Z2 + 0.88, "Mat_WoodOakDark", rot_z=-0.4)
# Balcony Planter Box with Petunias
add_box(col_fl2_furn, "Balcony_Planter", 3.45, -1.50, Z2, 4.82, -1.18, Z2 + 0.38, "Mat_PlanterWood", bevel=0.01)
for fl_i in range(6):
    fx = 3.60 + fl_i * 0.21
    add_sphere(col_fl2_furn, f"Balcony_Foliage_{fl_i}", fx, -1.34, Z2 + 0.44, 0.12, 0.12, 0.10, "Mat_FoliageGreen", subdiv=1)
    add_sphere(col_fl2_furn, f"Balcony_Petunia_{fl_i}", fx, -1.36, Z2 + 0.52, 0.06, 0.06, 0.06, "Mat_FlowerPink" if fl_i % 2 == 0 else "Mat_FlowerYellow", subdiv=1)

# B. MASTER SUITE OF THE OWNER (Piano, Yoga & Meditation, King Bed, Glass Wardrobe, En-Suite Bath)
# 1. Upright Acoustic Piano Corner (X = 0.24..1.25, Y = 0.32..1.80)
build_upright_piano(col_fl2_furn, "Master_UprightPiano", 0.25, 1.06, Z2)
# Brass Floor Lamp beside Piano
add_cyl(col_fl2_furn, "Piano_FloorLampBase", 0.55, 0.26, Z2, Z2 + 0.04, 0.14, 0.14, "Mat_BrassWarm")
add_cyl(col_fl2_furn, "Piano_FloorLampStem", 0.55, 0.26, Z2 + 0.04, Z2 + 1.58, 0.014, 0.014, "Mat_BrassWarm")
add_cyl(col_fl2_furn, "Piano_FloorLampShade", 0.55, 0.26, Z2 + 1.48, Z2 + 1.66, 0.16, 0.10, "Mat_WarmLED")

# 2. Yoga & Meditation Sanctuary (X = 3.05..4.68, Y = 0.35..2.85)
add_box(col_fl2_furn, "Master_YogaMat", 3.35, 0.65, Z2, 4.05, 2.45, Z2 + 0.022, "Mat_YogaMatPastel", bevel=0.008)
add_cyl(col_fl2_furn, "Master_RolledYogaMat", 4.35, 0.55, Z2 + 0.06, Z2 + 0.68, 0.065, 0.065, "Mat_CushionSage", rot=(0, math.pi / 2, 0))
# Round Meditation Cushion (Zafu) & Tibetan Singing Bowl on Low Zen Tray
add_cyl(col_fl2_furn, "Master_ZafuCushion", 3.70, 2.75, Z2, Z2 + 0.15, 0.24, 0.25, "Mat_CushionSage")
add_box(col_fl2_furn, "Master_ZenTray", 4.25, 2.55, Z2, 4.62, 2.95, Z2 + 0.08, "Mat_WoodOakDark", bevel=0.008)
add_cyl(col_fl2_furn, "Master_SingingBowl", 4.43, 2.75, Z2 + 0.08, Z2 + 0.16, 0.06, 0.085, "Mat_BuddhaGold")
# Full-Length Arched Floor Mirror & Monstera Plant
add_box(col_fl2_furn, "Master_FloorMirrorFrame", 4.58, 1.35, Z2, 4.64, 2.05, Z2 + 1.78, "Mat_BrassWarm", bevel=0.015)
add_box(col_fl2_furn, "Master_FloorMirrorGlass", 4.56, 1.39, Z2 + 0.04, 4.58, 2.01, Z2 + 1.74, "Mat_MirrorSilver")
build_potted_plant(col_fl2_furn, "Master_YogaMonstera", 4.45, 0.52, Z2, scale=1.05)

# 3. Master King Bed & Bedside Pendant Lights (X = 0.25..2.45, Y = 2.45..4.45)
build_detailed_bed(col_fl2_furn, "Master_KingBed", 1.30, 3.35, Z2, width=1.75, length=2.05, facing="+X", duvet_mat="Mat_BeddingWhite", accent_mat="Mat_CushionNavy")
build_nightstand_with_lamp(col_fl2_furn, "Master_Nightstand_L", 0.50, 2.20, Z2)
build_nightstand_with_lamp(col_fl2_furn, "Master_Nightstand_R", 0.50, 4.48, Z2)
# Walk-in Glass Wardrobe with Interior LED & Hanging Garments (along Y = 4.65..5.13, X = 0.28..2.22)
build_wardrobe(col_fl2_furn, "Master_GlassWardrobe", 0.28, 4.65, Z2, 2.22, 5.13, height=2.65, glass_doors=True)

# 4. Master En-Suite Bathroom (Freestanding Bathtub, Rain Shower, Vanity, LED Mirror, Toilet)
build_bathroom_fixtures(col_fl2_furn, "Master_EnsuiteBath", 3.17, 3.32, Z2, 4.78, 5.15, has_bathtub=True)

# C. SISTER 2 BEDROOM (Phòng Ngủ Chị Hai - X = 0.22..3.72, Y = 7.67..11.20)
build_detailed_bed(col_fl2_furn, "Sister2_QueenBed", 1.35, 9.30, Z2, width=1.60, length=2.0, facing="+X", duvet_mat="Mat_BeddingCream", accent_mat="Mat_CushionRose")
build_nightstand_with_lamp(col_fl2_furn, "Sister2_Nightstand_L", 0.55, 8.25, Z2)
build_nightstand_with_lamp(col_fl2_furn, "Sister2_Nightstand_R", 0.55, 10.35, Z2)
build_wardrobe(col_fl2_furn, "Sister2_Wardrobe", 0.35, 10.62, Z2, 2.50, 11.18, height=2.55, glass_doors=False)
build_desk_and_chair(col_fl2_furn, "Sister2_VanityDesk", 3.15, 9.25, Z2, width=1.20, depth=0.55, facing="+X")

# D. YOUNGEST SISTER BEDROOM (Phòng Ngủ Em Út - X = 0.22..3.72, Y = 11.32..14.85)
build_detailed_bed(col_fl2_furn, "Youngest_QueenBed", 1.35, 12.95, Z2, width=1.60, length=2.0, facing="+X", duvet_mat="Mat_BeddingWhite", accent_mat="Mat_CushionSage")
build_nightstand_with_lamp(col_fl2_furn, "Youngest_Nightstand_L", 0.55, 11.90, Z2)
build_nightstand_with_lamp(col_fl2_furn, "Youngest_Nightstand_R", 0.55, 14.00, Z2)
build_wardrobe(col_fl2_furn, "Youngest_Wardrobe", 0.35, 14.28, Z2, 2.50, 14.83, height=2.55, glass_doors=False)
build_desk_and_chair(col_fl2_furn, "Youngest_StudyDesk", 3.15, 12.95, Z2, width=1.25, depth=0.55, facing="+X")

# E. REAR BALCONY: HOME GYM & SMART ELEVATING LAUNDRY RACK (X = 0.0..5.0, Y = 15.05..18.0)
# 1. Motorized Treadmill (Máy chạy bộ)
add_box(col_fl2_furn, "Gym_TreadmillDeck", 0.55, 15.65, Z2 + 0.06, 1.35, 17.35, Z2 + 0.18, "Mat_MetalMatteBlack", bevel=0.02)
add_box(col_fl2_furn, "Gym_TreadmillBelt", 0.63, 15.75, Z2 + 0.18, 1.27, 17.25, Z2 + 0.195, "Mat_TireRubber")
for tx in [0.58, 1.32]:
    add_cyl(col_fl2_furn, f"Gym_TreadmillPost_{tx:.2f}", tx, 17.15, Z2 + 0.18, Z2 + 1.25, 0.025, 0.025, "Mat_MetalMatteBlack")
add_box(col_fl2_furn, "Gym_TreadmillConsole", 0.55, 17.05, Z2 + 1.20, 1.35, 17.32, Z2 + 1.38, "Mat_MetalMatteBlack", bevel=0.015)
# 2. Adjustable Workout Bench & Dumbbell Rack
add_box(col_fl2_furn, "Gym_BenchBase", 1.85, 15.80, Z2, 2.30, 17.05, Z2 + 0.38, "Mat_MetalMatteBlack", bevel=0.01)
add_box(col_fl2_furn, "Gym_BenchPad", 1.88, 15.82, Z2 + 0.38, 2.27, 17.02, Z2 + 0.45, "Mat_WoodOakDark", bevel=0.02)
add_box(col_fl2_furn, "Gym_DumbbellRack", 2.55, 16.20, Z2, 2.95, 16.95, Z2 + 0.75, "Mat_MetalMatteBlack", bevel=0.01)
for db in range(3):
    dz = Z2 + 0.22 + db * 0.22
    add_cyl(col_fl2_furn, f"Gym_Dumbbell_{db}", 2.75, 16.55, dz, dz + 0.08, 0.07, 0.07, "Mat_MetalMatteBlack", rot=(0, math.pi / 2, 0))

# 3. Smart Ceiling Clothes Drying Rack (Giàn phơi thông minh nâng hạ + Quần áo treo)
for r_bar in [15.95, 16.55]:
    add_cyl(col_fl2_furn, f"Laundry_SmartRod_{r_bar:.2f}", 3.95, r_bar, H2 - 0.85, H2 - 0.83, 0.018, 0.018, "Mat_MetalStainless", rot=(0, math.pi / 2, 0))
    for g_i in range(5):
        gx = 3.35 + g_i * 0.28
        g_col = ["Mat_BeddingWhite", "Mat_CushionSage", "Mat_CushionMustard", "Mat_CushionRose", "Mat_CushionNavy"][g_i]
        add_box(col_fl2_furn, f"Laundry_Garment_{r_bar:.1f}_{g_i}", gx, r_bar - 0.03, H2 - 1.55, gx + 0.04, r_bar + 0.03, H2 - 0.88, g_col, bevel=0.01)

# Rear Balcony Railing & Invisible Stainless Cable Safety Net (Lưới an toàn cáp inox)
add_box(col_fl2_arch, "BalconyRear_GlassRail", 0.0, 17.92, Z2, 5.0, 17.98, Z2 + 1.15, "Mat_BalconyGlassBronze")
for net_i in range(24):
    nx = 0.15 + net_i * 0.20
    add_cyl(col_fl2_arch, f"SafetyNet_Cable_{net_i}", nx, 17.95, Z2 + 1.15, H2, 0.004, 0.004, "Mat_MetalStainless")

# ---------------------------------------------------------------------------
# 10. ROOF SLAB, SKYLIGHT, WATER TANK, SOLAR WATER HEATER & PV PANELS
# ---------------------------------------------------------------------------
ZR = 7.38
# Roof Slab with Central Skylight Opening (X = 0.30..2.20, Y = 5.10..7.45)
add_box(col_roof, "Roof_Slab_Front", 0.0, -1.60, H2, 5.0, 5.10, ZR, "Mat_WallWarmWhite")
add_box(col_roof, "Roof_Slab_MidRight", 2.20, 5.10, H2, 5.0, 7.45, ZR, "Mat_WallWarmWhite")
add_box(col_roof, "Roof_Slab_Rear", 0.0, 7.45, H2, 5.0, 18.0, ZR, "Mat_WallWarmWhite")

# Roof Parapet Wall
add_box(col_roof, "Roof_Parapet_Front", -0.05, -1.65, ZR, 5.05, -1.48, ZR + 0.65, "Mat_WallFacadeWarm")
add_box(col_roof, "Roof_Parapet_Right", 4.85, -1.65, ZR, 5.05, 18.05, ZR + 0.65, "Mat_WallFacadeWarm")
add_box(col_roof, "Roof_Parapet_Rear", -0.05, 17.88, ZR, 5.05, 18.05, ZR + 0.65, "Mat_WallFacadeWarm")

# Central Glass Skylight Hood with Ventilation Louvers (Giếng trời trung tâm)
add_box(col_roof, "Skylight_CurbL", 0.25, 5.05, ZR, 0.35, 7.50, ZR + 0.55, "Mat_MetalMatteBlack")
add_box(col_roof, "Skylight_CurbR", 2.15, 5.05, ZR, 2.25, 7.50, ZR + 0.55, "Mat_MetalMatteBlack")
add_box(col_roof, "Skylight_CurbF", 0.25, 5.05, ZR, 2.25, 5.15, ZR + 0.55, "Mat_MetalMatteBlack")
add_box(col_roof, "Skylight_CurbB", 0.25, 7.40, ZR, 2.25, 7.50, ZR + 0.55, "Mat_MetalMatteBlack")
add_box(col_roof, "Skylight_TopGlass", 0.18, 4.98, ZR + 0.55, 2.32, 7.58, ZR + 0.62, "Mat_GlassClear")

# Horizontal Stainless Steel 1500L Water Tank on Elevated Frame
add_box(col_roof, "WaterTank_Stand", 0.45, 9.20, ZR, 1.95, 11.20, ZR + 0.35, "Mat_MetalMatteBlack")
# Make tank body 1.9m long along Y
bm_tank = bmesh.new()
bmesh.ops.create_cone(bm_tank, cap_ends=True, cap_tris=False, segments=28, radius1=0.58, radius2=0.58, depth=1.85)
link_mesh_obj(col_roof, "WaterTank_Body", bm_tank, "Mat_MetalStainless", loc=(1.20, 10.20, ZR + 0.93), rot=(math.pi / 2, 0, 0), smooth=True)

# Solar Water Heater (Thái Dương Năng 16 ống chân không)
bm_swh = bmesh.new()
bmesh.ops.create_cone(bm_swh, cap_ends=True, cap_tris=False, segments=24, radius1=0.26, radius2=0.26, depth=1.90)
link_mesh_obj(col_roof, "SolarHeater_Tank", bm_swh, "Mat_MetalStainless", loc=(3.55, 9.60, ZR + 1.05), rot=(0, math.pi / 2, 0), smooth=True)
for tube_i in range(16):
    tx = 2.70 + tube_i * 0.112
    bm_tube = bmesh.new()
    bmesh.ops.create_cone(bm_tube, cap_ends=True, cap_tris=False, segments=12, radius1=0.032, radius2=0.032, depth=1.55)
    link_mesh_obj(col_roof, f"SolarHeater_Tube_{tube_i}", bm_tube, "Mat_SolarPVPanels", loc=(tx, 10.25, ZR + 0.58), rot=(math.radians(32), 0, 0), smooth=True)

# 6 Tilted Solar PV Panels
for sp in range(6):
    spy = 12.0 + sp * 0.92
    add_box(col_roof, f"Solar_PV_Frame_{sp}", 0.55, spy, ZR + 0.18, 4.45, spy + 0.80, ZR + 0.24, "Mat_MetalStainless")
    add_box(col_roof, f"Solar_PV_Cells_{sp}", 0.60, spy + 0.04, ZR + 0.24, 4.40, spy + 0.76, ZR + 0.26, "Mat_SolarPVPanels")

# Hide the optional full left cutaway wall by default so opening the .blend immediately reveals the rich interior!
col_enclosure.hide_viewport = True
col_enclosure.hide_render = True

# ---------------------------------------------------------------------------
# 11. LIGHTING, WORLD SKY & INTERIOR/EXTERIOR CAMERAS
# ---------------------------------------------------------------------------
scene = bpy.context.scene
world = scene.world
if not world:
    world = bpy.data.worlds.new("Fullhouse_World")
    scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.78, 0.86, 0.96, 1.0)
    bg_node.inputs["Strength"].default_value = 1.15

# Warm Golden-Hour Sun Light
sun_data = bpy.data.lights.new(name="Sun_GoldenHour", type='SUN')
sun_data.energy = 4.2
sun_data.color = (1.0, 0.95, 0.86)
sun_obj = bpy.data.objects.new(name="Sun_GoldenHour", object_data=sun_data)
sun_obj.location = (18.0, -16.0, 24.0)
sun_obj.rotation_euler = (math.radians(52), math.radians(18), math.radians(-35))
col_lights.objects.link(sun_obj)

def add_warm_light(name, loc, energy=120.0, color=(1.0, 0.82, 0.56), size=0.6):
    ld = bpy.data.lights.new(name=name, type='POINT')
    ld.energy = energy
    ld.color = color
    ld.shadow_soft_size = size
    lo = bpy.data.objects.new(name=name, object_data=ld)
    lo.location = loc
    col_lights.objects.link(lo)
    return lo

add_warm_light("Light_Porch", (3.75, -2.35, 2.55), 90.0)
add_warm_light("Light_Living", (2.25, 1.95, 3.15), 180.0)
add_warm_light("Light_Altar", (3.85, 4.18, 2.65), 120.0, (1.0, 0.78, 0.35))
add_warm_light("Light_StairZen", (1.25, 6.25, 2.85), 110.0)
add_warm_light("Light_ParentsBed", (2.85, 9.50, 3.15), 150.0)
add_warm_light("Light_ReadingRoom", (2.85, 12.90, 3.15), 150.0)
add_warm_light("Light_KitchenDining", (2.65, 16.00, 3.15), 200.0)
add_warm_light("Light_MasterSuite", (2.35, 2.50, 6.75), 200.0)
add_warm_light("Light_MasterBath", (3.95, 4.25, 6.65), 110.0)
add_warm_light("Light_Sister2Bed", (2.85, 9.35, 6.75), 150.0)
add_warm_light("Light_YoungestBed", (2.85, 13.00, 6.75), 150.0)

def add_camera_look_at(name, eye, target, lens=32.0):
    cd = bpy.data.cameras.new(name=name)
    cd.lens = lens
    cd.clip_start = 0.05
    cd.clip_end = 200.0
    co = bpy.data.objects.new(name=name, object_data=cd)
    co.location = eye
    dx = target[0] - eye[0]
    dy = target[1] - eye[1]
    dz = target[2] - eye[2]
    dist_xy = math.hypot(dx, dy)
    rx = math.pi / 2.0 + math.atan2(dz, dist_xy)
    rz = math.atan2(dy, dx) - math.pi / 2.0
    co.rotation_euler = (rx, 0.0, rz)
    col_lights.objects.link(co)
    return co

cam_dollhouse = add_camera_look_at("Cam_01_Dollhouse_Cutaway", (-15.5, 6.5, 10.5), (2.8, 8.5, 3.2), lens=28.0)
cam_living = add_camera_look_at("Cam_02_Living_And_Altar", (0.75, 2.55, 1.55), (4.20, 3.55, 1.48), lens=20.0)
cam_kitchen = add_camera_look_at("Cam_03_Kitchen_Baking_Island", (4.5, 14.6, 1.95), (1.8, 16.2, 1.05), lens=21.0)
cam_master = add_camera_look_at("Cam_04_Master_Piano_Yoga", (2.6, 0.35, 5.55), (1.6, 3.2, 4.45), lens=20.0)
cam_front = add_camera_look_at("Cam_05_Exterior_Facade", (10.5, -14.5, 6.2), (2.8, 2.0, 3.2), lens=32.0)
cam_sofa_out = add_camera_look_at("Cam_06_Sofa_Look_Outside", (0.95, 2.15, 1.35), (3.55, -2.25, 1.05), lens=22.0)

scene.camera = cam_dollhouse

# ---------------------------------------------------------------------------
# 12. CONFIGURE BLENDER VIEWPORT SHADING & SAVE .BLEND + .OBJ/.MTL
# ---------------------------------------------------------------------------
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    space.shading.color_type = 'MATERIAL'
                    space.shading.show_cavity = True
                    space.shading.show_shadows = True

save_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else r"C:\Users\Administrator\.gemini\antigravity\scratch\myhome"
blend_path = os.path.join(save_dir, "Fullhouse_Model.blend")
obj_path = os.path.join(save_dir, "Fullhouse_Model.obj")

bpy.ops.wm.save_as_mainfile(filepath=blend_path)
try:
    bpy.ops.wm.obj_export(filepath=obj_path, export_materials=True, forward_axis='NEGATIVE_Z', up_axis='Y')
except Exception as e:
    print("OBJ export warning:", e)

print("=" * 70)
print(f"SUCCESS: Ultra-detailed Fullhouse model saved to {blend_path}")
print(f"Total objects created: {len(bpy.data.objects)}")
print("=" * 70)
