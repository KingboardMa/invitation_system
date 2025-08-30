#!/usr/bin/env python3
"""
邀请码导入工具

使用方法:
python -m cli.import_codes --offer fellou --file codes.txt
"""

import click
import sys
import os
from pathlib import Path
from tqdm import tqdm

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import SessionLocal, create_tables
from models.offer import Offer
from services.code_service import CodeService
from services.offer_service import OfferService

def read_codes_from_file(file_path: str) -> list[str]:
    """从文件读取邀请码"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            codes = [line.strip() for line in f if line.strip()]
        return codes
    except FileNotFoundError:
        click.echo(f"❌ 文件不存在: {file_path}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ 读取文件失败: {str(e)}", err=True)
        sys.exit(1)

@click.command()
@click.option('--offer', '-o', required=True, help='Offer名称，如: fellou')
@click.option('--file', '-f', required=True, help='邀请码文件路径')
@click.option('--title', '-t', help='Offer显示标题（仅在创建新offer时使用）')
@click.option('--description', '-d', help='Offer描述（仅在创建新offer时使用）')
def main(offer: str, file: str, title: str = None, description: str = None):
    """导入邀请码到指定的offer"""

    # 确保数据库表已创建
    create_tables()

    # 检查文件是否存在
    if not os.path.exists(file):
        click.echo(f"❌ 文件不存在: {file}", err=True)
        sys.exit(1)

    # 读取邀请码文件
    click.echo(f"📖 正在读取文件: {file}")
    codes = read_codes_from_file(file)

    if not codes:
        click.echo("❌ 文件中没有找到有效的邀请码", err=True)
        sys.exit(1)

    click.echo(f"✅ 发现 {len(codes)} 个邀请码")

    # 数据库操作
    db = SessionLocal()
    try:
        offer_service = OfferService(db)
        code_service = CodeService(db)

        # 检查offer是否存在，不存在则创建
        existing_offer = offer_service.get_offer_by_name(offer)
        if not existing_offer:
            if not title:
                title = f"{offer.title()} 邀请码"
            if not description:
                description = f"{offer} 项目的邀请码发放"

            click.echo(f"🆕 创建新的offer: {offer}")
            offer_service.create_offer(offer, title, description)
        else:
            click.echo(f"📂 使用现有offer: {offer}")

        # 导入邀请码
        click.echo(f"⬆️  正在导入邀请码到offer: {offer}")

        # 使用进度条显示导入过程
        with tqdm(total=len(codes), desc="导入进度", unit="码") as pbar:
            batch_size = 100  # 批量处理
            new_codes_total = 0
            duplicate_codes_total = 0

            for i in range(0, len(codes), batch_size):
                batch_codes = codes[i:i+batch_size]
                try:
                    result = code_service.import_codes(offer, batch_codes)
                    new_codes_total += result["new_codes"]
                    duplicate_codes_total += result["duplicate_codes"]
                except Exception as e:
                    click.echo(f"\n❌ 导入批次失败: {str(e)}", err=True)
                    continue

                pbar.update(len(batch_codes))

        # 显示结果
        click.echo(f"\n🎉 导入完成!")
        click.echo(f"   新增邀请码: {new_codes_total}")
        click.echo(f"   重复跳过: {duplicate_codes_total}")
        click.echo(f"   处理总数: {len(codes)}")

        # 显示最新统计
        updated_offer = offer_service.get_offer_by_name(offer)
        if updated_offer:
            click.echo(f"\n📊 Offer '{offer}' 最新统计:")
            click.echo(f"   总邀请码: {updated_offer.total_count}")
            click.echo(f"   剩余数量: {updated_offer.remaining_count}")
            click.echo(f"   已使用: {updated_offer.total_count - updated_offer.remaining_count}")

    except Exception as e:
        click.echo(f"❌ 导入过程中发生错误: {str(e)}", err=True)
        sys.exit(1)

    finally:
        db.close()

if __name__ == '__main__':
    main()
