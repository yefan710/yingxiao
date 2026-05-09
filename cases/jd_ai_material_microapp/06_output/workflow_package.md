# Workflow Package

Product: JD-AI商品素材微应用
Mode: `new_page`
Generated: 2026-05-06T11:23:06

## Status

READY FOR ROLE RUNS

## Intake Issues

- None

## Output Files

1. `00_design_spec.md`
2. `01_requirement_brief.md`
3. `02_screen_plan.md`
4. `03_copy_draft.md`
5. `04_visual_direction.md`
6. `05_asset_plan.md`
7. `05_screenshot_mask_plan.md`
8. `06_production_prompts.md`
9. `07_qa_scorecard.md`
10. `08_revision_routing.md`
11. `09_executed_workflow.md`
12. `10_ui_selection_guide.md`
13. `11_image2_production_workflow.md`
14. `12_review_skill_checklist.md`

## How To Use

1. Open `01_requirement_brief.md` and run the embedded Codex prompt with real source material.
2. Confirm the brief before opening `02_screen_plan.md`.
3. Write final copy before image2 generation; image2 must render the copy and visual layout together.
4. Use `11_image2_production_workflow.md` as the production authority.
5. Generate image2 text bases into `05_assets/image2_text_bases/`.
6. Put real UI screenshots into `05_assets/screenshots/`.
7. Run `python3 bin/compose_jd_ai_image2_text_finals.py` to paste screenshots only.
8. Run the review checklist in `12_review_skill_checklist.md` before accepting final comps.
9. Any `NEEDS_SOURCE` or `MISSING_ASSET` must be resolved or explicitly accepted before production.
