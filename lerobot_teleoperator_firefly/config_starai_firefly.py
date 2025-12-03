from dataclasses import dataclass

from lerobot.teleoperators.config import TeleoperatorConfig


@TeleoperatorConfig.register_subclass("lerobot_teleoperator_firefly")
@dataclass
class FireflyConfig(TeleoperatorConfig):
    # Port to connect to the arm
    port: str
    baudrate:int = 115200
    use_degrees: bool = False
    joint_dir = [-1,1,1,-1,1,-1]

