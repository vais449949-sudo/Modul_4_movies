import pytest
import allure
from sqlalchemy.orm import Session

from data_generator.data_generator import DataGenerator
from db_requester.models import AccountTransactionTemplate


@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplate:

    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
    Этот тест проверяет корректность перевода денег между двумя счетами.

    Шаги:
    1. Создание двух счетов: Stan и Bob
    2. Перевод 200 единиц от Stan к Bob
    3. Проверка изменения балансов
    4. Очистка тестовых данных
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ivan Petrovich")
    @allure.title("Тест перевода денег между счетами")

    def test_accounts_transaction_template(self, db_session: Session):

        # =========================================================
        # ARRANGE
        # =========================================================

        with allure.step("Создание тестовых аккаунтов"):

            stan = AccountTransactionTemplate(
                user=f"Stan_{DataGenerator.generate_random_int(100000)}",
                balance=1000
            )

            bob = AccountTransactionTemplate(
                user=f"Bob_{DataGenerator.generate_random_int(100000)}",
                balance=500
            )

            db_session.add_all([stan, bob])
            db_session.commit()

            db_session.refresh(stan)
            db_session.refresh(bob)

        # =========================================================
        # ACT
        # =========================================================

        def transfer_money(session, from_account, to_account, amount):

            with allure.step("Получаем счета из БД"):

                from_acc = (
                    session.query(AccountTransactionTemplate)
                    .filter_by(user=from_account)
                    .one()
                )

                to_acc = (
                    session.query(AccountTransactionTemplate)
                    .filter_by(user=to_account)
                    .one()
                )

            with allure.step("Проверяем баланс отправителя"):

                if from_acc.balance < amount:
                    raise ValueError("Недостаточно средств на счете")

            with allure.step("Выполняем перевод"):

                from_acc.balance -= amount
                to_acc.balance += amount

            with allure.step("Сохраняем изменения"):
                session.commit()

        # =========================================================
        # ASSERT
        # =========================================================

        with allure.step("Проверяем начальные балансы"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:

            with allure.step("Переводим 200 единиц от Stan к Bob"):

                transfer_money(
                    db_session,
                    from_account=stan.user,
                    to_account=bob.user,
                    amount=200
                )

            db_session.refresh(stan)
            db_session.refresh(bob)

            with allure.step("Проверяем итоговые балансы"):

                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:

            db_session.rollback()
            pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:

            with allure.step("Удаляем тестовые данные"):

                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()