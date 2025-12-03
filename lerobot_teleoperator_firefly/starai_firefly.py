import logging
import time
from typing import Any

from lerobot.utils.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError
from lerobot.motors import Motor, MotorCalibration, MotorNormMode
# from lerobot_motor_starai.starai import (
#     StaraiMotorsBus,
# )
from fashionstar_uart_sdk.uart_pocket_handler import (
    PortHandler ,
    SyncPositionControlOptions,
    Monitor_data
)
from lerobot.teleoperators.teleoperator import Teleoperator
from .config_starai_firefly import FireflyConfig

logger = logging.getLogger(__name__)


class Firefly(Teleoperator):
    config_class = FireflyConfig
    name = "starai_violin"

    def __init__(self, config: FireflyConfig):
        super().__init__(config)
        self.config = config
        # # self.bus:StaraiMotorsBus = StaraiMotorsBus(
        # self.port=self.config.port
        self._is_connected = False
        self.porthandler:PortHandler = PortHandler(self.config.port,self.config.baudrate)
        self.motors = {"Joint_1": 0,
                        "Joint_2": 1,
                        "Joint_3": 2,
                        "Joint_4": 3,
                        "Joint_5": 4,
                        "Joint_6": 5,
                        "Gripper": 6}
        self.joint_dir={}
        self.joint_dir["Joint_1"] = self.config.joint_dir[0]
        self.joint_dir["Joint_2"] = self.config.joint_dir[1]
        self.joint_dir["Joint_3"] = self.config.joint_dir[2]
        self.joint_dir["Joint_4"] = self.config.joint_dir[3]
        self.joint_dir["Joint_5"] = self.config.joint_dir[4]
        self.joint_dir["Joint_6"] = self.config.joint_dir[5]
        self.joint_dir["Gripper"] = 2

    @property
    def action_features(self) -> dict[str, type]:
        return {f"{motor}.pos": float for motor in self.motors}

    @property
    def feedback_features(self) -> dict[str, type]:
        return {}

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self, calibrate: bool = True) -> None:
        if self.is_connected:
            raise DeviceAlreadyConnectedError(f"{self} already connected")

        self.porthandler.openPort()
        for motor,value in self.motors.items():
            if not self.porthandler.ping(value):
                raise Exception(f"motor not found id:{value}")

        for motor,value in self.motors.items():
            self.porthandler.write["Stop_On_Control_Mode"](value, "unlocked", 900)
            time.sleep(0.01)
        self.porthandler.ResetLoop(0xFF)
        self._is_connected = True 
        logger.info(f"{self} connected.")

    @property
    def is_calibrated(self) -> bool:
        return True

    def calibrate(self) -> None:
        pass
        # if self.calibration:
        #     # Calibration file exists, ask user whether to use it or run new calibration
        #     user_input = input(
        #         f"Press ENTER to use provided calibration file associated with the id {self.id}, or type 'c' and press ENTER to run calibration: "
        #     )
        #     if user_input.strip().lower() != "c":
        #         logger.info(f"Writing calibration file associated with the id {self.id} to the motors")
        #         self.bus.write_calibration(self.calibration)
        #         return
        # self.bus.disable_torque(mode="unlocked")
        # logger.info(f"\nRunning calibration of {self}")
        # # self.bus.disable_torque()
        # # for motor in self.bus.motors:
        # #     self.bus.write("Operating_Mode", motor, OperatingMode.POSITION.value)

        # # input(f"Move {self} to the middle of its range of motion and press ENTER....")
        # homing_offsets = self.bus.set_half_turn_homings()

        # print(
        #     "Move all joints sequentially through their entire ranges "
        #     "of motion.\nRecording positions. Press ENTER to stop..."
        # )
        # range_mins, range_maxes = self.bus.record_ranges_of_motion()

        # self.calibration = {}
        # for motor, m in self.bus.motors.items():
        #     self.calibration[motor] = MotorCalibration(
        #         id=m.id,
        #         drive_mode=0,
        #         homing_offset=homing_offsets[motor],
        #         range_min=range_mins[motor],
        #         range_max=range_maxes[motor],
        #     )

        # self.bus.write_calibration(self.calibration)
        # self._save_calibration()
        # print(f"Calibration saved to {self.calibration_fpath}")

    def configure(self) -> None:
        pass

    def get_action(self) -> dict[str, float]:
        start = time.perf_counter()

        monitor_data: dict[str, Monitor_data]= self.porthandler.sync_read["Monitor"](self.motors)
        

        action = {f"{motor}.pos": (val.current_position * self.joint_dir[motor]) for motor, val in monitor_data.items()}
        dt_ms = (time.perf_counter() - start) * 1e3
        logger.debug(f"{self} read action: {dt_ms:.1f}ms")
        return action

    def send_feedback(self, feedback: dict[str, float]) -> None:
        # TODO(rcadene, aliberts): Implement force feedback
        raise NotImplementedError

    def disconnect(self) -> None:
        if not self.is_connected:
            DeviceNotConnectedError(f"{self} is not connected.")
        self.porthandler.closePort()
        self._is_connected = False

        logger.info(f"{self} disconnected.")

    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        raise DeviceNotConnectedError(f"{self} is not connected.")
        if not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        goal_pos = {key.removesuffix(".pos"): val for key, val in action.items() if key.endswith(".pos")}
        self.bus.sync_write("Goal_Position", goal_pos)
        return {f"{motor}.pos": val for motor, val in goal_pos.items()}
    
    # def move_to_initial_position(self)-> dict[str, Any]:
    #     postion = self.get_action()


    #     # if not self.is_connected:
    #     #     raise DeviceNotConnectedError(f"{self} is not connected.")
    #     goal_pos = {}
    #     goal_pos = {key.removesuffix(".pos"): val for key, val in postion.items() if key.endswith(".pos")}
    #     goal_pos["Motor_0"] = 0
    #     goal_pos["Motor_1"] = -100
    #     goal_pos["Motor_2"] = 60
    #     goal_pos["Motor_3"] = 0
    #     goal_pos["Motor_4"] = 30
    #     goal_pos["Motor_5"] = 0
    #     goal_pos["gripper"] = 50
    #     self.bus.sync_write("Goal_Position", goal_pos,motion_time = 1500)
    #     time.sleep(1.5)
    #     self.bus.disable_torque(motors = "gripper",mode = "unlocked")
    #     return {f"{motor}.pos": val for motor, val in goal_pos.items()}