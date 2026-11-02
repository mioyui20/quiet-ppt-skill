# Motion and compatibility

[中文](motion.md)

Choose motion after style/content matching. Annular imagery is a special reference example, not this skill's default. Management, research and teaching pages do not automatically receive wheels.

## Reference and treatments

The approximately 5.03-second Bilibili excerpt was inspected at roughly 0.2-second intervals. It shows image sectors rotating around a shared center, horizontal text handing over vertically, and a ring moving to the center. This establishes visual behavior, not the original application, easing or playback rate. Do not copy its artwork, subtitles, frame, watermark or copy. Live presentations need longer reading holds.

| Treatment | Relationship | Starting duration |
| --- | --- | --- |
| Continuous image | Overview/detail or related view | Morph about 0.55–0.85 s |
| Annular sectors | Requested chapter or multiple-view treatment | About 0.8–1.2 s |
| Horizontal text handover | Changed copy with a continuous visual | Fade, optionally 16–32 px vertical movement, about 0.25–0.45 s |
| Small local rotation | Diagram emphasis or alignment | About 0.7–1.0 s |
| Short fade | Independent argument or dense evidence | About 0.25–0.4 s |

These are recommendations, not measured video parameters. In a typical six-to-ten-slide report, one or two continuity moments may suffice. Adjust to narrative and user requirements.

## Native Morph

Design start/end states first. Preserve objects across adjacent slides, ideally by duplication. For forced matching, use identical `!!object-name` names, unique per slide. Put Morph on the destination using Objects mode. Do not force different body paragraphs into matching objects.

For annular sectors, preserve center, radius, boundaries and stacking. Use editable native pictures and clips/masks when possible. Avoid rotation around each sector's tight bounds instead of the shared center. Keep text outside the rotating group. Inspect intermediate states for drift, gaps, stretched crops and occlusion. If geometry cannot export reliably, choose an image continuity/fade simplification and disclose it.

The optional Python standard-library helper sets transitions on an existing deck:

```bash
python scripts/set_transitions.py draft.pptx animated.pptx --morph-slides 3 --duration 0.85
```

It rejects identical input/output, existing output, invalid targets and missing forced pairs. Ordinary slides become fades; chosen destinations become object Morph with a fade fallback. It does not build masks, centers, layouts or per-object sequences. Identical start/end states will not visibly rotate merely because a transition exists. Prefer the authoring tool for focused changes to complex existing transitions.

## Verification

1. Static: readable end states, editability, angles/centers and unique pairs.
2. File: intended destination, valid relationships, fonts and bounds.
3. Playback: native slideshow/video export; inspect seams, jumps, text deformation and pacing.

The first two do not establish playback. Static previews/PDFs have no native transitions; browser recreations do not establish PowerPoint behavior. Players may differ. Keep click-to-advance for live use unless automatic timing is requested.

Sources: [Microsoft Morph](https://support.microsoft.com/en-us/powerpoint/morph-transition-tips-and-tricks), [MS-PPTX Morph](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-pptx/68d26d78-f7f5-47ab-835d-4e6c82ff39f0).
