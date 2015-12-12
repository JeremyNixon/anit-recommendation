def recommend_link(user, centroids):
    max_distance = 0
    recommendation = None
    for centroid in centroids:
        if np.linalg.norm(user - centroid) > max_distance:
            max_distance = np.linalg.norm(user - centroid)
            recommendation = links[np.argmax(centroid)]
    return recommendation

