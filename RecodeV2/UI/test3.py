import ctypes, os, math  # os is new one

MAX_BRUSH_LIGHTMAP_DIM_WITHOUT_BORDER = 32
MAX_BRUSH_LIGHTMAP_DIM_INCLUDING_BORDER = 35
MAX_DISP_LIGHTMAP_DIM_WITHOUT_BORDER = 128
MAX_DISP_LIGHTMAP_DIM_INCLUDING_BORDER = 131
MAX_LIGHTMAP_DIM_WITHOUT_BORDER = MAX_DISP_LIGHTMAP_DIM_WITHOUT_BORDER
MAX_LIGHTMAP_DIM_INCLUDING_BORDER = MAX_DISP_LIGHTMAP_DIM_INCLUDING_BORDER

FLT_EPSILON = 1e-5
DIST_EPSILON = 0.03125
MAX_SURFINFO_VERTS = 32
BSPVERSION = 19
HEADER_LUMPS = 64
MAX_POLYGONS = 50120
MAX_MOD_KNOWN = 512
MAX_MAP_MODELS = 1024
MAX_MAP_BRUSHES = 8192
MAX_MAP_ENTITIES = 4096
MAX_MAP_ENTSTRING = 256 * 1024
MAX_MAP_NODES = 65536
MAX_MAP_TEXINFO = 12288
MAX_MAP_TEXDATA = 2048
MAX_MAP_LEAFBRUSHES = 65536
MIN_MAP_DISP_POWER = 2
MAX_MAP_DISP_POWER = 4
MAX_MAP_SURFEDGES = 512000
MAX_DISP_CORNER_NEIGHBORS = 4

# These are stored in a short in the engine now.  Don't use more than 16 bits
SURF_LIGHT = 0x0001  # value will hold the light strength
SURF_SLICK = 0x0002  # effects game physics
SURF_SKY = 0x0004  # don't draw, but add to skybox
SURF_WARP = 0x0008  # turbulent water warp
SURF_TRANS = 0x0010
SURF_WET = 0x0020  # the surface is wet
SURF_FLOWING = 0x0040  # scroll towards angle
SURF_NODRAW = 0x0080  # don't bother referencing the texture
SURF_Hint32_t = 0x0100  # make a primary bsp splitter
SURF_SKIP = 0x0200  # completely ignore, allowing non-closed brushes
SURF_NOLIGHT = 0x0400  # Don't calculate light
SURF_BUMPLIGHT = 0x0800  # calculate three lightmaps for the surface for bumpmapping
SURF_HITBOX = 0x8000  # surface is part of a hitbox

CONTENTS_EMPTY = 0  # No contents
CONTENTS_SOLID = 0x1  # an eye is never valid in a solid
CONTENTS_WINDOW = 0x2  # translucent, but not watery (glass)
CONTENTS_AUX = 0x4
CONTENTS_GRATE = (
    0x8  # alpha-tested "grate" textures.  Bullets/sight pass through, but solids don't
)
CONTENTS_SLIME = 0x10
CONTENTS_WATER = 0x20
CONTENTS_MIST = 0x40
CONTENTS_OPAQUE = 0x80  # things that cannot be seen through (may be non-solid though)
LAST_VISIBLE_CONTENTS = 0x80
ALL_VISIBLE_CONTENTS = LAST_VISIBLE_CONTENTS | LAST_VISIBLE_CONTENTS - 1
CONTENTS_TESTFOGVOLUME = 0x100
CONTENTS_UNUSED3 = 0x200
CONTENTS_UNUSED4 = 0x400
CONTENTS_UNUSED5 = 0x800
CONTENTS_UNUSED6 = 0x1000
CONTENTS_UNUSED7 = 0x2000
CONTENTS_MOVEABLE = 0x4000  # hits entities which are MOVETYPE_PUSH (doors, plats, etc.)
# remaining contents are non-visible, and don't eat brushes
CONTENTS_AREAPORTAL = 0x8000
CONTENTS_PLAYERCLIP = 0x10000
CONTENTS_MONSTERCLIP = 0x20000
# currents can be added to any other contents, and may be mixed
CONTENTS_CURRENT_0 = 0x40000
CONTENTS_CURRENT_90 = 0x80000
CONTENTS_CURRENT_180 = 0x100000
CONTENTS_CURRENT_270 = 0x200000
CONTENTS_CURRENT_UP = 0x400000
CONTENTS_CURRENT_DOWN = 0x800000
CONTENTS_ORIGIN = 0x1000000  # removed before bsping an entity
CONTENTS_MONSTER = 0x2000000  # should never be on a brush, only in game
CONTENTS_DEBRIS = 0x4000000
CONTENTS_DETAIL = 0x8000000  # brushes to be added after vis leafs
CONTENTS_TRANSLUCENT = 0x10000000  # int32_t set if any surface has trans
CONTENTS_LADDER = 0x20000000
CONTENTS_HITBOX = 0x40000000  # use accurate hitboxes on trace

# everyhting
MASK_ALL = 0xFFFFFFFF  # everything that is normally solid
MASK_SOLID = (
    CONTENTS_SOLID
    | CONTENTS_MOVEABLE
    | CONTENTS_WINDOW
    | CONTENTS_MONSTER
    | CONTENTS_GRATE
)  # everything that blocks player movement
MASK_PLAYERSOLID = (
    CONTENTS_SOLID
    | CONTENTS_MOVEABLE
    | CONTENTS_PLAYERCLIP
    | CONTENTS_WINDOW
    | CONTENTS_MONSTER
    | CONTENTS_GRATE
)  # blocks npc movement
MASK_NPCSOLID = (
    CONTENTS_SOLID
    | CONTENTS_MOVEABLE
    | CONTENTS_MONSTERCLIP
    | CONTENTS_WINDOW
    | CONTENTS_MONSTER
    | CONTENTS_GRATE
)  # water physics in these contents
MASK_WATER = (
    CONTENTS_WATER | CONTENTS_MOVEABLE | CONTENTS_SLIME
)  # everything that blocks line of sight
MASK_OPAQUE = (
    CONTENTS_SOLID | CONTENTS_MOVEABLE | CONTENTS_SLIME | CONTENTS_OPAQUE
)  # bullets see these as solid
MASK_SHOT = (
    CONTENTS_SOLID
    | CONTENTS_MOVEABLE
    | CONTENTS_MONSTER
    | CONTENTS_WINDOW
    | CONTENTS_DEBRIS
    | CONTENTS_HITBOX
)  # non-raycasted weapons see this as solid (includes grates)
MASK_SHOT_HULL = (
    CONTENTS_SOLID
    | CONTENTS_MOVEABLE
    | CONTENTS_MONSTER
    | CONTENTS_WINDOW
    | CONTENTS_DEBRIS
    | CONTENTS_GRATE
)  # everything normally solid, except monsters (world+brush only)
MASK_SOLID_BRUSHONLY = (
    CONTENTS_SOLID | CONTENTS_MOVEABLE | CONTENTS_WINDOW | CONTENTS_GRATE
)  # everything normally solid for player movement, except monsters (world+brush only)
MASK_PLAYERSOLID_BRUSHONLY = (
    CONTENTS_SOLID
    | CONTENTS_MOVEABLE
    | CONTENTS_WINDOW
    | CONTENTS_PLAYERCLIP
    | CONTENTS_GRATE
)  # everything normally solid for npc movement, except monsters (world+brush only)
MASK_NPCSOLID_BRUSHONLY = (
    CONTENTS_SOLID
    | CONTENTS_MOVEABLE
    | CONTENTS_WINDOW
    | CONTENTS_MONSTERCLIP
    | CONTENTS_GRATE
)  # just the world, used for route rebuilding
MASK_NPCWORLDSTATIC = (
    CONTENTS_SOLID | CONTENTS_WINDOW | CONTENTS_MONSTERCLIP | CONTENTS_GRATE
)  # UNDONE: This is untested, any moving water
MASK_CURRENT = (
    CONTENTS_CURRENT_0
    | CONTENTS_CURRENT_90
    | CONTENTS_CURRENT_180
    | CONTENTS_CURRENT_270
    | CONTENTS_CURRENT_UP
    | CONTENTS_CURRENT_DOWN
)
MASK_DEADSOLID = CONTENTS_SOLID | CONTENTS_PLAYERCLIP | CONTENTS_WINDOW | CONTENTS_GRATE


LUMP_ENTITIES = 0
LUMP_PLANES = 1
LUMP_TEXDATA = 2
LUMP_VERTEXES = 3
LUMP_VISIBILITY = 4
LUMP_NODES = 5
LUMP_TEXINFO = 6
LUMP_FACES = 7
LUMP_LIGHTING = 8
LUMP_OCCLUSION = 9
LUMP_LEAFS = 10
LUMP_EDGES = 12
LUMP_SURFEDGES = 13
LUMP_MODELS = 14
LUMP_WORLDLIGHTS = 15
LUMP_LEAFFACES = 16
LUMP_LEAFBRUSHES = 17
LUMP_BRUSHES = 18
LUMP_BRUSHSIDES = 19
LUMP_AREAS = 20
LUMP_AREAPORTALS = 21
LUMP_PORTALS = 22
LUMP_CLUSTERS = 23
LUMP_PORTALVERTS = 24
LUMP_CLUSTERPORTALS = 25
LUMP_DISPINFO = 26
LUMP_ORIGINALFACES = 27
LUMP_PHYSCOLLIDE = 29
LUMP_VERTNORMALS = 30
LUMP_VERTNORMALINDICES = 31
LUMP_DISP_LIGHTMAP_ALPHAS = 32
LUMP_DISP_VERTS = 33
LUMP_DISP_LIGHTMAP_SAMPLE_POSITIONS = 34
LUMP_GAME_LUMP = 35
LUMP_LEAFWATERDATA = 36
LUMP_PRIMITIVES = 37
LUMP_PRIMVERTS = 38
LUMP_PRIMINDICES = 39
LUMP_PAKFILE = 40
LUMP_CLIPPORTALVERTS = 41
LUMP_CUBEMAPS = 42
LUMP_TEXDATA_STRING_DATA = 43
LUMP_TEXDATA_STRING_TABLE = 44
LUMP_OVERLAYS = 45
LUMP_LEAFMINDISTTOWATER = 46
LUMP_FACE_MACRO_TEXTURE_INFO = 47
LUMP_DISP_TRIS = 48

id2size = {5: 32, 1: 20, 10: 48, 19: 8, 16: 4, 7: 58, 16: 4, 17: 4}


class Vector3(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float), ("y", ctypes.c_float), ("z", ctypes.c_float)]

    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def dot(self, dot):
        return self.x * dot.x + self.y * dot.y + self.z * dot.z

    def distance_from(self, other):
        return math.sqrt(
            ((self.x - other.x) ** 2)
            + ((self.y - other.y) ** 2)
            + ((self.z - other.z) ** 2)
        )

    def normalize(self):
        size = self.length()
        if size != 0:
            self.x /= size
            self.y /= size
            self.z /= size

    def get(self, id):
        if id == 0:
            return self.x
        elif id == 1:
            return self.y
        elif id == 2:
            return self.z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __truediv__(self, other):
        if isinstance(other, Vector3):  # Vector division
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        elif isinstance(other, int):  # Divide by a sigle number
            if other != 0:
                self.x /= other
                self.y /= other
                self.z /= other
        return self

    def __mul__(self, other):
        if isinstance(other, Vector3):  # Vector division
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif isinstance(other, int) or isinstance(
            other, float
        ):  # Divide by a sigle number
            if other != 0:
                self.x *= other
                self.y *= other
                self.z *= other
        return self


class lump_t(ctypes.Structure):
    _fields_ = [
        ("m_Fileofs", ctypes.c_int),  # 0x0
        ("m_Filelen", ctypes.c_int),  # 0x4
        ("m_Version", ctypes.c_int),  # 0x8
        ("m_FourCC", ctypes.c_char * 4),
    ]  # 0xC        #Size=0x10


class dheader_t(ctypes.Structure):
    _fields_ = [
        ("m_Ident", ctypes.c_int),  # 0x000
        ("m_Version", ctypes.c_int),  # 0x004
        ("m_Lumps", lump_t * HEADER_LUMPS),  # 0x008
        ("m_MapRevision", ctypes.c_int),
    ]  # 0x408     #Size=0x40C


class dplane_t(ctypes.Structure):
    _fields_ = [
        ("m_Normal", Vector3),  # 0x00
        ("m_Distance", ctypes.c_float),  # 0x0C
        ("m_Type", ctypes.c_int),
    ]  # 0x10      #Size=0x14


class cplane_t(ctypes.Structure):
    _fields_ = [
        ("m_Normal", Vector3),  # 0x00
        ("m_Distance", ctypes.c_float),  # 0x0C
        ("m_Type", ctypes.c_int),  # 0x10
        ("m_SignBits", ctypes.c_int),
    ]  # 0x11
    # (str(m_Pad[0x2]), ctypes.c_int)] # 0x12      #Size=0x14


class dedge_t(ctypes.Structure):
    _fields_ = [("m_V", ctypes.c_ushort * 2)]  # 0x0       #Size=0x4


class mvertex_t(ctypes.Structure):
    _fields_ = [("m_Position", Vector3)]  # 0x0     #Size=0xC


class dleaf_t(ctypes.Structure):
    _fields_ = [
        ("m_Contents", ctypes.c_int),  # 0x00
        ("m_Cluster", ctypes.c_short),  # 0x04
        ("m_Mins", ctypes.c_short * 3),  # 0x1A
        ("m_Maxs", ctypes.c_short * 3),  # 0x20
        ("m_Mins", ctypes.c_short * 3),  # 0x1A
        ("m_Maxs", ctypes.c_short * 3),  # 0x20
        ("m_Firstleafface", ctypes.c_ushort),  # 0x26
        ("m_Numleaffaces", ctypes.c_ushort),  # 0x28
        ("m_Firstleafbrush", ctypes.c_ushort),  # 0x2A
        ("m_Numleafbrushes", ctypes.c_ushort),  # 0x2C
        ("m_LeafWaterDataID", ctypes.c_short),
    ]  # 0x2E       #Size=0x30


class dnode_t(ctypes.Structure):
    _fields_ = [
        ("m_Planenum", ctypes.c_int),  # 0x00
        ("m_Children", ctypes.c_int * 2),  # 0x04
        ("m_Mins", ctypes.c_short * 3),  # 0x0C
        ("m_Maxs", ctypes.c_short * 3),  # 0x12
        ("m_Firstface", ctypes.c_ushort),  # 0x18
        ("m_Numfaces", ctypes.c_ushort),  # 0x1A
        ("m_Area", ctypes.c_short),
    ]  # 0x1C
    # (str(m_Pad[ 0x2 ]), ctypes.c_int)]              # 0x1E       #Size=0x20


class snode_t(ctypes.Structure):
    def __init__(self):
        self.m_pPlane = cplane_t()
        self.m_LeafChildren = dleaf_t()


snode_t._fields_ = [
    ("m_PlaneNum", ctypes.c_int),  # 0x00
    # ('byte', ctypes.c_int), # 0x04
    ("m_Children", ctypes.c_int * 2),  # 0x08
    ("byte", ctypes.c_int),  # 0x10
    ("m_NodeChildren", ctypes.c_int),  # 0x14
    ("m_Mins", ctypes.c_short * 3),  # 0x18
    ("m_Maxs", ctypes.c_short * 3),  # 0x1E
    ("m_Firstface", ctypes.c_ushort),  # 0x24
    ("m_Numfaces", ctypes.c_ushort),  # 0x26
    ("m_Area", ctypes.c_short),
]  # 0x28


# ('m_Pad', ctypes.c_int)] # 0x2A                   #Size=0x2C
class dface_t(ctypes.Structure):
    _fields_ = [
        ("m_Planenum", ctypes.c_ushort),  # 0x00
        ("m_Side", ctypes.c_int),  # 0x02
        ("m_OnNode", ctypes.c_int),  # 0x03
        ("m_Firstedge", ctypes.c_int),  # 0x04
        ("m_Numedges", ctypes.c_short),  # 0x08
        ("m_Texinfo", ctypes.c_short),  # 0x0A
        ("m_Dispinfo", ctypes.c_short),  # 0x0C
        ("m_SurfaceFogVolumeID", ctypes.c_short),  # 0x0E
        ("m_Styles", ctypes.c_int * 4),  # 0x10
        ("m_Lightofs", ctypes.c_int),  # 0x18
        ("m_Area", ctypes.c_float),  # 0x1C
        ("m_LightmapTextureMinsInLuxels", ctypes.c_int * 2),  # 0x20
        ("m_LightmapTextureSizeInLuxels", ctypes.c_int * 2),  # 0x28
        ("m_OrigFace", ctypes.c_int),  # 0x30
        ("m_NumPrims", ctypes.c_ushort),  # 0x34
        ("m_FirstPrimID", ctypes.c_ushort),  # 0x36
        ("m_SmoothingGroups", ctypes.c_ushort),
    ]  # 0x38       #Size=0x3A


class dbrush_t(ctypes.Structure):
    _fields_ = [
        ("m_Firstside", ctypes.c_int),  # 0x0
        ("m_Numsides", ctypes.c_int),  # 0x4
        ("m_Contents", ctypes.c_int),
    ]  # 0x8      #Size=0xC


class dbrushside_t(ctypes.Structure):
    _fields_ = [
        ("m_Planenum", ctypes.c_ushort),  # 0x0
        ("m_Texinfo", ctypes.c_short),  # 0x2
        ("m_Dispinfo", ctypes.c_short),  # 0x4
        ("m_Bevel", ctypes.c_int),  # 0x6
        ("m_Thin", ctypes.c_int),
    ]  # 0x7  #Size=0x8


class texinfo_t(ctypes.Structure):
    _fields_ = [
        ("m_TextureVecs", (ctypes.c_float * 4) * 2),  # 0x00
        ("m_LightmapVecs", (ctypes.c_float * 4) * 2),  # 0x20
        ("m_Flags", ctypes.c_int),  # 0x40
        ("m_Texdata", ctypes.c_int),
    ]  # 0x44     #Size=0x48


class dsurfedge_t(ctypes.Structure):
    _fields_ = [("m_V", ctypes.c_int)]  # Size=0x4


class dleafface_t(ctypes.Structure):
    _fields_ = [("m_V", ctypes.c_ushort)]  # Size=0x4


class dleafbrush_t(ctypes.Structure):
    _fields_ = [("m_V", ctypes.c_ushort)]  # Size=0x4


class VPlane(ctypes.Structure):
    _fields_ = [("m_Origin", Vector3), ("m_Distance", ctypes.c_float)]

    def dist_to(location):
        return m_Origin.dot(location) - m_Distance

    def init(origin, distance):
        m_Origin = origin
        m_Distance = distance


class Polygon(ctypes.Structure):
    _fields_ = [
        ("m_Verts", Vector3 * MAX_SURFINFO_VERTS),
        ("m_nVerts", ctypes.c_size_t),
        ("m_Plane", VPlane),
        ("m_EdgePlanes", VPlane * MAX_SURFINFO_VERTS),
        ("m_Vec2D", Vector3 * MAX_SURFINFO_VERTS),
        ("m_Skip", ctypes.c_int),
    ]


class BSPFile(ctypes.Structure):
    _fields_ = [
        ("m_FileName", ctypes.c_char_p),
        ("m_BSPHeader", dheader_t),
        ("m_Vertexes_t", mvertex_t),
        ("m_Planes_t", cplane_t),
        ("m_Edges_t", dedge_t),
        ("m_Surfedges_t", dsurfedge_t),
        ("m_Leaves_t", dleaf_t),
        ("m_Nodes_t", snode_t),
        ("m_Surfaces_t", dface_t),
        ("m_Texinfos_t", texinfo_t),
        ("m_Brushes_t", dbrush_t),
        ("m_Brushsides_t", dbrushside_t),
        ("m_Leaffaces_t", dleafface_t),
        ("m_Leafbrushes_t", dleafbrush_t),
        ("m_Polygons_t", Polygon),
    ]

    def __init__(self):
        self.m_Vertexes = []
        self.m_Planes = []
        self.m_Edges = []
        self.m_Surfedges = []
        self.m_Leaves = []
        self.m_Nodes = []
        self.m_Surfaces = []
        self.m_Texinfos = []
        self.m_Brushes = []
        self.m_Brushsides = []
        self.m_Leaffaces = []
        self.m_Leafbrushes = []
        self.m_Polygons = []

    def BSPFile(self, bsp_directory, bsp_file):
        parse(bsp_directory, bsp_file)

    def parse(self, bsp_directory, bsp_file):
        if bsp_directory == "" or bsp_file == "":
            return False

        bsp_binary = open(os.path.join(bsp_directory, bsp_file), "rb")
        m_FileName = bsp_file
        if 1:
            # parse the bsp header
            bsp_binary.readinto(self.m_BSPHeader)

            # check bsp version/ident
            if self.m_BSPHeader.m_Version < BSPVERSION:
                print(
                    "BSPFile.parse(): ",
                    bsp_file,
                    "has an unknown BSP version, trying to parse it anyway...",
                )

            self.m_Vertexes = self.parse_lump_data(
                bsp_binary, LUMP_VERTEXES, self.m_Vertexes_t
            )
            if not self.parse_planes(bsp_binary):
                return False

            self.m_Edges = self.parse_lump_data(bsp_binary, LUMP_EDGES, self.m_Edges_t)
            self.m_Surfedges = self.parse_lump_data(
                bsp_binary, LUMP_SURFEDGES, self.m_Surfedges_t
            )
            self.m_Leaves = self.parse_lump_data(
                bsp_binary, LUMP_LEAFS, self.m_Leaves_t
            )
            if not self.parse_nodes(bsp_binary):
                return False

            self.m_Surfaces = self.parse_lump_data(
                bsp_binary, LUMP_FACES, self.m_Surfaces_t
            )
            self.m_Texinfos = self.parse_lump_data(
                bsp_binary, LUMP_TEXINFO, self.m_Texinfos_t
            )
            self.m_Brushes = self.parse_lump_data(
                bsp_binary, LUMP_BRUSHES, self.m_Brushes_t
            )
            self.m_Brushsides = self.parse_lump_data(
                bsp_binary, LUMP_BRUSHSIDES, self.m_Brushsides_t
            )
            if (
                not self.parse_leaffaces(bsp_binary)
                or not self.parse_leafbrushes(bsp_binary)
                or not self.parse_polygons(bsp_binary)
            ):
                return False
        return True

    def parse_lump_data(self, bsp_binary, lump_index, type1):
        if lump_index in id2size:
            size = id2size[lump_index]
        else:
            size = ctypes.sizeof(type1)
        print(type1, size, lump_index)
        lump = []
        numLumps = (
            self.m_BSPHeader.m_Lumps[lump_index].m_Filelen // size
        )  # как BSPFile.m_BSPHeader  = header
        if type(type1) == mvertex_t:
            for i in range(numLumps):
                lump.append(mvertex_t())
        elif type(type1) == cplane_t:
            for i in range(numLumps):
                lump.append(cplane_t())
        elif type(type1) == dedge_t:
            for i in range(numLumps):
                lump.append(dedge_t())
        elif type(type1) == dsurfedge_t:
            for i in range(numLumps):
                lump.append(dsurfedge_t())
        elif type(type1) == dleaf_t:
            for i in range(numLumps):
                lump.append(dleaf_t())
        elif type(type1) == snode_t:
            for i in range(numLumps):
                lump.append(snode_t())
        elif type(type1) == dface_t:
            for i in range(numLumps):
                lump.append(dface_t())
        elif type(type1) == texinfo_t:
            for i in range(numLumps):
                lump.append(texinfo_t())
        elif type(type1) == dbrush_t:
            for i in range(numLumps):
                lump.append(dbrush_t())
        elif type(type1) == dbrushside_t:
            for i in range(numLumps):
                lump.append(dbrushside_t())
        elif type(type1) == dleafface_t:
            for i in range(numLumps):
                lump.append(dleafface_t())
        elif type(type1) == dleafbrush_t:
            for i in range(numLumps):
                lump.append(dleafbrush_t())
        elif type(type1) == Polygon:
            for i in range(numLumps):
                lump.append(Polygon())
        for i in range(numLumps):
            bsp_binary.seek(
                self.m_BSPHeader.m_Lumps[lump_index].m_Fileofs + i * size
            )  # как bsp_binary  = handle
            bsp_binary.readinto(lump[i])
        return lump

    def parse_planes(self, bsp_binary):
        try:
            planes = self.parse_lump_data(bsp_binary, LUMP_PLANES, self.m_Planes_t)
            self.m_Planes = planes
            # print(len(planes), 'gjgjjh')

            for i in range(len(planes)):
                out = self.m_Planes[i]
                in_ = planes[i]

                plane_bits = 0
                out.m_Normal = in_.m_Normal
                if out.m_Normal.x < 0.0:
                    plane_bits |= 1 << 0
                if out.m_Normal.y < 0.0:
                    plane_bits |= 1 << 1
                if out.m_Normal.z < 0.0:
                    plane_bits |= 1 << 2

                out.m_Distance = in_.m_Distance
                out.m_Type = in_.m_Type
                out.m_SignBits = plane_bits
        except Exception as e:
            print("parse_planes", e)
            return False
        return True

    def parse_nodes(self, bsp_binary):
        if 1:
            nodes = self.parse_lump_data(bsp_binary, LUMP_NODES, self.m_Nodes_t)

            num_nodes = len(nodes)
            for i in range(num_nodes):
                self.m_Nodes.append(snode_t())

            for i in range(num_nodes):
                self.m_Nodes[i] = nodes[i]
                self.m_Nodes[i].m_pPlane = self.m_Planes[nodes[i].m_PlaneNum]
        return True

    def parse_leaffaces(self, bsp_binary):
        try:
            self.m_Leaffaces = self.parse_lump_data(
                bsp_binary, LUMP_LEAFFACES, self.m_Leaffaces_t
            )

            num_leaffaces = len(self.m_Leaffaces)
            if num_leaffaces > MAX_MAP_LEAFBRUSHES:
                print(
                    "BSPFile.parse_leaffaces(): map has to many leaffaces, parsed more than required.."
                )
            elif not num_leaffaces:
                print("BSPFile.parse_leaffaces(): map has no leaffaces to parse!")
            print(num_leaffaces)
        except Exception as e:
            print("parse_leaffaces", e)
            return False
        return True

    def parse_leafbrushes(self, bsp_binary):
        try:
            self.m_Leafbrushes = self.parse_lump_data(
                bsp_binary, LUMP_LEAFBRUSHES, self.m_Leafbrushes_t
            )

            num_leaffaces = len(self.m_Leaffaces)
            if num_leaffaces > MAX_MAP_LEAFBRUSHES:
                print(
                    "BSPFile.parse_leaffaces(): map has to many leafbrushes, parsed more than required.."
                )
            elif not num_leaffaces:
                print("BSPFile.parse_leaffaces(): map has no leafbrushes to parse!")
        except Exception as e:
            print("parse_leafbrushes", e)
            dfg
            return False
        return True

    def parse_polygons(self, bsp_binary):
        if 1:
            for surface in self.m_Surfaces:
                first_edge = surface.m_Firstedge
                # if first_edge > len(self.m_Surfaces): print(len(self.m_Surfedges), first_edge); continue
                num_edges = surface.m_Numedges

                if num_edges < 3 or num_edges > MAX_SURFINFO_VERTS:
                    continue
                if surface.m_Texinfo <= 0:
                    continue

                polygon = Polygon()
                edge = Vector3()
                for i in range(num_edges):
                    edge_index = self.m_Surfedges[first_edge + i].m_V
                    if edge_index >= 0:
                        edge = self.m_Vertexes[
                            self.m_Edges[edge_index].m_V[0]
                        ].m_Position
                    else:
                        edge = self.m_Vertexes[
                            self.m_Edges[-edge_index].m_V[1]
                        ].m_Position
                    polygon.m_Verts[i] = edge
                polygon.m_nVerts = num_edges
                polygon.m_Plane.m_Origin = self.m_Planes[surface.m_Planenum].m_Normal
                polygon.m_Plane.m_Distance = self.m_Planes[
                    surface.m_Planenum
                ].m_Distance
                self.m_Polygons.append(polygon)
        #    except Exception as e:
        #        print("parse_polygons", e)
        #        return False
        return True


class trace_t(ctypes.Structure):
    _fields_ = [
        ("m_AllSolid", ctypes.c_bool),  # Determine if plane is NOT valid
        (
            "m_StartSolid",
            ctypes.c_bool,
        ),  # Determine if the start point was in a solid area
        ("m_Fraction", ctypes.c_float),  # Time completed, 1.0 = didn't hit anything :)
        ("m_FractionLeftSolid", ctypes.c_float),
        ("m_EndPos", Vector3),  # Final trace position
        ("m_pPlane", cplane_t),
        ("m_Contents", ctypes.c_int),
        ("m_pBrush", dbrush_t),
        ("m_nBrushSide", ctypes.c_int),
    ]


class TraceRay(ctypes.Structure):
    def is_visible(origin, final, pBSPFile):
        if not pBSPFile:
            return False

        trace = trace_t()
        TraceRay.ray_cast(origin, final, pBSPFile, trace)

        print(trace.m_Fraction)

        return not trace.m_Fraction < 1.0

    def ray_cast(origin, final, pBSPFile, pTrace):
        if pBSPFile.m_Planes == cplane_t():
            return False

        # ctypes.memset(trace_t(), 0, ctypes.sizeof(trace_t))
        pTrace.m_Fraction = 1.0
        pTrace.m_FractionLeftSolid = 0.0
        TraceRay.ray_cast_node(pBSPFile, 0, 0.0, 1.0, origin, final, pTrace)
        print(pTrace.m_Fraction)

        if pTrace.m_Fraction < 1.0:
            pTrace.m_EndPos = origin + (final - origin) * pTrace.m_Fraction
        else:
            pTrace.m_EndPos = final

    def ray_cast_node(
        pBSPFile, node_index, start_fraction, end_fraction, origin, final, pTrace
    ):
        # print(pTrace.m_Fraction, start_fraction, node_index)
        if pTrace.m_Fraction <= start_fraction:
            return 7
        if node_index < 0:
            pLeaf = pBSPFile.m_Leaves[-node_index - 1]
            for i in range(pLeaf.m_Numleafbrushes):
                iBrushIndex = pBSPFile.m_Leafbrushes[pLeaf.m_Firstleafbrush + i]
                # print(iBrushIndex)
                pBrush = pBSPFile.m_Brushes[iBrushIndex.m_V]
                if not pBrush:
                    continue
                if not pBrush.m_Contents & MASK_SHOT_HULL:
                    continue

                TraceRay.ray_cast_brush(pBSPFile, pBrush, pTrace, origin, final)
                if not pTrace.m_Fraction:
                    return 4

            if pTrace.m_StartSolid:
                return 5
            if pTrace.m_Fraction < 1.0:
                return 6
            for i in range(pLeaf.m_Numleaffaces):
                # print(len(pBSPFile.m_Leaffaces), pLeaf.m_Firstleafface, i)
                TraceRay.ray_cast_surface(
                    pBSPFile,
                    pBSPFile.m_Leaffaces[pLeaf.m_Firstleafface + i],
                    pTrace,
                    origin,
                    final,
                )
            return 8

        pNode = pBSPFile.m_Nodes[node_index]
        if not pNode:
            return 3
        pPlane = pNode.m_pPlane
        if not pPlane:
            return 2

        if pPlane.m_Type < 3:
            # print(pPlane.m_Type)
            start_distance = origin.get(pPlane.m_Type) - pPlane.m_Distance
            end_distance = final.get(pPlane.m_Type) - pPlane.m_Distance
        else:
            start_distance = origin.dot(pPlane.m_Normal) - pPlane.m_Distance
            end_distance = final.dot(pPlane.m_Normal) - pPlane.m_Distance

        if start_distance >= 0.0 and end_distance >= 0.0:
            TraceRay.ray_cast_node(
                pBSPFile,
                pNode.m_Children[0],
                start_fraction,
                end_fraction,
                origin,
                final,
                pTrace,
            )
        elif start_distance < 0.0 and end_distance < 0.0:
            TraceRay.ray_cast_node(
                pBSPFile,
                pNode.m_Children[1],
                start_fraction,
                end_fraction,
                origin,
                final,
                pTrace,
            )
        else:
            middle = Vector3()

            if start_distance < end_distance:
                # Back
                side_id = 1
                inversed_distance = 1.0 / (start_distance - end_distance)

                fraction_first = (start_distance + FLT_EPSILON) * inversed_distance
                fraction_second = (start_distance + FLT_EPSILON) * inversed_distance
            elif end_distance < start_distance:
                # Front
                side_id = 0
                inversed_distance = 1.0 / (start_distance - end_distance)

                fraction_first = (start_distance + FLT_EPSILON) * inversed_distance
                fraction_second = (start_distance - FLT_EPSILON) * inversed_distance
            else:
                # Front
                side_id = 0
                fraction_first = 1.0
                fraction_second = 0.0
            if fraction_first < 0.0:
                fraction_first = 0.0
            elif fraction_first > 1.0:
                fraction_first = 1.0
            if fraction_second < 0.0:
                fraction_second = 0.0
            elif fraction_second > 1.0:
                fraction_second = 1.0

            fraction_middle = (
                start_fraction + (end_fraction - start_fraction) * fraction_first
            )
            middle = origin + (final - origin) * fraction_first

            TraceRay.ray_cast_node(
                pBSPFile,
                pNode.m_Children[side_id],
                start_fraction,
                fraction_middle,
                origin,
                middle,
                pTrace,
            )
            fraction_middle = (
                start_fraction + (end_fraction - start_fraction) * fraction_second
            )
            middle = origin + (final - origin) * fraction_second

            TraceRay.ray_cast_node(
                pBSPFile,
                pNode.m_Children[not side_id],
                fraction_middle,
                end_fraction,
                middle,
                final,
                pTrace,
            )

    def ray_cast_brush(pBSPFile, pBrush, pTrace, origin, final):
        if not pBrush.m_Numsides:
            return

        fraction_to_enter = -99.0
        fraction_to_leave = 1.0
        starts_out = False
        ends_out = False
        for i in range(pBrush.m_Numsides):
            # print(pBrush.m_Firstside, i)
            # print(len(pBSPFile.m_Brushsides))
            pBrushSide = pBSPFile.m_Brushsides[pBrush.m_Firstside + i]
            if not pBrushSide or pBrushSide.m_Bevel:
                continue

            pPlane = pBSPFile.m_Planes[pBrushSide.m_Planenum]
            if not pPlane:
                continue

            start_distance = origin.dot(pPlane.m_Normal) - pPlane.m_Distance
            end_distance = final.dot(pPlane.m_Normal) - pPlane.m_Distance
            if start_distance > 0.0:
                starts_out = True
                if end_distance > 0.0:
                    return 1
            else:
                if end_distance <= 0.0:
                    continue
                ends_out = True

            if start_distance > end_distance:
                fraction = max((start_distance - DIST_EPSILON), 0.0)
                fraction = fraction / (start_distance - end_distance)
                if fraction > fraction_to_enter:
                    fraction_to_enter = fraction
            else:
                fraction = (start_distance + DIST_EPSILON) / (
                    start_distance - end_distance
                )
                if fraction < fraction_to_leave:
                    fraction_to_leave = fraction

        if starts_out:
            if pTrace.m_FractionLeftSolid - fraction_to_enter > 0.0:
                starts_out = false

        if not starts_out:
            pTrace.m_StartSolid = True
            pTrace.m_Contents = pBrush.m_Contents

            if not ends_out:
                pTrace.m_AllSolid = True
                pTrace.m_Fraction = 0.0
                pTrace.m_FractionLeftSolid = 1.0
            else:
                if (
                    fraction_to_leave != 1.0
                    and fraction_to_leave > pTrace.m_FractionLeftSolid
                ):
                    pTrace.m_FractionLeftSolid = fraction_to_leave
                    if pTrace.m_Fraction <= fraction_to_leave:
                        pTrace.m_Fraction = 1.0
            return

        if fraction_to_enter < fraction_to_leave:
            if fraction_to_enter > -99.0 and fraction_to_enter < pTrace.m_Fraction:
                if fraction_to_enter < 0.0:
                    fraction_to_enter = 0.0

                pTrace.m_Fraction = fraction_to_enter
                pTrace.m_pBrush = pBrush
                pTrace.m_Contents = pBrush.m_Contents

    def ray_cast_surface(pBSPFile, surface_index, pTrace, origin, final):
        pPolygon = pBSPFile.m_Polygons[surface_index]
        if not pPolygon:
            return

        pPlane = pPolygon.m_Plane
        dot1 = pPlane.dist_to(origin)
        dot2 = pPlane.dist_to(final)

        if dot1 > 0.0 != dot2 > 0.0:
            if dot1 - dot2 < DIST_EPSILON:
                return

            t = dot1 / (dot1 - dot2)
            if t <= 0:
                return

            intersection = origin + (final - origin) * t
            for i in range(pPolygon.m_nVerts):
                pEdgePlane = pPolygon.m_EdgePlanes[i]
                if pEdgePlane.m_Origin.empty():
                    pEdgePlane.m_Origin = pPlane.m_Origin - (
                        pPolygon.m_Verts[i]
                        - pPolygon.m_Verts[(i + 1) % pPolygon.m_nVerts]
                    )
                    pEdgePlane.m_Origin.normalize()
                    pEdgePlane.m_Distance = pEdgePlane.m_Origin.dot(pPolygon.m_Verts[i])
                if pEdgePlane.dist_to(intersection) < 0.0:
                    break
            if i == pPolygon.m_nVerts:
                pTrace.m_Fraction = 0.2
                pTrace.m_EndPos = intersection


class BSPParser(ctypes.Structure):
    _fields_ = [("m_LastMap", ctypes.c_char_p)]

    def __init__(self):
        self.m_BSPFile = BSPFile()

    def parse_map(self, bsp_directory, bsp_file):
        if bsp_directory == "" or bsp_file == "":
            return False

        if self.m_BSPFile.parse(bsp_directory, bsp_file):
            m_LastMap = bsp_file
            return True
        return False

    def is_visible(self, origin, final):
        return TraceRay.is_visible(origin, final, self.m_BSPFile)

    def get_bsp(self):
        return BSPFile


def getLumpFromId(id):
    lump = []
    if id == 1:
        numLumps = header.m_Lumps[id].m_Filelen // ctypes.sizeof(dplane_t)
        for i in range(numLumps):
            lump.append(dplane_t())
    elif id == 5:
        numLumps = header.m_Lumps[id].m_Filelen // ctypes.sizeof(dnode_t)
        for i in range(numLumps):
            lump.append(dnode_t())
    elif id == 10:
        numLumps = header.m_Lumps[id].m_Filelen // ctypes.sizeof(dleaf_t)
        for i in range(numLumps):
            lump.append(dleaf_t())
    for i in range(numLumps):
        handle.seek(header.m_Lumps[id].m_Fileofs + (i * ctypes.sizeof(lump[i])))
        handle.readinto(lump[i])
    return lump


def getLeafFromPoint(point):
    node = 0
    while node >= 0:
        pNode = nodeLump[node]
        pPlane = planeLump[pNode.m_Planenum]
        d = (
            point.dot(pPlane.m_Normal) - pPlane.m_Distance
        )  # d = D3DXVec3Dot(&point, &pPlane->normal) - pPlane->dist;
        if d > 0:
            node = pNode.m_Children[0]
        else:
            node = pNode.m_Children[1]
    return leafLump[-node - 1]


def isVisible(vStart, vEnd):
    MASK_SOLID = 0x1 | 0x4000 | 0x2 | 0x2000000 | 0x8
    MASK_SHOT = 0x1 | 0x4000 | 0x2 | 0x4000000 | 0x40000000
    pLeaf = None
    vDirection = vEnd - vStart
    vPoint = vStart
    iStepCount = int(vDirection.length())
    vDirection /= iStepCount
    while iStepCount:
        vPoint = vPoint + vDirection
        pLeaf = getLeafFromPoint(vPoint)
        if pLeaf and (pLeaf.m_Contents & 0x1):
            break
        iStepCount -= 1
    if pLeaf is None:
        return False
    else:
        return not (pLeaf.m_Contents & 0x1)
