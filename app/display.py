import streamlit as st
import pandas as pd
import random

from scoring import (
    calculate_checklist_score,
    calculate_vpi_components,
    VBS_PERFECTION_THRESHOLD,  # 1.0
    QSS_HIGH_QUALITY_THRESHOLD,  # 0.70
    QSS_1_RETENTION_THRESHOLD,  # 0.80
    VBS_MIN_PASS_RAW,  # 7
    QSS_1_MIN_PASS_RAW  # 10
)


def sample_preview_frames(frames, preview_count=6):
    total = len(frames)
    if total <= preview_count:
        return list(range(total))
    indices = {0, total - 1}
    remaining_needed = preview_count - 2
    middle_indices = list(range(1, total - 1))
    random_samples = random.sample(middle_indices, remaining_needed)
    indices.update(random_samples)
    return sorted(indices)


def display_final_vpi_report(full_result, total_frames):
    """
    Renders the detailed Video Evaluation Rubric results using the 4-Tier VPI system
    with the critical +/-1 tolerance buffer applied.
    """
    if "error" in full_result:
        st.error(
            f"Cannot display results due to evaluation error: {full_result['error']}")
        return

    # 1. CALCULATE CORE VBS/QSS COMPONENTS
    (vbs_score, max_vbs,
     qss_total_score, max_qss_total,
     qss_1_score, max_qss_1,
     category_data) = calculate_vpi_components(full_result)

    vbs_percent = vbs_score / max_vbs if max_vbs > 0 else 0
    qss_total_percent = qss_total_score / max_qss_total if max_qss_total > 0 else 0
    qss_1_percent = qss_1_score / max_qss_1 if max_qss_1 > 0 else 0

    qss_total_required = QSS_HIGH_QUALITY_THRESHOLD * max_qss_total
    qss_1_required = QSS_1_RETENTION_THRESHOLD * max_qss_1

    # Calculate Overall Raw Score for Conclusion
    total_passed = vbs_score + qss_total_score
    total_checks = max_vbs + max_qss_total
    final_percentage = (total_passed / total_checks) * \
        100 if total_checks > 0 else 0
    final_percentage_str = f"{final_percentage:.1f}%"

    # 2. APPLY THE CRITICAL GATES WITH +/-1 TOLERANCE
    vbs_gate_passed = (vbs_score >= VBS_MIN_PASS_RAW)
    qss_1_gate_passed = (qss_1_score >= QSS_1_MIN_PASS_RAW)

    # Check for strict perfection (Tier 1 requirement)
    vbs_is_perfect = (vbs_percent == VBS_PERFECTION_THRESHOLD)

    # 3. RUN 4-TIER VPI DIAGNOSTIC LOGIC (The updated system)

    if not vbs_gate_passed or not qss_1_gate_passed:
        # TIER 4: Self-Sabotage (Fatal Flaw - Failed even with tolerance)
        vpi_tier = "Tier 4: 🚫 Self-Sabotage"
        prediction_title = "FATAL FLAW IDENTIFIED"

        if not vbs_gate_passed:
            # Scenario A: VBS Failure
            diagnosis = f"**Topic Failed (VBS {vbs_score}/{max_vbs}):** The VBS fell below the critical threshold of {VBS_MIN_PASS_RAW}/{max_vbs}, making the video fundamentally unshareable. **Action Required: FIX TOPIC/EMOTIONAL CORE.**"
        else:
            # Scenario B: QSS-1 Failure (The crucial update)
            diagnosis = f"**Topic Passed (VBS {vbs_score}/{max_vbs}):** The video is highly relevant. **Action Required: CRITICAL FIX.** The video immediately failed the **Algorithm Gate (QSS-1)**, scoring only {qss_1_score}/{max_qss_1}. This means the hook, loopability, or algorithmic cue delivery was fundamentally broken."

        status_icon = "🔴"
        st.error(f"🚨 TIER 4 DIAGNOSIS: {prediction_title}")

    elif vbs_gate_passed and qss_1_gate_passed:
        # VBS and QSS-1 Gates Passed (The video has viral potential)

        if qss_total_percent >= 0.80 and vbs_is_perfect:  # Tier 1: Requires VBS 100% and QSS-Total 80%+
            # TIER 1: Viral Champion
            vpi_tier = "Tier 1: 🏆 Viral Champion"
            prediction_title = "OPTIMAL: Gold Standard"
            diagnosis = "The video is a 'Viral Champion.' Perfect connection (VBS 100%), strong retention, and excellent quality. Failure indicates an external factor."
            status_icon = "🟢"
            st.success(f"🎯 TIER 1 DIAGNOSIS: {prediction_title}")

        # Tier 2 Threshold (0.70 to 0.79 or VBS 7/8 with QSS-Total > 80%)
        elif qss_total_percent >= QSS_HIGH_QUALITY_THRESHOLD:
            # TIER 2: High Potential
            vpi_tier = "Tier 2: ✨ High Potential"
            prediction_title = "STRONG CONTENDER"
            if vbs_is_perfect:
                diagnosis = f"Perfect VBS and strong QSS. This suggests high reach, but the overall QSS ({qss_total_percent:.1%}) is slightly below the Champion level, leaving room for refinement."
            else:  # VBS was a near-miss (7/8)
                diagnosis = f"This is a Strong Contender. The VBS was a near-miss ({vbs_score}/{max_vbs}), but high execution quality (QSS-Total: {qss_total_percent:.1%}) indicates a high chance of sustained virality."

            status_icon = "🔵"
            st.info(f"✨ TIER 2 DIAGNOSIS: {prediction_title}")

        else:  # QSS-Total < 0.70
            # TIER 3: Lottery Ticket
            vpi_tier = "Tier 3: 💡 Lottery Ticket"
            prediction_title = "HIGH-RISK/HIGH-REWARD OUTLIER"
            diagnosis = f"The core gates passed (VBS/QSS-1), but poor overall execution (QSS-Total: {qss_total_percent:.1%}) makes the success high-risk. High reach is possible, but success is an outlier."
            status_icon = "🟡"
            st.warning(f"⚠️ TIER 3 DIAGNOSIS: {prediction_title}")

    else:
        # Fallback for unexpected states
        vpi_tier = "UNKNOWN"
        diagnosis = "Check scoring inputs."
        status_icon = "❓"
        prediction_title = "UNCLASSIFIED"

    st.title("✅ Video Content Rubric: VPI TIER REPORT")
    st.caption(
        "Diagnosis based on the 4-Tier Viral Potential Index (VPI) System with $\pm 1$ Tolerance.")
    st.markdown("---")

    st.header("📝 Evaluation Context")
    st.info(f"**Frames Analyzed:** {total_frames} (sampled at 1 fps)")
    st.markdown("---")

    # --- PREDICTION SUMMARY (Updated) ---
    st.header(f"{status_icon} VPI Tier Prediction")
    st.subheader(f"Final VPI Tier: **{vpi_tier}**")
    st.markdown(f"**Prediction Title:** {prediction_title}")
    st.markdown(f"**Diagnosis:** {diagnosis}")

    st.markdown("---")
    st.markdown("### 📊 The VPI Tier Logic")
    st.markdown("The final tier is determined by passing the **VBS ($\ge 7/8$)** and **QSS-1 ($\ge 10/13$)** critical gates, followed by the overall QSS-Total percentage. **Note:** Tier 1 requires strict VBS perfection (8/8).")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="❤️ VIRAL BASE SCORE (VBS) - Audience Connection",
            value=f"{vbs_score} / {max_vbs}",
            delta=f"{vbs_percent:.1%} (Pass $\ge {VBS_MIN_PASS_RAW}/{max_vbs}$)",
            delta_color="normal"
        )
        st.markdown("**VBS Categories:** Shareability, Relatability")

    with col2:
        st.metric(
            label="🛠️ QSS-TOTAL - Execution & Retention (Overall)",
            value=f"{qss_total_score} / {max_qss_total}",
            delta=f"{qss_total_percent:.1%}",
            delta_color="normal"
        )
        st.markdown(
            f"**Tier 2 Threshold:** {QSS_HIGH_QUALITY_THRESHOLD:.0%} ({qss_total_required:.0f} / {max_qss_total})")

    with col3:
        st.metric(
            label="⚡ QSS-1 - Hook & Retention (Critical Gate)",
            value=f"{qss_1_score} / {max_qss_1}",
            delta=f"{qss_1_percent:.1%}",
            delta_color="normal"
        )
        st.markdown(
            f"**Pass Gate:** $\ge {QSS_1_MIN_PASS_RAW}/{max_qss_1}$ ({QSS_1_RETENTION_THRESHOLD*100:.0f}%)")

    st.markdown("---")
    st.header("Detailed Category Breakdown")
    # ... (Category names and summary logic remain the same)

    # Define the order and name mapping
    category_names = {
        "shareability": "1. Shareability", "relatability": "2. Relatability",
        "hook_quality": "3. Hook Quality", "algorithmic_hook_retention": "4. Algorithmic Hook", "loopability": "5. Loopability",
        "story_dimension": "6. Story Dimension", "visual_quality": "7. Visual Quality",
        "emotional_coherence": "8. Emotional Coherence", "emotional_intensity": "9. Emotional Intensity",
        "relevance_to_video": "10. Relevance", "style_cohesion": "11. Style Cohesion",
        "linguistic_quality": "12. Linguistic Quality", "human_presence": "13. Human Presence",
        "creativity_vs_genericness": "14. Creativity/Value", "viral_archetype_match": "15. Viral Archetype Match",
    }

    summary_data = []

    # Update group names based on the new VPI_TIERS structure
    group_mapping = {
        'shareability': 'VBS', 'relatability': 'VBS',
        'hook_quality': 'QSS-1', 'algorithmic_hook_retention': 'QSS-1', 'loopability': 'QSS-1',
        # All others are QSS-2
        'story_dimension': 'QSS-2', 'visual_quality': 'QSS-2', 'emotional_coherence': 'QSS-2',
        'emotional_intensity': 'QSS-2', 'relevance_to_video': 'QSS-2', 'style_cohesion': 'QSS-2',
        'linguistic_quality': 'QSS-2', 'human_presence': 'QSS-2', 'creativity_vs_genericness': 'QSS-2',
        'viral_archetype_match': 'QSS-2',
    }

    for key, name in category_names.items():
        score_data = category_data.get(key, {})
        if score_data:
            summary_data.append([
                name,
                # Use the new mapping for display
                group_mapping.get(key, 'N/A'),
                f"{score_data['yes']}/{score_data['total']}",
                f"{score_data['yes']/score_data['total']:.1%}" if score_data['total'] > 0 else 'N/A'
            ])

    summary_df = pd.DataFrame(summary_data, columns=[
        "Category", "Group (VBS/QSS)", "Checks Passed (Raw)", "Score (%)"])

    st.dataframe(summary_df, use_container_width=True)

    st.markdown("---")

    st.header("🔎 Full CheckList Breakdown")

    def render_detail_checks(title, check_dict):
        yes, total = calculate_checklist_score(check_dict)
        st.subheader(f"🔹 {title} Checklist Score: **`{yes}/{total}`**")
        check_data = []
        for key, value in check_dict.items():
            icon = "✅" if value.strip().lower(
            ) == "yes" else "❌" if value.strip().lower() == "no" else "➖"
            display_key = key.replace('_', ' ').capitalize()
            check_data.append(
                [display_key, value, icon])
        df = pd.DataFrame(check_data, columns=["Check", "Result", "Icon"])
        st.dataframe(df, use_container_width=True)

    for key, name in category_names.items():
        st.markdown(f"### {name}")
        render_detail_checks(name, full_result.get(key, {}))

    st.markdown("---")
    st.header("✨ Conclusion")
    st.success(
        f"Overall RAW Checklist Score (All Categories): **{total_passed} / {total_checks}** ({final_percentage_str}). Use this only as a reference, not for prediction.")
    st.info("The VPI Tier system provides a clear roadmap: **Tier 4** requires fixing a fatal flaw (VBS or QSS-1). **Tier 3** is highly risky. Aim for **Tier 1** for reliable, repeatable viral success.")
