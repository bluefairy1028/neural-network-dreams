# Neural Network Dreams Lab · PRD 2.0

三个中英双语标签：训练过程、层与通道、创作与生成。所有热图、训练曲线和 Dream 帧均来自真实计算。

## 启动 / 离线展示

本目录运行 `npm start`，打开 http://127.0.0.1:8765 。启动仅需 Node.js，无需 npm install。也可用 `python3 -m http.server 8765 --bind 127.0.0.1 --directory dist`。

模型、脚本、训练记录、检查点及案例均在 dist 中，无外部 CDN。断开外网后本地服务器照常运行；远程网址不承诺断网重载。不要直接双击 index.html。

## 此次真实训练

- 数据：PathMNIST / MedMNIST v2 28px；结直肠 H&E 染色组织显微图块，9 类；CC BY 4.0。
- 数据来源：官方 https://zenodo.org/records/10519652/files/pathmnist.npz?download=1 。MD5 a8b06965200029087d5bd730944a56c1。
- 从官方 train / val / test 分别按类抽样 100 / 25 / 25 张，共 900 / 225 / 225。种子 5316，索引与校验值保存在 dist/training/dataset.json。不是随机混合后重新划分，测试集未参与训练或调参。
- MobileNet V1 0.25 ImageNet 初始化；冻结 conv_dw_11_relu 及之前的层，缓存其真实特征，仅微调 conv_pw_11 卷积与新 9 类分类头，BN 冻结。输入 28→64 双线性放大，[-1,1]，无数据增强。
- Adam 0.001，batch 30，8 epochs，固定已打乱的样本顺序。交叉熵分类目标；初始随机分类头的验证准确率约 11.6%，最终 43.6%；最终保留测试子集 54.2%。详见真实日志，不能当完整器官模型。
- 检查点 epoch 0 / 2 / 4 / 8，包含可直接用于浏览器特征响应和 Dream 的截断主干，以及 classifier 子目录中的训练尾部（接受缓存特征）。权重 SHA-256 在 run.json。
- 训练在本机 Apple M3 Max / TensorFlow.js CPU 上执行。运行时间和设备记在日志。

这是小规模组织图像局部微调实验，未证明人体结构识别能力或临床效用。第 5 层被冻结，两个版本的该层响应一致是正确结果。第 11 层确有权重和响应变化。新分类头未经训练的 epoch 0 指标不能解释为原始 ImageNet 分类器的组织分类能力。

## 交互与数据真实性

- 训练：曲线对应实际日志；拖动 0/2/4/8 检查点，同图同层同通道、相同步长和 20 步优化。检查点、原始 JSON 和权重可下载。
- 响应：可选两个真实层、全部或任一通道，12 个缩略图。热图是前向计算或注明的真实计算回放；每图独立 min–max 归一化，不能用跨图颜色比较绝对值；显示原始数值范围。
- 微调层候选 channel 121：在人物、咖啡、猫三个独立图像上筛选空间响应方差总和最高的通道，记录真实生成结果；均匀灰图作为失败观察。只是技术候选，未冒充小组已策展的器官预设。
- 创作：最长边 256 px、按比例、不裁剪；透明图白底。选模型/层/通道、步长 0.002–0.030、10–60 次迭代；梯度按 RMS 归一化，每 2 步保存真实帧。
- 生成中改参数：取消并从原图重启，最终记录是新参数快照，无混合续算。语言切换不改变任务、上传、参数或当前帧。
- 作品包：原图、真实过程帧、最终 PNG、JSON（模型/checkpoint/hash/数据集/层/通道/输入ID/请求与完成步数/代码版本/日期）、数据卡、训练记录和策展文本。
- 使用当前浏览器 IndexedDB 保留作品，沿用 v1 记录；新模型并不会重写旧结果。内置技术案例备注要导出永久保存。

## 复现

先 `npm ci`；Python 需 numpy 与 Pillow（本次使用系统提供的文档运行时）。

1. 将上述官方 pathmnist.npz 放到 training-data/。
2. `python3 scripts/prepare-data.py`：验证来源文件 MD5，固定划分与索引，导出真实训练样本。
3. `npm run train`：冻结特征缓存到 training-cache/，训练并保存日志、4 个检查点与分类尾部。
4. `npm run probes`：构建检查点响应/Dream、多输入候选与灰图失败观察；需 training-data/coffee.png、chelsea.png（scikit-image v0.19.3，CC0）。
5. `npm run check`：语法、日志、哈希、冻结层一致性、微调层差异、真实帧与双语键。

scripts/qa-v2.cjs 是本环境 Chrome / Playwright 的浏览器验收脚本，需按环境修改 Playwright 路径。训练源数据与特征缓存留在本机，不随网站仓库发布。

## 与建议架构的差异

不需要托管长时 Python 服务：训练离线完成后保存检查点，网页使用 TFJS 真实运行固定模型。因此没有伪装的 /api/training 或 Dream 任务 API；浏览器任务状态直接来自实际迭代。现场训练属于 P1，本版未放入界面。

## 仍需小组提供

最终器官主题与数据选择确认、共同选定的视觉预设、拥有使用权的小组照片、最终作品标题与排列、hero 分析、Miro 展陈证据、PDF。网站目前是可运行的组织显微技术实验与创作工具，不冒充这些小组决策。

## 来源与许可证

- PathMNIST：Jiancheng Yang et al., MedMNIST v2 (2023)，CC BY 4.0；原始组织图 Jakob Nikolas Kather et al., NCT-CRC-HE-100K / CRC-VAL-HE-7K (2019)。已标明子集抽样、缩放、微调等改动。
- NASA Eileen Collins：公共领域；咖啡 Rachel Michetti、猫 Stefan van der Walt：CC0，via scikit-image。
- TensorFlow.js / MobileNet：Apache 2.0，许可证在 dist/vendor/TENSORFLOW_LICENSE.txt。
- https://www.tensorflow.org/tutorials/generative/deepdream
- https://research.google/blog/inceptionism-going-deeper-into-neural-networks/
- https://memo.tv/projects/2017/learning-to-see-interactive/
- https://scikit-image.org/docs/stable/api/skimage.data.html
