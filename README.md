# Smart-Worhip-Controller
# 🎹 Smart-Worship-Controller (MediaPipe AI)
[![DOI](https://zenodo.org/badge/1168528875.svg)](https://doi.org/10.5281/zenodo.18812051)

An intelligent computer vision system designed to control worship music or backing tracks using body gestures. Built with Python and MediaPipe, this tool allows worship leaders or technicians to trigger song sections (Verse, Chorus, Bridge) through stable, real-time pose estimation.

## ✨ Key Features
- **Intelligent Pose Stabilizer**: Implements a 6-frame buffer to prevent "flickering" or accidental triggers.
- **Coordinate-Based Logic**: Uses precise Y and X axis margins to differentiate gestures, making it far more reliable than standard image classification.
- **Real-time Visualization**: Includes a live "Confidence Bar" window to monitor active poses and system accuracy.
- **Single-Execution Trigger**: Automatically stops the previous track and plays the new one once per gesture change.
- **Background Agnostic**: Powered by MediaPipe's 33-landmark skeleton tracking, ensuring stability regardless of lighting or background clutter.

## 🖐️ Worship Gesture Map
| Pose | Music Section | Trigger Action |
| :--- | :--- | :--- |
| **Right Hand Up** | VERSE | Plays `verse.mp3` |
| **Left Hand Up** | VERSE 2 | Plays `verse 2.mp3` |
| **Both Hands Up** | CHORUS | Plays `chorus.mp3` |
| **Right Hand Cross** | BRIDGE | Plays `bridge.mp3` |
| **Neutral Position** | IDLE | Resets trigger for next command |

## 🛠️ Requirements
- **Python**: 3.10.9 (Recommended for library stability)
- **MediaPipe**: For pose landmark detection
- **OpenCV**: For camera feed and visualization
- **Pygame**: For low-latency audio playback
- **NumPy**: Version < 2.0.0 (Required for TensorFlow/MediaPipe compatibility)

## 🚀 Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Smart-Worship-Controller.git](https://github.com/YOUR_USERNAME/Smart-Worship-Controller.git)
Smart-Worship-Controller (MediaPipe AI): An AI-based gesture controller using MediaPipe Pose Estimation to trigger worship music elements (Verse, Chorus, Bridge) with real-time stability and accuracy visualization.
