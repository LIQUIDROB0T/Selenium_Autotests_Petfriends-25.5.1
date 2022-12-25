import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing(selenium):
    selenium.get('https://petfriends.skillfactory.ru/')
    yield
    selenium.quit()


def test_half_pets_have_pic(selenium):
    """ Данный тест проверяет, что на странице со списком питомцев пользователя
    хотя бы у половины питомцев есть фото """
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
    # сохраняем в переменную все изображения питомцев найденных по локатору
    images = selenium.find_elements_by_css_selector('div#all_my_pets>table>tbody>tr>th>img')

    for i in range(len(images)):
        assert images[i].get_attribute('src') != '', "HAVE NO PHOTO"


# python -m pytest -v --driver Chrome --driver-path C:/WebDriver/chromedriver.exe test_selenium_homework2.py
