import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


# ============================================================
# PROBLEM 2
# TERM-DOCUMENT MATRIX
# ============================================================


# ============================================================
# 1. XÁC ĐỊNH THƯ MỤC PROJECT
# ============================================================

project_folder = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# 2. XÁC ĐỊNH THƯ MỤC DATA
# ============================================================

data_folder = os.path.join(
    project_folder,
    "Data"
)


# ============================================================
# 3. ĐỌC 50 FILE TEXT
# ============================================================

documents = []
document_names = []

for filename in sorted(os.listdir(data_folder)):

    # Chỉ lấy file .txt
    if filename.endswith(".txt"):

        filepath = os.path.join(
            data_folder,
            filename
        )

        # Đọc nội dung file
        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        documents.append(text)
        document_names.append(filename)

print("Number of documents:", len(documents))


# ============================================================
# 4. TẠO TERM-DOCUMENT MATRIX
# ============================================================

vectorizer = CountVectorizer()

matrix = vectorizer.fit_transform(documents)


# ============================================================
# 5. LẤY DANH SÁCH TERM
# ============================================================

terms = vectorizer.get_feature_names_out()


# ============================================================
# 6. CHUYỂN MATRIX THÀNH DATAFRAME
# ============================================================

td_matrix = pd.DataFrame(
    matrix.toarray(),
    index=terms,
    columns=document_names
)


# ============================================================
# 7. ĐẶT TÊN CHO CỘT TERM
# ============================================================

td_matrix.index.name = "term"


# ============================================================
# 8. LƯU THÀNH TD.csv
# ============================================================

output_path = os.path.join(
    project_folder,
    "TD.csv"
)

td_matrix.to_csv(
    output_path,
    encoding="utf-8"
)


# ============================================================
# 9. HIỂN THỊ KẾT QUẢ
# ============================================================

print("Term-document matrix created.")
print("Matrix shape:", td_matrix.shape)
print("Saved to:", output_path)