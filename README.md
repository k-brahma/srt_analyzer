# SRT Vocabulary Extractor

このプロジェクトは、SRTファイルから高度な表現や語彙を抽出し、分析レポートを生成するツールです。Anthropic APIを使用して、テキストセグメントを分析し、表現の意味や使用例を提供します。

## 機能

- SRTファイルからテキストとタイムスタンプを抽出
- 各セグメントを分析し、重要な表現を特定
- 分析結果をMarkdown形式でレポート生成

## 必要条件

- Python 3.x
- `anthropic` ライブラリ
- `pydantic` ライブラリ
- `dotenv` ライブラリ

## セットアップ

1. リポジトリをクローンします。

   ```bash
   git clone https://github.com/k-brahma/srt_analyzer.git
   cd srt_analyzer
   ```

2. 必要なPythonパッケージをインストールします。

   ```bash
   pip install -r requirements.txt
   ```

3. `.env` ファイルを作成し、Anthropic APIキーを設定します。

   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## 使用方法

1. SRTファイルを用意し、`data/srt_sample.srt` のようにパスを指定します。

2. スクリプトを実行して、レポートを生成します。

   ```bash
   python main.py
   ```

3. 結果のレポートは `results/srt_report.md` に保存されます。

## ファイル構成

- `main.py`: メインスクリプト。SRTファイルを処理し、レポートを生成します。
- `requirements.txt`: 必要なPythonパッケージのリスト。
- `data/`: SRTファイルを保存するディレクトリ。
- `results/`: 生成されたレポートを保存するディレクトリ。

## 注意事項

- このツールは、Anthropic APIを使用してテキストを分析します。APIキーが必要です。
- SRTファイルのフォーマットが正しくない場合、正しく解析できないことがあります。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。