ERR_REVIEW_ONE = 'Разрешён только один отзыв на произведение'
ERR_REVIEW_SCORE = 'Возможны оценки только от 1 до 10'

ERR_TITLE_YEAR_FROM_FUTURE = 'Год слишком далеко в будущем'

ERR_USER_NAME_NOT_ME = 'Использовать имя «me» запрещено'
ERR_USER_NAME_TEMPLATE = (
    'Имя пользователя не соответствует шаблону,'
    'используйте только буквы, цифры и символы _ . @ + -'
)
RE_USER_NAME_TEMPLATE = r'^[\w.@+-]+\Z'
ERR_USER_EMAIL_UNIQUE = 'Пользователь с такой электронной почты уже существует'
ERR_USER_NAME_UNIQUE = 'Пользователь с таким именем уже существует'

PERMISSION_ADMIN_USE = 'Пользоваться может только администратор'
PERMISSION_ADMIN_EDIT = 'Редактировать может только администратор'
PERMISSION_EDIT = (
    'Редактировать может только автор, модератор или администратор'
)

EMAIL_CONF_CODE_SUBJECT = 'Регистрация пользователя'
EMAIL_CONF_CODE_MESSAGE = 'Добрый день!\n\nВаш код подтверждения: '
