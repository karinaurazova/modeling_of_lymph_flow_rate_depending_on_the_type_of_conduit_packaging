from math import sqrt
import gmsh

def create_configuration_A():
    gmsh.initialize()
    lc = 0.001 / 2
    r = 20.0

    # Triangle Points
    x1 = [+r, 0]
    x2 = [-r, 0]
    x3 = [0, sqrt(3)*r]

    p1 = gmsh.model.occ.addPoint(x1[0], x1[1], 0, lc, 1)
    p2 = gmsh.model.occ.addPoint(x2[0], x2[1], 0, lc, 2)
    p3 = gmsh.model.occ.addPoint(x3[0], x3[1], 0, lc, 3)
    gmsh.model.occ.synchronize()

    # Triangle lines
    gmsh.model.occ.addLine(1, 2, 4)
    gmsh.model.occ.addLine(2, 3, 5)
    gmsh.model.occ.addLine(3, 1, 6)
    gmsh.model.occ.synchronize()

    # Circles at vertices
    gmsh.model.occ.addCircle(x1[0], x1[1], 0, r, 7)
    gmsh.model.occ.addCircle(x2[0], x2[1], 0, r, 8)
    gmsh.model.occ.addCircle(x3[0], x3[1], 0, r, 9)
    gmsh.model.occ.synchronize()

    # Curve loops
    t = gmsh.model.occ.addCurveLoop([4, 5, 6], 10)
    c1 = gmsh.model.occ.addCurveLoop([7], 11)
    c2 = gmsh.model.occ.addCurveLoop([8], 12)
    c3 = gmsh.model.occ.addCurveLoop([9], 13)
    gmsh.model.occ.synchronize()

    # Surfaces
    st = gmsh.model.occ.addSurfaceFilling(10, 14)
    sc1 = gmsh.model.occ.addSurfaceFilling(11, 15)
    sc2 = gmsh.model.occ.addSurfaceFilling(12, 16)
    sc3 = gmsh.model.occ.addSurfaceFilling(13, 17)

    # Cut out circles from a triangle
    e = gmsh.model.occ.cut([(2, 14)], [(2, 15), (2, 16), (2, 17)], 18)
    gmsh.model.occ.synchronize()

    # Physical groups
    b = gmsh.model.getEntities(1)
    for i, (dim, tag) in enumerate(b, start=1):
        gmsh.model.addPhysicalGroup(1, [tag], i, name=f"Boundary_{i}")
    gmsh.model.addPhysicalGroup(2, [18], 100, name="Domain")
    gmsh.model.occ.synchronize()

    # Grid settings
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 1)
    gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.MeshSizeMin", lc)
    gmsh.option.setNumber("Mesh.MeshSizeMax", 100*lc)

    gmsh.model.mesh.generate(2)
    gmsh.write("mesh_A.msh")
    gmsh.finalize()

def create_configuration_B():
    gmsh.initialize()
    lc = 0.001 / 2
    r = 20.0

    # Square points
    points = [
        gmsh.model.occ.addPoint(r, r, 0, lc, 1),
        gmsh.model.occ.addPoint(r, -r, 0, lc, 2),
        gmsh.model.occ.addPoint(-r, -r, 0, lc, 3),
        gmsh.model.occ.addPoint(-r, r, 0, lc, 4)
    ]
    gmsh.model.occ.synchronize()

    # Square lines
    lines = [
        gmsh.model.occ.addLine(1, 2, 5),
        gmsh.model.occ.addLine(2, 3, 6),
        gmsh.model.occ.addLine(3, 4, 7),
        gmsh.model.occ.addLine(4, 1, 8)
    ]
    gmsh.model.occ.synchronize()

    # Circles at vertices
    circles = [
        gmsh.model.occ.addCircle(r, r, 0, r, 9),
        gmsh.model.occ.addCircle(r, -r, 0, r, 10),
        gmsh.model.occ.addCircle(-r, -r, 0, r, 11),
        gmsh.model.occ.addCircle(-r, r, 0, r, 12)
    ]
    gmsh.model.occ.synchronize()

    # Curve loops
    t = gmsh.model.occ.addCurveLoop([5, 6, 7, 8], 13)
    c_loops = [gmsh.model.occ.addCurveLoop([c], 14+i) for i, c in enumerate([9, 10, 11, 12])]
    gmsh.model.occ.synchronize()

    # Surfaces
    st = gmsh.model.occ.addSurfaceFilling(13, 18)
    sc = [gmsh.model.occ.addSurfaceFilling(14+i, 19+i) for i in range(4)]
    gmsh.model.occ.synchronize()

    # Cut out circles from a square
    e = gmsh.model.occ.cut([(2, 18)], [(2, 19+i) for i in range(4)], 23)
    gmsh.model.occ.synchronize()

    # Physical groups
    b = gmsh.model.getEntities(1)
    for i, (dim, tag) in enumerate(b, start=1):
        gmsh.model.addPhysicalGroup(1, [tag], 100+i, name=f"Boundary_{i}")
    gmsh.model.addPhysicalGroup(2, [23], 200, name="Domain")
    gmsh.model.occ.synchronize()

    # Grid settings
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 1)
    gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.MeshSizeMin", lc)
    gmsh.option.setNumber("Mesh.MeshSizeMax", 100*lc)

    gmsh.model.mesh.generate(2)
    gmsh.write("mesh_B.msh")
    gmsh.finalize()

def create_configuration_C():
    gmsh.initialize()
    lc = 0.001 / 2
    r = 20.0
    r_small = 8.25

    # Square points + center
    points = [
        gmsh.model.occ.addPoint(r, r, 0, lc, 1),
        gmsh.model.occ.addPoint(r, -r, 0, lc, 2),
        gmsh.model.occ.addPoint(-r, -r, 0, lc, 3),
        gmsh.model.occ.addPoint(-r, r, 0, lc, 4),
        gmsh.model.occ.addPoint(0, 0, 0, lc, 5)
    ]
    gmsh.model.occ.synchronize()

    # Square lines
    lines = [
        gmsh.model.occ.addLine(1, 2, 6),
        gmsh.model.occ.addLine(2, 3, 7),
        gmsh.model.occ.addLine(3, 4, 8),
        gmsh.model.occ.addLine(4, 1, 9)
    ]
    gmsh.model.occ.synchronize()

    # Circles (4 large + 1 small)
    circles = [
        gmsh.model.occ.addCircle(r, r, 0, r, 10),
        gmsh.model.occ.addCircle(r, -r, 0, r, 11),
        gmsh.model.occ.addCircle(-r, -r, 0, r, 12),
        gmsh.model.occ.addCircle(-r, r, 0, r, 13),
        gmsh.model.occ.addCircle(0, 0, 0, r_small, 14)
    ]
    gmsh.model.occ.synchronize()

    # Curve loops
    t = gmsh.model.occ.addCurveLoop([6, 7, 8, 9], 15)
    c_loops = [gmsh.model.occ.addCurveLoop([c], 16+i) for i, c in enumerate([10, 11, 12, 13, 14])]
    gmsh.model.occ.synchronize()

    # Surfaces
    st = gmsh.model.occ.addSurfaceFilling(15, 21)
    sc = [gmsh.model.occ.addSurfaceFilling(16+i, 22+i) for i in range(5)]
    gmsh.model.occ.synchronize()

    # Cut out circles from a square
    e = gmsh.model.occ.cut([(2, 21)], [(2, 22+i) for i in range(5)], 27)
    gmsh.model.occ.synchronize()

    # Physical groups
    b = gmsh.model.getEntities(1)
    for i, (dim, tag) in enumerate(b, start=1):
        gmsh.model.addPhysicalGroup(1, [tag], 200+i, name=f"Boundary_{i}")
    gmsh.model.addPhysicalGroup(2, [27], 300, name="Domain")
    gmsh.model.occ.synchronize()

    # Grid settings
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 1)
    gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.MeshSizeMin", lc)
    gmsh.option.setNumber("Mesh.MeshSizeMax", 100*lc)

    gmsh.model.mesh.generate(2)
    gmsh.write("mesh_C.msh")
    gmsh.finalize()

# Generate all configurations
create_configuration_A()
create_configuration_B()
create_configuration_C()