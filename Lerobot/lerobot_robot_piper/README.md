# LeRobot + viola Integration

## Getting Started

```bash
pip install lerobot_robot_viola

lerobot-teleoperate \
    --robot.type=lerobot_robot_viola \
    --robot.port=/dev/ttyUSB1 \
    --robot.id=my_awesome_staraiviola_arm \
    --teleop.type=lerobot_teleoperator_violin \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=my_awesome_staraiviolin_arm

```

## Development

Install the package in editable mode:

```bash
git clone https://github.com/servodevelop/fashionstar-lerobot-robot-viola.git
cd fashionstar-lerobot-robot-viola
pip install -e .
```



下载pipersdk，并且设置can端口为can0

bash ~/code-ws/piper/piper_sdk/piper_sdk/find_all_can_port.sh 
bash ~/code-ws/piper/piper_sdk/piper_sdk/can_activate.sh can0 1000000

lerobot-teleoperate \
    --robot.type=lerobot_robot_piper \
    --robot.can_name=can0 \
    --robot.id=lerobot_robot_piper \
    --teleop.type=lerobot_teleoperator_firefly \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=lerobot_teleoperator_firefly \
    --teleop.baudrate=1000000