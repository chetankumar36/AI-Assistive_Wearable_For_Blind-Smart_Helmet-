# 🪖 Smart Helmet

### AI-Powered Assistive Wearable for Real-Time Object Detection and Voice Guidance

Smart Helmet is an AI-powered assistive wearable built with Python on a Raspberry Pi. It uses a camera and the YOLO object-detection model to recognise objects around the wearer and announces them through voice alerts, so the user gets information about their surroundings without looking at a screen.

The helmet also includes environmental sensing: an LDR detects day/night lighting and a DS18B20 sensor measures temperature. Push buttons let the wearer trigger each function. An additional GPS and emergency-email module is included in the source code.

Built with **Python, Raspberry Pi, OpenCV, YOLOv3-Tiny, gTTS, pygame, gpiozero and PySerial**.

> 🏆 Selected for funding (₹10,000) under the **NewGen IEDC Student Project Scheme**.

* * *

## Table of Contents

- [Features](#-features)
- [System Architecture](#️-system-architecture)
- [Project Structure](#-project-structure)
- [File Responsibilities](#-file-responsibilities)
- [Technology Stack](#️-technology-stack)
- [Hardware Components](#-hardware-components)
- [Requirements](#️-requirements)
- [Installation](#-installation)
- [Configuration and Security](#-configuration-and-security)
- [Running Smart Helmet](#️-running-smart-helmet)
- [Testing Individual Modules](#-testing-individual-modules)
- [GPIO Configuration Reference](#-gpio-configuration-reference)
- [Troubleshooting](#-troubleshooting)
- [Why Edge AI?](#-why-edge-ai)
- [Future Improvements](#-future-improvements)
- [Project Status](#-current-project-status)
- [Project Recognition](#-project-recognition)
- [Team](#-team)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

* * *

## ✨ Features

### 🎯 Real-Time Object Detection

The camera captures frames and the Raspberry Pi runs YOLOv3-Tiny through OpenCV's DNN module to detect objects from the COCO class list.

```
Camera → Raspberry Pi → YOLO Object Detection → Text-to-Speech → Audio Alert
```

- Captures frames from a connected camera
- Detects objects from the COCO class list
- Shows object labels with confidence values
- Applies Non-Maximum Suppression to remove duplicate boxes
- Announces detected object names through audio

### 🔊 Voice-Based Guidance

Detected objects and sensor readings are converted into speech using gTTS and played with pygame.

> gTTS needs an internet connection to generate **new** speech. Previously generated audio can be played locally. YOLO inference itself runs fully on the Raspberry Pi.

### 🌡️ Temperature Monitoring

- Reads the DS18B20 sensor through the Raspberry Pi 1-Wire interface
- Announces the measured temperature in Celsius

### 💡 Day / Night Detection

- Reads a digital LDR module
- Identifies the surrounding light condition as **Day** or **Night**
- Announces the lighting status

### 🔘 Button-Based Control

Separate push buttons activate the temperature reading, the light-status check, and object detection, so the helmet is simple to operate hands-on.

### 🚨 GPS Emergency Alert Module

An additional module in the source code (`gps_emergency.py`):

- Reads GPS NMEA data over the Raspberry Pi serial interface
- Extracts latitude and longitude from `GPGGA` messages
- On emergency-button press, builds a Google Maps location link and sends an email alert
- Sounds a buzzer as an alert indication

> This module needs a compatible GPS module, serial configuration and secure email setup. Verify the hardware integration before relying on it.

* * *

## 🏗️ System Architecture

```
                        Smart Helmet
                              │
                        Raspberry Pi
                              │
     ┌──────────┬─────────────┼─────────────┬──────────┐
     │          │             │             │          │
  Camera   Push Buttons   LDR Sensor   DS18B20 Sensor  GPS Module
     │          │             │             │          │
     ▼          ▼             ▼             ▼          ▼
  OpenCV   Function      Day / Night   Temperature   GPS Coordinates
     │      Selection      Status       Reading          │
     ▼          │             │             │             ▼
YOLOv3-Tiny     │             │             │       Emergency Email
     │          │             │             │            Alert
     ▼          └─────────────┴──────┬──────┘
Detected Object                      │
     │                               │
     └───────────────┬───────────────┘
                     ▼
            Text-to-Speech (gTTS)
                     │
                     ▼
             Speaker / Headphones
                     │
                     ▼
                 Wearer Alert
```

### Object Detection Pipeline

```
Camera Input
     ↓
Frame Capture
     ↓
Image Pre-processing
     ↓
YOLOv3-Tiny Model
     ↓
Object Detection
     ↓
Non-Maximum Suppression
     ↓
Object Name + Confidence
     ↓
Text-to-Speech (gTTS)
     ↓
Audio Alert
```

* * *

## 📂 Project Structure

```
Smart-Helmet/
│
├── main.py                  # Main helmet application
├── main_back.py             # Earlier / backup implementation
├── gps_emergency.py         # GPS + emergency email module
├── phase1.py                # Temperature + LDR test with LCD
├── phase1_without_lcd.py    # Temperature + LDR test
├── button_test.py           # Push-button test
├── ldr_test_digital.py      # LDR digital-input test
├── .ds18b_test.py           # DS18B20 sensor test
├── script_test.py           # Basic script test
├── requirements.txt
├── README.md
├── .gitignore
│
└── yolo-coco/
    ├── classes.txt
    ├── coco.names           # COCO object labels
    ├── yolov3-tiny.cfg      # YOLO network configuration
    └── yolov3-tiny.weights  # Pre-trained YOLO weights
```

* * *

## 📌 File Responsibilities

### `main.py`

Primary application. Responsible for:

- Initialising GPIO devices, temperature sensor, YOLO network, camera and audio
- Object detection with voice output
- Temperature reading
- Light-status (day/night) detection
- Emergency-alert workflow

### `gps_emergency.py`

GPS serial reading, coordinate conversion, emergency-button handling, buzzer control and email notification.

### `main_back.py`

Earlier / backup version of the main implementation.

### `phase1.py` / `phase1_without_lcd.py`

Temperature and light-sensing tests, with and without an I2C LCD display.

### `button_test.py`, `ldr_test_digital.py`, `.ds18b_test.py`, `script_test.py`

Small hardware tests for push buttons, the LDR module, the DS18B20 sensor and basic script execution.

### `yolo-coco/`

YOLOv3-Tiny configuration, pre-trained weights and COCO class labels required by the detection pipeline.

* * *

## 🛠️ Technology Stack

| Component             | Technology                  |
|-----------------------|-----------------------------|
| Programming Language  | Python                      |
| Embedded Platform     | Raspberry Pi                |
| Computer Vision       | OpenCV (DNN module)         |
| Object Detection      | YOLOv3-Tiny                 |
| Numerical Processing  | NumPy                       |
| GPIO Control          | gpiozero                    |
| Voice Generation      | gTTS                        |
| Audio Playback        | pygame                      |
| Video Capture         | OpenCV VideoCapture         |
| GPS Communication     | PySerial                    |
| Temperature Interface | Raspberry Pi 1-Wire         |
| Email Notifications   | Python `smtplib`            |

* * *

## 🧰 Hardware Components

| Component                  | Purpose                                   |
|----------------------------|-------------------------------------------|
| Raspberry Pi 4             | Main processing unit                      |
| Camera / USB Webcam        | Captures the surrounding environment      |
| DS18B20 Temperature Sensor | Measures temperature                      |
| LDR Sensor Module          | Detects light conditions                  |
| Push Buttons               | Activate individual functions             |
| Speaker / Headphones       | Audio feedback                            |
| GPS Module                 | Location data for the emergency module    |
| Buzzer                     | Alert indication                          |
| Power Bank / 5V Supply     | Powers the prototype                      |
| Helmet                     | Holds all components                      |

> Exact camera, GPS module, power arrangement and wiring may vary with the assembled prototype.

* * *

## ⚙️ Requirements

Recommended: **Raspberry Pi OS with Python 3**

**Hardware**

- Raspberry Pi (designed around Raspberry Pi 4)
- Pi-compatible camera or USB webcam
- DS18B20 temperature sensor
- Digital-output LDR module
- Push buttons
- Speaker or headphones
- Optional: GPS module and buzzer for the emergency module
- Suitable 5V power supply

**Software**

```
opencv-python
numpy
gpiozero
gTTS
pygame
imutils
pyserial
RPLCD        # only for the LCD test (phase1.py)
```

* * *

## 🚀 Installation

### 1. Clone the repository

```
git clone https://github.com/chetankumar36/Smart-Helmet.git
cd Smart-Helmet
```

> Replace the URL if your repository name is different.

### 2. Create a virtual environment (optional)

```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```
pip install opencv-python numpy gpiozero gTTS pygame imutils pyserial RPLCD
```

or, if you add a `requirements.txt`:

```
pip install -r requirements.txt
```

### 4. Enable Raspberry Pi interfaces

- Enable the **camera** interface if your camera setup needs it
- Enable the **1-Wire** interface for the DS18B20 (`/sys/bus/w1/devices/`)
- Enable the **serial** interface if you are using the GPS module
- Make sure the application can access GPIO and serial devices

### 5. Check the YOLO model files

```
yolo-coco/
├── coco.names
├── yolov3-tiny.cfg
└── yolov3-tiny.weights
```

The program loads these with relative paths, so run it from the project root.

* * *

## 🔐 Configuration and Security

Email alerts need sender credentials. **Never** write them directly in Python source code.

- Store email credentials in environment variables or a `.env` file excluded from Git
- Add `.env` to `.gitignore`
- If an app password was ever committed or shared, **revoke it immediately** and generate a new one
- Do not publish personal GPS coordinates or contact details

Example `.env` (do not commit):

```
ALERT_EMAIL_SENDER=your_email@example.com
ALERT_EMAIL_APP_PASSWORD=your_app_password
ALERT_EMAIL_RECEIVER=receiver@example.com
```

> The variable names above are suggestions — update `gps_emergency.py` / `main.py` to read them with `os.getenv(...)`.

* * *

## ▶️ Running Smart Helmet

```
python3 main.py
```

Use the connected push buttons to trigger temperature reading, light-status detection or object detection.

* * *

## 🧪 Testing Individual Modules

| Test                      | Command                           |
|---------------------------|-----------------------------------|
| Push buttons              | `python3 button_test.py`          |
| LDR digital input         | `python3 ldr_test_digital.py`     |
| Temperature + LDR         | `python3 phase1_without_lcd.py`   |
| Temperature + LDR + LCD   | `python3 phase1.py`               |
| GPS + emergency module    | `python3 gps_emergency.py`        |

> Run hardware tests only after connecting the components and checking the wiring.

* * *

## 📊 GPIO Configuration Reference

The current `main.py` uses these gpiozero pin numbers:

| Function                | GPIO Pin |
|-------------------------|----------|
| LDR digital input       | GPIO 21  |
| Temperature button      | GPIO 1   |
| LDR button              | GPIO 7   |
| Object-detection button | GPIO 8   |
| Emergency button        | GPIO 20  |
| Buzzer                  | GPIO 16  |

> Verify wiring and pin numbering before powering the circuit. Button logic is **active-low** in the current implementation.

* * *

## 🐛 Troubleshooting

**Camera is not opening**

- Check the camera connection and that Raspberry Pi OS detects it
- Verify the camera device index used by OpenCV
- Close other applications using the camera

**YOLO model files not found**

Run the program from the project root and confirm `yolo-coco/` contains the `.cfg`, `.weights` and `coco.names` files.

**DS18B20 temperature not detected**

- Check sensor wiring and the pull-up resistor
- Verify the 1-Wire interface is enabled
- Look for a device directory beginning with `28` under `/sys/bus/w1/devices/`

**GPIO permission or input issues**

- Verify pin numbering and wiring
- Make sure buttons and sensors share a common ground
- Confirm the app has GPIO permissions

**No voice output**

- Check the speaker or headphone connection
- Verify pygame audio playback works
- Remember that generating new speech with gTTS needs internet

**GPS data unavailable**

- Check the serial connection, port and baud rate
- Make sure the module has a satellite fix and outputs valid `GPGGA` messages

* * *

## 🧠 Why Edge AI?

Running detection directly on the Raspberry Pi means the wearer does not depend on a cloud server to find out what is in front of them. Frames are processed locally, which gives:

- Low-latency, real-time detection
- No video sent to external servers
- A compact, wearable, low-cost design
- Hands-free audio feedback instead of a screen

* * *

## 🚀 Future Improvements

- 🎯 Faster and more accurate detection on the Raspberry Pi
- 📏 Obstacle-distance estimation with distance sensors
- 🗣️ More contextual voice guidance
- 🌍 Multilingual voice assistance
- 📍 Improved GPS emergency notifications and contact configuration
- 🔋 Lower power consumption for longer wearable operation
- 🪖 Better helmet enclosure, comfort and component integration
- 🩺 Startup self-check and sensor-status monitoring
- 🔇 Fully offline text-to-speech

* * *

## 📈 Current Project Status

**Status: 🟢 Working prototype**

- [x] YOLOv3-Tiny object detection
- [x] Voice alerts for detected objects
- [x] DS18B20 temperature monitoring
- [x] LDR-based day/night detection
- [x] Push-button function control
- [x] Individual hardware test scripts
- [x] GPS + emergency email source module (hardware integration to be verified)
- [ ] Credentials moved to environment variables
- [ ] Offline text-to-speech
- [ ] Distance estimation

* * *

## 🏆 Project Recognition

Selected for funding under the **NewGen IEDC Student Project Scheme**.

| Detail              | Value                                          |
|---------------------|------------------------------------------------|
| Funding organisation | NewGen IEDC — Institution's Innovation Council |
| Sanctioned amount   | ₹10,000                                        |
| Institution         | JNN College of Engineering, Shivamogga         |

* * *

## 👨‍💻 Team

**Institution:** JNN College of Engineering, Shivamogga, Karnataka
**Department:** Information Science and Engineering
**Faculty Coordinator:** Dr. Chethan G S

| Team Member       | USN        |
|-------------------|------------|
| Chetan Kumar N K  | 4JN23IS025 |
| Chiranthan S      | 4JN23IS027 |
| Srushti H S       | 4JN23IS142 |
| Trupthi Niranjan  | 4JN23IS162 |

* * *

## 📜 License

No license file is included yet. Add a `LICENSE` file if you want to distribute the project as open source.

* * *

## 🙌 Acknowledgements

Built using open-source technologies:

Raspberry Pi · OpenCV · YOLO · NumPy · gpiozero · gTTS · pygame · PySerial

Supported by NewGen IEDC and the Department of Information Science & Engineering, JNNCE.

* * *

## ⭐ Star the Repository

If you find Smart Helmet useful, consider giving the repository a ⭐ on GitHub. Thank you!
