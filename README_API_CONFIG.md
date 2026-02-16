# 🚀 API密钥配置指南

## 🔑 获取阿里云API密钥

### 步骤1：登录阿里云控制台
访问 [阿里云官网](https://www.aliyun.com/) 并登录您的账号

### 步骤2：进入DashScope服务
1. 在控制台搜索 "DashScope"
2. 或者直接访问：https://dashscope.console.aliyun.com/
3. 如果是首次使用，需要先开通服务

### 步骤3：创建API密钥
1. 进入"API密钥管理"页面
2. 点击"创建密钥"
3. 保存生成的API密钥（注意：只显示一次！）

## ⚙️ 项目配置

### 方法一：修改.env文件（推荐）
```bash
# 编辑 .env 文件
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 方法二：设置系统环境变量
```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY="你的API密钥"

# Linux/Mac
export DASHSCOPE_API_KEY="你的API密钥"
```

## ✅ 验证配置

运行测试脚本验证配置是否正确：
```bash
python test_api_config.py
```

## 💰 费用说明

- 阿里云DashScope提供免费额度
- 超出免费额度后按量付费
- 建议设置消费预警避免超支

## ❓ 常见问题

**Q: 忘记保存API密钥怎么办？**
A: 需要重新生成新的API密钥

**Q: API调用出现401错误？**
A: 检查API密钥是否正确配置

**Q: 如何查看使用量和费用？**
A: 在阿里云控制台的账单中心查看