from faker import Faker


class DataGenerator:
    def __init__(self, faker: Faker):
        self.faker = faker

    def email(self) -> str:
        return self.faker.email()

    def first_name(self) -> str:
        return self.faker.first_name()

    def phone(self) -> str:
        return "+7" + self.faker.msisdn()[1:11]

    def password(self) -> str:
        return self.faker.password()

    def object_name(self) -> str:
        return self.faker.word()

    def description(self) -> str:
        return self.faker.text()

    def price(self) -> int:
        return self.faker.random_int(min=400, max=1200)

    def availability(self) -> bool:
        return self.faker.boolean()

    def image_url(self) -> str:
        return self.faker.image_url() + [".jpg", ".png", ".jpeg", ".webp"][self.faker.random_int(min=0, max=3)]

fake_ru = DataGenerator(Faker("ru_RU"))
