# 1. 簡介
###此程式使用**Python3.10**，為簡易虛擬後端功能，包含基本CRUD
###使用方法：開啟**run.sh**或是執行**app.py**即可在 命令列中輸入下方功能指令。

# 2. 功能及範例
###資料包含四個類別 *User*、*Folder*、*File*、*Label*，並提供使用者新增、修改以及刪除。

###User：使用此後端系統的人員，使用者名稱為唯一且大小寫不拘，能夠任意新增Folder等其他類別。

###相關功能：

1.將人員新增至系統
`register {username}`


###Folder：存放File的地方，名稱為唯一且大小寫不拘，能夠任意新增/刪除/重新命名。

###相關功能：

1.新增資料夾
`create_folder {username} {folder_name} {description}`
2.刪除已存在的資料夾
`delete_folder {username} {folder_id}`
3.獲取當前使用者的所有資料夾
`get_folders {username} {label_name} {sort_name | sort_time} {asc|dsc}`
4.為資料夾重新命名
`rename_folder {username} {folder_id} {new_folder_name}`


###File：基礎資料，名稱為唯一且大小寫需相同，並且必須包含附檔名。可供上傳/刪除/獲取檔案。

###相關功能：

1.將檔案上傳至對應資料夾
`upload_file {username} {folder_id} {file_name} {description}`
2.在對應資料夾中刪除檔案
`delete_file {username} {folder_id} {file_name}`
3.獲取使用者的特定資料夾中所有檔案
`get_files {username} {folder_id} {sort_name|sort_time|sort_extension} {asc|dsc}`


###Label：用於將資料夾分類，可供新增/刪除/新增類至資料夾/從資料夾移除類。

###相關功能：

1.新增類別
`add_label {username} {label_name} {color}`
2.獲取使用者的所有類別
`get_labels {username}`
3.刪除特定類別
`delete_labels {username} {label_name}`
4.將資料夾放入特定類別
`add_folder_label {username} {folder_id} {label_name}`
5.將資料夾從特定類別中刪除
`delete_folder_label {username} {folder_id} {label_name}`

# 3.API說明
####user 僅包含現有的 user 名稱，以 Dict 存放。
####folder 包含 id、label、name、description、created_at、username，以 Dict 存放。
####file 包含 id、name、extension、description、created_at、username，以 Dict 存放。
####label 包含 id、name、color、created_at、username，以 Dict 存放。

各Function功能及用法對應功能的指令，除了以下
```python
#將CLI指令初始化
def Init()
```

```python
#根據輸入執行特定功能
def action()
```

```python
#輸入字串處理
def InputSplit()
```

```python
#大小不拘的比對是否存在字典中
def compareStrIsInDicWithCaseInsensitive()
```

```python
#比對是否存在字典中
def compareStrIsInDicWithCaseSsensitive()
```


# 4. 注意事項與限制
####功能皆在CRUD.py中，若未來修改特定功能僅需到特定Function中修改，不需整體修改，新增功能除了功能Function外還需要在CRUD.Init中新增對應指令。
