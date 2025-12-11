
from google.genai import types

FULL_RUBRIC_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "relevance": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "relates_to_activity": types.Schema(type=types.Type.STRING),
                "no_invented_objects": types.Schema(type=types.Type.STRING),
                "theme_match": types.Schema(type=types.Type.STRING),
                "no_contradictions": types.Schema(type=types.Type.STRING)
            }
        ),
        "style_accuracy": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "motivational": types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "encourages_action": types.Schema(type=types.Type.STRING),
                        "empowering": types.Schema(type=types.Type.STRING),
                        "no_ambiguity": types.Schema(type=types.Type.STRING),
                        "tone_match": types.Schema(type=types.Type.STRING)
                    }
                ),
                "poetic": types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "imagery": types.Schema(type=types.Type.STRING),
                        "flow": types.Schema(type=types.Type.STRING),
                        "sensory": types.Schema(type=types.Type.STRING),
                        "lyrical": types.Schema(type=types.Type.STRING)
                    }
                ),
                "wholesome": types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "warm": types.Schema(type=types.Type.STRING),
                        "simple": types.Schema(type=types.Type.STRING),
                        "togetherness": types.Schema(type=types.Type.STRING),
                    }
                ),
                "nostalgic": types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "memory": types.Schema(type=types.Type.STRING),
                        "warmth": types.Schema(type=types.Type.STRING),
                        "no_motivational": types.Schema(type=types.Type.STRING),
                        "reflective": types.Schema(type=types.Type.STRING)
                    }
                )
            }
        ),
        "linguistic_quality": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "grammar": types.Schema(type=types.Type.STRING),
                "clarity": types.Schema(type=types.Type.STRING),
                "natural_flow": types.Schema(type=types.Type.STRING),
                "concise": types.Schema(type=types.Type.STRING)
            }
        ),
        "emotional_coherence": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "tone_fit": types.Schema(type=types.Type.STRING),
                "no_mismatch": types.Schema(type=types.Type.STRING),
                "consistent": types.Schema(type=types.Type.STRING)
            }
        ),
        "creativity": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "no_cliches": types.Schema(type=types.Type.STRING),
                "unique": types.Schema(type=types.Type.STRING),
                "no_repetition": types.Schema(type=types.Type.STRING)
            }
        ),
        "algorithmic_hook": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "curiosity_gap": types.Schema(type=types.Type.STRING),
                "trending_audio": types.Schema(type=types.Type.STRING),
                "save_worthy": types.Schema(type=types.Type.STRING),
                "call_to_action": types.Schema(type=types.Type.STRING)
            }
        ),
        "emotional_intensity": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "high_arousal": types.Schema(type=types.Type.STRING),
                "relatable": types.Schema(type=types.Type.STRING),
                "emotional_arc": types.Schema(type=types.Type.STRING)
            }
        ),
        "scores": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "relevance_score": types.Schema(type=types.Type.INTEGER),
                "style_score": types.Schema(type=types.Type.INTEGER),
                "linguistic_quality_score": types.Schema(type=types.Type.INTEGER),
                "emotional_coherence_score": types.Schema(type=types.Type.INTEGER),
                "creativity_score": types.Schema(type=types.Type.INTEGER),
                "algorithmic_hook_score": types.Schema(type=types.Type.INTEGER),
                "emotional_intensity_score": types.Schema(type=types.Type.INTEGER),
                "final_score": types.Schema(type=types.Type.INTEGER)
            }
        ),
    }
)
