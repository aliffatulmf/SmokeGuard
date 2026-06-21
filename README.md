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

### GUI Mode

```bash
python app.py
```

### CLI Mode

```bash
# Jalankan dengan webcam
python control_panel.py --run --source 0 --model weights/best.pt

# Jalankan dengan file video
python control_panel.py --run --source video.mp4 --model weights/best.pt

# Jalankan dengan direktori gambar
python control_panel.py --run --source images/ --model weights/best.pt

# Gunakan CPU alih-alih CUDA
python control_panel.py --run --source 0 --model weights/best.pt --device cpu
```

### CLI Options

| Flag                 | Keterangan                                               |
| -------------------- | -------------------------------------------------------- |
| `--run`              | Mulai deteksi                                            |
| `--source`           | Sumber input (0 untuk webcam, path file, atau direktori) |
| `--model`            | Path ke file model YOLOv5 (.pt)                          |
| `--device`           | Perangkat pemrosesan: `cpu` atau `cuda` (default: cuda)  |
| `--save`             | Simpan hasil deteksi                                     |
| `--output`           | Direktori output (default: outputs)                      |
| `--clean`            | Hapus cache untuk membebaskan memori                     |
| `--install-required` | Instal semua dependensi                                  |

## Configuration

Edit `config.json` untuk mengatur parameter deteksi:

```json
{
  "conf": 0.35,
  "iou": 0.45,
  "agnostic": "Enable",
  "max_det": 1000,
  "multi_label": "Enable",
  "augment": "Enable",
  "amp": "Disable"
}
```
