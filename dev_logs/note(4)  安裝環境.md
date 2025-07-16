### 📄 `requirements.txt` 是什麼？

它是一個 **純文字檔案**，裡面列出所有你專案需要的 Python 套件和版本，例如：

```
numpy==1.25.0
pandas>=1.5.0
requests
```

每一行是一個套件（可以指定版本），像這樣：

| 格式        | 說明      |
| --------- | ------- |
| `套件名`     | 安裝最新版   |
| `套件名==版本` | 指定版本    |
| `套件名>=版本` | 安裝該版本以上 |

---

`requirements.txt` 通常會放在 **專案根目錄**（專案的最外層資料夾），這是 Python 社群的慣例與最佳實踐。

---

### 🗂 常見的專案結構範例：

```
my_project/
├── requirements.txt       ← ✅ 就放這裡
├── main.py
├── some_module/
│   └── __init__.py
└── README.md
```

---

### 🚀 用法總結

1. 建立 `requirements.txt`：

   ```bash
   pip freeze > requirements.txt
   ```

2. 之後別人要跑你的程式，只要在虛擬環境中執行：

   ```bash
   pip install -r requirements.txt
   ```

   所有套件就會自動安裝完成。

---

### ✅ 小提醒

你可以在 `README.md` 裡加一句說明，像：

````md
## 安裝方法

```bash
pip install -r requirements.txt
````

```

---
