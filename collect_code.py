#!/usr/bin/env python3
"""
collect_code.py — Сборка исходного кода проекта в один файл для передачи в LLM.

Использование:
    python collect_code.py [--output FILE] [--exclude EXT] [--max-size BYTES]

Примеры:
    python collect_code.py
    python collect_code.py --output my_export.txt --exclude .json --max-size 100000
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# ==================== НАСТРОЙКИ ПО УМОЛЧАНИЮ ====================
DEFAULT_EXCLUDE_DIRS = {'.venv', 'venv', '.git', '__pycache__', '.vscode', '.idea', 'node_modules', '.pytest_cache'}
DEFAULT_EXCLUDE_FILES = {'project_export.txt', 'collect_code.py', 'export.py', '.gitignore', 'collect_code.pyc'}
DEFAULT_INCLUDE_EXTS = {'.py', '.html', '.css', '.js', '.txt', '.md', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'}
DEFAULT_OUTPUT = 'project_export.txt'
DEFAULT_MAX_FILE_SIZE = 500_000  # 500 KB — защита от больших файлов

# ==================== УТИЛИТЫ ====================
def format_size(bytes_count: int) -> str:
    """Человекочитаемый размер файла."""
    for unit in ['B', 'KB', 'MB']:
        if bytes_count < 1024:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.1f} GB"

def is_binary_file(filepath: str, sample_size: int = 1024) -> bool:
    """Эвристическая проверка: является ли файл бинарным."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(sample_size)
        # Если в первых 1KB есть нулевой байт — скорее всего бинарный
        return b'\x00' in chunk
    except:
        return True

def get_file_encoding(filepath: str) -> str:
    """Пытается определить кодировку файла с фолбэком."""
    for enc in ['utf-8', 'cp1251', 'latin-1', 'ascii']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                f.read(1024)
            return enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return 'utf-8'  # последний шанс

# ==================== ОСНОВНАЯ ЛОГИКА ====================
def collect_project_code(
    root_dir: str = '.',
    output_file: str = DEFAULT_OUTPUT,
    exclude_dirs: set = None,
    exclude_files: set = None,
    include_exts: set = None,
    max_file_size: int = DEFAULT_MAX_FILE_SIZE,
    skip_binary: bool = True,
    skip_empty: bool = True,
    verbose: bool = True
) -> dict:
    """
    Собирает код проекта в один файл.
    
    Returns:
        dict со статистикой: {files_count, total_lines, total_size, errors}
    """
    exclude_dirs = exclude_dirs or DEFAULT_EXCLUDE_DIRS
    exclude_files = exclude_files or DEFAULT_EXCLUDE_FILES
    include_exts = include_exts or DEFAULT_INCLUDE_EXTS
    
    stats = {'files_count': 0, 'total_lines': 0, 'total_size': 0, 'errors': [], 'by_ext': {}}
    
    with open(output_file, 'w', encoding='utf-8') as out:
        # Заголовок экспорта
        out.write(f"# PROJECT CODE EXPORT\n")
        out.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"# Root: {os.path.abspath(root_dir)}\n")
        out.write(f"# Settings: exts={include_exts}, max_size={format_size(max_file_size)}\n")
        out.write(f"{'#' * 60}\n\n")
        
        for root, dirs, files in os.walk(root_dir):
            # Исключаем ненужные директории (модификация на месте для os.walk)
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # Дополнительная защита: пропускаем пути с исключениями
            if any(ex in Path(root).parts for ex in exclude_dirs):
                continue

            for file in sorted(files):  # Сортировка для детерминированного порядка
                ext = Path(file).suffix.lower()
                
                # Фильтры
                if file in exclude_files or ext not in include_exts:
                    continue
                
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, root_dir)
                
                # Проверка размера
                try:
                    file_size = os.path.getsize(full_path)
                    if file_size > max_file_size:
                        if verbose:
                            print(f"⏭  Пропущен (большой): {relative_path} ({format_size(file_size)})")
                        continue
                except OSError as e:
                    stats['errors'].append(f"{relative_path}: {e}")
                    continue
                
                # Проверка на бинарность
                if skip_binary and is_binary_file(full_path):
                    if verbose:
                        print(f"⏭  Пропущен (бинарный): {relative_path}")
                    continue
                
                # Чтение файла
                try:
                    encoding = get_file_encoding(full_path)
                    with open(full_path, 'r', encoding=encoding, errors='replace') as f:
                        content = f.read()
                    
                    # Пропуск пустых файлов
                    if skip_empty and not content.strip():
                        if verbose:
                            print(f"⏭  Пропущен (пустой): {relative_path}")
                        continue
                    
                    # Запись в экспорт
                    out.write(f"\n{'=' * 60}\n")
                    out.write(f"📄 ФАЙЛ: {relative_path}\n")
                    out.write(f"📏 Размер: {format_size(file_size)} | Кодировка: {encoding}\n")
                    out.write(f"{'=' * 60}\n\n")
                    out.write(content)
                    out.write("\n\n")
                    
                    # Обновление статистики
                    stats['files_count'] += 1
                    stats['total_lines'] += content.count('\n') + 1
                    stats['total_size'] += file_size
                    stats['by_ext'][ext] = stats['by_ext'].get(ext, 0) + 1
                    
                    if verbose:
                        print(f"✅ {relative_path} ({format_size(file_size)}, {content.count(chr(10)) + 1} строк)")
                        
                except Exception as e:
                    error_msg = f"{relative_path}: {type(e).__name__}: {e}"
                    stats['errors'].append(error_msg)
                    if verbose:
                        print(f"❌ Ошибка: {error_msg}")
                    out.write(f"\n[⚠️ Ошибка чтения: {error_msg}]\n\n")
    
    return stats

# ==================== CLI ИНТЕРФЕЙС ====================
def main():
    parser = argparse.ArgumentParser(
        description='Сборка исходного кода проекта в один файл',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры:
  %(prog)s                          # сборка с настройками по умолчанию
  %(prog)s -o code.txt              # вывод в code.txt
  %(prog)s --exclude .json .log     # исключить расширения
  %(prog)s --max-size 100000        # лимит 100KB на файл
  %(prog)s --no-binary --no-empty   # строгие фильтры
        '''
    )
    
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT,
                       help=f'Имя выходного файла (по умолчанию: {DEFAULT_OUTPUT})')
    parser.add_argument('--exclude-ext', nargs='*', default=[],
                       help='Дополнительные расширения для исключения (например: .json .log)')
    parser.add_argument('--max-size', type=int, default=DEFAULT_MAX_FILE_SIZE,
                       help=f'Макс. размер файла в байтах (по умолчанию: {DEFAULT_MAX_FILE_SIZE})')
    parser.add_argument('--no-binary', action='store_true', default=True,
                       help='Пропускать бинарные файлы (по умолчанию: включено)')
    parser.add_argument('--allow-binary', dest='no_binary', action='store_false',
                       help='Включить обработку бинарных файлов')
    parser.add_argument('--no-empty', action='store_true', default=True,
                       help='Пропускать пустые файлы (по умолчанию: включено)')
    parser.add_argument('--allow-empty', dest='no_empty', action='store_false',
                       help='Включить пустые файлы')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Тихий режим (минимум вывода в консоль)')
    parser.add_argument('--root', default='.',
                       help='Корневая директория проекта (по умолчанию: текущая)')
    
    args = parser.parse_args()
    
    # Подготовка настроек
    include_exts = DEFAULT_INCLUDE_EXTS - set(args.exclude_ext)
    
    if not args.quiet:
        print(f"🚀 Сборка кода проекта: {os.path.abspath(args.root)}")
        print(f"📦 Выходной файл: {args.output}")
        print(f"🔧 Расширения: {sorted(include_exts)}")
        print(f"📏 Макс. размер файла: {format_size(args.max_size)}")
        print("-" * 40)
    
    # Запуск сбора
    stats = collect_project_code(
        root_dir=args.root,
        output_file=args.output,
        include_exts=include_exts,
        max_file_size=args.max_size,
        skip_binary=args.no_binary,
        skip_empty=args.no_empty,
        verbose=not args.quiet
    )
    
    # Итоговый отчёт
    if not args.quiet:
        print("\n" + "=" * 40)
        print("📊 СТАТИСТИКА")
        print("=" * 40)
        print(f"✅ Файлов собрано: {stats['files_count']}")
        print(f"📄 Всего строк: {stats['total_lines']:,}")
        print(f"💾 Общий размер: {format_size(stats['total_size'])}")
        
        if stats['by_ext']:
            print("\n📁 По расширениям:")
            for ext, count in sorted(stats['by_ext'].items(), key=lambda x: -x[1]):
                print(f"   {ext}: {count}")
        
        if stats['errors']:
            print(f"\n⚠️  Ошибок: {len(stats['errors'])}")
            for err in stats['errors'][:5]:  # Показать первые 5
                print(f"   • {err}")
            if len(stats['errors']) > 5:
                print(f"   ... и ещё {len(stats['errors']) - 5}")
        
        print(f"\n✨ Готово! Файл: {os.path.abspath(args.output)}")
    
    # Код возврата
    sys.exit(1 if stats['errors'] else 0)

if __name__ == '__main__':
    main()