def closeLoopHull(tri_origine,hull_bound_points_ext,mesh_resolution_ext,commonEdge1,commonEdge2):
    
    # find overlapped point on tri_original
    olP = np.concatenate((overlappedPoints(tri_origine.points, commonEdge1), overlappedPoints(tri_origine.points, commonEdge2)), axis=0)
    # find the positions of the ovelapped points
    olPP = overlappedPointsPosition(tri_origine.points,olP)
    # creat hull
    hull_bound_ext = Delaunay(hull_bound_points_ext)
    
    mesh_points = []
    for i in range(min(i[0] for i in hull_bound_points_ext),max(i[0] for i in hull_bound_points_ext)+1,mesh_resolution_ext):
        for j in range(min(i[1] for i in hull_bound_points_ext),max(i[1] for i in hull_bound_points_ext)+1,mesh_resolution_ext):
            mesh_points.append([i,j])
    mesh_ini = np.array(mesh_points)

    # find the overlapped point on new tri_
    olP2 = np.concatenate((overlappedPoints(mesh_ini, commonEdge1), overlappedPoints(mesh_ini, commonEdge2)), axis=0)
    # find the positions of the new ovelapped points
    olPP2 = overlappedPointsPosition(mesh_ini,olP2)
    # delete these nex overlapped points
    mesh_ini_del = np.delete(mesh_ini, olPP2, 0)
    # add the ovelapped points in the original tri
    if len(olPP2) > 0:
        mesh_ini = np.append(olP,mesh_ini_del, axis=0)
    # check if inside hull
    mesh_add = np.array([p_ for p_ in mesh_ini if hull_bound_ext.find_simplex(p_)>=0])
    # the extended tri
    tri_ext = Delaunay(mesh_add)
    
    # points in the merged tri
    tri_final_points = np.concatenate((tri_origine.points, mesh_ini_del), axis=0)
    
    tri_ext_simplices = tri_ext.simplices + tri_origine.points.shape[0] - len(olPP)
    for i in range(len(olPP)):
        pos = np.where(tri_ext_simplices == (i + tri_origine.points.shape[0] - len(olPP)))
        for j in range(len(pos[0])):
            tri_ext_simplices[pos[0][j]][pos[1][j]] = olPP[i]
            
    tri_final_simplices = np.concatenate((tri_origine.simplices, tri_ext_simplices), axis=0)
    
    return Delaunay_temp(tri_final_points,tri_final_simplices)
