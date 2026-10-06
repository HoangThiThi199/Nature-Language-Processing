import wikipedia
import os
import requests
import shutil
import time
from datetime import timedelta


# ============================================================
# PROBLEM SET 3
# PROBLEM 1 - CREATE DATASET
# ============================================================


# ============================================================
# 1. DANH SÁCH 50 BÀI WIKIPEDIA
# ============================================================

articles = [

    # =========================
    # SCIENCE
    # =========================
    "Artificial intelligence",
    "Physics",
    "Biology",
    "Chemistry",
    "Computer science",
    "Mathematics",
    "Astronomy",
    "Genetics",
    "Quantum mechanics",
    "Evolution",

    # =========================
    # POLITICS
    # =========================
    "Politics",
    "Democracy",
    "Government",
    "Election",
    "Political party",
    "Parliament",
    "International relations",
    "United Nations",
    "Donald Trump",
    "Political science",

    # =========================
    # NATURE
    # =========================
    "Forest",
    "Ocean",
    "Mountain",
    "River",
    "Climate change",
    "Rainforest",
    "Desert",
    "Volcano",
    "Natural environment",
    "Earth",

    # =========================
    # SPORT
    # =========================
    "Football",
    "Basketball",
    "Tennis",
    "Cricket",
    "Baseball",
    "Volleyball",
    "Swimming",
    "Boxing",
    "Golf",
    "Athletics",

    # =========================
    # FASHION
    # =========================
    "Fashion",
    "Clothing",
    "Dress",
    "Textile",
    "Jeans",
    "T-shirt",
    "Shoe",
    "Handbag",
    "Fashion design",
    "Fashion industry"
]


# ============================================================
# 2. KIỂM TRA SỐ LƯỢNG BÀI
# ============================================================

print("Number of articles:", len(articles))

if len(articles) != 50:
    print("ERROR: The dataset must contain exactly 50 articles.")
    exit()


# ============================================================
# 3. XÁC ĐỊNH THƯ MỤC PROJECT
# ============================================================

# __file__ = đường dẫn đến file problem_set_3.py
#
# Ví dụ:
# D:/Nature-Language-Processing/
#     Problem_set_3_Word_Embedding/
#         problem_set_3.py
#
# os.path.dirname(...) sẽ lấy:
# D:/Nature-Language-Processing/Problem_set_3_Word_Embedding

project_folder = os.path.dirname(
    os.path.abspath(__file__)
)

print("Project folder:", project_folder)


# ============================================================
# 4. TẠO THƯ MỤC DATA
# ============================================================

# Data sẽ nằm bên trong folder chứa problem_set_3.py

data_folder = os.path.join(
    project_folder,
    "Data"
)

os.makedirs(data_folder, exist_ok=True)

print("Data folder:", data_folder)


# ============================================================
# 5. CẤU HÌNH WIKIPEDIA
# ============================================================

# Sử dụng Wikipedia tiếng Anh
wikipedia.set_lang("en")
wikipedia.set_rate_limiting(True, min_wait=timedelta(seconds=1))


# ============================================================
# 6. TẢI 50 BÀI WIKIPEDIA
# ============================================================

success = 0
max_attempts = 3

for i, article_title in enumerate(articles, start=1):

    print(f"\n[{i}/{len(articles)}] Downloading: {article_title}")

    filename = f"{i} - {article_title}.txt"
    filepath = os.path.join(data_folder, filename)

    if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
        success += 1
        print("    Already downloaded; skipping:", filename)
        continue

    page = None

    for attempt in range(1, max_attempts + 1):
        try:
            page = wikipedia.page(
                article_title,
                auto_suggest=False
            )
            break
        except (
            wikipedia.exceptions.PageError,
            wikipedia.exceptions.DisambiguationError,
            wikipedia.exceptions.RedirectError,
        ) as error:
            print("    ERROR:", article_title)
            print("    Reason:", error)
            break
        except (
            wikipedia.exceptions.HTTPTimeoutError,
            requests.exceptions.RequestException,
        ) as error:
            if attempt == max_attempts:
                print("    ERROR:", article_title)
                print(f"    Failed after {max_attempts} attempts:", error)
            else:
                wait_seconds = 2 ** attempt
                print(
                    f"    Temporary download error "
                    f"(attempt {attempt}/{max_attempts}); "
                    f"retrying in {wait_seconds} seconds..."
                )
                time.sleep(wait_seconds)

    if page is None:
        continue

    temp_filepath = filepath + ".tmp"
    with open(temp_filepath, "w", encoding="utf-8") as file:
        file.write(page.content)
    os.replace(temp_filepath, filepath)

    success += 1
    print("    Saved:", filename)


# ============================================================
# 7. KIỂM TRA KẾT QUẢ
# ============================================================

print("\n" + "=" * 60)
print("DATASET CREATION RESULT")
print("=" * 60)

print(f"Available articles: {success}/{len(articles)}")


# ============================================================
# 8. TẠO DATA.ZIP
# ============================================================

if success > 0:
    zip_path = os.path.join(
        project_folder,
        "Data"
    )

    shutil.make_archive(
        zip_path,
        "zip",
        root_dir=project_folder,
        base_dir="Data"
    )

    archive_path = f"{zip_path}.zip"
    if success == len(articles):
        print(f"\nData.zip created successfully: {archive_path}")
    else:
        print(
            f"\nPartial Data.zip created: {archive_path} "
            f"({success}/{len(articles)} articles)."
        )

else:

    print("\nData.zip was NOT created because no articles are available.")


# ============================================================
# 9. KẾT THÚC
# ============================================================

print("\n" + "=" * 60)
print("PROBLEM 1 COMPLETED")
print("=" * 60)