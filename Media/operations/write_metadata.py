import os
import json
import subprocess
from Media.build_presentation_video import SCENES, BASE_DIR, ASSETS_DIR, OUTPUT_VIDEO, SUBTITLES_SRT, get_audio_duration

scene_durations = {}
for scene in SCENES:
    audio_file = os.path.join(ASSETS_DIR, f"audio_{scene['id']:02d}.mp3")
    dur = get_audio_duration(audio_file)
    scene_durations[scene['id']] = dur + 0.5

metadata_path = os.path.join(BASE_DIR, "video_metadata.json")
with open(metadata_path, "w", encoding="utf-8") as f_meta:
    json.dump({
        "title": "Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting",
        "institution": "University of Science and Technology Beijing (北京科技大学)",
        "video_file": "sand_dust_storm_ml_presentation.mp4",
        "subtitles_file": "sand_dust_storm_subtitles.srt",
        "total_duration_sec": sum(scene_durations.values()),
        "scenes": [
            {
                **sc,
                "duration": scene_durations[sc["id"]],
                "slide_image": f"video_assets/slide_{sc['id']:02d}.png",
                "audio_file": f"video_assets/audio_{sc['id']:02d}.mp3",
                "clip_file": f"video_assets/clip_{sc['id']:02d}.mp4"
            }
            for sc in SCENES
        ]
    }, f_meta, indent=2)

print(f"Saved video metadata to {metadata_path}")
print(f"Total video duration: {sum(scene_durations.values()) / 60.0:.2f} minutes")
