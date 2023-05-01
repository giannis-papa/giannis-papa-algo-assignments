import sys

# Dimiourgia tou arxikou pinaka opou apoteleite mono apo clusters me 1 stoixeio.
def calculate_initial_matrix(matrix): 
    distance_matrix = []
    for i in range (0, len(matrix)):
        temp_dist = []
        for j in range (0, len(matrix)):
            if len(matrix[i]) == 1 and len(matrix[j]) == 1 :
                dist = abs(matrix[i][0] - matrix[j][0])
                temp_dist.append(dist)
        distance_matrix.append(temp_dist)   
    return distance_matrix

# Euresi twn 2 stoixeiwn me tin mikroteri apostasi mazi me ta index gia ton pinaka.
def find_min_distance(distance_matrix):
    min_dist = 100000
    index_i = -1
    index_j = -1
    for i in range (0, len(distance_matrix)):
        for j in range (i+1, len(distance_matrix)):
            if distance_matrix[i][j] < min_dist and distance_matrix[i][j] != 0:
                min_dist = distance_matrix[i][j]
                index_i = i
                index_j = j
    return index_i, index_j,(round(min_dist,2))

def calculate_distance(t,s,u,method):
    if method == "single":
        # Upologismos apostasis me basi tin methodo single
        if abs(max(t) - min(u)) < abs(min(t) - max(u)):
            dtu = max(t) - min(u)
        else:
            dtu = min(t) - max(u)
        if abs(max(s) - min(u)) < abs(min(s) - max(u)):
            dsu = max(s) - min(u)
        else:
            dsu = min(s) - max(u)
        dist = 1/2*abs(dtu) + 1/2*abs(dsu) - 1/2*abs(dsu - dtu)
        return dist
    if method == "complete":
        # Upologismos apostasis me basi tin methodo complete
        if abs(max(t) - min(u)) > abs(min(t) - max(u)):
            dtu = max(t) - min(u)
        else:
            dtu = min(t) - max(u)
        if abs(max(s) - min(u)) > abs(min(s) - max(u)):
            dsu = max(s) - min(u)
        else:
            dsu = min(s) - max(u)
        dist = 1/2*abs(dtu) + 1/2*abs(dsu) + 1/2*abs(dsu - dtu)
        return dist
    if method == "average":
        # Upologismos apostasis me basi tin methodo average
        dist_total = 0
        for i in t:
            for z in u:
                dist_total+= abs(i-z) 
        dtu = dist_total/(len(t) * len(u))
        dist_total = 0
        for i in s:
            for z in u:
                dist_total+= abs(i-z) 
        dsu = dist_total/(len(s) * len(u))
        dist = (len(t)/(len(t) + len(s)))*abs(dtu) + (len(s)/(len(t) + len(s)))*abs(dsu) 
        return dist
    
def update_matrix(t,s, matrix, distance_matrix,method):
    index=0
    extra = []
    for i in distance_matrix: # bazoume tin nea apostasi gia kathe palio stoixeio tou pinaka se sxesi me to kainourio
        distance = calculate_distance(t,s,matrix[index],method)
        i.append(distance)
        index+=1
        extra.append(distance)
    extra.append(0)
    # to extra einai i teleutaia grammi 
    distance_matrix.append(extra)
    return distance_matrix

def lance_williams(method, matrix):
    # Briskoume ton arxiko pinaka
    distance_matrix = calculate_initial_matrix(matrix)
    # Epanalispi i opoia teleiwnei otan den exoume alla stoixeia na enwsoume
    while(len(matrix) >1):
        index_i, index_j, distance = find_min_distance(distance_matrix)
        if max(matrix[index_i]) < max(matrix[index_j]): 
            print("(",*matrix[index_i],") (",*matrix[index_j],")",distance, len(matrix[index_i])+len(matrix[index_j]))
        else:
            print("(",*matrix[index_j],") (",*matrix[index_i],")",distance, len(matrix[index_i])+len(matrix[index_j]))
        # kanoume delete ta stoixeia tou distance pou den xreiazomaste
        del distance_matrix[index_i]
        del distance_matrix[index_j-1]
        for i in distance_matrix:    
            del i[index_i]
            del i[index_j-1]# Kataxwtoume ta 2 stoixeia pou tha apotelesoun to u
        t = matrix[index_i]
        s = matrix[index_j]
        # enwnoume kai diagrafoume ta stoixeia pou enwnoume
        matrix.append(matrix[index_i] + matrix[index_j])
        matrix.remove(matrix[index_j])
        matrix.remove(matrix[index_i])
        matrix[len(matrix)-1].sort()
        if len(matrix) >1:
            distance_matrix = update_matrix(t,s,matrix,distance_matrix,method)

# Ksikinima programmatos
method = sys.argv[1]
filename= sys.argv[2]
with open(filename, "r") as file:
    lines = file.readlines()
num_list = []
for line in lines:
    num_list += list(map(int, line.split()))
num_list.sort()
matrix = [[num] for num in num_list]
lance_williams(method, matrix)