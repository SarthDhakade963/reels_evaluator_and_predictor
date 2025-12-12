VPI_TIERS = {
    "viral_base": [
        "shareability",
        "relatability",
    ],
    "qss_tier_1_retention": [
        "hook_quality",
        "algorithmic_hook_retention",
        "loopability"
    ],
    "qss_tier_2_core": [
        "relevance_to_video", "style_cohesion", "linguistic_quality", "emotional_coherence",
        "creativity_vs_genericness", "emotional_intensity", "story_dimension",
        "visual_quality", "human_presence", "viral_archetype_match"
    ]
}

VBS_PERFECTION_THRESHOLD = 1.0
QSS_HIGH_QUALITY_THRESHOLD = 0.70
QSS_1_RETENTION_THRESHOLD = 0.80
VBS_MIN_PASS_RAW = 7
QSS_1_MIN_PASS_RAW = 10


def calculate_checklist_score(check_dict):
    """
    Calculates the raw score (Yes/Total) for a category, handling nesting.
    (Function remains the same)
    """
    yes_count = 0
    total_count = 0
    for key, value in check_dict.items():
        if isinstance(value, dict):
            nested_yes, nested_total = calculate_checklist_score(value)
            yes_count += nested_yes
            total_count += nested_total
        elif isinstance(value, str):
            total_count += 1
            if value.strip().lower() == "yes":
                yes_count += 1
    return yes_count, total_count


def calculate_vpi_components(full_result):
    """
    Calculates the three core metrics: VBS, QSS-Total, and QSS-1.
    
    Returns: (vbs, max_vbs, qss_total, max_qss_total, qss_1, max_qss_1, category_data)
    """
    vbs_score, max_vbs = 0, 0
    qss_1_score, max_qss_1 = 0, 0
    qss_2_score, max_qss_2 = 0, 0

    category_data = {}

    for category in VPI_TIERS['viral_base']:
        yes, total = calculate_checklist_score(full_result.get(category, {}))
        vbs_score += yes
        max_vbs += total
        category_data[category] = {'yes': yes, 'total': total, 'group': 'VBS'}

    for category in VPI_TIERS['qss_tier_1_retention']:
        yes, total = calculate_checklist_score(full_result.get(category, {}))
        qss_1_score += yes
        max_qss_1 += total
        category_data[category] = {'yes': yes,
                                   'total': total, 'group': 'QSS-1'}

    for category in VPI_TIERS['qss_tier_2_core']:
        yes, total = calculate_checklist_score(full_result.get(category, {}))
        qss_2_score += yes
        max_qss_2 += total
        category_data[category] = {'yes': yes,
                                   'total': total, 'group': 'QSS-2'}

    qss_total_score = qss_1_score + qss_2_score
    max_qss_total = max_qss_1 + max_qss_2

    return (vbs_score, max_vbs, qss_total_score, max_qss_total, qss_1_score, max_qss_1, category_data)
