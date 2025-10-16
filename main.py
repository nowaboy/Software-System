import json
import os
from datetime import datetime

class ContactManager:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = self.load_contacts()
    
    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_contacts(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.contacts, f, ensure_ascii=False, indent=2)
    
    def add_contact(self, name, phone, email='', address=''):
        contact = {
            'id': len(self.contacts) + 1,
            'name': name,
            'phone': phone,
            'email': email,
            'address': address,
            'created': datetime.now().isoformat()
        }
        self.contacts.append(contact)
        self.save_contacts()
        return contact
    
    def delete_contact(self, contact_id):
        self.contacts = [c for c in self.contacts if c['id'] != contact_id]
        self.save_contacts()
    
    def search_contacts(self, query):
        query = query.lower()
        results = []
        for contact in self.contacts:
            if (query in contact['name'].lower() or 
                query in contact['phone'] or 
                query in contact.get('email', '').lower()):
                results.append(contact)
        return results
    
    def update_contact(self, contact_id, **kwargs):
        for contact in self.contacts:
            if contact['id'] == contact_id:
                for key, value in kwargs.items():
                    if key in contact:
                        contact[key] = value
                self.save_contacts()
                return contact
        return None
    
    def list_all(self):
        return self.contacts

def main():
    manager = ContactManager()
    
    while True:
        print("\n=== Менеджер Контактов ===")
        print("1. Добавить контакт")
        print("2. Удалить контакт")
        print("3. Поиск контакта")
        print("4. Показать все контакты")
        print("5. Обновить контакт")
        print("6. Выход")
        
        choice = input("\nВыберите действие: ")
        
        if choice == '1':
            name = input("Имя: ")
            phone = input("Телефон: ")
            email = input("Email (необязательно): ")
            address = input("Адрес (необязательно): ")
            contact = manager.add_contact(name, phone, email, address)
            print(f"Контакт добавлен с ID: {contact['id']}")
        
        elif choice == '2':
            contact_id = int(input("ID контакта для удаления: "))
            manager.delete_contact(contact_id)
            print("Контакт удален")
        
        elif choice == '3':
            query = input("Поиск: ")
            results = manager.search_contacts(query)
            if results:
                for contact in results:
                    print(f"\nID: {contact['id']}")
                    print(f"Имя: {contact['name']}")
                    print(f"Телефон: {contact['phone']}")
                    print(f"Email: {contact.get('email', 'Не указан')}")
            else:
                print("Контакты не найдены")
        
        elif choice == '4':
            contacts = manager.list_all()
            if contacts:
                for contact in contacts:
                    print(f"\nID: {contact['id']} | {contact['name']} | {contact['phone']}")
            else:
                print("Список контактов пуст")
        
        elif choice == '5':
            contact_id = int(input("ID контакта: "))
            field = input("Поле для обновления (name/phone/email/address): ")
            value = input("Новое значение: ")
            updated = manager.update_contact(contact_id, **{field: value})
            if updated:
                print("Контакт обновлен")
            else:
                print("Контакт не найден")
        
        elif choice == '6':
            break
        
        else:
            print("Неверный выбор")

if __name__ == '__main__':
    main()
