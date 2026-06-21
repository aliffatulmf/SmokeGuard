# Configuration

Edit `config.json` untuk mengatur parameter deteksi.

| Field         | Tipe   | Default | Values           | Keterangan                              |
| ------------- | ------ | ------- | ---------------- | --------------------------------------- |
| `conf`        | float  | 0.35    | 0 - 100          | Confidence threshold                    |
| `iou`         | float  | 0.45    | 0 - 100          | IoU threshold untuk NMS                 |
| `agnostic`    | bool   | true    | `true`, `false`  | Class-agnostic NMS                      |
| `max_det`     | int    | 1000    | -                | Maksimal jumlah deteksi per gambar      |
| `multi_label` | bool   | true    | `true`, `false`  | Izinkan multiple label per bounding box |
| `augment`     | bool   | true    | `true`, `false`  | Augmentasi saat inferensi               |
| `amp`         | bool   | false   | `true`, `false`  | Automatic Mixed Precision               |
