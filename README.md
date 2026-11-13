# AEOS AI-CAD｜RUGGED-H6000 高保真逆向建模项目

本仓库用于持续推进 RUGGED-H6000 工作灯的多视图逆向建模、开源工具评估、STEP/STP 交付和保真度验证。

## 当前归档版本

- 方案版本：V1.0
- 归档日期：2026-11-13
- 当前阶段：开源工具路线评估与第二轮 A/B 实测准备
- 最终目标：可编辑 STEP/STP 零件与总装、装配结构、关键尺寸、工程验证报告和多视图保真报告。

## 已提交内容

- `docs/AEOS_AI-CAD_RUGGED-H6000_执行方案_V1.0.md`：V1.0 完整执行方案。
- `tests/AB_round_2/README.md`：第二轮 A/B 测试协议、环境阻碍和旧版基线。
- `tests/AB_round_2/evaluate.py`：固定注册的正面图像指标评价程序。
- `tests/AB_round_2/verify_step.py`：OpenCascade STEP 实体与包围盒校验程序。
- `tests/AB_round_2/scripts/`：img2cad Windows/Linux、Agentic CAD CPU/hybrid 和对照评分脚本。
- `tests/AB_round_2/img2cad_job/`、`agentic_job/`：视觉建模指令和重建提示词。
- `tests/AB_round_2/results/`：G2.4/G2.5 既有指标和 G2.5 STEP 回读记录。
- `tests/AB_round_2/environment/`：评价依赖清单。

## 目录规划

- `docs/`：方案、设计规范、执行与验收文档
- `tests/AB_round_2/`：第二轮 A/B 测试脚本、配置和报告
- `references/`：冻结的原始参考图与尺寸基线（需补齐原始图片）
- `deliverables/step/`：通过验收的 STEP/STP 零件和总装
- `deliverables/reports/`：几何验证、尺寸核验和多视图保真报告
- `archive/`：版本化完整存档包

## 归档边界

本次 GitHub 提交已归档方案 Markdown、测试说明、脚本、提示词和 JSON 基线记录。此前生成的 DOCX/PDF 和约 24.7 MB 完整第二轮测试 ZIP 未作为二进制文件纳入本次提交；原始高分辨率参考图和大尺寸 PNG 对照图也未上传。详见 `docs/ARCHIVE_MANIFEST.md`。

如需完整二进制归档，使用本地 Git 客户端上传，或对大文件启用 Git LFS；不要将 base64 文本伪装成 ZIP/STEP 文件。

## 项目原则

1. 以冻结的正面、背面、侧面、等轴测及工程图作为统一基准。
2. 先建立尺寸/轮廓基线，再进行主壳、灯杯、侧灯、铰链、提手、电池包和底座的参数化建模。
3. 图像生成结果只能作为参考，不得替代可编辑 CAD 几何。
4. 采用多视图、局部 ROI、轮廓距离、SSIM/IoU 和 STEP 几何有效性进行量化验收。
5. 每轮测试保留环境、依赖版本、执行日志、源文件、STEP、渲染图和评估结果。

## 当前状态

- [x] V1.0 执行方案整理并提交
- [x] 第二轮 A/B 测试协议、脚本和基线指标归档
- [ ] img2cad 联网安装与真实项目建模
- [ ] Agentic CAD 联网安装与真实项目建模
- [ ] 基于统一基准完成高保真参数化 CAD
- [ ] STEP/STP 几何有效性、装配和多视图保真验收
