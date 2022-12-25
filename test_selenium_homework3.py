import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing(selenium):
    selenium.get('https://petfriends.skillfactory.ru/')
    yield
    selenium.quit()


def test_all_pets_have_name_age_breed(selenium):
    """ Данный тест проверяет, что на странице со списком питомцев пользователя
    у всех питомцев есть имя, возраст и порода """
    selenium.maximize_window()
    # нажимаем зеленую кнопку "Зарегистрироваться"
    btn_signup = selenium.find_element_by_xpath("//button[@onclick=\"document.location='/new_user';\"]")
    btn_signup.click()
    # нажимаем ссылку "У меня уже есть аккаунт" используя явное ожидание "кликабельности" элемента
    btn_ihave_acc = WebDriverWait(selenium,
                                  5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'У меня уже есть аккаунт')))
    btn_ihave_acc.click()
    # очищаем поле ввода "Электронная почта" и вводим email
    field_email = selenium.find_element_by_id("email")
    field_email.clear()
    field_email.send_keys("japanflower@rambler.ru")
    # очищаем поле ввода "Пароль" и вводим пароль
    field_pass = selenium.find_element_by_id("pass")
    field_pass.clear()
    field_pass.send_keys("1bYkov3")
    # нажимаем зеленую кнопку "Войти"
    btn_login = selenium.find_element_by_xpath("//button[@type='submit']")
    btn_login.click()
    # проверяем, что мы оказались на главной странице сайта
    assert selenium.find_element_by_tag_name('h1').text == "PetFriends", "login error"
    # нажимаем на кнопку "Мои питомцы"
    btn_mypts = selenium.find_element_by_link_text(u"Мои питомцы")
    # используем неявное ожидание
    selenium.implicitly_wait(5)
    btn_mypts.click()
    # сохраняем в переменную все имена питомцев найденных по локатору
    names = selenium.find_elements_by_xpath('//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
    # сохраняем в переменную все породы питомцев найденных по локатору
    breed = selenium.find_elements_by_css_selector('div#all_my_pets>table>tbody>tr>td:nth-of-type(2)')
    # сохраняем в переменную все возрасты питомцев найденных по локатору
    age = selenium.find_elements_by_css_selector('div#all_my_pets>table>tbody>tr>td:nth-of-type(3)')

    for i in range(len(names)):
        assert names[i].text != '', "HAVE NO NAME"
        assert breed[i].text != '', "HAVE NO BREED"
        assert age[i].text != '', "HAVE NO NAME"


# python -m pytest -v --driver Chrome --driver-path C:/WebDriver/chromedriver.exe test_selenium_homework3.py
