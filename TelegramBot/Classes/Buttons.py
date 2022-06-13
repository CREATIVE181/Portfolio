from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Buttons:
    def __init__(self, conn, cursor, table_name):
        self.col_names = (table_name, [i[0] for i in (conn.execute(f"SELECT * from {table_name}")).description])
        self.c = [conn, cursor]
        self.db = self.c[1].execute(f'SELECT {self.col_names[1][0]}, {self.col_names[1][1]}, {self.col_names[1][2]} FROM {self.col_names[0]}').fetchall()
        self.users = {}
        self.pages = [self.db[i:i + 4] for i in range(0, len(self.db), 4)]
        self.pages_len = len(self.pages)

    def page_default(self, user_id):
        if user_id in self.users:
            self.users[user_id] = [0, 1]
        else:
            self.users.update({user_id: [0, 1]})
        page_ind, page_numb = self.users[user_id]
        try:
            page_now = self.pages[page_ind]
        except IndexError:
            page_now = []
            self.pages_len = 1
            for _ in range(4):
                page_now.append(('❌', '❌', '❌', '❌'))
        if len(page_now) != 4:
            for _ in range(4):
                page_now.append(('❌', '❌', '❌'))
        buttons_shop = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text=page_now[0][0], callback_data=f'Game_{page_now[0][0]}'),
            InlineKeyboardButton(text=page_now[1][0], callback_data=f'Game_{page_now[1][0]}'),
            InlineKeyboardButton(text=page_now[2][0], callback_data=f'Game_{page_now[2][0]}'),
            InlineKeyboardButton(text=page_now[3][0], callback_data=f'Game_{page_now[3][0]}'),
            InlineKeyboardButton(text='⬅', callback_data=f'Pages_⬅'),
            InlineKeyboardButton(text='➡', callback_data='Pages_➡'),
            InlineKeyboardButton(text='Remove buttons', callback_data='Pages_Remove_buttons'))
        return page_numb, self.pages_len, buttons_shop

    def page_up(self, user_id):
        if user_id not in self.users:
            return False
        self.users[user_id] = [self.users[user_id][0] + 1, self.users[user_id][1] + 1]
        page_ind, page_numb = self.users[user_id]
        if page_numb > self.pages_len:
            self.users[user_id] = [0, 1]
            page_ind, page_numb = self.users[user_id]
        page_now = self.pages[page_ind]
        if len(page_now) != 4:
            for _ in range(4):
                page_now.append(('❌', '❌', '❌'))
        buttons_shop = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text=page_now[0][0], callback_data=f'Game_{page_now[0][0]}'),
            InlineKeyboardButton(text=page_now[1][0], callback_data=f'Game_{page_now[1][0]}'),
            InlineKeyboardButton(text=page_now[2][0], callback_data=f'Game_{page_now[2][0]}'),
            InlineKeyboardButton(text=page_now[3][0], callback_data=f'Game_{page_now[3][0]}'),
            InlineKeyboardButton(text='⬅', callback_data=f'Pages_⬅'),
            InlineKeyboardButton(text='➡', callback_data='Pages_➡'),
            InlineKeyboardButton(text='Remove buttons', callback_data='Pages_Remove_buttons'))
        return page_numb, self.pages_len, buttons_shop

    def page_down(self, user_id):
        if user_id not in self.users:
            return False
        self.users[user_id] = [self.users[user_id][0] - 1, self.users[user_id][1] - 1]
        page_ind, page_numb = self.users[user_id]
        if page_numb == 0:
            self.users[user_id] = [self.pages_len - 1, self.pages_len]
            page_ind, page_numb = self.users[user_id]
        page_now = self.pages[page_ind]
        if len(page_now) != 4:
            for _ in range(4):
                page_now.append(('❌', '❌', '❌'))
        buttons_shop = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text=page_now[0][0], callback_data=f'Game_{page_now[0][0]}'),
            InlineKeyboardButton(text=page_now[1][0], callback_data=f'Game_{page_now[1][0]}'),
            InlineKeyboardButton(text=page_now[2][0], callback_data=f'Game_{page_now[2][0]}'),
            InlineKeyboardButton(text=page_now[3][0], callback_data=f'Game_{page_now[3][0]}'),
            InlineKeyboardButton(text='⬅', callback_data=f'Pages_⬅'),
            InlineKeyboardButton(text='➡', callback_data='Pages_➡'),
            InlineKeyboardButton(text='Remove buttons', callback_data='Pages_Remove_buttons'))
        return page_numb, self.pages_len, buttons_shop

    def page_return(self, user_id):
        if user_id not in self.users:
            return False
        self.users[user_id] = [self.users[user_id][0], self.users[user_id][1]]
        page_ind, page_numb = self.users[user_id]
        page_now = self.pages[page_ind]
        if len(page_now) != 4:
            for _ in range(4):
                page_now.append(('❌', '❌', '❌'))
        buttons_shop = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text=page_now[0][0], callback_data=f'Game_{page_now[0][0]}'),
            InlineKeyboardButton(text=page_now[1][0], callback_data=f'Game_{page_now[1][0]}'),
            InlineKeyboardButton(text=page_now[2][0], callback_data=f'Game_{page_now[2][0]}'),
            InlineKeyboardButton(text=page_now[3][0], callback_data=f'Game_{page_now[3][0]}'),
            InlineKeyboardButton(text='⬅', callback_data=f'Pages_⬅'),
            InlineKeyboardButton(text='➡', callback_data='Pages_➡'),
            InlineKeyboardButton(text='Remove buttons', callback_data='Pages_Remove_buttons'))
        return page_numb, self.pages_len, buttons_shop

    def page_delete(self, user_id):
        if user_id not in self.users:
            return False
        del self.users[user_id]

    def page_add(self, command):
        game = " ".join(command[0].split(" ")[:-1])
        price = int(command[0].split(" ")[-1])
        try:
            keys = command[1]
        except IndexError:
            keys = None
        check = self.c[1].execute(
            f'SELECT {self.col_names[1][0]} FROM {self.col_names[0]} WHERE {self.col_names[1][0]} = "{game}"').fetchone()
        if check is None:
            self.c[1].execute(f"INSERT INTO {self.col_names[0]} VALUES (?, ?, ?)", (game, keys, price))
            self.c[0].commit()
        else:
            return False

    def page_restart(self):
        self.db = self.c[1].execute(f'SELECT {self.col_names[1][0]}, {self.col_names[1][1]}, {self.col_names[1][2]} FROM {self.col_names[0]}').fetchall()
        self.pages = [self.db[i:i + 4] for i in range(0, len(self.db), 4)]
        self.pages_len = len(self.pages)

    def page_del(self, product):
        self.c[1].execute(f"DELETE FROM {self.col_names[0]} WHERE {self.col_names[1][0]} = '{product}'")
        self.c[0].commit()
