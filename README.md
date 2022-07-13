#basis_supervise

## 环境配置

- Python版本：3.8
- 依赖包列表：requirements.txt
- 运行环境初次配置步骤：
    1. 创建python3.8虚拟环境
    2. 安装依赖包: `pip install -r requirements.txt`
- 依赖包列表更新流程：
    1. 需要新增依赖包时，先用`pip install`命令安装所需的依赖包
    2. 安装结束后，执行`pip freeze > requirements.txt`更新依赖包列表文件
    
## 单元测试环境

- 单元测试框架：pytest
- 单元测试文件目录：`tests/`
- 启动全部测试命令：pytest tests/
