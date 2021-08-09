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

    def free_chest(self):
        soup = BeautifulSoup(self.s.get(self.url + 'shop/chest/view/?chest_id=1').text, 'html.parser')
        text_free_chest = soup.find('span', attrs={'class': 'ok'}).text
        print(text_free_chest)
        if text_free_chest:
            get_link_open_chest = soup.find('a', attrs={'class': 'btn'}, href=True)['href']
            print(get_link_open_chest)
            self.s.post(self.url + 'shop/chest/view/' + get_link_open_chest)

    def boss(self):
        soup = BeautifulSoup(self.s.get(self.url + 'boss').text, 'html.parser')
        main_div_boss_farm = soup.find('div', attrs={'class': 'boss-farm'})
        link_boss_farm = main_div_boss_farm.find('div', attrs={'class': 'menu'})
        link_boss_farm3 = link_boss_farm.findAll('li', attrs={'class': 'menu__item menu__item_size_l'})

        for link in link_boss_farm3:
            try:
                href = link.find('a', attrs={'class': 'menu__link'}, href=True)['href']
                self.s.post(self.url + 'boss/'+ href)
                self.boss_fight()
            except:
                pass
    def boss_fight(self):
        soup = BeautifulSoup(self.s.get(self.url + 'boss/fight/').text, 'html.parser')
        try:
            text = soup.find('a', attrs={'class': 'btn'}).text

            if text == 'Ударить':
                get_link_battle = soup.find('a', attrs={'class': 'btn'}, href=True)['href']
                print('Ударить противника')
                self.s.post(self.url + 'boss/fight' + get_link_battle)
                sleep(1)
                self.boss_fight()
            elif text == 'Завершить':
                self.s.post(self.url + 'boss/fight/?complete')
                print('Завершить бой')
                self.boss()
        except Exception as e:
            print(e)
            print('Error in boss fight')

    def run(self):
        while True:
            try:
                self.auth()

            except AttributeError:
                print('Auth is not successfully')
                exit()
            try:
                self.boss()
            except Exception as e:
                print('Ошибка в босс')
            try:
                self.free_chest()
            except Exception as e:
                print('Бесплатный сундук уже открыт')
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
