# README.md
## 安第斯与拉拉米德平俯冲模拟代码库
本仓库存放我硕士毕业论文的相关代码，主要用于文件备份留存。全部数值模拟均在格拉斯哥大学高性能计算集群完成。

> 说明：模拟输出的vtu可视化文件、计算检查点文件因文件体积较大，未上传至本仓库。

### 仓库目录结构
```
├── aspect输入参数文件/
│   ├── andes_FS2.txt          # 安第斯平俯冲ASPECT配置文件
│   └── laramide_FS2.txt       # 拉拉米德平俯冲ASPECT配置文件
├── python初始场生成脚本/
│   ├── com_andes.py           # 生成安第斯模型组分场输入文件
│   ├── tem_andes.py           # 生成安第斯模型温度场输入文件
│   ├── com_laramide.py        # 生成拉拉米德模型组分场输入文件
│   └── tem_laramide.py        # 生成拉拉米德模型温度场输入文件
└── README.md
```

### ASPECT输入参数文件
这两个文件为ASPECT的主输入配置，定义模拟的模型几何、网格策略、边界条件、流变参数、求解器与输出设置。

- `andes_FS2.txt`：安第斯端元基准模型。二维热‑力学平俯冲模型，板片以板片拆离（slab break‑off）作为消亡方式，总模拟时长20 Myr。开启自由地表与坡面扩散，支持地形演化计算。
- `laramide_FS2.txt`：拉拉米德端元基准模型。模拟法拉隆板块向北美克拉通下的平俯冲过程，板片通过板片回卷（slab roll‑back）逐步消亡。调整了模型横向范围、地幔温度以及岩石圈流变参数，总模拟时长60 Myr。

> 注意：使用前需要修改文件内的文件读写路径，适配本地或集群环境，否则程序无法读取初始场文件。

### Python初始场生成脚本
ASPECT可读取外部ASCII文本作为自定义初始条件。由于内置初始条件无法满足本研究复杂几何需求，通过Python预先计算温度、组分的空间分布，输出txt文件供ASPECT的`ascii data`模块读取。

- `com_andes.py`：构建安第斯模型的组分场，区分背景地幔、大洋地壳、大陆地壳、大陆岩石圈根，输出`com_andes.txt`。
- `tem_andes.py`：基于半空间冷却模型计算安第斯模型初始温度场，输出`tem_andes.txt`。
- `com_laramide.py`：构建拉拉米德模型的组分场，设置法拉隆洋壳、克拉通陆壳以及克拉通岩石圈根，输出`com_laramide.txt`。
- `tem_laramide.py`：计算拉拉米德模型的初始热结构，适配更古老的大洋板块与克拉通，输出`tem_laramide.txt`。

脚本运行方式：
```bash
# 安装依赖库
pip install numpy scipy

# 执行脚本，生成对应的初始场txt文件
python com_andes.py
python tem_andes.py
python com_laramide.py
python tem_laramide.py
```
运行完成后，将输出的txt文件放置到参数文件指定目录，即可启动模拟。

## 项目概况
论文题目：*Evolutionary Controls and Parameter Sensitivity: A Comparative Study of Andean and Laramide Flat‑Slab Subduction*
软件版本：ASPECT 3.1.0
模型设置：二维热‑力学有限元模型；采用布辛涅斯克近似，复合位错‑扩散蠕变流变，搭配Drucker‑Prager塑性屈服准则。
研究目标：对比安第斯型平俯冲（板片拆离）与拉拉米德型平俯冲（板片回卷）的动力学差异，探究板片热状态对造山变形的控制作用。

AI使用说明：生成式AI仅在项目早期用于代码思路参考，全部参数调试、脚本修改、模拟运算与结果解释均由本人独立完成，与论文声明保持一致。

### 使用提示
1. 该套参数为本论文基准算例，若开展参数敏感性测试，需要自行修改模型内相关配置。
2. 模拟结果可使用ParaView软件读取`.vtu`格式文件进行可视化分析。
3. 本仓库采用MIT开源协议。
