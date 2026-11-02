# Differences / 差异说明

[English README](../README.md) · [中文首页](../README.zh-CN.md)

## Assessment / 判断

Quiet PPT has enough independent workflow content to publish as a focused skill: it combines content-driven style selection, a default presentation density that supports the speaker, per-slide talk tracks, and a separation between visual direction and motion. It also includes reviewed native PPTX examples and a small transition helper.

Its individual techniques are established presentation practices. This is not a claim that style selection, speaker notes or Morph are unique inventions. No controlled benchmark was run against the projects below, and the examples do not prove that every future generated deck will be good.

Quiet PPT 的独立价值是工作流组合：先按内容选风格、默认正文足够讲述、每页附讲稿、视觉方向与动效分开判断，并提供经过检查的原生 PPTX 样例和小型转场工具。各项技术属于已有演示设计实践；本项目不把它们宣称为独有发明，也未开展与下列项目的效果基准比较。

## Reviewed entry points / 核对的入口

Reviewed on 2026-11-02. This comparison describes the linked entry points, not every feature or file in their repositories.

| Project | Emphasis in the reviewed material | Quiet PPT's emphasis |
| --- | --- | --- |
| [anthropics/skills: pptx](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md) | Broad PowerPoint creation, editing, templates, package tooling, editable charts and visual design advice | A focused content/audience style decision before authoring; medium-density explanations and usable talk tracks as the default |
| [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides/blob/main/SKILL.md) | Browser-based HTML presentations, visual style exploration, preset selection and animation | Native editable PPTX as the default; one content-matched direction without requiring a preset questionnaire; motion chosen separately |

| 项目 | 本次核对材料的侧重点 | Quiet PPT 的侧重点 |
| --- | --- | --- |
| Anthropic PPTX Skill | 创建、修改、模板、包结构工具、可编辑图表和视觉建议 | 制作前按内容与受众选风格；默认中等文字密度及可直接讲述的备注 |
| frontend-slides | HTML 演示、视觉探索、预设选择与动画 | 默认可编辑 PPTX；无需先做审美问卷；按内容单独选择动效 |

Both references contain overlapping good practices, including content-aware design. The distinction is the defaults and the way the workflow is assembled, not an assertion that the references cannot support these outcomes.

两个参考项目也包含按内容设计等相同的良好实践。这里强调默认选择和流程组织的不同，不声称参考项目无法实现相同结果。

## Implementation and provenance / 实现与来源

- No reference project's scripts, templates or instruction text were copied into this repository. External instruction files were read as research material.
- The reviewed Anthropic PPTX entry point identifies its license as proprietary; no permission to relicense its implementation is assumed.
- Microsoft's documented Morph object matching and OOXML transition representation informed the helper.
- The Bilibili clip was used to study visual continuity. The clip, its frames, subtitles and photographs are not redistributed.
- Representative outputs were opened and rendered in desktop PowerPoint. Native chart editing was checked in a separate copy. Video previews were exported by PowerPoint and inspected as video frames.

没有复制参考项目的脚本、模板或指令文本；未把 Anthropic PPTX 文件的专有许可误当作开放复制授权。辅助脚本依据 Microsoft 公开文档编写。B 站片段只用于理解视觉连续性，不分发原片段或画面。样例经过桌面 PowerPoint 渲染、独立副本中的图表编辑检查和原生导出视频画面检查。
