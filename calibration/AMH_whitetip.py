import RPi.GPIO as GPIO
import time
import numpy as np
import numpy.polynomial.polynomial as poly
import serial
import sys

driverPUL = 12  
driverDIR = 18  
 
Steps_per_revolution = 276 #可以根据敲击位置调整

###############################################################################
# 1. 在这里放置你的 300 组 (激励, speed) 数据, 并进行多项式拟合
###############################################################################
# 假设 excitations_data 是 1D 数组，包含你的 300 组激励值
# 假设 speeds_data      是 1D 数组，包含与激励值对应的 forward_speed
# 下面仅举例，实际使用时请替换为你自己的数据
excitations_data = np.array([
    # 在此处放置你的 300 组激励值
    0,12,14,13,22,9,11,12,14,15,
    14,19,21,24,24,18,29,32,35,36,
    41,43,45,49,54,60,66,73,78,94,
    83,42,46,52,51,44,47,52,56,58,
    63,66,72,75,73,76,78,80,85,88,
    94,98,100,101,109,114,113,120,125,141,
    135,146,156,142,130,128,132,126,122,128,
    133,131,136,135,135,135,137,142,141,139,
    145,146,153,154,156,155,157,160,162,158,
    159,161,166,168,174,172,177,175,181,186,
    178,180,176,183,188,200,196,198,206,202,
    198,196,209,216,208,210,225,216,220,211,
    220,218,225,228,238,230,238,248,235,240,
    243,242,250,256,254,260,262,270,272,260,
    271,273,276,280,282,273,273,280,282,292,
    279,290,290,302,300,312,308,300,296,298,
    296,302,313,321,316,322,306,310,330,318,
    326,320,326,324,336,350,358,338,330,340,
    338,338,338,350,342,342,344,362,358,365,
    375,382,360,370,368,368,376,380,378,382,
    382,390,378,395,382,380,382,386,396,390,
    400,394,410,398,398,418,416,402,408,412,
    418,412,416,426,438,430,442,436,430,436,
    448,438,442,458,436,450,440,436,430,430,
    440,438,442,462,450,458,470,446,456,458,
    476,482,462,475,478,476,482,490,478,476,
    479,476,502,488,479,481,516,496,483,480,
    478,496,494,484,492,490,495,506,516,490,
    508,496,500,510,496,516,516,520,496,512,
    518,530,520,532,518,528,538,522,542,538

# 示例
    # ...
])
speeds_data = np.array([
    # 在此处放置你的 500 组 speed
    0,5,10,15,20,25,30,35,40,45,
    50,55,60,65,70,75,80,85,90,95,
    100,105,110,115,120,125,130,135,140,145,
    150,155,160,165,170,175,180,185,190,195,
    200,205,210,215,220,225,230,235,240,245,
    250,255,260,265,270,275,280,285,290,295,
    300,305,310,315,320,325,330,335,340,345,
    350,355,360,365,370,375,380,385,390,395,
    400,405,410,415,420,425,430,435,440,445,
    450,455,460,465,470,475,480,485,490,495,
    500,505,510,515,520,525,530,535,540,545,
    550,555,560,565,570,575,580,585,590,595,
    600,605,610,615,620,625,630,635,640,645,
    650,655,660,665,670,675,680,685,690,695,
    700,705,710,715,720,725,730,735,740,745,
    750,755,760,765,770,775,780,785,790,795,
    800,805,810,815,820,825,830,835,840,845,
    850,855,860,865,870,875,880,885,890,895,
    900,905,910,915,920,925,930,935,940,945,
    950,955,960,965,970,975,980,985,990,995,
    1000,1005,1010,1015,1020,1025,1030,1035,1040,1045,
    1050,1055,1060,1065,1070,1075,1080,1085,1090,1095,
    1100,1105,1110,1115,1120,1125,1130,1135,1140,1145,
    1150,1155,1160,1165,1170,1175,1180,1185,1190,1195,
    1200,1205,1210,1215,1220,1225,1230,1235,1240,1245,
    1250,1255,1260,1265,1270,1275,1280,1285,1290,1295,
    1300,1305,1310,1315,1320,1325,1330,1335,1340,1345,
    1350,1355,1360,1365,1370,1375,1380,1385,1390,1395,
    1400,1405,1410,1415,1420,1425,1430,1435,1440,1445,
    1450,1455,1460,1465,1470,1475,1480,1485,1490,1495
    # 示例
    # ...
])

# 进行多项式拟合，选择一个合适的拟合阶数（如 3 次、4 次等，需要自行实验）
# 这里示例使用 3 次多项式
# 注意：我们拟合的是 激励(e) -> speed(s)
degree = 8
coefs = poly.polyfit(excitations_data, speeds_data, degree)

def get_speed_from_excitation(excitation_value):
    """
    根据输入的激励，通过多项式函数预测出相应的电机转速forward_speed
    """
    return poly.polyval(excitation_value, coefs)


###############################################################################
# 保持原有电机控制类不变
###############################################################################
class StepperMotor:
    def __init__(self, step_pin, direction_pin):
        self.step_pin = step_pin
        self.direction_pin = direction_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)

    def move_steps_constant_speed(self, steps, speed):
        """
        使用给定的速度 speed（steps/s）转动 steps 步
        """
        # 判断正转或反转方向
        direction = GPIO.HIGH if steps > 0 else GPIO.LOW
        GPIO.output(self.direction_pin, direction)

        # 计算单个脉冲的延时
        step_delay = 1.0 / (2.0 * abs(speed))  # speed = steps/s, 因此半个周期是 1/(2*speed)
        for _ in range(abs(steps)):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(step_delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(step_delay)

    def move_steps_linear_decel(self, steps, start_speed, end_speed):
        """
        从 start_speed 线性变化到 end_speed 的方式完成 steps 步的运动
        """
        direction = GPIO.HIGH if steps > 0 else GPIO.LOW
        GPIO.output(self.direction_pin, direction)

        total_steps = abs(steps)
        if total_steps <= 1:
            avg_speed = (start_speed + end_speed) / 2.0
            self.move_steps_constant_speed(steps, avg_speed)
            return

        for i in range(total_steps):
            ratio = i / float(total_steps - 1)  
            current_speed = start_speed + (end_speed - start_speed) * ratio

            # 避免速度为 0
            if current_speed <= 0:
                current_speed = 1  

            half_pulse_delay = 1.0 / (2.0 * current_speed)
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(half_pulse_delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(half_pulse_delay)


###############################################################################
# 2. 主函数：演示如何使用 多项式拟合 后的速度 来进行电机控制
###############################################################################
if __name__ == "__main__":
    try:
        # 1) 打开树莓派硬件串口
        ser = serial.Serial("/dev/serial0", 9600, timeout=1)
        time.sleep(2)  # 等待串口稳定

        motor = StepperMotor(driverPUL, driverDIR)
        steps_for_90_deg = int((90.0 / 360.0) * Steps_per_revolution)

        print("[+] 进入循环监听模式。等待LabVIEW发送激励值...")

        while True:
            # 2) 读取一行数据
            raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not raw_line:
                # 如果没有数据，就继续等待
                continue

            # 若你想给LabVIEW发一个命令"STOP"来停止脚本：
            if raw_line.lower() == "stop":
                print("[!] 收到停止指令，脚本退出。")
                break

            # 3) 解析激励值
            try:
                desired_excitation = float(raw_line)
            except ValueError:
                print(f"[!] 无法解析为浮点数: {raw_line}")
                continue

            print(f"[<] Received excitation: {desired_excitation}")

            # 4) 计算速度
            forward_speed = get_speed_from_excitation(desired_excitation)
            if forward_speed < 1:
                forward_speed = 1
            forward_speed = int(forward_speed)

            # 5) 驱动电机
            motor.move_steps_constant_speed( steps_for_90_deg, forward_speed )
            # 可选：做一些反转或别的动作
            motor.move_steps_linear_decel(-steps_for_90_deg, 200, 200)

            # 6) 回发 ACK
            ack_msg = f"ACK:{desired_excitation}\n"
            ser.write(ack_msg.encode('utf-8'))
            print(f"[>] Sent: {ack_msg.strip()}")

    except KeyboardInterrupt:
        print("\n[!] Ctrl+C捕捉到, 准备退出脚本...")

    finally:
        ser.close()
        GPIO.cleanup()
        print("[+] 串口已关闭, GPIO已清理, 脚本退出.")
