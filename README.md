# Neural Network Dreams：从特征可视化到机器之梦

Scientist → DeepDream 机制 → 蟑螂恐惧实验 → 科学分析。2026-10-12 实验版。

网站入口：https://neural-network-dreams-lab.bluefairy1028.chatgpt.site （保留原有私有访问设置；发布状态以 Sites 工具返回为准）。

## 演示

点击「导览演示」按五步讲解。案例内可以切换训练、响应、生成。内置排水口、瓷砖、墙角、空调电线、厨房水槽五张作者照片；全部排除于训练、验证、正式测试之外。

「回放该照片的真实对照」读取已保存计算帧；「同参数运行双模型」在浏览器重新执行真实梯度上升。成对运行时参数锁定；单次运行改变参数会取消并从原图重启。语言切换不重置输入或任务。PNG、JSON 与 ZIP 导出包含模型哈希、目标、来源、个人叙事和真实帧。

本地运行：`npm start` 后打开 http://127.0.0.1:8765 。上传图片仅在浏览器处理。

## 数据与实验

84 张网络照片：24 张 Blattidae 蟑螂、24 张 Coleoptera 甲虫、36 张 Wikimedia Commons 生活空间。逐张保留摄影者、许可、来源、哈希与分组。训练 48、验证 18、测试 18。同 observation、来源／摄影者连拍组、重复或近重复不跨划分。网络空间照片不宣称拍摄于广东；空间标签仅指下载分辨率下未见昆虫。

原始预训练清单：`data/experiment-v1/manifest.json`。含展示使用情况的公开清单：`dist/experiment/dataset-candidates.json`。作者授权与原文件哈希：`dist/author/manifest.json`。用户在 2026-10-12 提供五张照片并授权项目使用，未把照片再许可为 CC。

基础模型为 ImageNet MobileNet V1 0.25，原本就有 cockroach 类 314。仅微调 conv_pw_13，其他权重及原始 1000 类分类头保持相同。训练目标是三组概率的交叉熵：cockroach、其他昆虫（ImageNet300–326 除314）、其余类作为空间粗略代理。它不是专门的害虫／空间检测器。

输入等比缩放并留白至 96×96，Adam 0.0003，batch 8，12 轮；保存 0/4/8/12 检查点。仅按验证损失从 4/8/12 中选出第 4 轮，随后进行正式保留测试，结果 17/18；一张甲虫被判为空间。不能把小样本准确率解释为普遍检测能力。

作者照片按最长边 256px 处理，不使用训练集的正方形留白方式；它们代表额外的展示条件，不纳入正式指标。空墙照片触发微调分类误响应（cockroach softmax 约 0.7527）。训练集选出的内部通道 22 在保留图上也有误响应、漏响应；这些通道错误与分类错误分别标注。

所有展示 Dream 均来自实际计算：cockroach logit 314、步长 0.012、20 次更新、每 2 步存帧。四个检查点使用同一排水口输入。生成的纹理不是可靠生物结构，模型没有恐惧、情绪或主观体验。

## 复现与审计

- `scripts/import-author.py`：导入作者照片，保留原图哈希并移除展示副本 EXIF。
- `scripts/collect-inaturalist.py`：开放许可昆虫候选；不要在正式实验后覆写清单。
- `data/space-candidates/`：空间来源与审计。
- `scripts/finalize-data.py`：分组划分、预训练 manifest、96px 输入。需原本地候选图片，图片和二进制不纳入 Git。
- `scripts/train-cockroach.cjs`：真实训练；冻结 BatchNorm 通过等价的固定仿射层实现，导出保持原架构。
- `scripts/evaluate-cockroach.cjs`：完整导出模型评估与训练集通道选择。
- `scripts/capture-evidence.cjs` / `finalize-evidence.cjs`：浏览器真实对照帧与展示清单。
- `npm run check`、`npm run qa`（需预览服务）、`npm run release:check`：静态／数据审计、浏览器交互和七项发布检查。

旧医学版本位于 `audit/medical-v2-2026-10-09/`，不在网站服务目录内。新网站不使用旧医学权重、数据、示例图或病例叙事。
