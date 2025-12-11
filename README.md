# lerobot_teleoperator_firefly

[资料一览](TODO)

## Getting Started

1.下载并安装piper sdk

2.通过下载piper sdk，你可以得到如下两个脚本，完成寻找can port 和 激活can port两个步骤

    bash find_all_can_port.sh 

    bash can_activate.sh can0 1000000

3.运行piper sdk里提供的代码，确认piper已经可以正常工作。

4.安装lerobot， lerobot_teleoperator_firefly 的安装包，teleoperator

    ~~~bash
    pip install lerobot                         # 安装lerobot
    pip install lerobot_robot_piper             # 安装lerobot_robot_piper
    pip install lerobot_teleoperator_firefly    # 安装lerobot_teleoperator_firefly
    ~~~

5.运行遥操作代码。

    ~~~bash
    TODO
    lerobot-teleoperate \
        --robot.type=lerobot_robot_piper \
        --robot.can_name=can0 \
        --robot.id=lerobot_robot_piper \
        --teleop.type=lerobot_teleoperator_firefly \
        --teleop.port=/dev/ttyUSB0 \
        --teleop.id=lerobot_teleoperator_firefly \
        --teleop.baudrate=1000000
    ~~~

