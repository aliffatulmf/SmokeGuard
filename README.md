# SmokeGuard

Aplikasi deteksi aktivitas merokok secara real-time dengan YOLOv5 dan antarmuka PySide6.

## Features

- Deteksi objek real-time melalui webcam, file video, atau direktori gambar
- Parameter deteksi yang dapat dikonfigurasi (confidence, IoU, augmentasi, dll.)
- Penangkapan snapshot dengan pencatatan metadata
- Dukungan perangkat CUDA dan CPU
- Panel kontrol CLI untuk konfigurasi lanjutan

## Tech Stack

- **Model**: YOLOv5 (Ultralytics)
- **Framework**: PyTorch
- **GUI**: PySide6 (Qt)
- **Vision**: OpenCV

## Requirements

- Python 3.8+
- GPU dengan CUDA (opsional, untuk inferensi yang lebih cepat)

## Installation

```bash
git clone https://github.com/aliffatulmf/SmokeGuard.git
cd SmokeGuard
pip install -r requirements.txt
```

## Usage

```bash
# Jalankan dengan webcam
python app.py --model weights/best.pt

# Jalankan dengan file video
python app.py --model weights/best.pt --source video.mp4

# Jalankan dengan direktori gambar
python app.py --model weights/best.pt --source images/

# Gunakan CPU
python app.py --model weights/best.pt --device cpu
```

### Options

| Flag       | Keterangan                                               |
| ---------- | -------------------------------------------------------- |
| `--model`  | Path ke file model (wajib)                               |
| `--source` | Sumber input (0 untuk webcam, path file, atau direktori) |
| `--device` | Perangkat: `cpu` atau `cuda` (default: cuda)             |
| `--output` | Direktori output (default: outputs)                      |
