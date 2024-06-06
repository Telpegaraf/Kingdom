import os


def delete_migrations():
    for root, dirs, files in os.walk("apps/"):
        for file in files:
            if file.endswith(".py") and "migrations" in root and file != "__init__.py":
                path = os.path.join(root, file)
                try:
                    os.remove(path)
                    print(f"Удалено: {path}")
                except Exception as e:
                    print(f"Ошибка при удалении {path}: {e}")


if __name__ == "__main__":
    delete_migrations()
