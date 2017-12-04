#動作環境
・RaspberryPi3 model B
・python3.x

#インストール手順
・本ディレクトリをraspberrypi上に配置する
・インターネットに接続可能な状態で以下コマンドを実行し、必要なライブラリをインストール
　$ pip install -r requirements.txt

#実行
$ python <配置ディレクトリ>/xxxxxx.py

※systemdへの登録を推奨


#スクリプト概要
・environmental_info_reporter.py
　　iRemoconから取得した温度,湿度,照度をプラットフォームにアップロードする
・ir_command_forwarder.py
　　プラットフォームからMQTT経由で送信された信号をiRemoconに転送する常駐スクリプト
・iremocon_util.py
　　各スクリプトで利用する共有ライブラリ
　　iRemoconのI/F部分の機能を提供
・onem2m_util.py
　　各スクリプトで利用する共有ライブラリ
　　oneM2Mの仕様に関するユーティリティ機能を提供


