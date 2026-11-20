$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $folder
New-Item -ItemType Directory -Force -Path '.\outputs' | Out-Null

python .\t1.py *> .\outputs\tugas1.txt
python .\jelajah.py .\contoh_100_baris.py *> .\outputs\tugas2.txt
python .\q.py .\contoh.py all *> .\outputs\tugas3.txt
python ..\cek\cek.py ..\cek\uji *> .\outputs\tugas6.txt

Write-Host 'Output tugas 1, 2, 3, dan 6 tersimpan di folder outputs.'
