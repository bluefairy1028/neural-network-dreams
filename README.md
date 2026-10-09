# Neural Network Dreams · 梦境实验室

依据 ../DeepDream_Interactive_PRD.md 实现的可演示交互网站。中文界面，支持课堂模式、两个真实层预设、上传 JPG/PNG、浏览器内真实 DeepDream、迭代回放、作品档案、PNG / JSON / ZIP 导出。

## 启动（断网也可用）

在本目录执行 `npm start`，打开 http://127.0.0.1:8765 。启动不需要安装依赖，Node.js 即可。也可执行 `python3 -m http.server 8765 --bind 127.0.0.1 --directory dist`。不要直接双击 index.html：浏览器的文件协议限制模型与案例读取。

所有运行资源均在 dist 内，包括模型权重、JS、示例照片、两组真实过程帧。浏览器端不调用第三方生成 API，不上传用户照片。不依赖外部 CDN、字体或 Python 后端。完整离线可用性指在本机启动 HTTP 服务后断开外网，不保证远程 URL 在断网后仍可重新打开。

## 60 秒课堂演示

1. 点击“课堂模式”，展示默认「形态漫游」案例。
2. 点击播放，用约 10 秒回放 0–40 次真实迭代。
3. 点击「纹理回声」，对比同图不同层的效果。
4. 说明：预训练网络保持固定，反复修改的是输入像素；“梦”是观看的比喻。
5. 退出课堂模式，打开“来源与方法”展示技术与艺术案例的区别。

## 实际计算

- TensorFlow.js 4.22.0，MobileNet V1 0.25 / ImageNet 预训练。
- 纹理回声：conv_pw_5_relu；形态漫游：conv_pw_11_relu。
- 最大化所选层平均激活；梯度除以自身 RMS；归一化像素截断到 [-1,1]。
- 强度低 / 中 / 高对应 0.006 / 0.012 / 0.02；20 / 40 / 60 步。
- 保持原图比例、最长边最多 256 px，不裁剪；透明区域合成在白色背景上。
- 每 2 步保存 PNG，没有 CSS 滤镜或插值冒充中间结果。
- 浏览器优先 WebGL，失败回退 CPU。CPU 可能需要数分钟；预计算回放即时可用。
- 网络图的输入空间维度改为动态，以支持等比例尺寸；预训练权重未修改。
- 和 PRD 建议架构的差异：使用浏览器 MobileNet 替代 Python + Inception，让静态托管也能真实生成。

## 作品与存储

内置 NASA / Eileen Collins 公共领域照片（via scikit-image），是技术案例，不冒充小组自摄或最终作品。创作档案保存在当前浏览器 IndexedDB 中；清理浏览器数据会删除记录。请下载完整作品 ZIP 长期备份，内含原图、真实帧、最终图和参数备注。浏览器内置示例的备注只保留于本次会话，编辑后需导出。

本工具不代替课程 PDF 提交、两位 hero 的最终选择和分析、Miro 展陈与证据。小组需上传有使用权的照片，完成选择、命名和来源记录。

## 开发与复现

`npm ci` 后：
- `npm run check`：校验语法、案例、图片尺寸、模型完整性。
- `npm run examples`：CPU 重新运行两组真实案例（约数分钟）。
- `scripts/browser-qa.cjs`：本次环境专用的 Playwright 实测脚本，需预览服务及已有 Chrome；依赖位置按实际环境调整。

## 来源 / 许可

实现代码为本项目新编写的梯度上升实现，概念参考 TensorFlow 官方 DeepDream 教程。
- https://www.tensorflow.org/tutorials/generative/deepdream
- https://research.google/blog/inceptionism-going-deeper-into-neural-networks/
- https://memo.tv/projects/2017/learning-to-see-interactive/
- 照片：https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.astronaut （NASA / Public domain）
- 预训练模型：https://storage.googleapis.com/tfjs-models/tfjs/mobilenet_v1_0.25_224/model.json
- TensorFlow.js / 模型：Apache 2.0，完整许可证见 dist/vendor/TENSORFLOW_LICENSE.txt。
