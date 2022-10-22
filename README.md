# tipdetect

## Git インストール

[ここらへん](https://note.com/cd_ss_829/n/n4e7d80723381)を参考にGitをインストールする。

## Githubへの接続設定
以下あたりも参考になります。
[参考](https://qiita.com/shizuma/items/2b2f873a0034839e47ce)
[GitHubで複数アカウントを使い分ける方法](https://www.wakuwakubank.com/posts/380-git-multiple-account/)
[複数のGitHubアカウントを使い分けたい時の設定方法とTips](https://zenn.dev/taichifukumoto/articles/how-to-use-multiple-github-accounts)

### 公開鍵・秘密鍵を作成する

次のコマンドで鍵を生成します。
```
$ cd ~/.ssh
$ ssh-keygen -t rsa
```

```
$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/(username)/.ssh/id_rsa): <= もしすでに鍵がある場合、ここでファイル名を指定する。
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```

2回目、3回目はパラフレーズの設定（パスワード設定のようなもの）ですが、ここはなくてオーケーです。（慣れてきたらパラフレーズの設定もありですが、なくていいでしょう。）

ちなみに、ファイル名を指定しない時は勝手に~/.ssh内に鍵を生成してくれますが、上記のように名前を指定するときは~/.ssh内にいないとこの中に生成してくれないので注意です。

### 公開鍵をGitHubにアップする

[https://github.com/settings/ssh](https://github.com/settings/ssh)

で公開鍵の設定が出来ます。（GitHubに登録していることが前提条件です）


画面右上の「Add SSH key」のボタンを押します。

「title」に公開鍵名、「key」に公開鍵の中身を入れます。

なお、鍵の中身のクリップボードへのコピーは
```
$ pbcopy < ~/.ssh/id_rsa.pub (Mac)
$ clip < ~/.ssh/id_rsa.pub (Windows)
```
*鍵の名前は自分の作成したもの。

### 接続を確かめる

```
$ ssh -T git@github.com
```

以下が帰ってきたら、成功！！

```
Hi (account名)! You've successfully authenticated, but GitHub does not provide shell access.
```

しかし…
鍵を作るときに名前を指定していれば、うまくいかないかもしれません。
それは、ssh接続の際「~/.ssh/id_rsa」、「~/.ssh/id_dsa」、「~/.ssh/identity」しかデフォルトでは見にいかないからです。
それに対応するためには
~/.ssh/configを作成しその中に

```
Host github github.com
  HostName github.com
  IdentityFile ~/.ssh/id_git_rsa #ここに自分の鍵のファイル名
  User git
```
を作成しましょう。
これで、もう一度接続をやってみるとうまくいくはずです。
以下のようにコマンドを打って確かめて見ましょう。



## 作業の最初

- コードのクローン

```
git clone https://github.com/dinov2021pub/tipdetect.git

```

- ローカルでブランチを切る（最初だけ）

```
git checkout -b feature/code-rev
```

- ローカルで仮想環境を作る

```
python venv -m tipdetect

```

- 仮想環境に入る

```
cd tipdetect
source ./bin/activate
```

- 必要なパッケージのインストール

```
pip install -r requirements.txt
```

#####################
- コードの更新
#####################


- リモートリポジトリへpush

```
git add <変更したファイル>
git commit -m "code rev"
git push origin feature/code-rev
```

### うまくいかないとき
以下を順番に見ていきましょう。

1．configファイルある？ 2つのアカウントがあるとして
```

#メインアカウント
Host github #任意のホスト名
  HostName github.com
  IdentityFile ~/.ssh/id_rsa #メインアカウントの鍵のファイル
  User git
  Port 22
  TCPKeepAlive yes
  IdentitiesOnly yes

#サブアカウント
Host github-sub #任意のホスト名
  HostName github.com
  IdentityFile ~/.ssh/id_sub_rsa #サブアカウントの鍵のファイル
  User git
  Port 22
  TCPKeepAlive yes
  IdentitiesOnly yes

```

2．接続を確認する。
```
$ ssh -T github-sub
```
と打つと
```
$ ssh -T github-sub
Hi [サブアカウントのユーザー名]! You've successfully authenticated, but GitHub does not provide shell access.
```

3. アカウントを切り替える
```
$ git config --global user.name "[GitHubアカウント名]"
$ git config --global user.email "[GitHubのメールアドレス]"

```
アカウントが切り替わっているかどうかは
```
git config user.name
git config user.email
```
で確認することができます。

`~/.bashrc` に以下を書いておいても良い
```
function gitmain() {
  git config --global user.name "[メインのGitHubアカウント名]"
  git config --global user.email "[メインのGitHubのメールアドレス]"
}

function gitsub() {
  git config --global user.name "[メインのGitHubアカウント名]"
  git config --global user.email "[メインのGitHubのメールアドレス]"
}
```
コマンドラインから
```
$ gitmain
```
とか打つと切り替えられる。

3. もういっかい、Closeしてみる
```
$ gitsub  # <- ~/.bashrc に書いてある関数
$ git clone git@github-sub:dinov2021pub/qrcode-api.git
```
変更、add, commit, push してみる。

## 次回、作業時

- 仮想環境に入る

```
cd tipdetect
source ./bin/activate
```

- ローカルのコードの変更の更新

```
git checkout main
git branch -d feature/code-rev
git pull origin main
git checkout -d feature/code-rev
```

#####################
- コードの更新
#####################


- リモートリポジトリへpush

```
git add <変更したファイル>
git commit -m "code rev"
git push origin feature/code-rev
```

不明点は遠慮なく聞いてください。

## 途中までの結果は、こちらに保存されている。　（2022年6月23日）
[https://drive.google.com/drive/u/0/folders/1WcOykUBFo1ooh83qFKuc0nNUhwTcQEu_
](https://drive.google.com/drive/u/0/folders/1WcOykUBFo1ooh83qFKuc0nNUhwTcQEu_)

