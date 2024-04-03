import io

with io.open('fixtures/test_db.json', 'r', encoding='windows-1251') as source_file:
    data = source_file.read()

with io.open('fixtures/test_db.json', 'w', encoding='utf-8') as target_file:
    target_file.write(data)
