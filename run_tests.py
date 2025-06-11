#!/usr/bin/env python3
"""
テスト実行スクリプト
"""

import sys
import unittest
from pathlib import Path

# プロジェクトルートを Python パスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_all_tests():
    """全てのテストを実行"""
    print("=== メンターエージェント テスト実行 ===\n")
    
    # テストディスカバリー
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 結果サマリー
    print(f"\n=== テスト結果サマリー ===")
    print(f"実行されたテスト数: {result.testsRun}")
    print(f"失敗: {len(result.failures)}")
    print(f"エラー: {len(result.errors)}")
    
    if result.failures:
        print("\n失敗したテスト:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nエラーが発生したテスト:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    # 成功判定
    if result.wasSuccessful():
        print("\n✅ 全てのテストが成功しました!")
        return True
    else:
        print("\n❌ テストに失敗がありました。")
        return False


def run_specific_test(test_name):
    """特定のテストを実行"""
    print(f"=== 特定テスト実行: {test_name} ===\n")
    
    suite = unittest.TestSuite()
    
    try:
        # テストクラスを動的にインポート
        module_name = f"tests.{test_name}"
        module = __import__(module_name, fromlist=[test_name])
        
        # テストクラスを探して追加
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, unittest.TestCase):
                suite.addTest(unittest.makeSuite(attr))
        
        # テスト実行
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"エラー: テストモジュール '{test_name}' が見つかりません: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 特定のテストを実行
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # 全てのテストを実行
        success = run_all_tests()
    
    # 終了コード
    sys.exit(0 if success else 1)