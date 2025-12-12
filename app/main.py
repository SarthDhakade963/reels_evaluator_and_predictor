import streamlit as st

from display import display_final_vpi_report, sample_preview_frames
from evaluator import evaluate_video
from extract_frame import extract_frames

st.set_page_config(page_title="Reel Evaluator Evaluator", layout="wide")

st.title("🎥 Reel Evaluator")

uploaded_video = st.file_uploader("Upload a video", type=["mp4", "mov", "mkv"])

if uploaded_video:
    st.subheader("Extracting Frames…")

    @st.cache_data
    def get_frames(video_file, fps):
        return extract_frames(video_file.read(), fps)

    frames = get_frames(uploaded_video, fps=1)

    st.write(f"Extracted {len(frames)} frames (1 fps sampling)")

    st.subheader("Preview Frames")

    preview_indices = sample_preview_frames(frames, preview_count=6)

    cols = st.columns(3)
    for i, idx in enumerate(preview_indices):
        with cols[i % 3]:
            st.image(frames[idx], caption=f"Frame {idx}")

    st.subheader("Run Rubric Evaluation")
    if st.button("Evaluate Video Content"):
        with st.spinner("Analyzing frames for evaluation…"):
            full_evaluation_result = evaluate_video(frames)
            
            st.subheader("Evaluation Results")

            display_final_vpi_report(full_evaluation_result, len(frames))

            st.success("Evaluation Complete!")
