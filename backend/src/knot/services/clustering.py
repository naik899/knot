"""Patent clustering by classification and keyword overlap."""

from knot.models.patent import Patent
from knot.models.landscape import PatentCluster
from knot.services.similarity import keyword_similarity


def cluster_patents(patents: list[Patent], similarity_threshold: float = 0.15) -> list[PatentCluster]:
    """Cluster patents by classification code and keyword overlap.

    Uses a simple greedy clustering approach:
    1. Group by primary classification code prefix
    2. Merge groups with high keyword overlap
    """
    if not patents:
        return []

    # Step 1: Group by classification code prefix (first 4 chars)
    code_groups: dict[str, list[Patent]] = {}
    for patent in patents:
        if patent.classifications:
            code = patent.classifications[0].code[:4]
        else:
            code = "NONE"
        code_groups.setdefault(code, []).append(patent)

    # Step 2: Build initial clusters
    clusters = []
    for i, (code, group) in enumerate(code_groups.items()):
        # Collect all keywords from patents in this group
        all_keywords = set()
        for p in group:
            all_keywords.update(k.lower() for k in p.keywords)

        cluster = PatentCluster(
            id=f"CLU{i+1:03d}",
            label=f"{code} cluster",
            keywords=sorted(all_keywords),
            patent_ids=[p.id for p in group],
            density=len(group) / max(len(patents), 1),
            classification_codes=[code],
        )
        clusters.append(cluster)

    # Step 3: Merge clusters with high keyword overlap
    merged = True
    while merged:
        merged = False
        new_clusters = []
        skip = set()
        for i, c1 in enumerate(clusters):
            if i in skip:
                continue
            for j, c2 in enumerate(clusters):
                if j <= i or j in skip:
                    continue
                sim = keyword_similarity(c1.keywords, c2.keywords)
                if sim >= similarity_threshold:
                    # Merge c2 into c1
                    new_cluster = PatentCluster(
                        id=c1.id,
                        label=f"{c1.label} + {c2.label}",
                        keywords=sorted(set(c1.keywords) | set(c2.keywords)),
                        patent_ids=c1.patent_ids + c2.patent_ids,
                        density=(len(c1.patent_ids) + len(c2.patent_ids)) / max(len(patents), 1),
                        classification_codes=list(set(c1.classification_codes + c2.classification_codes)),
                    )
                    new_clusters.append(new_cluster)
                    skip.add(i)
                    skip.add(j)
                    merged = True
                    break
            if i not in skip:
                new_clusters.append(c1)
        clusters = new_clusters

    return clusters


def identify_white_spaces(
    clusters: list[PatentCluster],
    all_keywords: set[str],
) -> list[dict]:
    """Identify technology areas not well covered by existing patents.

    White spaces are keyword areas that appear in few or no clusters.
    """
    # Collect covered keywords
    covered_keywords = set()
    for cluster in clusters:
        covered_keywords.update(cluster.keywords)

    # Find uncovered or lightly covered keywords
    uncovered = all_keywords - covered_keywords

    white_spaces = []
    if uncovered:
        white_spaces.append({
            "description": f"Uncovered technology area: {', '.join(sorted(uncovered)[:5])}",
            "keywords": sorted(uncovered),
            "adjacent_clusters": [c.id for c in clusters[:3]],
            "opportunity_score": min(0.9, len(uncovered) / max(len(all_keywords), 1)),
        })

    # Also find gaps between clusters (areas with low density)
    low_density = [c for c in clusters if c.density < 0.1]
    for cluster in low_density:
        white_spaces.append({
            "description": f"Low density area near {cluster.label}",
            "keywords": cluster.keywords[:5],
            "adjacent_clusters": [cluster.id],
            "opportunity_score": 1.0 - cluster.density,
        })

    return white_spaces
