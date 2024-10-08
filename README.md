﻿# Action Recognition System: Dynamic Hand Gesture Classification

## Introduction

This project introduces a novel Convolutional Neural Network (CNN)-based approach for dynamic hand gesture classification. It aims to enable intuitive computer control through hand gestures, paving the way for more natural human-computer interaction.

## Features

- Analyzes video frame sequences to capture temporal dynamics of hand gestures
- Utilizes preprocessing techniques for noise reduction and data preparation
- Employs data augmentation to improve model adaptability
- Leverages transfer learning for enhanced performance
- Achieves 96% accuracy in gesture recognition

## Applications

- Human-computer interaction (HCI)
- Gesture-based control systems for devices like drones or robots
- PowerPoint presentation control using hand gestures

## Installation

```bash
git clone https://github.com/your-username/action-recognition-system.git
cd action-recognition-system
pip install -r requirements.txt
```

## Usage

1. Run the main script:

```bash
python handGesture.py
```

2. When prompted, enter the path to your PowerPoint file:

```
Enter a file path: /path/to/your/presentation.pptx
```

3. The script will convert the PowerPoint to images and launch the gesture recognition system.

4. Use the following gestures to control the presentation:
   - Left hand (pinky out): Previous slide
   - Right hand (thumb out): Next slide
   - Two fingers out: Pointer mode
   - One finger out: Drawing mode
   - Three fingers out: Erase last annotation

## Project Structure

- `handGesture.py`: Main script for hand gesture recognition and presentation control
- `cvfpsCalc.py`: Module for FPS calculation
- `ppt2img.py`: Module for converting PowerPoint to images

## Methodology

1. Data Collection: Diverse dataset including various backgrounds, lighting conditions, and hand orientations
2. Preprocessing: Hand detection and segmentation using MediaPipe Hands or OpenPose
3. Feature Extraction: 3D CNNs for depth perception (if depth information available)
4. Data Augmentation: Advanced techniques like elastic deformations and random erasing
5. Model Training: Dynamic learning rates and mixup augmentation
6. Evaluation: Confusion matrix analysis and real-world robustness testing

## Future Work

- Extend the gesture vocabulary for more complex interactions
- Improve performance in challenging lighting conditions
- Integrate with more applications beyond presentation control

## Images

![Hand Gesture](/handGesture.png "Hand Gesture using Meadpipe")
