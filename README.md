Tiny_DFF_Read
---

Small C based DFF model loader for GTA (RenderWare) Files (inspired by syoyo tiny libraries)

What it does?

· Loads RenderWare DFF (GTA III, VC, SA) model files
· Extracts geometry data (vertices, normals, UVs, faces)
· Reads materials and textures
· Supports bone/skin data for character models
· Supports binmesh (optimized mesh format)

Requirements

None except a C compiler.

Uses these stdlib headers:

| Header    | Purpose                                    |
|-----------|--------------------------------------------|
| stdint.h  | for uint32_t, int64_t etc.                 |
| stdbool.h | for bool                                   |
| stddef.h  | for size_t                                 |
| string.h  | for memcpy                                 |
| stdlib.h  | for malloc/free (only in implementation)   |

How to build

1. Include `tiny_dff_read.h` in your project
2. In one C file define `TINYDFF_READ_IMPLEMENTATION` before including the header:

```c
#define TINYDFF_READ_IMPLEMENTATION
#include "tiny_dff_read.h"
```

How to load a DFF

Create a context with callbacks for:

· error reporting
· alloc
· free
· read
· seek
· tell

Then call TinyDFF_Read_Read() to parse the file.

```c
static void errorCallback(void* user, const char* msg) {
    fprintf(stderr, "ERROR: %s\n", msg);
}

static void* allocCallback(void* user, size_t size) {
    return malloc(size);
}

static void freeCallback(void* user, void* data) {
    free(data);
}

static size_t readCallback(void* user, void* data, size_t size) {
    return fread(data, 1, size, (FILE*)user);
}

static bool seekCallback(void* user, int64_t offset) {
    return fseek((FILE*)user, offset, SEEK_CUR) == 0;
}

static int64_t tellCallback(void* user) {
    return ftell((FILE*)user);
}

// Load DFF file
TinyDFF_Read_Handle loadDFF(const char* filename) {
    FILE* file = fopen(filename, "rb");
    if (!file) return NULL;
    
    TinyDFF_Read_Callbacks callbacks = {
        .errorFn = errorCallback,
        .allocFn = allocCallback,
        .freeFn = freeCallback,
        .readFn = readCallback,
        .seekFn = seekCallback,
        .tellFn = tellCallback
    };
    
    TinyDFF_Read_Handle ctx = TinyDFF_Read_CreateContext(&callbacks, file);
    if (!ctx) return NULL;
    
    if (!TinyDFF_Read_Read(ctx)) {
        TinyDFF_Read_DestroyContext(ctx);
        return NULL;
    }
    
    return ctx;
}

// Print model info
void printModelInfo(TinyDFF_Read_Handle ctx) {
    printf("Version: 0x%X\n", TinyDFF_Read_GetVersion(ctx));
    printf("Atomics: %u\n", TinyDFF_Read_GetAtomicCount(ctx));
    printf("Geometries: %u\n", TinyDFF_Read_GetGeometryCount(ctx));
    printf("Frames: %u\n", TinyDFF_Read_GetFrameCount(ctx));
    
    for (uint32_t i = 0; i < TinyDFF_Read_GetGeometryCount(ctx); i++) {
        uint32_t verts, faces, flags, uv;
        TinyDFF_Read_GetGeometryInfo(ctx, i, &verts, &faces, &flags, &uv);
        printf("  Geom %u: %u verts, %u faces, UVs: %u\n", i, verts, faces, uv);
        
        // Get vertices
        const TinyDFF_Read_Vector3* vertices = TinyDFF_Read_GetVertices(ctx, i);
        // Get faces
        const TinyDFF_Read_Face* faces_data = TinyDFF_Read_GetFaces(ctx, i);
        
        // Process first 3 vertices for example
        for (int j = 0; j < 3 && j < verts; j++) {
            printf("    v[%d]: %.2f %.2f %.2f\n", j, 
                   vertices[j].x, vertices[j].y, vertices[j].z);
        }
    }
}

int main() {
    TinyDFF_Read_Handle ctx = loadDFF("model.dff");
    if (!ctx) {
        printf("Failed to load DFF\n");
        return 1;
    }
    
    printModelInfo(ctx);
    TinyDFF_Read_DestroyContext(ctx);
    return 0;
}
```

API Functions:

Context management:

| Function | Description |
|----------|-------------|
| TinyDFF_Read_CreateContext() | Create Parser Context |
| TinyDFF_Read_DestroyContext() | Destroy Context |
| TinyDFF_Read_Reset() | Reset Context |
| TinyDFF_Read_Read() | Parse DFF Data |

Query counts:

| Function | Description |
|----------|-------------|
| TinyDFF_Read_GetVersion() | RW Version |
| TinyDFF_Read_GetAtomicCount() | Number of Atomics |
| TinyDFF_Read_GetGeometryCount() | Number of Geometries |
| TinyDFF_Read_GetFrameCount() | Number of Frames |

Geometry data:

| Function | Description |
|----------|-------------|
| TinyDFF_Read_GetGeometryInfo() | Geometry Info |
| TinyDFF_Read_GetVertices() | Vertex Positions |
| TinyDFF_Read_GetNormals() | Normals |
| TinyDFF_Read_GetUVs() | Texture Coordinates |
| TinyDFF_Read_GetVertexColors() | Vertex Colors |
| TinyDFF_Read_GetFaces() | Triangle Faces |

Materials:

| Function | Description |
|----------|-------------|
| TinyDFF_Read_GetMaterialCount() | Material Count |
| TinyDFF_Read_GetMaterial() | Material by Index |
| TinyDFF_Read_GetMaterialName() | Texture Name |
| TinyDFF_Read_GetMaterialColor() | Material Color |

Bones/Skin:

| Function | Description |
|----------|-------------|
| TinyDFF_Read_HasSkin() | Check if has Skin Data |
| TinyDFF_Read_GetBoneCount() | Bone Count |
| TinyDFF_Read_GetBoneIndices() | Bone Indices Per Vertex |
| TinyDFF_Read_GetBoneWeights() | Bone Weights Per Vertex |

Frames:

| Function | Description |
|----------|-------------|
| TinyDFF_Read_GetFrameMatrix() | Frame Transform |
| TinyDFF_Read_GetFrameName() | Frame Name |
| TinyDFF_Read_GetFrameParent() | Parent Frame Index |

Bin Mesh:

| Function | Description |
|----------|-------------|
| TinyDFF_Read_GetBinMeshInfo() | Bin Mesh Info |
| TinyDFF_Read_GetBinMeshSplit() | Split Data |

---
