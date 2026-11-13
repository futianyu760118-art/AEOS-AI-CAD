# RUGGED-H6000 第二轮开源 AI-CAD A/B 测试

**状态**：G2.4/G2.5 旧版基线有记录；A=Agentic CAD、B=img2cad 尚未完成联网安装和本项目真实建模。不得将旧版结果算作 A/B 新工具成绩。

## 已完成的基线工作
- 已归档旧版 G2.4/G2.5 正面局部评价与对照指标。
- 已对 G2.5 STEP 回读：79/79 个实体有效；几何包络与总体积已记录。
- 已准备 img2cad 与 Agentic CAD 的安装、运行、重建与评价脚本。
- STEP 有效性不等于原图高保真，也不等于尺寸正确。

## 当前阻碍
- 此前执行环境无法解析 GitHub 与 PyPI 域名，未能完成联网安装。
- 当前基线环境为 Python 3.13 + CadQuery/OCCT/OpenCV；缺少 img2cad、agentic-cad 等候选依赖。
- 当前无 CUDA GPU，也未设置模型服务密钥；Agentic CAD hybrid 路线还需 COLMAP/SAM2/DA3 和相应权重。
- 参考图为展示渲染图，不是现场多视角照片；多视图相机可能不一致。

## 复现实验
先安装评分依赖：
```bash
python -m pip install -r requirements_eval.txt
```

对齐尺寸和相机后运行：
```bash
python evaluate.py --reference reference/FRONT.png --candidate candidate_front.png --out results/candidate
python verify_step.py path/to/candidate.step --out results/step_validation.json
```

## B 组：img2cad
- Windows PowerShell：`scripts/01_img2cad_windows.ps1`
- Linux：`bash scripts/01_img2cad_linux.sh`
- 将 `img2cad_job/AGENT_INSTRUCTIONS.md` 与统一参考图交给具备视觉能力的 Coding Agent。
- 必须生成可编辑 build123d Python、STEP、GLB、四视角预览和报告。只执行 doctor/安装不算 A/B 成功。

## A 组：Agentic CAD
- Linux + Python 3.12 + 网络 + OPENAI_API_KEY + OPENAI_MODEL_ID：`bash scripts/02_agentic_cpu_linux.sh`
- 完成官方 GPU 环境后再执行：`bash scripts/03_agentic_hybrid_linux.sh`
- CPU GPT 路线不等于完整多视图几何融合；hybrid 需检查 CUDA、COLMAP、SAM2、DA3 与模型权重。

## 统一评价约束
1. 同一原始图片、同一尺寸约束、同一坐标系和同一人工修正预算。
2. 固定相机与分辨率，不允许事后通过任意缩放/旋转让某一方案得分。
3. 分别保留原始模型、统一工程修正模型和最终交付模型。
4. 除 SSIM/IoU 外，还需报告边缘距离、尺寸误差、四视图结构一致性、STEP 实体有效性和人工工时。
5. 未生成文件的方案标记 NOT_RUN，不得将其记为 0 分或伪造结果。

## 旧版基线数据

| 指标 | G2.4 | G2.5 |
|---|---:|---:|
| 左侧橙色护角 IoU | 0.9767 | 0.9767 |
| 右侧橙色护角 IoU | 0.9776 | 0.9776 |
| LED 区域 IoU | 0.3171 | 0.3171 |
| 主壳区域 SSIM | 0.5046 | 0.4693 |
| 灯杯区域 SSIM | 0.6082 | 0.5309 |
| 灯杯边缘平均对称距离 | 4.59 px | 7.31 px |

G2.5 STEP：79/79 个实体有效，包围盒约 259.85 × 203.79 × 92.80 mm。此记录只说明拓扑回读有效。

## 文件说明
本仓库当前提交包含测试脚本、提示词、配置和 JSON 基线报告。原始高分辨率参考图片、完整 24.7 MB 第二轮测试 ZIP 和大尺寸 PNG 对照图未包含在本次 GitHub 提交中；请从原始归档包恢复到相应目录后再运行。不得用缩略图替代基准图。
