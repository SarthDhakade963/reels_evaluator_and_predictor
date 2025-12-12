from google.genai import types

FULL_RUBRIC_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "relevance_to_video": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "relate_to_happening": types.Schema(type=types.Type.STRING, description="Does the quote clearly relate to what is happening in the video?"),
                "avoid_unshown_objects": types.Schema(type=types.Type.STRING, description="Does it avoid mentioning objects or actions not shown?"),
                "theme_match": types.Schema(type=types.Type.STRING, description="Does the quote’s theme match the video’s theme?"),
                "no_contradictions": types.Schema(type=types.Type.STRING, description="Does it avoid contradicting any visual detail?"),
            }
        ),
        "style_cohesion": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "tone_consistent": types.Schema(type=types.Type.STRING, description="Does the chosen style (e.g., Poetic, Wholesome) remain consistent throughout the video?"),
                "visuals_support_style": types.Schema(type=types.Type.STRING, description="Do the visuals/color/pacing strongly support the chosen style?"),
                "style_dominant": types.Schema(type=types.Type.STRING, description="Is the intended emotional/aesthetic style clearly dominant over other possible styles?"),
            }
        ),
        "linguistic_quality": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "grammar": types.Schema(type=types.Type.STRING, description="Is it grammatically correct?"),
                "clarity": types.Schema(type=types.Type.STRING, description="Is the sentence structure clear?"),
                "natural_flow": types.Schema(type=types.Type.STRING, description="Does the line flow naturally?"),
                "concise": types.Schema(type=types.Type.STRING, description="Is it concise without filler?"),
            }
        ),
        "emotional_coherence": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "tone_fit": types.Schema(type=types.Type.STRING, description="Does the emotional tone match the video?"),
                "no_mismatch": types.Schema(type=types.Type.STRING, description="Does it avoid any emotional mismatch?"),
                "consistent": types.Schema(type=types.Type.STRING, description="Is the emotional tone consistent throughout?"),
            }
        ),
        "creativity_vs_genericness": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "novelty_of_insight": types.Schema(type=types.Type.STRING, description="Does the quote/video offer a perspective or emotional truth that feels new to the niche?"),
                "immediate_value_save": types.Schema(type=types.Type.STRING, description="Does the content provide actionable advice, deep comfort, or a unique aesthetic worth Saving? **CRITICAL: If the value is generic or common in this niche, score NO.**"),
                "no_cliches": types.Schema(type=types.Type.STRING, description="Does the quote text avoid generic, overused language?"),
            }
        ),
        "algorithmic_hook_retention": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "curiosity_gap": types.Schema(type=types.Type.STRING, description="Does the first line create a curiosity gap or promise value? **CRITICAL: If the first line can be ignored without losing context, score NO.**"),
                "encourage_saves": types.Schema(type=types.Type.STRING, description="Does the content encourage Saves (tips, comfort, deep thoughts)?"),
                "encourage_replay": types.Schema(type=types.Type.STRING, description="Does the quote encourage replay due to depth or nuance?"),
                "tight_pacing": types.Schema(type=types.Type.STRING, description="Is the pacing tight, with no dead moments?"),
                "text_placement": types.Schema(type=types.Type.STRING, description="Does the text placement enhance retention?"),
            }
        ),
        "emotional_intensity": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "clear_emotion_start": types.Schema(type=types.Type.STRING, description="Does the video deliver a clear emotion in the first 3 seconds?"),
                "high_arousal": types.Schema(type=types.Type.STRING, description="Does the quote trigger a high-arousal emotion (awe, surprise, joy, etc.)?"),
                "deeply_relatable": types.Schema(type=types.Type.STRING, description="Is the quote deeply relatable to a large niche audience?"),
                "emotional_arc": types.Schema(type=types.Type.STRING, description="Does the quote contain a micro emotional arc?"),
                "emotionally_satisfying": types.Schema(type=types.Type.STRING, description="Do the video and quote together feel emotionally “satisfying”?"),
                "dopamine_spike": types.Schema(type=types.Type.STRING, description="Does the quote create a brief dopamine spike?"),
                "tension_shift": types.Schema(type=types.Type.STRING, description="Is there a tension → release or negative → positive shift?"),
            }
        ),
        "hook_quality": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "clear_hook_start": types.Schema(type=types.Type.STRING, description="Is there a clear hook at the start of the video?"),
                "hold_viewers_past_1s": types.Schema(type=types.Type.STRING, description="Would this hook hold millions of viewers past 1 second?"),
                "high_arousal_response": types.Schema(type=types.Type.STRING, description="Does the hook produce a high-arousal emotional response?"),
                "hook_type": types.Schema(type=types.Type.STRING, description="Is the hook visual, textual, or movement-based? (YES/NO based on presence/effectiveness.)"),
                "thumbnail_hook": types.Schema(type=types.Type.STRING, description="Does the thumbnail itself act as a hook? **CRITICAL: If the thumbnail is blurry, too busy, or doesn't visually deliver the hook's promise, score NO.**"),
            }
        ),
        "story_dimension": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "meaningful_story": types.Schema(type=types.Type.STRING, description="Does the video tell an emotional or meaningful story?"),
                "transformation_arc": types.Schema(type=types.Type.STRING, description="Does it show a transformation or comeback arc?"),
                "text_contributes_story": types.Schema(type=types.Type.STRING, description="Does text in the video contribute to the storytelling?"),
            }
        ),
        "visual_quality": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "visually_appealing": types.Schema(type=types.Type.STRING, description="Is the video visually appealing and clean?"),
                "good_lighting_color": types.Schema(type=types.Type.STRING, description="Good lighting and strong color palette?"),
                "visuals_quote_match": types.Schema(type=types.Type.STRING, description="Do visuals and quote match in emotion and tone?"),
                "depth_present": types.Schema(type=types.Type.STRING, description="Is there depth (foreground, midground, background)?"),
                "smooth_camera_movement": types.Schema(type=types.Type.STRING, description="Is smooth camera movement (pan, tilt, dolly, glide)?"),
                "color_palette_consistent": types.Schema(type=types.Type.STRING, description="Is the color palette emotionally consistent?"),
            }
        ),
        "relatability": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "broad_audience": types.Schema(type=types.Type.STRING, description="Is the content relatable to a broad audience?"),
                "resonate_young_adults": types.Schema(type=types.Type.STRING, description="Does it resonate with teens and young adults?"),
                "evoke_universal_memories": types.Schema(type=types.Type.STRING, description="Does it evoke universal or childhood memories?"),
                "create_empathy": types.Schema(type=types.Type.STRING, description="Does it create empathy or “I feel this too”?"),
            }
        ),
        "human_presence": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "human_meaningful": types.Schema(type=types.Type.STRING, description="Is human presence meaningful (not random or distracting)?"),
                "video_feels_personal": types.Schema(type=types.Type.STRING, description="Does the video feel personal or “this is so me”?"),
                "silhouette_relatability": types.Schema(type=types.Type.STRING, description="Does the silhouette/distance increase relatability?"),
            }
        ),
        "loopability": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "loop_seamlessly": types.Schema(type=types.Type.STRING, description="Does the video loop naturally or seamlessly?"),
                "motion_returns_start": types.Schema(type=types.Type.STRING, description="Does the motion return near the starting point?"),
                "ending_encourages_rewatch": types.Schema(type=types.Type.STRING, description="Does the ending feel open enough to encourage rewatch?"),
            }
        ),
        "shareability": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "share_with_friend": types.Schema(type=types.Type.STRING, description="Would someone share this with a friend?"),
                "save_for_comfort": types.Schema(type=types.Type.STRING, description="Is it something people Save for comfort/advice?"),
                "needed_this_today": types.Schema(type=types.Type.STRING, description="Does it feel like “I needed this today”?"),
                "reinforce_identity": types.Schema(type=types.Type.STRING, description="Does it reinforce identity (“This is me”)?"),
            }
        ),
        "viral_archetype_match": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "fits_known_archetype": types.Schema(type=types.Type.STRING, description="Does the reel fit a known viral archetype?"),
                "blends_archetypes": types.Schema(type=types.Type.STRING, description="Does it blend 2–3 archetypes (e.g., nostalgia + healing + aesthetics)?"),
            }
        ),
    }
)
