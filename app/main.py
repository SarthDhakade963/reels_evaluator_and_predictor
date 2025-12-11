import streamlit as st

from display import display_final_rubric_output
from evaluator import evaluate_video
from extract_frame import extract_frames

st.set_page_config(page_title="Video Rubric Evaluator", layout="wide")

st.title("🎥 Video → Frames → Rubric Evaluator (Gemini Powered)")

uploaded_video = st.file_uploader("Upload a video", type=["mp4", "mov", "mkv"])

if uploaded_video:
    st.subheader("Extracting Frames…")

    @st.cache_data
    def get_frames(video_file, fps):
        return extract_frames(video_file.read(), fps)

    frames = get_frames(uploaded_video, fps=1)

    st.write(f"Extracted {len(frames)} frames (1 fps sampling)")

    st.subheader("Preview Frames")
    cols = st.columns(3)
    for i, f in enumerate(frames[:6]):
        with cols[i % 3]:
            st.image(f, caption=f"Frame {i}")

    st.subheader("Run Rubric Evaluation")
    if st.button("Evaluate Video Content"):
        with st.spinner("Analyzing frames for evaluation…"):
            full_evaluation_result = evaluate_video(frames)
            
            st.subheader("Evaluation Results")

            display_final_rubric_output(full_evaluation_result, len(frames))

            st.success("Evaluation Complete!")
