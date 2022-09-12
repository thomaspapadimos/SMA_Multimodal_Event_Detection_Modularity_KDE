library("igraph")

### Parameters ###
#input_file = "users.csv"
input_file = 'user_pairs.csv'
### Import data and make graph ###
g = read.csv(file = input_file, header = FALSE, sep = ";", encoding = 'iso-8859-3')
g = as.matrix(g)
g = matrix(as.character(g),ncol=2)
g = graph_from_edgelist(g, directed = FALSE)
g = simplify(g)
g = delete_vertices(g, which(degree(g)==0))

start_time <- Sys.time()

### Find communities ###
 #communities_g = cluster_edge_betweenness(g)
 #communities_g = cluster_fast_greedy
 #communities_g=cluster_infomap
 #communities_g=cluster_label_prop
 #communities_g=cluster_leading_eigen
 communities_g=cluster_louvain(g)
 #communities_g=cluster_optimal
 #communities_g=cluster_spinglass
 #communities_g=cluster_walktrap
# print(length(communities_g))
 
# communities = communities(communities_g)
# members = membership(communities_g)
# members_table = table(members)
# print(max(members_table))
# 
 modularity = modularity(communities_g)
 cat(modularity)
 #print(round(modularity, digits = 2))
# 
# codelen = code_len(communities_g)
# print(codelen)

### Find top key players ###
# components_g = components(g)
# members_components = components_g$membership
# 
# graph.components.size = components_g$csize
# giant_component = induced.subgraph(g, names(which(members_components==which.max(graph.components.size))))
# 
# MEB = rep(0,length(V(giant_component)))
# Betweenness_centrality = betweenness(giant_component, normalized = TRUE)
# Betweenness_centrality = Betweenness_centrality + 10^(-9)
# for(i in 1:length(V(giant_component))) MEB[i] = -Betweenness_centrality[i]*sum(log(10^(-9) + betweenness
# (giant_component, v = neighbors(giant_component, V(giant_component)[i]), normalized = TRUE)))
# 
# MEB_results = sort.int(MEB, decreasing = TRUE, index.return = TRUE)
# if(length(MEB_results$ix)>10){top_MEB_users = names(V(giant_component)[MEB_results$ix[1:10]])}else{top_MEB_users = names(V(giant_component)[MEB_results$ix])}
# print(top_MEB_users)

end_time <- Sys.time()
#print(round(end_time - start_time, digits = 2))
