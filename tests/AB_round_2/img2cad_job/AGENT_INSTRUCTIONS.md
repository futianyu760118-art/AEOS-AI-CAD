# B 组：img2cad 实际生成指令

参考仓库：https://github.com/YUI-TIEN/img2cad

使用 FRONT、BACK、SIDE、ISO 和 DRAWING 参考资料，先核对官方 workflow 与许可证，再运行 doctor。之后由具备视觉能力的 Coding Agent 完成真实建模。

要求：
1. 以整灯作为统一 A/B 输入，不得只画主壳冒充整机。
2. 目标为 visual_approximation；先建立观察证据和零件计划。
3. 输出可编辑 build123d Python 源文件；逐个零件记录颜色、尺寸和尺寸来源。
4. 先恢复主灯体、左右侧灯、顶部握柄、U 形支架和铰链的空间层级，再添加灯杯、橙色护角和背部电池仓。
5. 直线边缘必须保持直线；使用 line+arc+fillet 或受控 NURBS，不允许无约束平滑导致边缘波浪。
6. 输出 model.py、model.step、model.glb、report.json，以及 FRONT/BACK/SIDE/ISO 四视角预览。
7. 使用工具检查 STEP；说明相机标定不足和跨视角不一致。
8. 运行统一 evaluate.py；报告护角、灯杯、LED、结构缺失、四视图和尺寸偏差。
9. 不得只报告 IoU；不符合高保真要求必须标记 FAIL。
10. 仅安装或 doctor 成功不算 A/B 成功，必须真实生成项目模型。
