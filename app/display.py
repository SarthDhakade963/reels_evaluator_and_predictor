import streamlit as st

from scoring import calculate_checklist_score, calculate_total_rubric_score
import pandas as pd

def display_final_rubric_output(full_result, total_frames):
    """
    Renders the detailed Quote Evaluation Rubric results, now using the total 
    checklist score for the final rating.
    """
    if "error" in full_result:
        error_details = full_result['error']
        if isinstance(error_details, dict) and 'message' in error_details:
            st.error(
                f"Cannot display results due to evaluation error:\n\n{error_details['message']}")
        else:
            st.error(
                f"Cannot display results due to evaluation error: {error_details}")
        return

    total_passed, total_checks = calculate_total_rubric_score(full_result)

    if total_checks > 0:
        final_percentage = (total_passed / total_checks) * 100
        final_percentage_str = f"{final_percentage:.1f}%"
    else:
        final_percentage_str = "N/A"

    st.title("✅ Video Content Rubric: FINAL REPORT")
    st.markdown("---")

    st.header("📝 Evaluation Context")
    st.info(f"**Frames Analyzed:** {total_frames} (sampled at 1 fps)")
    st.markdown("---")

    st.header("⭐ Overall Checklist Score Summary")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(
            label="FINAL CHECKLIST RATING (Passed/Total)",
            value=f"{total_passed} / {total_checks}",
            delta=f"Equivalent to {final_percentage_str}",
            delta_color="normal"
        )

    score_mapping = {
        "relevance": "Relevance",
        "linguistic_quality": "Linguistic Quality",
        "emotional_coherence": "Emotional Coherence",
        "creativity": "Creativity",
        "algorithmic_hook": "Algorithmic Hook",
        "emotional_intensity": "Emotional Intensity",
    }

    summary_data = []

    style_checks = full_result.get("style_accuracy", {})
    style_yes, style_total = calculate_checklist_score(style_checks)
    summary_data.append(
        ["Style Accuracy (Nested)", f"{style_yes}/{style_total}"])

    for key, name in score_mapping.items():
        check_dict = full_result.get(key, {})
        yes, total = calculate_checklist_score(check_dict)
        summary_data.append([name, f"{yes}/{total}"])

    with col2:
        summary_df = pd.DataFrame(summary_data, columns=[
            "Category", "Checklist Score"])
        st.dataframe(summary_df.set_index(
            'Category'), use_container_width=True)

    st.markdown("---")

    st.header("🔎 Detailed Rubric Checks (Yes/No Breakdown)")

    def render_nested_checks(title, check_dict, is_style_accuracy=False):
        yes, total = calculate_checklist_score(check_dict)
        st.subheader(f"🔹 {title} Checklist Score: **`{yes}/{total}`**")

        if is_style_accuracy:
            for style_key, style_checks in check_dict.items():
                if isinstance(style_checks, dict):
                    nested_yes, nested_total = calculate_checklist_score(
                        style_checks)
                    st.markdown(
                        f"**{style_key.title()} Sub-Category Score:** **`{nested_yes}/{nested_total}`**")

                    check_data = []
                    for sub_key, sub_value in style_checks.items():
                        icon = "✅" if sub_value.lower() == "yes" else "❌" if sub_value.lower() == "no" else "➖"
                        check_data.append(
                            [f"{sub_key.replace('_', ' ').capitalize()}", sub_value, icon])

                    df = pd.DataFrame(check_data, columns=[
                        "Check", "Result", "Icon"])
                    st.dataframe(df, use_container_width=True)
            return

        check_data = []
        for key, value in check_dict.items():
            icon = "✅" if value.lower() == "yes" else "❌" if value.lower() == "no" else "➖"
            check_data.append(
                [key.replace('_', ' ').capitalize(), value, icon])

        df = pd.DataFrame(check_data, columns=["Check", "Result", "Icon"])
        st.dataframe(df, use_container_width=True)

    st.markdown("### 1. Relevance to Scene")
    render_nested_checks("Relevance", full_result.get("relevance", {}))

    st.markdown("### 2. Style Accuracy (with sub-scores)")
    render_nested_checks("Style Accuracy", full_result.get(
        "style_accuracy", {}), is_style_accuracy=True)

    st.markdown("### 3. Linguistic Quality")
    render_nested_checks("Linguistic Quality",
                         full_result.get("linguistic_quality", {}))

    st.markdown("### 4. Emotional Coherence")
    render_nested_checks("Emotional Coherence",
                         full_result.get("emotional_coherence", {}))

    st.markdown("### 5. Creativity")
    render_nested_checks("Creativity", full_result.get("creativity", {}))

    st.markdown("### 6. Algorithmic Hook")
    render_nested_checks("Algorithmic Hook",
                         full_result.get("algorithmic_hook", {}))

    st.markdown("### 7. Emotional Intensity")
    render_nested_checks("Emotional Intensity",
                         full_result.get("emotional_intensity", {}))

    st.markdown("---")
    st.header("✨ Conclusion")
    st.success(
        f"Final Checklist Score: {total_passed}/{total_checks} ({final_percentage_str}).")
