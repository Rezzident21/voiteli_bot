import requests
from bs4 import BeautifulSoup
import random
from time import sleep
import datetime
import json


class Voiteli:
    def __init__(self, login, password):
        self.url = 'https://voiteli.mobi/'
        self.login = login
        self.password = password
        self.s = requests.Session()

    def auth(self):
        soup = BeautifulSoup(self.s.get(self.url).text, 'html.parser')

        data = {"aut[login]": self.login, "aut[password]": self.password}

        self.s.post(self.url, data=data, headers=dict(Referer=self.url))  # Send post auth

    def get_count_of_battles(self, location):  # Get fuel
        soup = BeautifulSoup(self.s.get(self.url + location).text, 'html.parser')
        battles = soup.find('span', attrs={'class': 'title__info'}).text
        try:
            battles = int(battles.split('/')[-2])
        except IndexError:
            battles = 0
        return battles

    def hunt(self):
        print('Available battles: {}'.format(self.get_count_of_battles('hunt')))

        if self.get_count_of_battles('hunt') > 0:
            while self.get_count_of_battles('hunt') > 0:
                soup = BeautifulSoup(self.s.get(self.url + 'hunt').text, 'html.parser')
                get_link_battle = soup.find('a', attrs={'class': 'btn'}, href=True)['href']
                print(self.s.post(self.url + 'hunt/' + get_link_battle).url)
                sleep(1)
        else:
            print("Out of available get_count_hunt")

    def dungeon(self):
        dung_id = 3
        link_dung = 'dung/list/?dung_id={}'.format(dung_id)
        print('Available battles: {}'.format(self.get_count_of_battles(link_dung)))
        count_of_battles = self.get_count_of_battles(link_dung)
        loc_id = random.randint(12, 15)

        if count_of_battles > 0:
            self.s.post(self.url + link_dung + '&loc_id=' + str(loc_id))

            self.dungeon_fight()

        else:
            print("Out of available get_count_dung")

    def dungeon_fight(self):

        soup = BeautifulSoup(self.s.get(self.url + 'dung/fight/').text, 'html.parser')
        try:
            text = soup.find('a', attrs={'class': 'btn'}).text

            if text == 'Ударить':
                get_link_battle = soup.find('a', attrs={'class': 'btn'}, href=True)['href']
                print('Ударить противника')
                self.s.post(self.url + 'dung/fight' + get_link_battle)
                sleep(1)
                self.dungeon_fight()
            elif text == 'Завершить':
                self.s.post(self.url + 'dung/fight/?complete')
                print('Завершить бой')
                self.dungeon()

        except Exception as e:
            print(e)

    def arena(self):
        soup = BeautifulSoup(self.s.get(self.url + 'arena/').text, 'html.parser')
        battles = soup.findAll('span', attrs={'class': 'arena_points'})[1].text
        daily_point_arena = int(battles.split('из')[0])
        max_point_arena = int(battles.split('из')[1])

        print('Arena: {} of {}'.format(daily_point_arena, max_point_arena))
        if daily_point_arena < max_point_arena:
            self.s.post(self.url + 'arena/?fight')

            self.arena_fight()
        else:
            print('Arena isnt avaiable today')

    def arena_fight(self):
        soup = BeautifulSoup(self.s.get(self.url + 'arena/fight/').text, 'html.parser')
        try:
            text = soup.find('a', attrs={'class': 'btn'}).text

            if text == 'Ударить':
                get_link_battle = soup.find('a', attrs={'class': 'btn'}, href=True)['href']
                print('Ударить противника')
                self.s.post(self.url + 'arena/fight' + get_link_battle)
                sleep(1)
                self.arena_fight()
            elif text == 'Завершить':
                self.s.post(self.url + 'arena/fight/?complete')
                print('Завершить бой')
                self.arena()
        except Exception as e:
            print(e)
            print('Error in arena fight')

    def task(self):
        soup = BeautifulSoup(self.s.get(self.url + 'task/').text, 'html.parser')
        link_task = soup.find('div', attrs={'class': 'tasks'})
        try:
            get_link_task = link_task.find('a', attrs={'class': 'btn'}, href=True)['href']
            self.s.post(self.url + 'task/' + get_link_task)
            sleep(1)
            self.task()
            print(get_link_task)
        except Exception as e:
            print('Доступные задания завершены')

    def run(self):
        while True:
            try:
                self.auth()

            except AttributeError:
                print('Auth is not successfully')
                exit()
            self.task()
            self.arena()
            self.hunt()
            self.dungeon()

            print("Бот завершить работу до запуска 2 часа")
            sleep(7200)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    with open('account.json') as json_load_accounts:
        accounts = json.load(json_load_accounts)
    try:

        for account in accounts:
            w = Voiteli(account['login'], account['password'])
            w.run()
    except Exception as e:
        print(e)
        print('Ошибка в логине или пароле')
