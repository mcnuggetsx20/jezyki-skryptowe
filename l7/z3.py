from random import choice

class PasswordGenerator:
    def __init__(self, length, charset, count):
        self.length = length
        self.charset = charset if charset else [char for i in range(ord('a'), ord('z')) for char in [chr(i).lower(), chr(i).upper()]]
        self.count = count

        self.current = 0
        return

    def __iter__(self):
        return self

    def __next__(self):
        if(self.current == self.count):
            raise StopIteration(f'Wygenerowano juz {self.count} hasel!')

        new_password = ''
        for i in range(self.length):
            new_password += choice(self.charset)

        self.current +=1
        return new_password
