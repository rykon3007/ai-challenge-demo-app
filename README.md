# python-tool-template
--
DevContainerを使って簡単にPythonでツール環境が用意できるリポジトリ
モノレポは考慮されていない

## 前提条件
- Docker Desktopがインストールされていること
- Visual Studio Codeがインストールされていること
- Visual Studio CodeにRemote - Containers拡張機能がインストールされていること  

## 手順

※この手順を始める前に実施すること
- Docker Desktopの起動（Dockerの起動）が必要

### Step 1: リポジトリのクローン（GitHub Desktopを使用）

GitHub Desktopを開き、「File」メニューから「Clone Repository」を選択します。

「URL」タブをクリックし、クローンしたいリポジトリのURLを入力します。次に、リポジトリを保存するローカルパスを選択し、「Clone」ボタンをクリックします。

クローニングが完了したら、GitHub Desktop上で「Open in Visual Studio Code」ボタンをクリックして、クローンしたリポジトリをVS Codeで開きます。

### Step 2: DevContainerの設定を確認

クローンしたリポジトリのルートディレクトリに`.devcontainer`ディレクトリが含まれていることを確認してください。このディレクトリには、`devcontainer.json`ファイルとDockerfileが含まれている必要があります。

### Step 3: Visual Studio Codeで開く

VS Codeが自動的に開かない場合は、Visual Studio Codeを開き、「ファイル」メニューから「フォルダーを開く...」を選択し、クローンしたリポジトリのルートディレクトリを選択します。

### Step 4: Remote - Containers拡張機能を使用して開く

左下の緑色の「><」アイコン（もしくは左下隅にある「リモートウィンドウを開く」アイコン）をクリックし、「Reopen in Container」を選択します。これにより、DevContainerの構築プロセスが開始されます。

### Step 5: コンテナの起動を待つ

DevContainerのビルドと起動が完了するまで数分かかる場合があります。プロセスが完了すると、VS Codeは自動的にコンテナ内の環境に接続し、コンテナ内で作業ができるようになります。

## おわりに

これで、DevContainerを使用した開発環境のセットアップが完了しました。この環境内で、コードの編集、実行、デバッグを行うことができます。何か問題が発生した場合は、コンテナの再起動や再ビルドを試みてください。
