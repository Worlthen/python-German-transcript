#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transcribe all audio/video files in a folder to SRT subtitles and plain text.
Author: <Worlthen>
Date: 2025-08-05
"""

import argparse
import os
import sys
import glob
from pathlib import Path
import torch # 导入torch
import subprocess # 导入subprocess


try:
    import whisper
except ImportError:
    sys.exit("请先安装 whisper：pip install openai-whisper")

# -----------------------------
# 1. 解析命令行参数
# -----------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="批量转写音视频文件为字幕（SRT）和纯文本（TXT）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=".",
        help="目标文件夹，所有音视频文件都会被处理",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="输出文件夹，若不指定则默认与输入文件同文件夹",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="de",
        help="目标语言，whisper 支持的语言代码（en, zh, ja, ...）",

    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="base",
        help="whisper 模型大小：tiny / base / small / medium / large",
    )
    parser.add_argument(
        "-c",
        "--cpu",
        action="store_true",
        help="强制使用 CPU（默认会检测是否有 GPU）",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=True,
        help="强制重写已存在的 output 文件",
    )
    return parser.parse_args()


# -----------------------------
# 2. 检查文件类型
# -----------------------------
VALID_EXTS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".mp3",
    ".wav",
    ".flac",
    ".aac",
    ".m4a",
}


def is_audio_video(file_path: Path) -> bool:
    return file_path.suffix.lower() in VALID_EXTS


# -----------------------------
# 3. 转写 + 输出
# -----------------------------
def transcribe_and_write(
    model, file_path: Path, output_dir: Path, language: str, force_overwrite: bool
):
    file_path = file_path.resolve()
    base_name = file_path.stem
    srt_path = output_dir / f"{base_name}.srt"
    txt_path = output_dir / f"{base_name}.txt"

    # 如有 --force 选项可以覆盖
    if not force_overwrite:
        if srt_path.exists() or txt_path.exists():
            print(f"跳过已存在的文件：{file_path.name}")
            return

    print(f"\n=== 处理: {file_path.name} ===")

    # --- 添加FFmpeg测试 ---


    # -----------------------------
    # Transcribe
    # -----------------------------
    result = model.transcribe(
        str(file_path),
        language=language,
        verbose=False,
        # 你可以调大 n_threads、task 等参数
    )

    # -----------------------------
    # 写 SRT
    # -----------------------------
    with open(srt_path, "w", encoding="utf-8") as f_srt:
        for idx, segment in enumerate(result["segments"], start=1):
            start = whisper.utils.format_timestamp(segment["start"])
            end = whisper.utils.format_timestamp(segment["end"])
            text = segment["text"].strip()
            f_srt.write(f"{idx}\n{start} --> {end}\n{text}\n\n")

    # -----------------------------
    # 写 TXT
    # -----------------------------
    with open(txt_path, "w", encoding="utf-8") as f_txt:
        txt = "\n".join(seg["text"].strip() for seg in result["segments"])
        f_txt.write(txt)

    print(f"✅ 写入: {srt_path.name} | {txt_path.name}")


# -----------------------------
# 4. 主入口
# -----------------------------
def main():
    args = parse_args()

    input_dir = Path(args.input).expanduser().resolve()
    if not input_dir.is_dir():
        sys.exit(f"❌ 输入路径不是目录: {input_dir}")

    output_dir = (
        Path(args.output).expanduser().resolve()
        if args.output
        else input_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    # 检测显卡
    # 动态添加FFmpeg路径到PATH环境变量
    import os
    ffmpeg_bin_path = r"F:\softwares\ffmpeg\bin"
    if ffmpeg_bin_path not in os.environ['PATH']:
        os.environ['PATH'] = f"{ffmpeg_bin_path};{os.environ['PATH']}"
        print(f"已将FFmpeg路径添加到PATH环境变量: {ffmpeg_bin_path}")

    device = "cuda" if not args.cpu and torch.cuda.is_available() else "cpu"
    print(f"将使用设备: {device}")

    print(f"加载 Whisper 模型: {args.model}")
    # 强制设置FFmpeg路径
    import whisper.audio
    whisper.audio.ffmpeg_path = r"F:\softwares\ffmpeg\bin\ffmpeg.exe"
    try:
        model = whisper.load_model(args.model, device=device)
    except Exception as e:
        sys.exit(f"❌ 模型加载失败: {e}")

    # 让脚本一次性遍历全部音视频文件
    all_files = sorted(input_dir.rglob("*"))
    target_files = [f for f in all_files if f.is_file() and is_audio_video(f)]

    if not target_files:
        sys.exit("❌ 没有找到可处理的音视频文件")

    print(f"共发现 {len(target_files)} 个文件，开始转写…")

    for file_path in target_files:
        transcribe_and_write(
            model,
            file_path,
            output_dir,
            language=args.language,
            force_overwrite=args.force,
        )

    print("\n✨ 所有文件已完成！", flush=True)


if __name__ == "__main__":
    main()
