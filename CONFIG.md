# Configuration

Edit `config.json` untuk mengatur parameter deteksi.

| Field         | Tipe   | Default | Values              | Keterangan                              |
| ------------- | ------ | ------- | ------------------- | --------------------------------------- |
| `conf`        | float  | 0.35    | 0 - 100             | Confidence threshold                    |
| `iou`         | float  | 0.45    | 0 - 100             | IoU threshold untuk NMS                 |
| `agnostic`    | string | Enable  | `Enable`, `Disable` | Class-agnostic NMS                      |
| `max_det`     | int    | 1000    | -                   | Maksimal jumlah deteksi per gambar      |
| `multi_label` | string | Enable  | `Enable`, `Disable` | Izinkan multiple label per bounding box |
| `augment`     | string | Enable  | `Enable`, `Disable` | Augmentasi saat inferensi               |
| `amp`         | string | Disable | `Enable`, `Disable` | Automatic Mixed Precision               |
