# GitHub 归档清单｜2026-11-13

## 已提交到仓库
- V1.0 执行方案 Markdown
- 第二轮 A/B 测试说明
- 固定注册图像评价脚本 `evaluate.py`
- STEP/OpenCascade 校验脚本 `verify_step.py`
- img2cad Windows/Linux 安装脚本
- Agentic CAD CPU/hybrid 启动脚本
- img2cad 视觉 Coding Agent 指令
- Agentic CAD 重建提示词
- G2.4/G2.5 JSON 指标记录及 G2.5 STEP 校验记录
- 评价依赖清单

## 本次未上传的二进制资料
- V1.0 正式 DOCX 与 PDF
- `RUGGED_H6000_AI_CAD_AB_第二轮实测与执行包.zip`（约 24.7 MB）
- 原始高分辨率 FRONT/BACK/SIDE/ISO/DRAWING 图片
- 大尺寸 front comparison PNG 和部分局部证据图

原因：本次 GitHub 连接通道适合提交文本文件和小型变更，无法直接从当前会话文件系统把上述完整二进制包传入仓库。没有用 base64 文本冒充二进制文件，也没有声称完整 ZIP 已上传。

## 后续完整归档建议
在本地 Windows 项目目录克隆本仓库后：
1. 将正式 DOCX/PDF 放入 `docs/`；
2. 将完整第二轮测试 ZIP 放入 `archive/`；
3. 将冻结的原始图片放入 `references/`；
4. 大于 10 MB 的二进制文件建议使用 Git LFS；
5. 提交后核对 GitHub 文件大小、SHA 和下载回读结果。

## 当前真实性边界
G2.4/G2.5 是旧版 CAD 基线，不是 img2cad 或 Agentic CAD 的新测试成绩。两款候选工具针对 RUGGED-H6000 的联网安装、模型生成和新 STEP 输出仍待 Work 联网环境执行。
