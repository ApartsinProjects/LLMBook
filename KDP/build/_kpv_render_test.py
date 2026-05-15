"""Quick test: open a KPF in Kindle Previewer 3 and screenshot.

Direct minimal version of what KPVDebug should do. Avoid subprocess
issues by using os.startfile + screenshot via PIL ImageGrab.
"""
import os
import sys
import time
import subprocess
from pathlib import Path


KPV = Path("C:/Users/apart/AppData/Local/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe")


def open_in_kpv(target_path: Path):
    """Launch KPV with target file. Returns process handle."""
    if not target_path.exists():
        print(f"ERROR: target not found: {target_path}")
        return None
    if not KPV.exists():
        print(f"ERROR: KPV not found: {KPV}")
        return None
    # Use shell=False but pass single string command via cmd /c
    # The space in path is the issue with subprocess on Windows when
    # used as program name. Workaround: use cmd.exe as launcher.
    cmd = ['cmd.exe', '/c', 'start', '""', str(KPV), str(target_path)]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        return proc
    except Exception as e:
        print(f"Launch failed: {e}")
        return None


def screenshot(out_path: Path, method='pil'):
    """Capture full desktop to PNG."""
    if method == 'pil':
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            img.save(out_path)
            return True
        except ImportError:
            print("PIL not available; falling back to PowerShell")
            method = 'ps'
    if method == 'ps':
        # PowerShell screen capture
        ps_script = f'''
$Width = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width
$Height = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bmp = New-Object System.Drawing.Bitmap $Width, $Height
$gfx = [System.Drawing.Graphics]::FromImage($bmp)
$gfx.CopyFromScreen(0, 0, 0, 0, $bmp.Size)
$bmp.Save('{out_path}', [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
'''
        try:
            subprocess.run(['powershell', '-Command', ps_script],
                           check=True, capture_output=True, timeout=30)
            return True
        except Exception as e:
            print(f"PowerShell screenshot failed: {e}")
            return False
    return False


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <epub-or-kpf-path> [output.png] [wait_sec]")
        sys.exit(1)
    target = Path(sys.argv[1]).resolve()
    out_png = Path(sys.argv[2] if len(sys.argv) > 2
                   else target.with_suffix('.kpv.png'))
    wait = int(sys.argv[3]) if len(sys.argv) > 3 else 15

    print(f"Target: {target}")
    print(f"Output: {out_png}")
    print(f"Wait:   {wait}s")

    print(f"\nLaunching KPV with {target.name}...")
    proc = open_in_kpv(target)
    if not proc:
        sys.exit(2)

    print(f"Waiting {wait}s for KPV to render...")
    time.sleep(wait)

    print(f"Capturing screenshot...")
    if screenshot(out_png):
        print(f"OK: saved {out_png} ({out_png.stat().st_size} bytes)")
    else:
        print(f"FAIL: screenshot failed")
        sys.exit(3)

    print(f"\nKPV is still running. Kill manually if needed:")
    print(f"  powershell Stop-Process -Name KPR_NCD,'Kindle Previewer 3' -Force")


if __name__ == '__main__':
    main()
