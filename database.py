import sqlite3

# データベースを開く
db = sqlite3.connect('faqlist.db')
c = db.cursor()

# テーブル作成
c.execute('create table faq(keyword text, answer text, information text)')

# データ追加（レコード登録）
sql = 'insert into faq(keyword, answer, information) values(?,?,?)'
data = [('配列','タンスです','https://qiita.com/r_otaka/items/a65af9bf5629bcb04a17'),
        ('オブジェクト','クローゼットです','https://qiita.com/r_otaka/items/e7c0d97e170156a95e65')]

c.executemany(sql, data)

# コミット（変更確定）
db.commit()

# データを取得して表示
sql = 'select * from faq'
print('1---------------')
for row in c.execute(sql):
    print(row)

db.close()

# https://www.youtube.com/watch?v=cFY1BNZQ7Xo

# 上書きされず、レコードがどんどん追加されてしまう。DBは作成用の管理画面を別途作ってそこで管理できるようにしたい。MySQLから持ってくるようにしようかな。



