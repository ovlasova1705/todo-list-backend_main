from typing import List

import os

import json
import os


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def __str__(self):
        return self.title

    def print_entries(self, indent=0):
        print_with_indent(self.title, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        entries = []
        for entry in self.entries:
            entries.append(entry.json())
        return {
            "title": self.title,
            "entries": entries
        }

    def save(self, path):
        filename = os.path.join(path, f"{self.title}.json")
        with open(filename, "w") as f:
            json.dump(self.json(), f)

    @classmethod
    def from_json(cls, value):
        title = value['title']
        entries = []
        for entry in value.get('entries', []):
            entries.append(cls.from_json(entry))
        return cls(title, entries)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:
            content = json.load(file)
        return cls.from_json(content)


def print_with_indent(value, indent=0):
    print('\t' * indent + str(value))

# entry = {"title": "Дела по дому", "entries": []}
# category = Entry.from_json(entry)

# category.print_entries()

# def entry_from_json(data):
#     entry = Entry(data['title'])
#     for subentry in data['entries']:
#         entry.add_entry(entry_from_json(subentry))
#     return entry

# grocery_list = {
#   "title": "Продукты",
#   "entries": [
#     {
#       "title": "Молочные",
#       "entries": [
#         {
#           "title": "Йогурт",
#           "entries": []
#         },
#         {
#           "title": "Сыр",
#           "entries": []
#         }
#       ]
#     }
#   ]
# }

# entry = entry_from_json(grocery_list)
# entry.print_entries()

# category = Entry('Еда')

# category.add_entry(Entry('Морковь'))
# category.add_entry(Entry('Капуста'))

# print(category.json())
# Зададим список продуктов с двумя уровнями вложенности
# groceries = Entry('Продукты')
# category = Entry('Мясное')

# category.add_entry(Entry('Курица'))
# category.add_entry(Entry('Говядина'))
# category.add_entry(Entry('Колбаса'))

# groceries.add_entry(category)

# groceries.print_entries()

# print_with_indent('test')
# print_with_indent('test', indent=2)
# print_with_indent('test', indent=3)

class EntryManager:
    def __init__(self, data_path: str, entries: List[Entry] = []):
        self.data_path = data_path
        self.entries = entries

    def save(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for filename in os.listdir(self.data_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_path, filename)
                entry = Entry.load(filepath)
                self.entries.append(entry)

    def add_entry(self, title: str):
        entry = Entry(title)
        self.entries.append(entry)
        entry.parent = self
