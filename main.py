import argparse
import sys
import tkinter as tk
import traceback
from tkinter import filedialog

import pyloudnorm as pyln
import soundfile as sf


def calculate_lufs(audio_path):
    data, rate = sf.read(audio_path)
    # 使用 ITU-R BS.1770-4 标准
    meter = pyln.Meter(rate)
    loudness = meter.integrated_loudness(data)
    return loudness


def main():
    parser = argparse.ArgumentParser(description='计算音频文件的整体响度')
    parser.add_argument('audio_file', nargs='?', help='音频文件路径')
    args = parser.parse_args()

    # 如果未提供参数，则弹出文件选择对话框
    audio_file = args.audio_file
    if not audio_file:
        root = tk.Tk()
        root.withdraw()
        audio_file = filedialog.askopenfilename(
            title='请选择音频文件',
            filetypes=[('音频文件', '*.wav *.flac *.mp3'), ('所有文件', '*.*')]
        )
        if not audio_file:
            print('未选择文件，程序退出。')
            sys.exit(0)

    try:
        print(f"正在处理文件: {audio_file}")
        lufs_value = calculate_lufs(audio_file)

        print(f"音频整体响度: {lufs_value:.1f} LUFS")
        print(f"如果这是人声，您需要增益 {-16. - lufs_value:.1f} dB 来达到 -16 LUFS 的目标响度；")
        print(f"如果这是 BGM，您需要增益 {-28. - lufs_value:.1f} dB 来达到 -28 LUFS 的目标响度。")

        # 提供参考信息
        # print("\n参考标准:")
        # print("- 电影/电视: -23 LUFS (±2 LU)")
        # print("- 流媒体平台 (Spotify, Apple Music等): -14 LUFS")
        # print("- 广播: -24 LUFS")
        # print("- 音乐制作（母带）: 通常在-9到-14 LUFS之间")
    except Exception:
        traceback.print_exc()

    input("按 Enter 退出 ...")


if __name__ == "__main__":
    main()
