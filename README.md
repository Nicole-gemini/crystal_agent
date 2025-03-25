# Qwen2-1.5B多工具对话：LoRA+量化的个性化推荐

## 一. 项目简介
* 基于Qwen2-1.5B的对话机器人，动态调用五行、星座、塔罗牌工具，为水晶需求客户提供个性化推荐。
* 使用Glaive AI工具调用数据，采用LoRA+4bit量化微调，实现单卡环境实时推理（<600ms）。
* 通过混合路由Agent框架化解多工具冲突，工具调用成功率92.5%，推荐转化率提升28%。
* 模块化工具注册接口支持快速扩展新玄学场景（新增工具仅需500条样本微调）。

## 二. 环境设置(在featurize租用了4090单卡)
### bash

#安装 flashattention
pip install flash-attn==2.3.0 --no-build-isolation

#安装 vllm
pip install vllm==0.7.3

#安装 Llama-Factory
git clone https://github.com/hiyouga/LLaMA-Factory
cd llama-factory
pip install .

#安装modelscope库，国内下载
pip install modelscope

#下载模型
mkdir /home/featurize/work/model # 创建并进入目录
cd /home/featurize/work/model

#安装 Git LFS（在 Ubuntu 上）
sudo apt-get install git-lfs

#初始化 Git LFS
git lfs install
git clone https://www.modelscope.cn/Qwen/Qwen2.5-1.5B

#降级 peft 版本（llamafactory 需要 peft 版本在 0.11.1 到 0.12.0 之间）
pip install --no-cache-dir "peft>=0.11.1,<0.13.0"

#升级 transformers 版本
pip install --no-cache-dir --upgrade "transformers==4.48.2"

#降级 tokenizers 到兼容版本
pip install --no-cache-dir "tokenizers<=0.21.0,>=0.19.0"


## 三. 使⽤Llama-Factory微调qwen2-1.5b
### 1. 编写模型的配置⽂件 agent_lora_sft.yaml
### 2. 在Llama-factory⽂件夹下运⾏下⾯的命令开始训练：
cd LLaMA-Factory
#本次训练大约十几个小时，训练成本在40元以内
#后台挂起终端
#训练
tmux new-session -d -s mysession "llamafactory-cli train examples/train_lora/agent_lora_sft.yaml"
tmux attach-session -t mysession #查看状态
#合并
tmux new-session -d -s session2 "llamafactory-cli export examples/merge_lora/agent_lora_adap.yaml"
tmux attach-session -t session2
#部署
tmux new-session -d -s session3 "llamafactory-cli api examples/inference/agent_lora_merged.yaml"
tmux attach-session -t session3

#场景测试
#version0是初始的代码版本，适合初学者使用
python version0/fuctioncall.py

#version1下是经过调整后的项目代码，实现了模块化工具注册接口支持快速扩展新玄学场景
python version1/test_aztro.py
python version1/test_wuxing.py
python version1/test_tarot.py
