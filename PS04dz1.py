# Напишите программу, с помощью которой можно искать информацию на Википедии с помощью консоли.
#
# 1. Спрашивать у пользователя первоначальный запрос.
#
# 2. Переходить по первоначальному запросу в Википедии.
#
# 3. Предлагать пользователю три варианта действий:
#
# а) листать параграфы текущей статьи;

# б) перейти на одну из связанных страниц — и снова выбор из двух пунктов:
# - листать параграфы статьи;
# - перейти на одну из внутренних статей.
#
# в) выйти из программы.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def print_paragraphs(page, start_paragraph=0):
   paragraphs = page.text.split('\n\n')
   for i in range(start_paragraph, len(paragraphs)):
       print(f"Параграф {i+1}:\n{paragraphs[i]}\n")
       cont = input("Хотите продолжить листать параграфы? (Да/Нет)\n")
       if cont.lower() != 'да':
           return i + 1
   return len(paragraphs)

def show_links(page):
   links = page.links.keys()
   links_list = list(links)
   for i, link in enumerate(links_list):
       print(f"{i+1}. {link}")
   return links_list

def main():
   initial_query = input("Введите ваш запрос: ")
   answer = initial_query

   browser = webdriver.Chrome()

   browser.get("https://ru.wikipedia.org/wiki/" + initial_query)
   time.sleep(5)

   action = ''
   last_paragraph = 0
   while action != 'в':
       print("\nВыберите действие:")
       print("а) Листать параграфы текущей статьи")
       print("б) Перейти на одну из связанных страниц")
       print("в) Выйти из программы")
       action = input().strip().lower()

       if action == 'а':
           # Вывод параграфов
           paragraphs = browser.find_elements(By.TAG_NAME, "p")

           for i, paragraph in enumerate(paragraphs, start=1):
               print(f"Параграф {i}:\n{paragraph.text}\n")
               cont = input("Хотите продолжить листать параграфы? (Да/Нет)\n")
               if cont.lower() != 'да':
                   break

       elif action == 'б':
           links = browser.find_elements(By.TAG_NAME, "a")
           links_list = [link.get_attribute("href") for link in links]
           for i, link in enumerate(links_list, start=1):
               print(f"{i}. {link}")

           link_choice = int(input("Введите номер ссылки для перехода: ")) - 1

           if 0 <= link_choice < len(links_list):
               browser.get(links_list[link_choice])
           else:
               print("Неверный выбор ссылки.")
       elif action == 'в':
           print("Спасибо за использование программы!")
       else:
           print("Неверный выбор. Пожалуйста, выберите а, б или в.")

if __name__ == "__main__":
   main()