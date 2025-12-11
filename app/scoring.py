def calculate_checklist_score(check_dict):
    """
    Calculates the score (e.g., 3/4) from a dictionary of 'yes/no' checks. 
    It is now recursive to handle Style Accuracy's nested structure.
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


def calculate_total_rubric_score(full_result):
    """
    Calculates the final score based on summing all 'Yes' checks across the entire rubric.
    """
    total_passed = 0
    total_checks = 0

    categories = [
        "relevance", "style_accuracy", "linguistic_quality",
        "emotional_coherence", "creativity", "algorithmic_hook",
        "emotional_intensity"
    ]

    for category in categories:
        check_dict = full_result.get(category, {})
        if check_dict:
            yes, total = calculate_checklist_score(check_dict)
            total_passed += yes
            total_checks += total

    return total_passed, total_checks
