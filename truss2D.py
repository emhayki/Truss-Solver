import numpy as np

def truss2D(coords_entries, elements_entries, prescribed_entries, point_load_entries):
    
    nelem  = len(elements_entries)                                      # Total number of elements
    lnods  = [(entry[0], entry[1]) for entry in elements_entries]       # Table of connectivities
    young  = np.array([row[2] for row in elements_entries])             # Young's modulus
    csarea = np.array([row[3] for row in elements_entries])             # Cross-sectional areas
    coord  = np.array(coords_entries)                                   # Nodal coordinates
    ngdof  =  2 * len(coords_entries)

    # Element length, cosine, and sine calculations
    elength = np.zeros(nelem)
    ecos    = np.zeros(nelem)
    esin    = np.zeros(nelem)

    for ie, (n1, n2) in enumerate(lnods):
        
        dx = coord[n2 - 1, 0] - coord[n1 - 1, 0]
        dy = coord[n2 - 1, 1] - coord[n1 - 1, 1]

        elength[ie] = np.sqrt(dx ** 2 + dy ** 2)
        ecos[ie]    = dx / elength[ie]
        esin[ie]    = dy / elength[ie]


    # Global stiffness matrix
    K = np.zeros((ngdof, ngdof))
    for ie, (n1, n2) in enumerate(lnods):
        ke = young[ie] * csarea[ie] / elength[ie] * np.array([
            [ ecos[ie] ** 2      ,  ecos[ie] * esin[ie], -ecos[ie] ** 2      , -ecos[ie] * esin[ie]],
            [ ecos[ie] * esin[ie],  esin[ie] ** 2      , -ecos[ie] * esin[ie], -esin[ie] ** 2],
            [-ecos[ie] ** 2      , -ecos[ie] * esin[ie],  ecos[ie] ** 2      ,  ecos[ie] * esin[ie]],
            [-ecos[ie] * esin[ie], -esin[ie] ** 2      ,  ecos[ie] * esin[ie],  esin[ie] ** 2]])

        dof_indices = np.array([2 * (n1 - 1), 2 * (n1 - 1) + 1, 2 * (n2 - 1), 2 * (n2 - 1) + 1])
        for i in range(4):
            for j in range(4):
                K[dof_indices[i], dof_indices[j]] += ke[i, j]

    # Apply boundary conditions
    fixed_dofs = []
    for node, dx, dy in prescribed_entries:
        if dx: fixed_dofs.append(2 * (node - 1))
        if dy: fixed_dofs.append(2 * (node - 1) + 1)

    free_dofs = np.setdiff1d(np.arange(ngdof), fixed_dofs)

    # Apply loads
    F = np.zeros(ngdof)
    for node, fx, fy in point_load_entries:
        F[2 * (node - 1)] += fx
        F[2 * (node - 1) + 1] += fy

    # Solve system
    Kff = K[np.ix_(free_dofs, free_dofs)]
    Kfp = K[np.ix_(free_dofs, fixed_dofs)]
    Ff  = F[free_dofs]

    # Solve for displacements
    u = np.linalg.solve(Kff, Ff)
    q = np.zeros(ngdof)
    q[free_dofs] = u

    # Calculate reactions
    R = np.dot(K, q) - F

    # Element stresses
    stresses = np.zeros(nelem)
    for i, (n1, n2, E, A) in enumerate(elements_entries):
        d = q[[2*(n1-1), 2*(n1-1)+1, 2*(n2-1), 2*(n2-1)+1]]
        L = np.sqrt((coord[n2 -1,0] - coord[n1-1,0])**2 + (coord[n2-1,1] - coord[n1-1,1])**2)
        c = (coord[n2-1,0] - coord[n1-1,0])/L
        s = (coord[n2-1,1] - coord[n1-1,1])/L
        u = np.dot(np.array([-c, -s, c, s]), d)
        stresses[i] = (E * u)/L


    return K, q, R, stresses